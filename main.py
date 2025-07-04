#!/usr/bin/env python3
"""
Slack MCP Server with Real-time Socket Mode Integration
Professional AI assistant for Slack workspace management and web research.
"""

import os
import json
import threading
import time
import asyncio
import concurrent.futures
from typing import Dict, Any, List, Optional
from datetime import datetime

from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ResourceError
from openai import OpenAI
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.errors import SlackApiError
import aiohttp
import requests

from autonomous_agent import AutonomousAgent

load_dotenv()


class SlackMCPServer:
    """Professional Slack MCP Server with real-time Socket Mode capabilities."""

    def __init__(self):
        """Initialize the Slack MCP Server with all required clients and tools."""
        self.mcp = FastMCP(
            name="Slack AI Assistant",
            mask_error_details=True,
            on_duplicate_resources="warn"
        )
        
        # Initialize clients
        self.slack_client = self._initialize_slack_client()
        self.socket_client = self._initialize_socket_mode()
        self.openai_client = self._initialize_openai_client()
        self.autonomous_agent = AutonomousAgent()
        
        # Bot configuration
        self.bot_user_id = None
        
        # Setup server components
        self._register_mcp_tools()
        self._setup_socket_event_handlers()

    def _initialize_slack_client(self) -> Optional[WebClient]:
        """Initialize and authenticate Slack WebClient."""
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return None

        try:
            client = WebClient(token=token)
            auth_response = client.auth_test()
            self.bot_user_id = auth_response.get("user_id")
            return client
        except SlackApiError as e:
            print(f"Slack authentication failed: {e}")
            return None

    def _initialize_socket_mode(self) -> Optional[SocketModeClient]:
        """Initialize Socket Mode client for real-time event handling."""
        app_token = os.getenv("SLACK_APP_TOKEN")
        if not app_token or not self.slack_client:
            return None

        try:
            return SocketModeClient(
                app_token=app_token,
                web_client=self.slack_client
            )
        except Exception as e:
            print(f"Socket Mode initialization failed: {e}")
            return None

    def _initialize_openai_client(self) -> Optional[OpenAI]:
        """Initialize OpenAI client for AI processing."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        try:
            return OpenAI(api_key=api_key)
        except Exception as e:
            print(f"OpenAI client initialization failed: {e}")
            return None

    def _setup_socket_event_handlers(self) -> None:
        """Configure Socket Mode event handlers for real-time processing."""
        if not self.socket_client:
            return

        def handle_socket_mode_request(client, req) -> None:
            """Process incoming Socket Mode requests."""
            try:
                # Acknowledge request immediately
                response = SocketModeResponse(envelope_id=req.envelope_id)
                client.send_socket_mode_response(response)

                # Process events
                if req.type == "events_api":
                    event = req.payload.get("event", {})
                    if event.get("type") == "app_mention":
                        self._handle_app_mention(event)
                        
            except Exception as e:
                print(f"Socket Mode request handling error: {e}")

        self.socket_client.socket_mode_request_listeners.append(handle_socket_mode_request)

    def _handle_app_mention(self, event: Dict[str, Any]) -> None:
        """Process app mentions with intelligent query routing."""
        try:
            # Validate event and clients
            if not self._validate_mention_event(event):
                return

            # Extract and clean message content
            channel = event.get("channel")
            user = event.get("user")
            text = self._clean_mention_text(event.get("text", ""))
            
            if not text or user == self.bot_user_id or not channel:
                return

            # Route query based on content analysis
            self._route_and_process_query(text, channel)
                
        except Exception as e:
            print(f"App mention handling error: {e}")
            self._send_error_response(event.get("channel"))

    def _validate_mention_event(self, event: Dict[str, Any]) -> bool:
        """Validate that mention event can be processed."""
        return (
            self.slack_client is not None and
            event.get("channel") is not None and
            event.get("user") is not None
        )

    def _clean_mention_text(self, text: str) -> str:
        """Remove bot mentions and clean up message text."""
        if self.bot_user_id:
            text = text.replace(f"<@{self.bot_user_id}>", "").strip()
        return text

    def _route_and_process_query(self, query: str, channel: str) -> None:
        """Intelligently route queries to appropriate processing methods."""
        query_type = self._analyze_query_type(query)
        
        try:
            if query_type == "web_search":
                self._process_web_search(query, channel)
            elif query_type == "slack_query":
                self._process_slack_query(query, channel)
            else:
                self._process_general_chat(query, channel)
                
        except Exception as e:
            print(f"Query processing error: {e}")
            self._send_error_response(channel)

    def _analyze_query_type(self, query: str) -> str:
        """Analyze query content to determine processing type."""
        query_lower = query.lower()
        
        # Web search indicators
        search_keywords = ["search", "find", "research", "news", "latest", "investigate"]
        if any(keyword in query_lower for keyword in search_keywords):
            return "web_search"
        
        # Slack-specific query indicators  
        slack_keywords = ["channel", "message", "discuss", "slack", "who", "what"]
        if any(keyword in query_lower for keyword in slack_keywords):
            return "slack_query"
            
        return "general_chat"

    def _process_web_search(self, query: str, channel: str) -> None:
        """Process web search requests using Tavily API with AI enhancement."""
        try:
            # Send initial search notification
            self._send_message(channel, "🔍 Searching...")
            
            # Determine search type and execute
            search_type = "news" if "news" in query.lower() else "general"
            result = self._execute_web_search(query, search_type)
            
            # Send results
            self._send_message(channel, result)
            
        except Exception as e:
            print(f"Web search error: {e}")
            self._send_message(channel, "❌ Search failed. Please try again later.")

    def _execute_web_search(self, query: str, search_type: str = "general") -> str:
        """Execute web search with AI processing."""
        try:
            # Run async search in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                if search_type == "news":
                    result = loop.run_until_complete(self._tavily_news_search(query))
                else:
                    result = loop.run_until_complete(self._tavily_web_search(query))
                return result
            finally:
                loop.close()
                
        except Exception as e:
            return f"❌ Search execution failed: {str(e)}"

    async def _tavily_web_search(self, query: str) -> str:
        """Perform enhanced web search using Tavily API."""
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            if not tavily_key:
                return "❌ Web search unavailable - API key not configured"

            # Execute Tavily search
            search_data = await self._call_tavily_api(query, "general")
            if not search_data:
                return "❌ Search failed - no results returned"

            # Process results with AI if available
            if self.openai_client:
                return await self._process_search_with_ai(search_data, query, "web")
            else:
                return self._format_basic_search_results(search_data, query)
                
        except Exception as e:
            return f"❌ Web search error: {str(e)}"

    async def _tavily_news_search(self, query: str) -> str:
        """Perform news-focused search using Tavily API."""
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            if not tavily_key:
                return "❌ News search unavailable - API key not configured"

            # Execute Tavily news search
            search_data = await self._call_tavily_api(f"latest news {query}", "news")
            if not search_data:
                return "❌ News search failed - no results returned"

            # Process results with AI if available
            if self.openai_client:
                return await self._process_search_with_ai(search_data, query, "news")
            else:
                return self._format_basic_news_results(search_data, query)
                
        except Exception as e:
            return f"❌ News search error: {str(e)}"

    async def _call_tavily_api(self, query: str, search_type: str) -> Optional[Dict[str, Any]]:
        """Make API call to Tavily search service."""
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            payload = {
                "api_key": tavily_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_raw_content": False,
                "max_results": 8 if search_type == "general" else 6
            }
            
            if search_type == "news":
                payload["topic"] = "news"

            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.tavily.com/search", json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Tavily API error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"Tavily API call failed: {e}")
            return None

    async def _process_search_with_ai(self, data: Dict[str, Any], query: str, search_type: str) -> str:
        """Process search results using AI for enhanced formatting."""
        try:
            # Prepare results for AI processing
            results_summary = {
                "query": query,
                "answer": data.get("answer", ""),
                "results": data.get("results", [])[:5]
            }

            # Create AI prompt based on search type
            if search_type == "news":
                prompt = self._create_news_processing_prompt(results_summary)
                prefix = "📰 **Latest News:**"
            else:
                prompt = self._create_web_processing_prompt(results_summary)
                prefix = "🔍 **Search Results:**"

            # Process with OpenAI
            if not self.openai_client:
                # Fallback if OpenAI not available
                if search_type == "news":
                    return self._format_basic_news_results(data, query)
                else:
                    return self._format_basic_search_results(data, query)
                    
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": self._get_ai_system_prompt(search_type)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )

            processed_content = response.choices[0].message.content
            return f"{prefix} {query}\n\n{processed_content}"
            
        except Exception as e:
            print(f"AI processing failed: {e}")
            # Fallback to basic formatting
            if search_type == "news":
                return self._format_basic_news_results(data, query)
            else:
                return self._format_basic_search_results(data, query)

    def _create_web_processing_prompt(self, results: Dict[str, Any]) -> str:
        """Create prompt for AI processing of web search results."""
        prompt = f"Based on the web search results for '{results['query']}', provide a comprehensive summary.\n\n"
        prompt += f"Main Answer: {results['answer']}\n\nTop Sources:\n"
        
        for i, result in enumerate(results['results'], 1):
            prompt += f"{i}. {result.get('title', 'Untitled')}\n"
            prompt += f"   URL: {result.get('url', 'N/A')}\n"
            prompt += f"   Content: {result.get('content', 'No content')[:300]}...\n\n"
        
        prompt += "Please provide a well-structured, informative summary with key findings and credible sources."
        return prompt

    def _create_news_processing_prompt(self, results: Dict[str, Any]) -> str:
        """Create prompt for AI processing of news search results."""
        prompt = f"Based on the news search results for '{results['query']}', provide a news summary.\n\n"
        prompt += f"Summary: {results['answer']}\n\nLatest News:\n"
        
        for i, result in enumerate(results['results'], 1):
            prompt += f"{i}. {result.get('title', 'Untitled')}\n"
            prompt += f"   Source: {result.get('url', 'N/A')}\n"
            prompt += f"   Content: {result.get('content', 'No content')[:300]}...\n\n"
        
        prompt += "Please provide a clear news summary highlighting recent developments with proper source attribution."
        return prompt

    def _get_ai_system_prompt(self, search_type: str) -> str:
        """Get appropriate system prompt for AI processing."""
        if search_type == "news":
            return "You are a professional news reporter that processes search results and provides accurate, well-formatted news summaries with focus on recent developments."
        else:
            return "You are a research assistant that processes web search results and provides comprehensive, well-formatted summaries with proper citations."

    def _format_basic_search_results(self, data: Dict[str, Any], query: str) -> str:
        """Basic formatting fallback for search results."""
        result = f"🔍 **Search Results: {query}**\n\n"
        
        if data.get("answer"):
            result += f"**Summary:** {data['answer']}\n\n"
        
        result += "**Key Sources:**\n"
        for i, item in enumerate(data.get("results", [])[:3], 1):
            result += f"{i}. **{item.get('title', 'N/A')}**\n"
            result += f"   {item.get('content', 'No content')[:200]}...\n"
            result += f"   Source: {item.get('url', 'N/A')}\n\n"
        
        return result

    def _format_basic_news_results(self, data: Dict[str, Any], query: str) -> str:
        """Basic formatting fallback for news results."""
        result = f"📰 **Latest News: {query}**\n\n"
        
        if data.get("answer"):
            result += f"**Summary:** {data['answer']}\n\n"
        
        result += "**Recent News:**\n"
        for i, item in enumerate(data.get("results", [])[:3], 1):
            result += f"{i}. **{item.get('title', 'N/A')}**\n"
            result += f"   {item.get('content', 'No content')[:200]}...\n"
            result += f"   Source: {item.get('url', 'N/A')}\n\n"
        
        return result

    def _process_slack_query(self, query: str, channel: str) -> None:
        """Process Slack-specific queries using MCP tools."""
        try:
            result = self._handle_slack_operation(query, channel)
            self._send_message(channel, result)
            
        except Exception as e:
            print(f"Slack query processing error: {e}")
            self._send_message(channel, "❌ Unable to process Slack query.")

    def _handle_slack_operation(self, query: str, channel: str) -> str:
        """Execute specific Slack operations based on query content."""
        query_lower = query.lower()
        
        # Channel listing
        if "channel" in query_lower and any(word in query_lower for word in ["list", "show", "what"]):
            return self._get_channel_list()
        
        # Message history from specific channel
        elif "message" in query_lower or "discuss" in query_lower:
            target_channel = self._extract_channel_from_query(query)
            if target_channel:
                return self._get_channel_messages(target_channel)
            else:
                return "Please specify which channel you'd like to check. Example: 'What was discussed in #general?'"
        
        # General capabilities
        elif "tool" in query_lower or "can" in query_lower:
            return self._get_capabilities_info()
        
        else:
            # Use autonomous assistant for complex queries
            return self._use_autonomous_assistant(query, channel)

    def _get_channel_list(self) -> str:
        """Retrieve and format list of accessible channels."""
        try:
            if not self.slack_client:
                return "❌ Slack connection not available."
            
            response = self.slack_client.conversations_list(exclude_archived=True)
            channels = response.get("channels", [])
            
            if not channels:
                return "No accessible channels found."
            
            channel_info = ["📋 **Available Channels:**\n"]
            for ch in channels[:10]:
                name = ch.get("name", "Unknown")
                purpose = ch.get("purpose", {}).get("value", "")
                channel_info.append(f"#{name}" + (f" - {purpose[:50]}..." if purpose else ""))
            
            return "\n".join(channel_info)
            
        except Exception as e:
            return f"❌ Error retrieving channels: {str(e)}"

    def _extract_channel_from_query(self, query: str) -> Optional[str]:
        """Extract channel name from user query."""
        import re
        
        # Look for #channel or "channel" patterns
        patterns = [
            r'#(\w+)',
            r'(\w+)\s+channel',
            r'in\s+(\w+)',
            r'from\s+(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1)
        
        return None

    def _get_channel_messages(self, channel_name: str) -> str:
        """Retrieve and format recent messages from specified channel."""
        try:
            if not self.slack_client:
                return "❌ Slack connection not available."
            
            # Get channel ID
            channel_id = self._resolve_channel_id(channel_name)
            if not channel_id:
                return f"❌ Channel '{channel_name}' not found."
            
            # Fetch recent messages
            response = self.slack_client.conversations_history(
                channel=channel_id,
                limit=10
            )
            
            messages = response.get("messages", [])
            if not messages:
                return f"No recent messages found in #{channel_name}."
            
            # Format messages
            formatted_messages = [f"💬 **Recent messages from #{channel_name}:**\n"]
            for msg in messages[:5]:
                user_name = self._get_user_display_name(msg.get("user", ""))
                text = msg.get("text", "")[:100]
                timestamp = self._format_message_timestamp(msg.get("ts"))
                
                if text and user_name != "MCP Bot":
                    formatted_messages.append(f"**{user_name}** ({timestamp}): {text}")
            
            return "\n\n".join(formatted_messages) if len(formatted_messages) > 1 else f"No displayable messages in #{channel_name}."
            
        except Exception as e:
            return f"❌ Error retrieving messages: {str(e)}"

    def _get_capabilities_info(self) -> str:
        """Return information about bot capabilities."""
        return """🛠️ **Slack MCP Bot Capabilities:**

