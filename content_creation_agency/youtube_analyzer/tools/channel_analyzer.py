from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class ChannelAnalyzer(BaseTool):
    """
    A tool to analyze YouTube channel demographics and performance.
    """
    channel_id: str = Field(
        ..., description="The YouTube channel ID to analyze."
    )

    def run(self):
        """Analyze YouTube channel statistics and demographics."""
        try:
            youtube = build('youtube', 'v3', 
                          developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            # Get channel statistics
            channel_response = youtube.channels().list(
                part='statistics,snippet,contentDetails',
                id=self.channel_id
            ).execute()

            if not channel_response['items']:
                return "Channel not found"

            channel_stats = channel_response['items'][0]
            
            # Get channel's playlists
            playlists = youtube.playlists().list(
                part='snippet',
                channelId=self.channel_id,
                maxResults=50
            ).execute()

            # Get recent videos
            videos_response = youtube.search().list(
                part='id,snippet',
                channelId=self.channel_id,
                order='date',
                type='video',
                maxResults=50
            ).execute()

            result = {
                "channel_info": {
                    "title": channel_stats['snippet']['title'],
                    "description": channel_stats['snippet']['description'],
                    "published_at": channel_stats['snippet']['publishedAt'],
                    "subscriber_count": channel_stats['statistics']['subscriberCount'],
                    "video_count": channel_stats['statistics']['videoCount'],
                    "view_count": channel_stats['statistics']['viewCount']
                },
                "playlists": [
                    {
                        "title": playlist['snippet']['title'],
                        "description": playlist['snippet']['description']
                    }
                    for playlist in playlists.get('items', [])
                ],
                "recent_videos": [
                    {
                        "title": video['snippet']['title'],
                        "published_at": video['snippet']['publishedAt'],
                        "description": video['snippet']['description']
                    }
                    for video in videos_response.get('items', [])
                ]
            }
            
            return result
        except Exception as e:
            return f"Error analyzing channel: {str(e)}"

if __name__ == "__main__":
    tool = ChannelAnalyzer(channel_id="UCEkGp-dPcLZ6TxvkxjdDvPA")
    print(tool.run()) 