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
    
    let generatedNumber=Math.floor(Math.random()*max)+min;
    
    callback(null, generatedNumber);
    
};

```

## Part 3 Connecting Lambda to API Gateway
https://www.youtube.com/watch?annotation_id=annotation_1347208637&feature=iv&src_vid=PEatXsXIkLc&v=DSrg7hG-jV4


## Getting started with AWS Lambda, part 4
https://www.youtube.com/watch?v=afhNipd6TkE
