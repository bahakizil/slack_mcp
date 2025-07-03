#!/usr/bin/env python3
"""
Tavily MCP Server
A modern web search server with FastMCP 2.8+ architecture.
"""

import os
import json
from typing import Dict, Any, List, Optional

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError
import requests
from dotenv import load_dotenv

load_dotenv()


class TavilyMCPServer:
    """A Tavily MCP Server implementation."""

    def __init__(self):
        self.mcp = FastMCP(
            name="Tavily Search Server",
            mask_error_details=True,  # Hide internal details for security
            on_duplicate_resources="warn"  # Warn on duplicate resources
        )
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.session = requests.Session()
        self._register_tools()

    def _register_tools(self) -> None:
        """Register Tavily search tools."""

        @self.mcp.tool
        def search_web(
            query: str,
            max_results: int = 5,
            search_depth: str = "basic",
            include_answer: bool = True,
        ) -> Dict[str, Any]:
            """
            Search the web using Tavily API.
            """
            if not self.api_key:
                raise ResourceError("Tavily API key not configured")

            try:
                response = self.session.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": min(max_results, 20),
                        "search_depth": search_depth,
                        "include_answer": include_answer,
                        "format": "json",
                    },
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                raise ResourceError(f"Request failed: {e}") from e

        @self.mcp.tool
        def search_news(
            query: str, max_results: int = 5, days: int = 7
        ) -> Dict[str, Any]:
            """
            Search recent news using Tavily API.
            """
            if not self.api_key:
                raise ResourceError("Tavily API key not configured")

            try:
                response = self.session.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": min(max_results, 20),
                        "search_depth": "advanced",
                        "include_answer": True,
                        "include_domains": [
                            "reuters.com",
                            "bbc.com",
                            "cnn.com",
                            "bloomberg.com",
                            "techcrunch.com",
                            "theverge.com",
                        ],
                        "days": min(days, 30),
                    },
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                raise ResourceError(f"News search failed: {e}") from e

        @self.mcp.tool
        def research_topic(
            topic: str, focus_areas: Optional[List[str]] = None
        ) -> Dict[str, Any]:
            """
            Conduct comprehensive research on a topic.
            """
            if not self.api_key:
                raise ResourceError("Tavily API key not configured")

            research_results: Dict[str, Any] = {
                "topic": topic,
                "sections": {},
            }

            # Main topic search using internal API call
            try:
                main_response = self.session.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": topic,
                        "max_results": 5,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "format": "json",
                    },
                    timeout=30,
                )
                main_response.raise_for_status()
                main_search = main_response.json()
                
                research_results["sections"]["overview"] = {
                    "summary": main_search.get("answer", ""),
                    "key_sources": [
                        r["title"] for r in main_search.get("results", [])[:3]
                    ],
                }

                # Focus area searches
                if focus_areas:
                    for area in focus_areas[:3]:  # Limit to 3 areas
                        focus_response = self.session.post(
                            "https://api.tavily.com/search",
                            json={
                                "api_key": self.api_key,
                                "query": f"{topic} {area}",
                                "max_results": 3,
                                "search_depth": "basic",
                                "include_answer": True,
                                "format": "json",
                            },
                            timeout=30,
                        )
                        focus_response.raise_for_status()
                        focus_search = focus_response.json()
                        
                        research_results["sections"][area] = {
                            "findings": focus_search.get("answer", ""),
                            "sources": [
                                r["title"] for r in focus_search.get("results", [])[:2]
                            ],
                        }

            except requests.RequestException as e:
                raise ResourceError(f"Research failed: {e}") from e

            return research_results

    def run(self) -> None:
        """Run the Tavily MCP server."""
        self.mcp.run(
            transport="streamable-http",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("TAVILY_PORT", "8002")),
        )


def main() -> None:
    """Entry point."""
    server = TavilyMCPServer()
    server.run()


if __name__ == "__main__":
    main()