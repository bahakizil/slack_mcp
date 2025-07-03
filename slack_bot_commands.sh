#!/bin/bash
# Slack MCP Bot Management Commands

echo "🤖 Slack MCP Bot Management Commands"
echo "===================================="

case "$1" in
    "start")
        echo "🚀 Starting MCP Server..."
        python main.py
        ;;
    "test")
        echo "🧪 Testing bot connections..."
        python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('🔍 Environment Check:')
print(f'  SLACK_BOT_TOKEN: {\"✅ Set\" if os.getenv(\"SLACK_BOT_TOKEN\") else \"❌ Missing\"}')
print(f'  OPENAI_API_KEY: {\"✅ Set\" if os.getenv(\"OPENAI_API_KEY\") else \"❌ Missing\"}')
print(f'  TAVILY_API_KEY: {\"✅ Set\" if os.getenv(\"TAVILY_API_KEY\") else \"❌ Missing\"}')
print()
print('🔧 Testing imports...')
try:
    from slack_sdk import WebClient
    from openai import OpenAI
    from fastmcp import FastMCP
    print('✅ All dependencies available')
except ImportError as e:
    print(f'❌ Import error: {e}')
"
        ;;
    "status")
        echo "📊 Checking server status..."
        ps aux | grep -E "python.*main.py|MCP.*Server" | grep -v grep || echo "❌ No MCP server processes found"
        ;;
    "stop")
        echo "🛑 Stopping all bot services..."
        pkill -f "python.*main.py"
        echo "✅ Services stopped"
        ;;
    *)
        echo ""
        echo "📋 Available commands:"
        echo ""
        echo "  ./slack_bot_commands.sh start   # Start the MCP Server"
        echo "  ./slack_bot_commands.sh test    # Test environment and dependencies"
        echo "  ./slack_bot_commands.sh status  # Check server status"
        echo "  ./slack_bot_commands.sh stop    # Stop all services"
        echo ""
        echo "🎯 Quick usage:"
        echo "   1. Configure your .env file with API keys"
        echo "   2. Run './slack_bot_commands.sh test' to verify setup"
        echo "   3. Run './slack_bot_commands.sh start' to launch the server"
        echo "   4. Mention @MCP Bot in Slack for real-time responses"
        echo ""
        ;;
esac 