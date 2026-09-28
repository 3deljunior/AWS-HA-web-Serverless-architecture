#!/bin/bash
apt-get update -y
apt-get install -y docker.io awscli
systemctl start docker
systemctl enable docker

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 893877416641.dkr.ecr.eu-central-1.amazonaws.com

docker run -d --restart always -p 80:80 \
  -e AWS_REGION="<>" \
  -e S3_BUCKET_NAME="<>" \
  -e DB_HOST="<>" \
  -e DB_NAME="<>" \
  -e DB_USER="<>" \
  -e DB_PASSWORD="<>" \
  893877416641.dkr.ecr.eu-central-1.amazonaws.com/my-flask-app:latest