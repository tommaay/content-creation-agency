from agency_swarm.tools import BaseTool
from pydantic import Field
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

class TrendAnalyzer(BaseTool):
    """
    A tool to analyze keyword trends using Google Trends.
    """
    keywords: list = Field(
        ..., description="List of keywords to analyze."
    )
    timeframe: str = Field(
        "today 3-m", description="Timeframe for trend analysis (e.g., 'today 3-m', 'today 12-m')."
    )
    geo: str = Field(
        "", description="Geographic location to analyze (empty for worldwide)."
    )

    def run(self):
        """Analyze trends using Google Trends."""
        try:
            # Initialize pytrends
            pytrends = TrendReq(hl='en-US', tz=360)
            
            # Build payload
            pytrends.build_payload(
                self.keywords[:5],  # Google Trends allows max 5 keywords
                cat=0,
                timeframe=self.timeframe,
                geo=self.geo
            )
            
            # Get interest over time
            interest_over_time_df = pytrends.interest_over_time()
            
            # Get related queries
            related_queries = pytrends.related_queries()
            
            # Process and format results
            result = {
                "interest_over_time": interest_over_time_df.to_dict(),
                "related_queries": {
                    kw: {
                        "top": queries["top"].to_dict() if queries["top"] is not None else {},
                        "rising": queries["rising"].to_dict() if queries["rising"] is not None else {}
                    }
                    for kw, queries in related_queries.items()
                }
            }
            
            return result
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"

if __name__ == "__main__":
    tool = TrendAnalyzer(
        keywords=["artificial intelligence", "machine learning", "deep learning"],
        timeframe="today 3-m"
    )
    print(tool.run()) 