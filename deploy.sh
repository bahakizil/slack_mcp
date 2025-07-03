#!/bin/bash

# AWS Deployment Script for Slack MCP Server
# Make sure to update the account ID and region as needed

set -e

# Configuration
AWS_ACCOUNT_ID="123456789012"
AWS_REGION="us-east-1"
ECR_REPOSITORY="slack-mcp-server"
ECS_CLUSTER="slack-mcp-cluster"
ECS_SERVICE="slack-mcp-service"

echo "🚀 Starting deployment of Slack MCP Server..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t slack-mcp-server:latest .

# Tag for ECR
echo "🏷️  Tagging image for ECR..."
docker tag slack-mcp-server:latest \
    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest

# Login to ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin \
    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Push to ECR
echo "⬆️  Pushing image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest

# Update ECS service
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster ${ECS_CLUSTER} \
    --service ${ECS_SERVICE} \
    --force-new-deployment \
    --region ${AWS_REGION}

echo "✅ Deployment completed successfully!"
echo "🔍 Check service status with:"
echo "aws ecs describe-services --cluster ${ECS_CLUSTER} --services ${ECS_SERVICE} --region ${AWS_REGION}"