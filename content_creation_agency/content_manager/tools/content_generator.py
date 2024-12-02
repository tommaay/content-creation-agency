from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ContentGenerator(BaseTool):
    """
    A tool to generate content ideas using OpenAI's latest model.
    """
    prompt: str = Field(
        ..., description="The prompt to generate content ideas based on trends and analysis."
    )

    def run(self):
        """Generate content ideas using OpenAI's latest model."""
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a creative content strategist specializing in AI content."},
                    {"role": "user", "content": self.prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"

if __name__ == "__main__":
    tool = ContentGenerator(prompt="Generate 5 video ideas about AI tools")
    print(tool.run()) 