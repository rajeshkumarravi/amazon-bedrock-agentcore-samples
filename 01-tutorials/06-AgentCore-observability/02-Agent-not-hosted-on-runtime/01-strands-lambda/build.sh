#!/bin/bash

# echo "Cleaning existing deployment packages..."
# rm -rf package.zip
# rm -rf package
# mkdir -p package

echo "Cleaning and building deployment packages from requirement file..."

# launch build container with current folder mapped to containers /var/task folder
# Note: replace finch with docker if using docker
finch run --rm -v "$PWD":/var/task public.ecr.aws/sam/build-python3.13:latest-x86_64 /bin/sh -c "
  rm -rf package.zip
  rm -rf package
  mkdir -p package
  pip install --quiet -r requirements.txt -t /var/task/package;
  cd /var/task/package;
  cp ./bin/opentelemetry-instrument .
  zip -r9q /var/task/package.zip .;
  cd /var/task;
  zip -g package.zip lambda_agent.py
"

echo "...Completed!"
