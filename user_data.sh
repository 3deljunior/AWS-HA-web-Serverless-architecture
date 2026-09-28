
  #!/bin/bash
set -euo pipefail

AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:-<your-aws-account-id>}"
AWS_REGION="${AWS_REGION:-<region>}"

apt-get update -y
apt-get install -y docker.io awscli
systemctl start docker
systemctl enable docker

aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker run -d --restart always -p 80:80 \
  -e AWS_REGION="$AWS_REGION" \
  -e S3_BUCKET_NAME="<s3-bucket-name>" \
  -e DB_HOST="<db-host>" \
  -e DB_NAME="<db-name>" \
  -e DB_USER="<db-user>" \
  -e DB_PASSWORD="<db-password>" \
  "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/my-flask-app:latest"