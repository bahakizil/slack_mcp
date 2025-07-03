# 🚀 Slack MCP Server

A modern FastMCP server for Slack integration, built with FastMCP 2.8.0 and designed to work seamlessly with Claude Desktop and other MCP clients.

## ✨ Features

- 🔧 **18 Powerful Tools**: 6 Slack + 3 AI + 3 Web Search + 6 MCP Server Management tools
- 🤖 **AI Integration**: OpenAI GPT-4o-mini for intelligent responses  
- 🧠 **Autonomous Agent**: AI that plans its own execution strategies
- 🌐 **Web Search**: Tavily integration for real-time web research
- 💬 **Smart Slack Bot**: AI can respond directly in Slack channels
- 📊 **Conversation Analysis**: AI-powered analysis of Slack conversations
- 🔗 **MCP Server Integration**: Connect to external MCP servers dynamically
- 🛠️ **External Tool Access**: Use tools from other MCP servers through our server
- 🧠 **AI + External Tools**: AI can suggest and use external MCP tools
- 🏠 **Local Development**: Easy setup with environment variables
- ☁️ **AWS Ready**: Optional AWS Secrets Manager integration for production
- 🤖 **Claude Desktop**: Pre-configured for Claude Desktop integration
- 🔄 **Modern FastMCP**: Built with latest FastMCP 2.8.0 framework
- 🛡️ **Secure**: Environment-based credential management with ResourceError handling

## 🛠️ Available Tools

### 📱 Slack Tools
1. **send_slack_message** - Send messages to Slack channels
2. **get_slack_channels** - List all available channels
3. **get_slack_messages** - Retrieve messages from channels
4. **get_slack_user_info** - Get user information
5. **search_slack_messages** - Search across workspace messages
6. **create_slack_channel** - Create new channels

### 🤖 AI-Powered Tools
7. **ask_ai_question** - Ask questions to OpenAI GPT model
8. **send_ai_response_to_slack** - AI responds directly in Slack channels
9. **analyze_slack_conversation** - AI analysis of Slack conversations (summary, sentiment, action items, key topics)

### 🌐 Web Search Tools (Tavily Integration)
10. **search_web** - General web search with real-time results
11. **search_news** - News-specific search with latest articles
12. **research_topic** - Deep research with comprehensive analysis

### 🔗 MCP Server Management Tools
13. **add_mcp_server** - Add external MCP server connections
14. **list_mcp_servers** - List all configured MCP servers and their status
15. **connect_mcp_server** - Connect to an external MCP server
16. **disconnect_mcp_server** - Disconnect from an MCP server
17. **list_external_tools** - List all tools available from connected MCP servers
18. **call_external_tool** - Execute tools from external MCP servers

### 🧠 Autonomous Intelligence
19. **autonomous_slack_agent** - **Revolutionary autonomous AI** that plans its own execution strategies

## 🚀 Quick Start (Local Development)

### 1. Setup Slack App

1. Go to [Slack API](https://api.slack.com/apps) and create a new app
2. Enable these **Bot Token Scopes**:
   - `channels:read` - View basic information about public channels
   - `channels:history` - View messages in public channels
   - `chat:write` - Send messages as the bot
   - `groups:read` - View basic information about private channels
   - `groups:history` - View messages in private channels
   - `im:read` - View basic information about direct messages
   - `im:history` - View messages in direct messages
   - `users:read` - View people in the workspace
   - `search:read` - Search messages (requires special approval)
   - `channels:manage` - Create and manage channels

3. Install the app to your workspace
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 2. Setup OpenAI API

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the API key (starts with `sk-`)

### 3. Setup Tavily API (Optional - for Web Search)

1. Go to [Tavily.com](https://tavily.com)
2. Sign up for a free account
3. Create a new API key
4. Copy the API key (starts with `tvly-`)

### 4. Install Dependencies

```bash
# Clone or download this repository
cd mcpslack

# Install Python dependencies
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and add your credentials:
# SLACK_BOT_TOKEN=xoxb-your-actual-bot-token-here
# SLACK_APP_TOKEN=xapp-your-actual-app-token-here      # For Socket Mode real-time responses
# OPENAI_API_KEY=sk-your-actual-openai-api-key-here
# TAVILY_API_KEY=tvly-your-actual-tavily-api-key-here  # Optional
```

### 6. Test the Server

```bash
# Run the server directly
python main.py

# The server will start and show available tools
```

## 🤖 Claude Desktop Integration

### 1. Install for Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "slack-mcp-server": {
      "command": "python",
      "args": ["/full/path/to/mcpslack/main.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-actual-bot-token-here",
        "SLACK_APP_TOKEN": "xapp-your-actual-app-token-here",
        "OPENAI_API_KEY": "sk-your-actual-openai-api-key-here",
        "TAVILY_API_KEY": "tvly-your-actual-tavily-api-key-here"
      }
    }
  }
}
```

### 2. Update Path

Replace `/full/path/to/mcpslack/main.py` with the actual path to your `main.py` file.

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. You should see all 9 tools available in Claude:
- 6 Slack tools for workspace management  
- 3 AI tools for intelligent responses and analysis

## 🧠 AI-Powered Usage Examples

### Direct AI Chat
```
Ask: "What are the key benefits of using microservices architecture?"
Tool: ask_ai_question
```

### AI Slack Bot
```
Send AI response directly to #general channel:
Tool: send_ai_response_to_slack
Channel: general
Question: "Can you explain our new deployment process?"
```

### Conversation Analysis
```
Analyze recent discussion in #planning:
Tool: analyze_slack_conversation  
Channel: planning
Analysis Type: action_items
```

**Use Cases:**
- 💼 **Meeting Summaries**: Analyze channel conversations for key decisions
- 📊 **Sentiment Analysis**: Check team mood and engagement
- ✅ **Action Items**: Extract tasks and follow-ups from discussions  
- 🤖 **Smart Responses**: AI bot answers team questions in real-time

## 🔗 MCP Server Integration

### Add External MCP Servers
```
Add a weather MCP server:
Tool: add_mcp_server
Server Name: weather-server
URL/Command: https://weather-mcp.example.com/mcp
```

### Connect and Use External Tools
```
1. Connect to the server:
Tool: connect_mcp_server
Server Name: weather-server

