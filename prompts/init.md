Please create a content creation agency with three agents: Content Manager, Trend Analyzer Agent, and YouTube Analyzer Agent.

The Content Manager can generate content ideas using OpenAI's latest o1 preview model via the chat completions API @https://platform.openai.com/docs/guides/reasoning.
It also has a tool to write and edit scripts in Markdown which are saved locally.

The process is as follows:

1. Analyze the performance of the latest Youtube videos
2. Analyze latest trends with the Trend Analyzer Agent
3. Analyze content performance for these trends using the Youtube Analyzer Agent
4. Generate content ideas
5. Select and confirm ideas with the user
6. Write a script draft
7. Edit the script based on user suggestions

The Trend Analyzer Agent's role is to analyze the latest AI trends. It has 3 tools: search the web using the Tavily API @https://docs.tavily.com/docs/python-sdk/tavily-search/getting-started,
extract keywords from news articles using NLTK, and analyze keywords using pytrends. It then compiles a comprehensive report identifying content gaps and sends it back to the Content Manager.

The Youtube Analyzer Agent identifies content gaps on YouTube and analyzes channel performance. It can analyze demographics of the channel (Channel ID: UCEkGp-dPcLZ6TxvkxjdDvPA),
asseses the performance of my videos, analyze competitors, and evaluate sentiment in comments. The goal is to identify content gaps and high performing topics.
