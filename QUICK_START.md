# ⚡ Quick Start Guide - Real-Time AI Slack Assistant

## 🎯 What You're Building

A **real-time AI system** that:
- 🧠 **Responds instantly** to Slack mentions with AI-powered answers
- 📱 **Manages Slack workspaces** intelligently via MCP tools
- 🌐 **Researches web information** automatically using Tavily API
- ⚡ **Works 24/7** with Socket Mode - no manual intervention needed!

## 🚀 30-Second Setup

### 1. Install & Configure

```bash
# Clone and install
git clone <repo-url>
cd Slack_MCP_Server-main
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 2. Get Your API Keys

1. **Slack Bot Token & App Token**: 
   - Go to [slack.com/api/apps](https://slack.com/api/apps) → Create App → OAuth & Permissions
   - Get Bot Token (xoxb-...) and App Token (xapp-...) for Socket Mode
2. **OpenAI API Key**: Go to [platform.openai.com](https://platform.openai.com) → API Keys → Create new key  
3. **Tavily API Key**: Go to [tavily.com](https://tavily.com) → Sign up → Get API key (for web search)

### 3. Add Your API Keys

Edit `.env`:
```bash
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token      # Required: From slack.com/api/apps
SLACK_APP_TOKEN=xapp-your-slack-app-token      # Required: For Socket Mode real-time events
OPENAI_API_KEY=sk-your-openai-api-key          # Required: From platform.openai.com
TAVILY_API_KEY=tvly-your-tavily-api-key        # Optional: From tavily.com (enables web search)
```

### 4. Start the System (Single Command!)

```bash
# Start the unified server with Socket Mode
python main.py
```

**✅ Success Output:**
```
🤖 Starting Slack MCP Server with Real-time Mode
⚡ Socket Mode: Enabled (Real-time auto-responses)
✅ Bot ready for mentions: @MCP Bot
INFO: Uvicorn running on http://0.0.0.0:8003
```

### 5. Test Real-Time Responses

Go to any Slack channel and mention the bot:
```
@MCP Bot merhaba!
```

The bot responds automatically within 2 seconds! 🎉

## 🎮 Instant Usage

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "slack-ai-assistant": {
      "command": "python",
      "args": ["/path/to/main.py"],
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

### Try These Commands in Claude Desktop

**Simple Message:**
```
send_slack_message(channel="general", message="Hello AI! 👋")
```

**AI-Powered Analysis:**
```
ask_ai(question="Analyze the pros and cons of remote work", context="For our team discussion")
```

**Web Research:**
```
search_web(query="latest AI developments 2024", max_results=5)
```

**Autonomous Intelligence:**
```
autonomous_assistant(
  request="Summarize #engineering discussions and research mentioned technologies",
  channel="engineering", 
  send_to_slack=true
)
```

## 🧠 Real-Time Bot Magic

### How Socket Mode Works:
```
👤 User mentions: "@MCP Bot help me with project planning"
⚡ Socket Mode: Receives event instantly (no polling!)
🤖 AI: Generates contextual response with GPT-4o-mini
💬 Bot: "🤖 I'd be happy to help with project planning! What specific aspects would you like assistance with - timeline, resources, task breakdown, or risk assessment? 😊"
✅ Total time: < 2 seconds
```

### Traditional vs Our Approach:
**Traditional Chatbot (Polling every 30s):**
```python
while True:
    check_for_mentions()  # API call every 30 seconds
    time.sleep(30)        # May hit rate limits
```

**Our Socket Mode Bot:**
```python
@socket_client.event_handler("app_mention")
def handle_mention(event):
    ai_response = generate_response(event.text)
    send_to_slack(ai_response)  # Instant response!
