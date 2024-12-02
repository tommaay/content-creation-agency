from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()

class VideoAnalyzer(BaseTool):
    """
    A tool to analyze YouTube video performance and sentiment.
    """
    video_id: str = Field(
        ..., description="The YouTube video ID to analyze."
    )

    def run(self):
        """Analyze video performance and comment sentiment."""
        try:
            youtube = build('youtube', 'v3', 
                          developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            # Get video statistics
            video_response = youtube.videos().list(
                part='statistics,snippet',
                id=self.video_id
            ).execute()

            if not video_response['items']:
                return "Video not found"

            video_stats = video_response['items'][0]
            
            # Get video comments
            comments = []
            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=self.video_id,
                    textFormat='plainText',
                    maxResults=100
                ).execute()
                
                comments = [
                    comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    for comment in comments_response.get('items', [])
                ]
            except:
                # Comments might be disabled
                pass

            # Perform sentiment analysis on comments
            sentiment_scores = []
            for comment in comments:
                analysis = TextBlob(comment)
                sentiment_scores.append(analysis.sentiment.polarity)

            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

            result = {
                "video_info": {
                    "title": video_stats['snippet']['title'],
                    "description": video_stats['snippet']['description'],
                    "published_at": video_stats['snippet']['publishedAt'],
                    "view_count": video_stats['statistics']['viewCount'],
                    "like_count": video_stats['statistics'].get('likeCount', 'N/A'),
                    "comment_count": video_stats['statistics'].get('commentCount', '0')
                },
                "engagement": {
                    "comments_analyzed": len(comments),
                    "average_sentiment": avg_sentiment,
                    "sentiment_distribution": {
                        "positive": len([s for s in sentiment_scores if s > 0]),
                        "neutral": len([s for s in sentiment_scores if s == 0]),
                        "negative": len([s for s in sentiment_scores if s < 0])
                    }
                }
            }
            
            return result
        except Exception as e:
            return f"Error analyzing video: {str(e)}"

if __name__ == "__main__":
    tool = VideoAnalyzer(video_id="example_video_id")
    print(tool.run()) 