📋 **Channel Management:**
• List accessible channels
• Send messages to channels
• Read channel message history

🔍 **Web Research:**
• General web search with AI processing
• Latest news search and analysis
• Comprehensive research reports

🤖 **AI Assistant:**
• Natural language conversations
• Intelligent query routing
• Real-time automated responses

🔧 **Integration:**
• MCP tool access via Claude Desktop
• Socket Mode real-time event handling
• Autonomous task execution"""

    def _use_autonomous_assistant(self, query: str, channel: str) -> str:
        """Use autonomous assistant for complex query processing."""
        try:
            context = {
                "slack_channel": channel,
                "can_send_to_slack": False
            }
            
            # Execute autonomous agent
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.autonomous_agent.execute(query, context)
                )
                return result
            finally:
                loop.close()
                
        except Exception as e:
            print(f"Autonomous assistant error: {e}")
            return "❌ Unable to process complex query."

    def _process_general_chat(self, query: str, channel: str) -> None:
        """Process general AI chat queries."""
        try:
            if not self.openai_client:
                self._send_message(channel, "❌ AI chat unavailable - OpenAI API key required.")
                return
            
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": """You are MCP Bot, a professional AI assistant integrated with Slack.

Your capabilities include:
• Slack workspace management
• Web research and news analysis
• Real-time automated responses
• AI-powered analysis and assistance

