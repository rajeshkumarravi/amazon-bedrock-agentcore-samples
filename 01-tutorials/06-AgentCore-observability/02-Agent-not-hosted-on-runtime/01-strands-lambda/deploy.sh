#!/bin/bash


cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
  --role-name lambda-execution-role \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
  --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam get-role \
  --role-name lambda-execution-role \
  --query 'Role.Arn' \
  --output text


aws lambda create-function \
  --function-name strands-lambda-obs-demo \
  --runtime python3.13 \
  --role arn:aws:iam::your-account-id:role/your-lambda-execution-role \
  --handler lambda_function.handler \
  --zip-file fileb://package.zip \
  --architectures x86_64 \
  --timeout 30 \
  --memory-size 128
