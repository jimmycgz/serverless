# Build Serverless application with Python

Refer to below post to build Worker and API functions, but seems it doesn't indicate how to integrate two of them, showing the result of web request to API endpoint.
https://read.iopipe.com/the-right-way-to-do-serverless-in-python-e99535574454
I've completed all of the excercises listed in Part I.

## Environment:

Python 3.6

Serverless AWS Lambda Function 

## Initialize AWS Serverless in Ubuntu

Refer to below pages for details:

> Serverless Quick Start
https://serverless.com/framework/docs/providers/aws/guide/quick-start/

> Install Nodejs 
https://github.com/nodesource/distributions/blob/master/README.md

> Install Docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository


``` 
sudo apt-get update
sudo apt install npm -y
npm --version
3.5.2
sudo apt install nodejs-legacy
node --version
v4.2.6
sudo npm install -g serverless #might see some errors like sls update error, just go ahead to check sls version
sls version
1.35.1


```

## Creating a new sls service
sls create --template hello-world --path hello-world
cd hello-world
ls
cat serverless.yml
cat handler.js
sudo sls deploy

## Remove service to avoid billing
sudo sls remove


# Issue List

## Serverless plugin "serverless-python-requirements" initialization errored: Unexpected token
Solution: upgrade Node 4to 6 details: https://github.com/UnitedIncome/serverless-python-requirements/issues/20
