from agency_swarm.tools import BaseTool
from pydantic import Field
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

# Suppress the pandas warning
pd.options.mode.copy_on_write = True
pd.set_option("future.no_silent_downcasting", True)


class TrendAnalyzer(BaseTool):
    """
    A tool to analyze keyword trends using Google Trends.
    """

    keywords: list = Field(..., description="List of keywords to analyze.")
    timeframe: str = Field(
        "today 3-m",
        description="Timeframe for trend analysis (e.g., 'today 3-m', 'today 12-m').",
    )
    geo: str = Field(
        "", description="Geographic location to analyze (empty for worldwide)."
    )

    def run(self):
        """Analyze trends using Google Trends."""
        try:
            if not self.keywords:
                return "Error: No keywords provided"

            if len(self.keywords) > 5:
                self.keywords = self.keywords[:5]  # Google Trends allows max 5 keywords

            # Initialize pytrends
            pytrends = TrendReq(hl="en-US", tz=360)

            result = {
                "keywords_analyzed": self.keywords,
                "timeframe": self.timeframe,
                "interest_over_time": {},
                "trend_summary": {},
                "errors": [],
            }

            # Build payload
            try:
                pytrends.build_payload(
                    self.keywords, cat=0, timeframe=self.timeframe, geo=self.geo
                )
            except Exception as e:
                result["errors"].append(f"Error building payload: {str(e)}")
                return result

            # Get interest over time
            try:
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    # Store the raw time series data
                    result["interest_over_time"] = {
                        str(date): {col: val for col, val in row.items()}
                        for date, row in interest_over_time_df.iterrows()
                    }

                    # Calculate trend summary statistics
                    for keyword in self.keywords:
                        if keyword in interest_over_time_df.columns:
                            keyword_data = interest_over_time_df[keyword]
                            result["trend_summary"][keyword] = {
                                "mean": round(keyword_data.mean(), 2),
                                "max": int(keyword_data.max()),
                                "min": int(keyword_data.min()),
                                "current": int(keyword_data.iloc[-1]),
                                "trend": (
                                    "up"
                                    if keyword_data.iloc[-1] > keyword_data.iloc[0]
                                    else "down"
                                ),
                                "growth_rate": (
                                    round(
                                        (
                                            (
                                                keyword_data.iloc[-1]
                                                - keyword_data.iloc[0]
                                            )
                                            / keyword_data.iloc[0]
                                            * 100
                                        ),
                                        2,
                                    )
                                    if keyword_data.iloc[0] != 0
                                    else 0
                                ),
                            }
            except Exception as e:
                result["errors"].append(f"Error getting interest over time: {str(e)}")

            # Try to get related topics instead of queries (more stable)
            try:
                related_topics = pytrends.related_topics()
                if related_topics:
                    result["related_topics"] = {}
                    for keyword, topics in related_topics.items():
                        result["related_topics"][keyword] = {
                            "rising": (
                                topics.get("rising", pd.DataFrame()).to_dict()
                                if topics.get("rising") is not None
                                else {}
                            ),
                            "top": (
                                topics.get("top", pd.DataFrame()).to_dict()
                                if topics.get("top") is not None
                                else {}
                            ),
                        }
            except Exception as e:
                result["errors"].append(f"Error getting related topics: {str(e)}")

            if not result["interest_over_time"] and not any(
                result["related_topics"].values()
            ):
                result["errors"].append("No data found for any keywords")

            return result

        except Exception as e:
            return {
                "keywords_analyzed": self.keywords,
                "timeframe": self.timeframe,
                "interest_over_time": {},
                "trend_summary": {},
                "errors": [f"Error analyzing trends: {str(e)}"],
            }


if __name__ == "__main__":
    # Test with a single keyword first
    tool = TrendAnalyzer(
        keywords=["artificial intelligence"],
        timeframe="today 1-m",  # Shorter timeframe for testing
    )
    result = tool.run()
    print("\nErrors:", result.get("errors", []))
    print("\nKeywords analyzed:", result["keywords_analyzed"])
    print("\nTimeframe:", result["timeframe"])
    print("\nNumber of data points:", len(result["interest_over_time"]))
