# Despliegue en AWS ECS Fargate

Requisitos: Docker, AWS CLI v2, credenciales con `aws configure` y permisos para ECR, ECS, IAM, VPC y CloudWatch Logs.

```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export IMAGE_NAME=session-duration-api
export ECR_REPOSITORY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME
```

## ECR

```bash
aws ecr create-repository --repository-name $IMAGE_NAME --region $AWS_REGION
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

## Imagen

Desde `example/`:

```bash
docker build -t $IMAGE_NAME:latest .
docker tag $IMAGE_NAME:latest $ECR_REPOSITORY:latest
docker push $ECR_REPOSITORY:latest
```

## ECS

```bash
aws ecs create-cluster --cluster-name session-duration-cluster --region $AWS_REGION
aws ecs register-task-definition --cli-input-json file://infra/aws/task-definition.json --region $AWS_REGION
```

Crea el servicio con subnets y security group reales de tu VPC:

```bash
aws ecs create-service \
  --cluster session-duration-cluster \
  --service-name session-duration-service \
  --task-definition session-duration-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxxx],securityGroups=[sg-xxxxxxxx],assignPublicIp=ENABLED}" \
  --region $AWS_REGION
```

## Limpieza

```bash
aws ecs update-service --cluster session-duration-cluster --service session-duration-service --desired-count 0 --region $AWS_REGION
aws ecs delete-service --cluster session-duration-cluster --service session-duration-service --force --region $AWS_REGION
aws ecs delete-cluster --cluster session-duration-cluster --region $AWS_REGION
aws ecr delete-repository --repository-name session-duration-api --force --region $AWS_REGION
```