Provide helpful, concise, and professional responses. For web research requests, suggest using search keywords like 'search', 'research', or 'news'."""
                    },
                    {"role": "user", "content": query}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content or "I didn't understand that."
            self._send_message(channel, f"🤖 {ai_response}")
            
        except Exception as e:
            print(f"General chat error: {e}")
            self._send_message(channel, "❌ Unable to process request.")

    def _resolve_channel_id(self, channel_name: str) -> Optional[str]:
        """Resolve channel name to channel ID."""
        if not self.slack_client:
            return None
            
        try:
            response = self.slack_client.conversations_list()
            for channel in response.get("channels", []):
                if channel["name"] == channel_name:
                    return channel["id"]
        except Exception:
            pass
        
        return None

    def _get_user_display_name(self, user_id: str) -> str:
        """Get user's display name from user ID."""
        if not user_id or not self.slack_client:
            return "Unknown User"

        try:
            response = self.slack_client.users_info(user=user_id)
            user = response.get("user", {})
            return user.get("real_name") or user.get("name", "Unknown User")
        except Exception:
            return user_id

    def _format_message_timestamp(self, timestamp: Optional[str]) -> str:
        """Format message timestamp to readable format."""
        if not timestamp:
            return "Unknown time"
        
        try:
            dt = datetime.fromtimestamp(float(timestamp))
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return timestamp

    def _send_message(self, channel: str, message: str) -> bool:
        """Send message to Slack channel."""
        if not self.slack_client or not channel or not message:
            return False
            
        try:
            self.slack_client.chat_postMessage(
                channel=channel,
                text=message
            )
            return True
        except SlackApiError as e:
            print(f"Failed to send message: {e}")
            return False

    def _send_error_response(self, channel: Optional[str]) -> None:
        """Send generic error response to channel."""
        if channel:
            self._send_message(channel, "❌ An error occurred. Please try again.")

    def _register_mcp_tools(self) -> None:
        """Register all MCP tools for Claude Desktop integration."""
        self._register_slack_management_tools()
        self._register_ai_processing_tools()
        self._register_web_search_tools()

    def _register_slack_management_tools(self) -> None:
        """Register Slack workspace management tools."""

        @self.mcp.tool
        def send_slack_message(channel: str, message: str) -> str:
            """Send a message to a Slack channel."""
            if not self.slack_client:
                raise ResourceError("Slack client not available")

            try:
                response = self.slack_client.chat_postMessage(
                    channel=channel.lstrip("#"),
                    text=message
                )
                return f"Message sent successfully: {response['ts']}"
            except SlackApiError as e:
                raise ResourceError(f"Slack API error: {e.response['error']}") from e

        @self.mcp.tool
        def get_slack_channels() -> List[Dict[str, Any]]:
            """Retrieve list of accessible Slack channels."""
            if not self.slack_client:
                raise ResourceError("Slack client not available")

            try:
                response = self.slack_client.conversations_list(exclude_archived=True)
                return response.get("channels", [])
            except SlackApiError as e:
                raise ResourceError(f"Slack API error: {e.response['error']}") from e

        @self.mcp.tool
        def get_slack_messages(channel: str, limit: int = 50) -> List[Dict[str, Any]]:
            """Retrieve messages from a Slack channel."""
            if not self.slack_client:
                raise ResourceError("Slack client not available")

            try:
                channel_id = self._resolve_channel_id(channel.lstrip("#"))
                if not channel_id:
                    raise ResourceError(f"Channel '{channel}' not found")

                response = self.slack_client.conversations_history(
                    channel=channel_id,
                    limit=min(limit, 100)
                )

                messages = []
                for msg in response.get("messages", []):
                    user_name = self._get_user_display_name(msg.get("user", ""))
                    messages.append({
                        "user": user_name,
                        "text": msg.get("text", ""),
                        "timestamp": msg.get("ts", ""),
                        "datetime": self._format_message_timestamp(msg.get("ts")),
                    })

                return messages
            except SlackApiError as e:
                raise ResourceError(f"Slack API error: {e.response['error']}") from e

    def _register_ai_processing_tools(self) -> None:
        """Register AI processing and analysis tools."""

        @self.mcp.tool
        def ask_ai(question: str, context: Optional[str] = None) -> str:
            """Ask AI assistant a question with optional context."""
            if not self.openai_client:
                raise ResourceError("OpenAI client not available")

            try:
                from typing import cast
                from openai.types.chat import ChatCompletionMessageParam
                
                messages: List[ChatCompletionMessageParam] = [
                    cast(ChatCompletionMessageParam, {"role": "system", "content": "You are a helpful AI assistant providing accurate and informative responses."})
                ]

                if context:
                    messages.append(cast(ChatCompletionMessageParam, {"role": "system", "content": f"Context: {context}"}))

                messages.append(cast(ChatCompletionMessageParam, {"role": "user", "content": question}))

                response = self.openai_client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                )

                return response.choices[0].message.content or "No response generated"
            except Exception as e:
                raise ResourceError(f"AI processing error: {e}") from e

        @self.mcp.tool
        async def autonomous_assistant(
            request: str,
            channel: Optional[str] = None,
            send_to_slack: bool = False,
        ) -> str:
            """Execute autonomous AI task with dynamic tool discovery."""
            try:
                context = {}
                if channel:
                    context["slack_channel"] = channel
                    context["can_send_to_slack"] = send_to_slack

                # Execute autonomous agent
                result = await self.autonomous_agent.execute(request, context)

                # Send to Slack if requested
                if send_to_slack and channel and self.slack_client:
                    try:
                        self.slack_client.chat_postMessage(
                            channel=channel.lstrip("#"),
                            text=f"**Autonomous AI Result**\n\n{result}",
                        )
                        return f"{result}\n\n✅ Sent to #{channel}"
                    except SlackApiError:
                        return f"{result}\n\n❌ Failed to send to Slack"

                return result

            except Exception as e:
                raise ResourceError(f"Autonomous processing error: {e}") from e

    def _register_web_search_tools(self) -> None:
        """Register web search and research tools."""

        @self.mcp.tool
        async def tavily_web_search(query: str, ctx: Context) -> str:
            """
            Perform comprehensive web search using Tavily API with AI processing.
            
            Args:
                query: Search query to execute
                
            Returns:
                AI-enhanced search results with professional formatting
            """
            return await self._tavily_web_search(query)

        @self.mcp.tool
        async def tavily_news_search(query: str, ctx: Context) -> str:
            """
            Perform news-focused search using Tavily API with AI processing.
            
            Args:
                query: News search query
                
            Returns:
                AI-enhanced news results with professional formatting
            """
            return await self._tavily_news_search(query)

        @self.mcp.tool
        async def tavily_research_search(query: str, max_results: int = 10, ctx: Optional[Context] = None) -> str:
            """
            Perform comprehensive research using Tavily API with detailed AI analysis.
            
            Args:
                query: Research query
                max_results: Maximum number of results to analyze
                
            Returns:
                Comprehensive research report with AI analysis
            """
            try:
                tavily_key = os.getenv("TAVILY_API_KEY")
                if not tavily_key:
                    return "❌ Research search unavailable - Tavily API key not configured"

                # Execute comprehensive search
                search_data = await self._call_tavily_api(query, "research")
                if not search_data:
                    return "❌ Research search failed - no results returned"

                # Enhanced AI processing for research
                if self.openai_client:
                    return await self._process_research_with_ai(search_data, query, max_results)
                else:
                    return self._format_basic_research_results(search_data, query)
                    
            except Exception as e:
                return f"❌ Research search error: {str(e)}"

    async def _process_research_with_ai(self, data: Dict[str, Any], query: str, max_results: int) -> str:
        """Process research results with comprehensive AI analysis."""
        try:
            results_data = {
                "query": query,
                "answer": data.get("answer", ""),
                "results": data.get("results", [])[:max_results]
            }

            # Create comprehensive research prompt
            prompt = f"Based on comprehensive research results for '{query}', provide a detailed research report.\n\n"
            prompt += f"Executive Summary: {results_data['answer']}\n\nDetailed Sources:\n"
            
            for i, result in enumerate(results_data['results'], 1):
                prompt += f"{i}. {result.get('title', 'Untitled')}\n"
                prompt += f"   URL: {result.get('url', 'N/A')}\n"
                prompt += f"   Content: {result.get('content', 'No content')[:500]}...\n\n"
            
            prompt += "Please provide a comprehensive research report with executive summary, key findings, detailed analysis, and conclusions."

            # Process with AI
            if not self.openai_client:
                return self._format_basic_research_results(data, query)
                
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert research analyst providing comprehensive, well-structured research reports with proper citations and in-depth analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.2
            )

            processed_content = response.choices[0].message.content
            return f"🔬 **Research Report: {query}**\n\n{processed_content}"
            
        except Exception as e:
            print(f"Research AI processing failed: {e}")
            return self._format_basic_research_results(data, query)

    def _format_basic_research_results(self, data: Dict[str, Any], query: str) -> str:
        """Basic formatting fallback for research results."""
        result = f"🔬 **Research Results: {query}**\n\n"
        
        if data.get("answer"):
            result += f"**Executive Summary:** {data['answer']}\n\n"
        
        result += "**Research Sources:**\n"
        for i, item in enumerate(data.get("results", [])[:5], 1):
            result += f"{i}. **{item.get('title', 'N/A')}**\n"
            result += f"   {item.get('content', 'No content')[:300]}...\n"
            result += f"   Source: {item.get('url', 'N/A')}\n\n"
        
        return result

    def start_socket_mode(self) -> None:
        """Initialize and start Socket Mode for real-time event processing."""
        if not self.socket_client:
            return

        try:
            def run_socket_client():
                if self.socket_client:
                    self.socket_client.connect()

            socket_thread = threading.Thread(target=run_socket_client, daemon=True)
            socket_thread.start()
            time.sleep(2)  # Allow connection to establish
            
        except Exception as e:
            pass

    def run(self) -> None:
        """Start the MCP server with all integrated capabilities."""
        # Initialize Socket Mode
        if self.socket_client:
            self.start_socket_mode()

        # Start MCP server with stdio transport for Claude Desktop
        self.mcp.run()


def main() -> None:
    """Application entry point."""
    try:
        server = SlackMCPServer()
        server.run()
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown requested")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")


if __name__ == "__main__":
    main()
