from agency_swarm import Agent
from .tools.web_searcher import WebSearcher
from .tools.keyword_extractor import KeywordExtractor
from .tools.trend_analyzer import TrendAnalyzer

class TrendAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Trend Analyzer",
            description="Analyzes latest AI trends and identifies content opportunities.",
            instructions="./instructions.md",
            tools=[WebSearcher, KeywordExtractor, TrendAnalyzer],
            temperature=0.5,
            max_prompt_tokens=25000,
        ) 