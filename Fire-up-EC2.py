import boto3
client = boto3.client('lambda')
import sys
import time
import random

#Get trigger from the scaling group for how many new instances are scaled up.
#Fire up stopped VMs from pool, count=n <= capacity
#Launch same new VM to fulfil the pool, increase capacity as need.

region = 'ca-central-1'
ec2_client = boto3.client('ec2', region_name=region)
ec2_resource = boto3.resource('ec2', region_name=region)
autoscaling = boto3.client('autoscaling')
asg_name='tf-asg-202222'
lc_name='terraform-209999'

pool_capacity=5

def lambda_handler(event, context):
    
    #Check how many instances are just scaled up as pending state from the scaling group: 
    #The tag of new EC2 aws:autoscaling:groupName is None at begining of scaling up.
    asg_list=chk_asg_pool('','pending')
    asg_count=len(asg_list)
    print('asg_pool_count:',asg_count)
    print('asg_pool_list:',asg_list)
    
    # fire_count =f_random(5)  #fire radom number of VMs between 1 to 5.
    
    #As workaround, fire the same number of EC2 from the pool when get the count of scaling up VMs.
    # #Idealy we should calculate according to CPUU, Redis.
    fire_count =asg_count
    
    # Check how many VMs are available in the pool
    pool_list=list_pool()
    pool_count=len(pool_list)
    print('pool_count:',pool_count, 'Predefined Cap:',pool_capacity)
    print('pool_list:',pool_list)
    
    if pool_count>0 and fire_count>0:
        if fire_count>pool_count:
            fire_count=pool_count
            
        instance_ids=[]
            
        for i in range(0,fire_count):
            instance_ids=instance_ids+[pool_list[i]]
            tagging_ec2(pool_list[i],'Paired_ID', asg_list[i])
            
        print('instances to fire up: ', instance_ids)    
        
        #Fire up VMs from pool and they will be attached to the scaling group by Status Change function.
        
        if len(instance_ids)>0:
            inst_fired=start_pool(instance_ids)
        
        
    # #Launch new VM to the pool
    instance_ids_launched=launch_instances()
    
def f_random(count):
    #generate radom numbers from 1 to count
    rand = random.randint(1, count)
    print('Running for {} seconds'.format(rand))
    time.sleep(rand)
    return count

def tagging_ec2(instance_id,Key_id, Value_str):
    ec2_client.create_tags(
                Resources = [instance_id],
                Tags= [{"Key":Key_id, "Value":Value_str}]
               )

def list_pool():

    pool_ids=[]
    #stopping_inst_pool=chk_pool('Worker-Standby-Pool','stopping')
    #pending_inst_pool=chk_pool('Worker-New-Pool','pending')
    stopped_inst_pool=chk_pool('Worker-Standby-Pool','stopped')
    running_inst_pool=chk_pool('Worker-New-Pool','running')
    pool_ids=stopped_inst_pool+running_inst_pool
    
    return pool_ids
    
def start_pool(instance_ids):
    #Fire up the stopped VMs from the pool and attach to scaling group
 
    ec2_client.start_instances(InstanceIds=instance_ids)
    instance_count=len(instance_ids)
    print('\n',instance_count,'instances fired : ' , str(instance_ids),'\n\n')
    return instance_ids
    
def stop_pool(instances):
    #Fire up the stopped VMs from the pool and attach to scaling group
 
    ec2_client.stop_instances(InstanceIds=instances)
    print('\n',instance_count,'instances stopped : ' , str(instances),'\n\n')
    return instances

#[Step1] Launch new VMs to fulfill the pre-defined capacity of the pool
#Works on Oct 31st, need to continue improve on below items:
# launch VMs in 2 subnets for AZ



