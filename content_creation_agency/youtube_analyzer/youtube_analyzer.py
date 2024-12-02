from agency_swarm import Agent
from .tools.channel_analyzer import ChannelAnalyzer
from .tools.video_analyzer import VideoAnalyzer
from .tools.competitor_analyzer import CompetitorAnalyzer

class YouTubeAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="YouTube Analyzer",
            description="Analyzes YouTube channel performance, video metrics, and competitor content.",
            instructions="./instructions.md",
            tools=[ChannelAnalyzer, VideoAnalyzer, CompetitorAnalyzer],
            temperature=0.5,
            max_prompt_tokens=25000,
        ) 