```

## 🔧 Available Tools (18+)

### 📱 Slack Management (6 tools)
- `send_slack_message` - Send messages to channels
- `get_slack_channels` - List all channels  
- `get_slack_messages` - Get conversation history
- `search_slack_messages` - Search workspace content
- `create_slack_channel` - Create new channels
- `analyze_slack_conversation` - AI-powered conversation analysis

### 🤖 AI Intelligence (3 tools)
- `ask_ai` - Ask questions to GPT-4o-mini
- `autonomous_assistant` - **🌟 Full autonomous AI agent**
- Socket Mode Real-time responses (automatic)

### 🌐 Web Research (3 tools)  
- `search_web` - General web search with real-time results
- `search_news` - Latest news and articles
- `research_topic` - Deep research with comprehensive analysis

### 🔗 MCP Server Management (6 tools)
- `add_mcp_server` - Connect to external MCP servers
- `list_mcp_servers` - See all available servers
- `connect_mcp_server` - Establish connections
- `disconnect_mcp_server` - Close connections
- `list_external_tools` - Browse external tools
- `call_external_tool` - Execute external tools

## 💡 Pro Usage Examples

### Real-Time Slack Bot
```
# Just mention the bot anywhere in Slack:
@MCP Bot what are the best practices for code reviews?

# Bot responds automatically with AI-powered answer!
```

### Meeting Summary + Tech Research
```
# Via Claude Desktop:
autonomous_assistant(
  request="Analyze yesterday's #product-meeting channel and research current trends for any technologies discussed. Create a strategic report.",
  channel="product-meeting",
  send_to_slack=true
)
```

### Multi-Channel Intelligence  
```
# Compare discussions across channels:
ask_ai(
  question="What are the common themes across our design, engineering, and marketing discussions this week?",
  context="Include Slack data from #design, #engineering, #marketing"
)
```

## 🏗️ Simplified Architecture

```
┌─────────────────────────────────────────┐
│           UNIFIED SERVER                │
│           (main.py - Port 8003)         │
│                                         │
│  ┌─────────────┐    ┌─────────────┐    │
│  │ Socket Mode │    │  MCP Tools  │    │
│  │   Real-time │    │   18+ tools │    │
│  │  Slack Bot  │    │             │    │
│  └─────────────┘    └─────────────┘    │
│           │                  │          │
│           └──────┬──────────┘          │
│                  │                      │
│         ┌─────────────┐                │
│         │ AI Engine   │                │
│         │ GPT-4o-mini │                │
│         │ + Tavily    │                │
│         └─────────────┘                │
└─────────────────────────────────────────┘
```

## 🚨 Troubleshooting

**Server won't start:**
```bash
# Check if port is available
lsof -i :8003

# Test API keys  
python -c "from openai import OpenAI; print('OpenAI OK')"
python -c "from slack_sdk import WebClient; print('Slack OK')"
```

**Socket Mode not working:**
```bash
# Verify App Token in .env
echo $SLACK_APP_TOKEN  # Should start with xapp-

# Check Slack app settings:
# 1. Go to api.slack.com/apps
# 2. Your App → Socket Mode → Enable Socket Mode
# 3. Event Subscriptions → Subscribe to bot events → app_mention
```

**Bot not responding:**
```bash
# Check terminal output for Socket Mode status:
# ✅ Socket Mode: Enabled (Real-time auto-responses)
# ✅ Bot ready for mentions: @MCP Bot

# If missing, check SLACK_APP_TOKEN configuration
```

## 🎯 Success Indicators

✅ **Terminal shows:** "Socket Mode: Enabled"  
✅ **Bot responds** to @MCP Bot mentions automatically  
✅ **Claude Desktop** shows 18+ tools available  
✅ **Response time** < 2 seconds for Slack mentions  
✅ **No manual commands** needed for bot operation

## 🚀 You're Ready!

Your AI assistant is now:
- 🤖 **Responding automatically** to Slack mentions
- 🔧 **Available in Claude Desktop** with 18+ tools
- 🌐 **Researching web information** via Tavily
- ⚡ **Working 24/7** with Socket Mode

**Just mention @MCP Bot in any Slack channel and watch the magic happen!** ✨