def launch_instances():
    #we Add a task state at the beginning of the state machine that checks if any other executions are currently running
    instances=[]
    instance_ids=[]
    pool_list=[]
    #inst_count=event['instance_count2'] # number of VMs need to launch
    

    lc=[]
 
    stopping_inst_pool=chk_pool('Worker-Standby-Pool','stopping')
    stopped_inst_pool=chk_pool('Worker-Standby-Pool','stopped')
    pending_inst_pool=chk_pool('Worker-New-Pool','pending')
    running_inst_pool=chk_pool('Worker-New-Pool','running')
    pool_list=stopped_inst_pool+stopping_inst_pool+pending_inst_pool+running_inst_pool
    pool_count=len(pool_list)
    
    print('pool_count:',pool_count)
    
    if pool_count>=pool_capacity:
        sys.exit("No need to add new VM")
        
    else:
        inst_count=pool_capacity-pool_count
        #launch_quota=ec2_client.describe_account_attributes(**kwargs)
        if inst_count>pool_capacity:
            inst_count=launch_quota
            
        lc=get_launch_configuration(asg_name)
        if lc:
            instance_ids_launched = create_new_vm(inst_count,lc)
            # Launch EC2 instances, get input from the LaunchConfiguration of AutoScalingGroup
            # Tag every instance and get a list of instance IDs
            
            inst_count_launched=len(instance_ids_launched)
            
            if inst_count_launched==inst_count: # Check if get all the right number of EC2 instances 
                print ("\n\n", inst_count_launched,"New instance created.",instance_ids_launched,'\n\n')
                # Has another function: Lambda Stop the new instances and tag them as standby pool
            else:
                print('error launching instances!')

def chk_pool(inst_tag_name,inst_state):
    #Check how many stopped VMs in the pool

    # create filter for instances in running state
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': [inst_state]
        }
    ]
    
    filtered_instances = ec2_resource.instances.filter(Filters=filters)
    #print('list of instances filtered:',list(list_instances),'\n')
    
    Instances_my_group=[]
    
    if filtered_instances:
        for instance in filtered_instances:
            if instance.tags:
                inst_name = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name']
                if len(inst_name)>0 and inst_name[0]==inst_tag_name:
                    Instances_my_group.append(instance.id)
        
    return Instances_my_group
   
def chk_asg_pool(inst_tag_name,inst_state):
    #Check how many stopped VMs in the pool

    # create filter for instances in running state
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': [inst_state]
        }
    ]
    
    filtered_instances = ec2_resource.instances.filter(Filters=filters)
    #print('list of instances filtered:',list(list_instances),'\n')
    
    Instances_my_group=[]
    
    if filtered_instances:
        for instance in filtered_instances:
            print('tags:',instance.tags)
            if instance.tags is None:
                Instances_my_group.append(instance.id)
                
                #Add state record here to avoid Lambda function excution again by filtering the paired instances.
                tagging_ec2(instance.id,'Already_Paired', 'YES')
        
    return Instances_my_group


def create_new_vm(inst_count,lc):
    # Launch EC2 instances, get input from the LaunchConfiguration of AutoScalingGroup    
    # Tag every instance and get a list of instance IDs

    instances = ec2_client.run_instances(
        ImageId=lc['ImageId'],
        InstanceType=lc['InstanceType'],
        MinCount=inst_count, # required by boto, even though it's kinda obvious.
        MaxCount=inst_count,
        #InstanceInitiatedShutdownBehavior='terminate', # make shutdown in script terminate ec2
        SecurityGroupIds=lc['SecurityGroups'],
        SubnetId='subnet-06'
         #UserData=init_script # file to run on instance init.
    )
    # time.sleep(32)
    instance_ids = []
    # Tag every instance and get a list of instance IDs
    for instance in instances['Instances']:
        instance_id = instance['InstanceId']
        ec2_client.create_tags(
            Resources = [instance_id],
            Tags= [{"Key":'Name', "Value":'Worker-New-Pool'}]
           )
           
        instance_ids.append(instance_id)
        #instance_ids = instances['Instances'][]['InstanceId']
            
    return instance_ids
    

def get_launch_configuration(asg_name):
    asgs = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])['AutoScalingGroups']
    lc_name = asgs[0]['LaunchConfigurationName']
    lcs = autoscaling.describe_launch_configurations(LaunchConfigurationNames=[lc_name])['LaunchConfigurations']
    
    if lcs[0]:
        return lcs[0]
    return None
    
