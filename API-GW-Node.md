# Excercise on AWS Lambda

Cover topics like creating a function in Node.js, deploying them with automated tools, executing functions with HTTP calls, integrating them with other AWS services and much more!

## Getting started with AWS Lambda, part 1
https://www.youtube.com/watch?v=fSUEk6iMW88

## Part 2: A simple function to generate random numbers by nodejs
https://www.youtube.com/watch?v=PEatXsXIkLc

```
'use strict';
console.log('Loading function');

exports.handler = (event, context, callback) => {
    // TODO implement
    let min=10;
    let max=90;
    
    let generatedNumber=Math.floor(Math.random()*(max-min))+min;
    
    callback(null, generatedNumber);
    
};

```

## Part 3 Connecting Lambda to API Gateway
https://www.youtube.com/watch?annotation_id=annotation_1347208637&feature=iv&src_vid=PEatXsXIkLc&v=DSrg7hG-jV4

Step1: Create a new API with resource:
API Gateway=>APIs => Random-Number-API /number /GET

Step2: Add parameters 
API Gateway=>APIs => Random-Number-API /number - GET - Integration Request => Mapping Templates =>Check When there are no templates defined (recommended) on "Request Body Passthrough"

```
{
    "min": $input.params('min'),
    "max": $input.params('max')
}
```

## Getting started with AWS Lambda, part 4
https://www.youtube.com/watch?v=afhNipd6TkE

Step1: Change nodejs code as below:
```
'use strict';
console.log('Loading function');

exports.handler = (event, context, callback) => {
    // TODO implement
    let min=event.min;
    let max=event.max;
    
    let generatedNumber=Math.floor(Math.random()*max)+min;
    
    callback(null, generatedNumber);
    
};
```
Step2: Re-deploy and open below url:

https://d1f614nf05.execute-api.ca-central-1.amazonaws.com/POC/number?min=50&max=100
