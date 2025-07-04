# 🚀 Slack MCP Server

*Transform your Slack workspace into an intelligent AI assistant with real-time responses*

[![GitHub stars](https://img.shields.io/github/stars/bahakizil/slack_mcp?style=social)](https://github.com/bahakizil/slack_mcp)
[![GitHub license](https://img.shields.io/github/license/bahakizil/slack_mcp)](https://github.com/bahakizil/slack_mcp/blob/main/LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.8.0-green.svg)](https://github.com/jlowin/fastmcp)

A production-ready **Slack MCP Server** that combines real-time Socket Mode integration with AI-powered tools. Built with FastMCP 2.8.0, this project provides **18+ tools** for Claude Desktop and features an autonomous AI assistant that can plan and execute complex tasks.

## ⭐ What Makes This Special?

🤖 **Real-Time Socket Mode Bot** - Instant responses to Slack mentions (< 2 seconds)  
🧠 **Autonomous AI Agent** - AI that plans its own execution strategies  
🔧 **18+ MCP Tools** - Complete Slack workspace management via Claude Desktop  
🌐 **Web Research Integration** - Real-time web search with Tavily API  
⚡ **Production Ready** - Docker + AWS ECS deployment included  
🛡️ **Enterprise Security** - AWS Secrets Manager integration  

## 🎥 Demo

![claude_text](https://github.com/user-attachments/assets/dd1b6b01-5bda-46df-9f7d-05a19be6109f)

![slackchat](https://github.com/user-attachments/assets/2a9599e5-430c-434f-a1b3-4da4bcbcb244)


@MCP Bot analyze yesterday's #product-meeting and research mentioned technologies
```
↓ *2 seconds later* ↓
```
🤖 Analysis Complete! Found discussion about React 18, TypeScript 5.0, and Docker.
📊 Meeting Summary: [Detailed analysis...]
🔍 Technology Research: [Latest developments...]
📝 Action Items: [Extracted tasks...]
```

## 🚀 Quick Start (5 Minutes)

### 1. Clone & Install
```bash
git clone https://github.com/bahakizil/slack_mcp.git
cd slack_mcp
pip install -r requirements.txt
```

### 2. Configure API Keys
Create `.env` file:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token        # From api.slack.com/apps
SLACK_APP_TOKEN=xapp-your-app-token        # For Socket Mode (required!)
OPENAI_API_KEY=sk-your-openai-key          # From platform.openai.com
TAVILY_API_KEY=tvly-your-tavily-key        # From tavily.com (optional)
```

### 3. Start the Server
```bash
python main.py
```

**Success Output:**
```
🤖 Starting Slack MCP Server with Real-time Mode
⚡ Socket Mode: Enabled (Real-time auto-responses)
✅ Bot ready for mentions: @MCP Bot
INFO: Uvicorn running on http://0.0.0.0:8003
```

### 4. Test in Slack
```
@MCP Bot hello!
```
```
🤖 Hello! I'm your AI assistant. How can I help you today? 😊
```

**🎉 Your AI assistant is now live!**

## 🔧 Complete Feature Set

### 📱 Slack Management (6 Tools)
| Tool | Description | Example |
|------|-------------|---------|
| `send_slack_message` | Send messages to channels | `send_slack_message("general", "Hello team!")` |
| `get_slack_channels` | List all workspace channels | `get_slack_channels()` |
| `get_slack_messages` | Retrieve channel history | `get_slack_messages("engineering", limit=50)` |
| `search_slack_messages` | Search across workspace | `search_slack_messages("deployment")` |
| `create_slack_channel` | Create new channels | `create_slack_channel("new-project")` |
| `analyze_slack_conversation` | AI-powered analysis | `analyze_slack_conversation("planning", "summary")` |

### 🤖 AI Intelligence (3 Tools)
| Tool | Description | Use Case |
|------|-------------|----------|
| `ask_ai` | Ask questions to GPT-4o-mini | Technical explanations, brainstorming |
| `autonomous_assistant` | **🌟 Self-planning AI agent** | Complex multi-step tasks |
| Socket Mode Bot | Real-time auto-responses | Instant Slack interaction |

### 🌐 Web Research (3 Tools)
| Tool | Description | Example |
|------|-------------|---------|
| `search_web` | General web search | `search_web("latest AI developments 2024")` |
| `search_news` | News-specific search | `search_news("tech industry", days=7)` |
| `research_topic` | Deep research analysis | `research_topic("microservices architecture")` |

### 🔗 MCP Server Management (6 Tools)
| Tool | Description | Purpose |
|------|-------------|---------|
| `add_mcp_server` | Connect external MCP servers | Extend functionality |
| `list_mcp_servers` | Show all configured servers | Server management |
| `connect_mcp_server` | Establish connections | Activate external tools |
| `disconnect_mcp_server` | Close connections | Resource management |
| `list_external_tools` | Browse external tools | Tool discovery |
| `call_external_tool` | Execute external tools | Cross-server operations |

## 🧠 Autonomous AI Assistant

The **autonomous assistant** is the crown jewel of this project. It can:

- 📋 **Plan its own execution** - No pre-programmed workflows
- 🔍 **Discover tools dynamically** - Adapts to available resources  
- 🔄 **Self-reflect and optimize** - Learns from execution history
- 📊 **Synthesize multi-source data** - Combines Slack + web + AI knowledge

### Example: Complex Task Execution
```python
autonomous_assistant(
    request="Analyze all engineering discussions this week, research mentioned technologies, and create a strategic report",
    send_to_slack=True
)
```

**What happens behind the scenes:**
1. 🔍 **Discovery**: Finds available Slack channels and tools
2. 🧠 **Planning**: AI creates step-by-step execution plan
3. ⚡ **Execution**: Runs multiple tools in sequence
4. 🔬 **Research**: Web searches for mentioned technologies
5. 📊 **Synthesis**: Combines all data into comprehensive report
6. 📨 **Delivery**: Posts results to Slack automatically

## 🖥️ Claude Desktop Integration

### Configuration
Add to `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "slack-ai-assistant": {
      "command": "python",
      "args": ["/full/path/to/main.py"],
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

### Usage Examples in Claude Desktop

**Meeting Analysis:**
```
Analyze yesterday's #product-meeting channel and summarize key decisions, action items, and sentiment.
```

**Tech Research + Slack Update:**
```
Research current best practices for microservices deployment and share findings in #engineering channel.
```

**Multi-Channel Intelligence:**
```
Compare discussions across #design, #engineering, and #marketing channels this week. Identify common themes and potential collaboration opportunities.
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AUTONOMOUS AI SYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  SLACK MCP      │    │  TAVILY MCP     │                │
│  │  SERVER         │    │  SERVER         │                │
│  │  Port: 8001     │    │  Port: 8002     │                │
│  │                 │    │                 │                │
│  │ • Slack Tools   │    │ • Web Search    │                │
│  │ • AI Tools      │    │ • News Search   │                │
│  │ • Orchestration │    │ • Research      │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                        │
│           └───────────┐   ┌───────┘                        │
│                      │   │                               │
│               ┌─────────────────┐                          │
│               │ AUTONOMOUS      │                          │
│               │ AGENT           │                          │
│               │                 │                          │
│               │ • Tool Discovery│                          │
│               │ • Plan Creation │                          │
│               │ • Execution     │                          │
│               │ • Synthesis     │                          │
│               └─────────────────┘                          │
│                       │                                    │
│               ┌─────────────────┐                          │
│               │ OPENAI GPT      │                          │
│               │ (gpt-4.1-nano)  │                          │
│               └─────────────────┘                          │
└─────────────────────────────────────────────────────────────┘






![diagram](https://github.com/user-attachments/assets/ec1584c6-a194-4414-8861-d8cc86d74e35)





## ☁️ Production Deployment

### 🐳 Docker Deployment
```bash
# Build and run locally
docker build -t slack-mcp-server .
docker run -p 8003:8003 --env-file .env slack-mcp-server
```

### 🚀 AWS ECS Deployment (Production)
```bash
# Automated deployment
./deploy.sh
```

**Includes:**
- ✅ **Auto-scaling** based on traffic
- ✅ **Health checks** and monitoring
- ✅ **AWS Secrets Manager** for secure credential management
- ✅ **Application Load Balancer** for high availability
- ✅ **CloudWatch logging** for debugging

### 📊 Production Features
- **Zero downtime deployments**
- **Horizontal scaling** (multiple instances)
- **SSL/TLS termination**
- **Custom domain support**
- **Monitoring & alerting**

## 🛡️ Security Best Practices

### 🔐 Credential Management
- **Environment variables** for local development
- **AWS Secrets Manager** for production
- **No hardcoded secrets** in code
- **Git ignore** for sensitive files

### 🛠️ Error Handling
- **Graceful degradation** when services are down
- **Retry logic** for transient failures
- **User-friendly error messages**
- **Comprehensive logging**

### 📈 Performance
- **Socket Mode** eliminates polling overhead
- **Async processing** for non-blocking operations
- **Connection pooling** for API efficiency
- **Response time < 2 seconds**

## 🎯 Real-World Use Cases

### 👥 For Teams
- **Daily standups**: "Summarize yesterday's progress across all channels"
- **Sprint planning**: "Analyze #product-backlog and prioritize by urgency"
- **Knowledge sharing**: "Research best practices for the technologies we discussed"

### 🏢 For Managers
- **Team sentiment**: "Analyze team mood and engagement this week"
- **Progress tracking**: "Extract action items from all project channels"
- **Strategic insights**: "Compare our technical discussions with industry trends"

### 🔬 For Developers
- **Tech research**: "Find the latest updates on frameworks we're using"
- **Code review insights**: "Analyze #code-review discussions for common issues"
- **Learning automation**: "Create weekly tech digest from our discussions"

## 📚 Documentation

- 📖 **[Quick Start Guide](./QUICK_START.md)** - 5-minute setup
- 🏗️ **[Complete Technical Guide](./COMPLETE_GUIDE.md)** - In-depth architecture
- 🚀 **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - Production deployment
- ✅ **[Project Status](./FINAL_STATUS.md)** - Current implementation status

## 🔧 Requirements

### Slack App Setup
Required **Bot Token Scopes**:
```
channels:read, channels:history, chat:write, groups:read, 
groups:history, users:read, search:read, channels:manage
```

### API Keys
- **Slack Bot Token** (`xoxb-...`) - Required
- **Slack App Token** (`xapp-...`) - Required for Socket Mode
- **OpenAI API Key** (`sk-...`) - Required for AI features
- **Tavily API Key** (`tvly-...`) - Optional for web search

### System Requirements
- **Python 3.11+**
- **4GB RAM** (minimum)
- **Network access** to Slack, OpenAI, and Tavily APIs

## 🔍 Troubleshooting

### Common Issues

**1. Socket Mode not working**
```bash
# Check App Token configuration
echo $SLACK_APP_TOKEN  # Should start with xapp-

# Verify Socket Mode is enabled in Slack app settings
# Go to api.slack.com/apps → Your App → Socket Mode → Enable
```

**2. Bot not responding**
```bash
# Check bot token
echo $SLACK_BOT_TOKEN  # Should start with xoxb-

# Verify terminal shows:
# ✅ Socket Mode: Enabled (Real-time auto-responses)
```

**3. Claude Desktop not loading**
```bash
# Check config file path and restart Claude Desktop
# Verify Python is in PATH: python --version
```

### Debug Mode
```bash
# Enable detailed logging
export DEBUG=true
export LOG_LEVEL=DEBUG
python main.py
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 🎯 Areas for Contribution
- 🔧 **New MCP tools** - Extend functionality
- 🌐 **Language support** - Add more languages
- 📊 **Analytics features** - Advanced reporting
- 🔌 **Integration templates** - More external services
- 📚 **Documentation** - Examples and tutorials

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support & Community

- 💬 **Issues**: [GitHub Issues](https://github.com/bahakizil/slack_mcp/issues)
- 📖 **Documentation**: Check the `docs/` folder
- 🐛 **Bug Reports**: Use issue templates
- 💡 **Feature Requests**: Community-driven roadmap

## 🌟 Acknowledgments

- **[FastMCP](https://github.com/jlowin/fastmcp)** - Amazing MCP framework
- **[Slack SDK](https://github.com/slackapi/python-slack-sdk)** - Robust Slack integration
- **[OpenAI](https://openai.com)** - Powerful AI capabilities
- **[Tavily](https://tavily.com)** - Excellent web search API

---

## 🚀 Ready to Get Started?

1. **⭐ Star this repository** if you find it useful
2. **🍴 Fork it** to start customizing
3. **📥 Clone it** and follow the 5-minute setup
4. **🤖 Mention your bot** in Slack and watch the magic happen!

**Built with ❤️ by [Baha Kızıl](https://github.com/bahakizil)**

*Transform your Slack workspace into an AI-powered productivity hub today!* 🚀
