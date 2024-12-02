from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class CompetitorAnalyzer(BaseTool):
    """
    A tool to analyze competitor YouTube channels and their content.
    """
    competitor_channels: list = Field(
        ..., description="List of competitor channel IDs to analyze."
    )
    time_range: str = Field(
        "month", description="Time range for analysis: 'week', 'month', or 'year'."
    )

    def run(self):
        """Analyze competitor channels and their content performance."""
        try:
            youtube = build('youtube', 'v3', 
                          developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            competitor_analysis = {}
            
            for channel_id in self.competitor_channels:
                # Get channel statistics
                channel_response = youtube.channels().list(
                    part='statistics,snippet,contentDetails',
                    id=channel_id
                ).execute()

                if not channel_response['items']:
                    competitor_analysis[channel_id] = "Channel not found"
                    continue

                channel_stats = channel_response['items'][0]
                
                # Get recent videos
                videos_response = youtube.search().list(
                    part='id,snippet',
                    channelId=channel_id,
                    order='date',
                    type='video',
                    maxResults=50
                ).execute()

                videos = []
                for video in videos_response.get('items', []):
                    video_id = video['id']['videoId']
                    
                    # Get detailed video statistics
                    video_stats = youtube.videos().list(
                        part='statistics,snippet',
                        id=video_id
                    ).execute()
                    
                    if video_stats['items']:
                        stats = video_stats['items'][0]
                        videos.append({
                            "title": stats['snippet']['title'],
                            "published_at": stats['snippet']['publishedAt'],
                            "view_count": stats['statistics']['viewCount'],
                            "like_count": stats['statistics'].get('likeCount', 'N/A'),
                            "comment_count": stats['statistics'].get('commentCount', '0')
                        })

                competitor_analysis[channel_id] = {
                    "channel_info": {
                        "title": channel_stats['snippet']['title'],
                        "subscriber_count": channel_stats['statistics']['subscriberCount'],
                        "video_count": channel_stats['statistics']['videoCount'],
                        "view_count": channel_stats['statistics']['viewCount']
                    },
                    "recent_videos": videos,
                    "content_analysis": {
                        "avg_views": sum(int(v['view_count']) for v in videos) / len(videos) if videos else 0,
                        "total_videos_analyzed": len(videos),
                        "top_performing_videos": sorted(
                            videos, 
                            key=lambda x: int(x['view_count']), 
                            reverse=True
                        )[:5] if videos else []
                    }
                }
            
            return competitor_analysis
        except Exception as e:
            return f"Error analyzing competitors: {str(e)}"

if __name__ == "__main__":
    tool = CompetitorAnalyzer(
        competitor_channels=["example_channel_id1", "example_channel_id2"]
    )
    print(tool.run()) 