2. List available tools:
Tool: list_external_tools

3. Use external tool:
Tool: call_external_tool
Server: weather-server
Tool: get_weather
Arguments: {"city": "Istanbul"}
```

### AI with External Tools
```
Ask AI with access to all connected tools:
Tool: ask_ai_with_external_tools
Question: "What's the weather like in Istanbul and should I schedule an outdoor meeting?"
```

**MCP Integration Benefits:**
- 🔌 **Modular**: Add any MCP-compatible tool/service
- 🤝 **Collaborative**: Multiple team members can use shared MCP servers
- 🧠 **AI-Enhanced**: AI can suggest and use appropriate external tools
- 📈 **Scalable**: Connect to dozens of specialized MCP servers

## ☁️ AWS Production Deployment

### Prerequisites

- AWS CLI configured
- ECR repository created
- ECS cluster and service configured
- AWS Secrets Manager secrets created

### 1. Create AWS Secrets

```bash
# Create Slack Bot Token secret
aws secretsmanager create-secret \
    --name slack-mcp/slack-bot-token \
    --description "Slack Bot Token for MCP Server" \
    --secret-string "xoxb-your-bot-token-here"

# Create OpenAI API Key secret
aws secretsmanager create-secret \
    --name slack-mcp/openai-api-key \
    --description "OpenAI API Key for AI features" \
    --secret-string "sk-your-openai-api-key-here"

# Create other secrets as needed
aws secretsmanager create-secret \
    --name slack-mcp/slack-app-token \
    --description "Slack App Token" \
    --secret-string "xapp-your-app-token-here"
```

### 2. Update Environment for AWS

```bash
# Set USE_AWS_SECRETS=true in your deployment environment
export USE_AWS_SECRETS=true
export AWS_REGION=us-east-1
```

### 3. Deploy with Docker

```bash
# Build and tag the image
docker build -t slack-mcp-server:latest .

# Tag for ECR (replace with your account ID)
docker tag slack-mcp-server:latest \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/slack-mcp-server:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.us-east-1.amazonaws.com

# Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/slack-mcp-server:latest

# Deploy to ECS (update service)
aws ecs update-service \
    --cluster slack-mcp-cluster \
    --service slack-mcp-service \
    --force-new-deployment
```

### 4. ECS Task Definition

Use the provided `task-definition.json` file with your AWS account details:

```bash
# Register the task definition
aws ecs register-task-definition \
    --cli-input-json file://task-definition.json
```

### 5. Load Balancer Setup

The server will be available at your ALB endpoint:
- Health check: `GET /health`
- MCP endpoint: `POST /mcp/`

## 🔧 Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests (when test files are created)
pytest
```

### Code Structure

```
mcpslack/
├── main.py                 # FastMCP server implementation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .env                   # Your environment variables
├── Dockerfile             # Container configuration
├── task-definition.json   # ECS task definition
├── deploy.sh              # Deployment script
├── claude_desktop_config.json  # Claude Desktop config
└── README.md              # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **"Slack client not initialized"**
   - Check your `SLACK_BOT_TOKEN` in `.env` file
   - Ensure the token starts with `xoxb-`

2. **"OpenAI client not initialized"**
   - Check your `OPENAI_API_KEY` in `.env` file
   - Ensure the token starts with `sk-`
   - Verify you have sufficient OpenAI credits

3. **"Missing scope" errors**
   - Add required scopes in your Slack app settings
   - Reinstall the app to your workspace

4. **Claude Desktop not loading server**
   - Check the path in `claude_desktop_config.json`
   - Ensure Python is in your PATH
   - Restart Claude Desktop

5. **AWS deployment issues**
   - Verify IAM roles have correct permissions
   - Check CloudWatch logs for error details
   - Ensure secrets exist in Secrets Manager

### Debugging

Enable debug mode by setting `DEBUG=true` in your `.env` file:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📋 Required Slack Permissions

Make sure your Slack app has these OAuth scopes:

- `channels:read` - List public channels
- `channels:history` - Read public channel messages
- `chat:write` - Send messages
- `groups:read` - List private channels
- `groups:history` - Read private channel messages
- `users:read` - Get user information
- `search:read` - Search messages (requires approval)
- `channels:manage` - Create channels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with Claude Desktop
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙋 Support

- Check the troubleshooting section above
- Review Claude Desktop MCP documentation
- Open an issue for bugs or feature requests

---

Built with ❤️ using [FastMCP](https://github.com/jlowin/fastmcp) 2.8.0