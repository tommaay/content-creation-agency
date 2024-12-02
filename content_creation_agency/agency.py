from agency_swarm import Agency
from content_manager.content_manager import ContentManager
from trend_analyzer.trend_analyzer import TrendAnalyzerAgent
from youtube_analyzer.youtube_analyzer import YouTubeAnalyzer

# Initialize agents
content_manager = ContentManager()
trend_analyzer = TrendAnalyzerAgent()
youtube_analyzer = YouTubeAnalyzer()

# Create agency with communication flows
agency = Agency(
    [
        content_manager,  # Content Manager is the entry point
        [content_manager, trend_analyzer],  # Content Manager can communicate with Trend Analyzer
        [content_manager, youtube_analyzer],  # Content Manager can communicate with YouTube Analyzer
        [trend_analyzer, youtube_analyzer],  # Trend Analyzer can communicate with YouTube Analyzer
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.5,
    max_prompt_tokens=25000
)

if __name__ == "__main__":
    agency.run_demo() 