#!/bin/bash

echo "Cleaning existing deployment packages..."
rm -rf package.zip
rm -rf package
mkdir -p package

echo "Building deployment packages from requirement file..."

finch run --rm -v "$PWD":/var/task public.ecr.aws/sam/build-python3.13:latest-x86_64 /bin/sh -c "
  pip install --quiet -r requirements.txt -t /var/task/package;
  cd /var/task/package;
  zip -r9q /var/task/package.zip .;
  cd /var/task;
  zip -g package.zip lambda_agent.py
"

# echo "Preparing deployment package..."
# cd package
# zip -rq ../package.zip .
# cd ..
# zip package.zip lambda_agent.py

echo "...Completed!"