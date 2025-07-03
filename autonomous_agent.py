#!/usr/bin/env python3
"""
Clean Autonomous Agent
Modern AI agent that discovers and orchestrates MCP tools dynamically.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional

import httpx
from openai import OpenAI
from dotenv import load_dotenv
from fastmcp.exceptions import ResourceError

load_dotenv()


class AutonomousAgent:
    """Self-directed AI agent for dynamic MCP tool orchestration."""

    def __init__(self):
        self.openai_client = self._init_openai()
        self.available_servers = self._discover_servers()
        self.tool_registry = {}

    def _init_openai(self) -> Optional[OpenAI]:
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        try:
            return OpenAI(api_key=api_key)
        except Exception:
            return None

    def _discover_servers(self) -> Dict[str, Dict]:
        """Discover available MCP servers."""
        servers = {
            "slack_mcp": {
                "url": "http://localhost:8001/mcp",
                "description": "Slack workspace management"
            },
            "tavily_mcp": {
                "url": "http://localhost:8002/mcp",
                "description": "Web search and research"
            }
        }

        active_servers = {}
        for name, config in servers.items():
            if self._test_server(config["url"]):
                active_servers[name] = config

        return active_servers

    def _test_server(self, url: str) -> bool:
        """Test if MCP server is available."""
        try:
            import requests
            response = requests.get(url.replace("/mcp", ""), timeout=2)
            return response.status_code < 500
        except Exception:
            return False

    async def discover_tools(self) -> Dict[str, List[Dict]]:
        """Discover tools from all available MCP servers."""
        all_tools = {}

        for server_name, server_config in self.available_servers.items():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        server_config["url"],
                        json={
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "tools/list",
                            "params": {}
                        },
                        timeout=10
                    )

                    if response.status_code == 200:
                        data = response.json()
                        if "result" in data and "tools" in data["result"]:
                            tools = data["result"]["tools"]
                            all_tools[server_name] = [
                                {
                                    "name": tool.get("name", ""),
                                    "description": tool.get("description", ""),
                                    "server": server_name
                                }
                                for tool in tools
                            ]
            except Exception:
                continue

        self.tool_registry = all_tools
        return all_tools

    async def execute_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Dict:
        """Execute a specific tool on an MCP server."""
        if server_name not in self.available_servers:
            return {"success": False, "error": f"Server {server_name} not available"}

        server_config = self.available_servers[server_name]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    server_config["url"],
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": tool_name,
                            "arguments": arguments
                        }
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    if "result" in data and "content" in data["result"]:
                        return {
                            "success": True,
                            "result": data["result"]["content"][0].get("text", ""),
                            "server": server_name,
                            "tool": tool_name
                        }

                return {"success": False, "error": "Invalid response format"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute(self, user_request: str, context: Optional[Dict] = None) -> str:
        """Execute user request autonomously."""
        if not self.openai_client:
            raise ResourceError("OpenAI client not configured")

        try:
            # Discover available tools
            await self.discover_tools()
            tools_description = self._format_tools()

            # Create execution plan
            plan = await self._create_plan(user_request, tools_description, context)
            if not plan:
                return "❌ Could not create execution plan"

            # Execute plan
            results = []
            for step in plan.get("steps", []):
                if step.get("action") == "tool_execution":
                    result = await self.execute_tool(
                        step.get("server"),
                        step.get("tool"),
                        step.get("arguments", {})
                    )
                    results.append(result)

            # Synthesize results
            return await self._synthesize_results(user_request, plan, results)

        except Exception as e:
            return f"❌ Execution error: {str(e)}"

    async def _create_plan(self, request: str, tools: str, context: Optional[Dict]) -> Optional[Dict]:
        """Create execution plan using AI."""
        if not self.openai_client:
            raise ResourceError("OpenAI client not configured")
            
        planning_prompt = f"""
        You are an autonomous AI agent with access to MCP servers and tools.

        USER REQUEST: {request}
        CONTEXT: {json.dumps(context or {})}

        AVAILABLE TOOLS:
        {tools}

        Create a step-by-step execution plan. Respond with JSON:
        {{
            "reasoning": "Why you chose this approach",
            "steps": [
                {{
                    "step": 1,
                    "action": "tool_execution",
                    "server": "server_name",
                    "tool": "tool_name",
                    "arguments": {{"key": "value"}},
                    "purpose": "Why this step is needed"
                }}
            ]
        }}

        Be intelligent about tool selection and execution order.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an AI that creates optimal execution plans. Respond only with valid JSON."},
                    {"role": "user", "content": planning_prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )

            return json.loads(response.choices[0].message.content or "{}")
        except Exception:
            return None

    async def _synthesize_results(self, request: str, plan: Dict, results: List[Dict]) -> str:
        """Synthesize execution results into final answer."""
        if not self.openai_client:
            raise ResourceError("OpenAI client not configured")
            
        synthesis_prompt = f"""
        USER REQUEST: {request}

        EXECUTION PLAN: {json.dumps(plan)}

        EXECUTION RESULTS: {json.dumps(results)}

        Create a comprehensive response that:
        1. Addresses the user's request completely
        2. Synthesizes information from all executed tools
        3. Provides clear, actionable insights
        4. Is well-structured and concise
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert analyst who synthesizes information from multiple sources."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            return response.choices[0].message.content or "No synthesis available"
        except Exception as e:
            raise ResourceError(f"Synthesis failed: {str(e)}")

    def _format_tools(self) -> str:
        """Format available tools for AI understanding."""
        formatted = ""
        for server_name, tools in self.tool_registry.items():
            formatted += f"\\n**{server_name.upper()}**:\\n"
            for tool in tools:
                formatted += f"  - {tool['name']}: {tool['description']}\\n"
        return formatted


def main():
    """Test the autonomous agent."""
    async def test():
        agent = AutonomousAgent()
        result = await agent.execute(
            "Test autonomous execution with available tools"
        )
        print(result)

    asyncio.run(test())


if __name__ == "__main__":
    main()
