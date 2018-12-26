
import sys
import time
import random

#Generate a random number from a range
#Get trigger from the API call via browser url like below.
#https://d1f614nf05.execute-api.ca-central-1.amazonaws.com/POC/number?min=50&max=60


pool_capacity=5

def my_lambda_handler(event, context):
    
    #Get max_count and min_count from event
    max_count=event['max']
    min_count=event['min']
    rand_number=f_random(min_count,max_count)
    message='Python 3.7: A number from range of min {} to max {} : {}'.format(min_count,max_count,rand_number)
    
    return(message)
    
def f_random(min_count,max_count):
    #generate radom numbers from range of min to max
    rand = random.randint(min_count, max_count)
    #print('Running for {} seconds'.format(rand))
    #time.sleep(rand)
    return rand
