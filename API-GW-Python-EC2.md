# Excercise on AWS Lambda -Python

Based on the initial excercise following API-GW-NodeJS.md, integrate with Python run time to manage EC2 instances

## Previous steps

* Part 1: Create a simple function to generate random numbers by nodejs
* Part 2: Connecting Lambda to API Gateway
* Part 3: Transfer Parameters to Lambda Function via API Calls

https://d1f614nf05.execute-api.ca-central-1.amazonaws.com/POC/number?min=50&max=100

## Part 4: Change run time from NodeJS to Python

Refer to code file: rand_number.py

> Generate a random number from a range
> Get trigger from the API call via browser url like below.
> https://d1f614nf05.execute-api.ca-central-1.amazonaws.com/POC/number?min=50&max=60

## Part 5: Add more parameters to call EC2 managment functions

* pending_task:50-1300
* command:up, fire_more 
Fire up EC2 instances from scaling group or standby pool by calling boto3 code via Python
Refer to code file: Fire-up-EC2.py
* request_ID:context.aws_request_id or time_stamp
