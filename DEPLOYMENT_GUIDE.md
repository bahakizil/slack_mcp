# 🚀 Deployment Guide - Production Setup

## 📋 Deployment Options

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)  
3. [AWS ECS Deployment](#aws-ecs-deployment)
4. [Claude Desktop Integration](#claude-desktop-integration)
5. [Slack App Distribution](#slack-app-distribution)

---

## 💻 Local Development

### Prerequisites
- Python 3.10+
- Slack workspace with admin access
- API keys (Slack, OpenAI, Tavily)

### Quick Setup

```bash
# Clone repository
git clone <your-repo-url>
cd Slack_MCP_Server-main

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start servers
python tavily_mcp_server.py &  # Background process
python main.py                 # Main server
```

### Development Commands

```bash
# Run with debug logging
DEBUG=true LOG_LEVEL=DEBUG python main.py

# Test individual components
python -c "from autonomous_agent import autonomous_assistant; print('Agent loaded')"

# Health check
curl http://localhost:8001/health
curl http://localhost:8002/health
```

---

## 🐳 Docker Deployment

### Build Images

```bash
# Build main server
docker build -t slack-mcp-server .

# Build Tavily server
docker build -f Dockerfile.tavily -t tavily-mcp-server .
```

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  slack-mcp:
    build: .
    ports:
      - "8001:8001"
    environment:
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - PORT=8001
      - HOST=0.0.0.0
    depends_on:
      - tavily-mcp
    restart: unless-stopped

  tavily-mcp:
    build:
      context: .
      dockerfile: Dockerfile.tavily
    ports:
      - "8002:8002"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - TAVILY_PORT=8002
      - HOST=0.0.0.0
    restart: unless-stopped

networks:
  default:
    name: mcp-network
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f slack-mcp
docker-compose logs -f tavily-mcp

# Health check
curl http://localhost:8001/health
curl http://localhost:8002/health

# Stop services
docker-compose down
```

---

## ☁️ AWS ECS Deployment

### Prerequisites

- AWS CLI configured
- ECR repositories created
- ECS cluster running
- AWS Secrets Manager setup

### Step 1: Create AWS Secrets

```bash
# Create secrets in AWS Secrets Manager
aws secretsmanager create-secret \
    --name "slack-mcp/slack-bot-token" \
    --description "Slack Bot Token" \
    --secret-string "xoxb-your-token-here"

aws secretsmanager create-secret \
    --name "slack-mcp/openai-api-key" \
    --description "OpenAI API Key" \
    --secret-string "sk-your-key-here"

aws secretsmanager create-secret \
    --name "slack-mcp/tavily-api-key" \
    --description "Tavily API Key" \
    --secret-string "tvly-your-key-here"
```

### Step 2: Build and Push Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag images
docker build -t slack-mcp-server .
docker tag slack-mcp-server:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/slack-mcp-server:latest

docker build -f Dockerfile.tavily -t tavily-mcp-server .
docker tag tavily-mcp-server:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/tavily-mcp-server:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/slack-mcp-server:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/tavily-mcp-server:latest
```

### Step 3: ECS Task Definition

Create `task-definition-production.json`:

```json
{
  "family": "slack-mcp-production",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "slack-mcp-server",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/slack-mcp-server:latest",
      "portMappings": [
        {
          "containerPort": 8001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "USE_AWS_SECRETS",
          "value": "true"
        },
        {
          "name": "AWS_REGION", 
          "value": "us-east-1"
        },
        {
          "name": "PORT",
          "value": "8001"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/slack-mcp-server",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "essential": true
    },
    {
      "name": "tavily-mcp-server",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/tavily-mcp-server:latest",
      "portMappings": [
        {
          "containerPort": 8002,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "USE_AWS_SECRETS",
          "value": "true"
        },
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        },
        {
          "name": "TAVILY_PORT", 
          "value": "8002"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/tavily-mcp-server",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "essential": true
    }
  ]
}
```

### Step 4: Deploy to ECS

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition-production.json

# Create or update service
aws ecs create-service \
    --cluster slack-mcp-cluster \
    --service-name slack-mcp-service \
    --task-definition slack-mcp-production \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"

# Update existing service
aws ecs update-service \
    --cluster slack-mcp-cluster \
    --service slack-mcp-service \
    --force-new-deployment
```

### Step 5: Load Balancer Setup

Create Application Load Balancer:

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name slack-mcp-alb \
    --subnets subnet-12345 subnet-67890 \
    --security-groups sg-12345

# Create target group
aws elbv2 create-target-group \
    --name slack-mcp-targets \
    --protocol HTTP \
    --port 8001 \
    --vpc-id vpc-12345 \
    --target-type ip \
    --health-check-path /health

# Create listener
aws elbv2 create-listener \
    --load-balancer-arn <alb-arn> \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=<target-group-arn>
```

---

## 🖥️ Claude Desktop Integration

### Production Configuration

For production deployments, update Claude Desktop config:

```json
{
  "mcpServers": {
    "slack-autonomous-ai": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", "@-",
        "https://your-production-domain.com/mcp"
      ],
      "env": {}
    }
  }
}
```

### Local Development Configuration

```json
{
  "mcpServers": {
    "slack-mcp-local": {
      "command": "python",
      "args": ["/absolute/path/to/main.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "OPENAI_API_KEY": "sk-...",
        "TAVILY_API_KEY": "tvly-...",
        "PORT": "8001",
        "DEBUG": "false"
      }
    }
  }
}
```

### Verification

After configuration:

1. Restart Claude Desktop
2. Look for available tools in tool picker
3. Test with simple command: `send_slack_message(channel="test", message="Hello!")`

---

## 📱 Slack App Distribution

### Option 1: Workspace-Specific

1. Create app at [https://api.slack.com/apps](https://api.slack.com/apps)
2. Configure OAuth scopes (see main guide)
3. Install to your workspace
4. Use bot token in deployment

### Option 2: Public Distribution

For distributing to multiple workspaces:

1. **Create Slack App**
   - Enable "Distribute App" in app settings
   - Set redirect URLs for OAuth flow
   - Configure app manifest

2. **OAuth Implementation**
   ```python
   from slack_sdk.oauth import AuthorizeUrlGenerator, OAuthStateUtils
   
   # Generate OAuth URL
   auth_url = AuthorizeUrlGenerator(
       client_id="your-client-id",
       scopes=["channels:read", "chat:write", ...],
       redirect_uri="https://your-domain.com/oauth/callback"
   ).generate("state-value")
   ```

3. **Token Management**
   ```python
   # Store tokens per workspace
   workspace_tokens = {
       "T1234567890": "xoxb-workspace-1-token",
       "T0987654321": "xoxb-workspace-2-token"
   }
   ```

### App Manifest Example

```yaml
display_information:
  name: Autonomous AI Assistant
  description: Intelligent Slack assistant with web research capabilities
  background_color: "#2c3e50"
features:
  bot_user:
    display_name: AI Assistant
    always_online: true
oauth_config:
  scopes:
    bot:
      - channels:read
      - channels:history
      - chat:write
      - users:read
      - search:read
      - channels:manage
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

---

## 📊 Monitoring & Logging

### CloudWatch Setup

```bash
# Create log groups
aws logs create-log-group --log-group-name /ecs/slack-mcp-server
aws logs create-log-group --log-group-name /ecs/tavily-mcp-server

# Create custom metrics
aws logs put-metric-filter \
    --log-group-name /ecs/slack-mcp-server \
    --filter-name ErrorCount \
    --filter-pattern "ERROR" \
    --metric-transformations \
        metricName=SlackMCPErrors,metricNamespace=CustomApp,metricValue=1
```

### Health Checks

Add health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "slack": bool(slack_client),
            "openai": bool(openai_client),
            "tavily": bool(tavily_client)
        }
    }

@app.get("/metrics")
async def metrics():
    return {
        "requests_total": request_counter,
        "active_connections": active_connections,
        "avg_response_time": avg_response_time
    }
```

### Alerting

```bash
# Create CloudWatch alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "SlackMCP-HighErrorRate" \
    --alarm-description "High error rate detected" \
    --metric-name SlackMCPErrors \
    --namespace CustomApp \
    --statistic Sum \
    --period 300 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

---

## 🔒 Security Best Practices

### Environment Variables

```bash
# Never commit these to code
SLACK_BOT_TOKEN=xoxb-...
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...

# Use AWS Secrets Manager in production
USE_AWS_SECRETS=true
AWS_REGION=us-east-1
```

### Network Security

```yaml
# Security group for ECS
SecurityGroupIngress:
  - IpProtocol: tcp
    FromPort: 8001
    ToPort: 8002
    SourceSecurityGroupId: !Ref ALBSecurityGroup
  - IpProtocol: tcp
    FromPort: 443
    ToPort: 443
    CidrIp: 0.0.0.0/0
```

### IAM Roles

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:*:*:secret:slack-mcp/*"
      ]
    }
  ]
}
```

---

## 🚀 Performance Optimization

### Caching Strategy

```python
from functools import lru_cache
import redis

# In-memory caching
@lru_cache(maxsize=1000)
def get_channel_info(channel_id):
    return slack_client.conversations_info(channel=channel_id)

# Redis caching for production
redis_client = redis.Redis(host='elasticache-endpoint')

def cache_search_results(query, results):
    redis_client.setex(f"search:{query}", 3600, json.dumps(results))
```

### Connection Pooling

```python
import httpx

# Async HTTP client with connection pooling
async_client = httpx.AsyncClient(
    limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
    timeout=httpx.Timeout(30.0)
)
```

### Resource Limits

```yaml
# ECS task definition
"resourceRequirements": [
  {
    "type": "MEMORY",
    "value": "2048"
  },
  {
    "type": "CPU", 
    "value": "1024"
  }
]
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

```bash
# Scale ECS service
aws ecs update-service \
    --cluster slack-mcp-cluster \
    --service slack-mcp-service \
    --desired-count 3

# Auto Scaling
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/slack-mcp-cluster/slack-mcp-service \
    --min-capacity 1 \
    --max-capacity 10
```

### Load Testing

```python
import asyncio
import aiohttp

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            task = session.post('http://localhost:8001/mcp', json={
                "jsonrpc": "2.0",
                "id": i,
                "method": "tools/call",
                "params": {"name": "send_slack_message", "arguments": {"channel": "test", "message": f"Load test {i}"}}
            })
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        print(f"Completed {len(responses)} requests")

asyncio.run(load_test())
```

---

## 🎯 Production Checklist

### Pre-Deployment

- [ ] All API keys configured in AWS Secrets Manager
- [ ] Docker images built and pushed to ECR
- [ ] ECS cluster and services configured
- [ ] Load balancer and target groups created
- [ ] CloudWatch logging enabled
- [ ] Health checks configured
- [ ] Security groups properly configured
- [ ] IAM roles and policies applied

### Post-Deployment

- [ ] Health checks passing
- [ ] All tools working in Claude Desktop
- [ ] Slack integration functional
- [ ] Monitoring dashboards created
- [ ] Alerts configured
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team training completed

### Maintenance

- [ ] Regular security updates
- [ ] Performance monitoring
- [ ] Log analysis
- [ ] Cost optimization
- [ ] Backup strategies
- [ ] Disaster recovery testing

---

**🎉 Your autonomous AI system is now production-ready!**