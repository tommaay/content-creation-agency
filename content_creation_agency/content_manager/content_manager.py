from agency_swarm import Agent
from .tools.content_generator import ContentGenerator
from .tools.script_manager import ScriptManager

class ContentManager(Agent):
    def __init__(self):
        super().__init__(
            name="Content Manager",
            description="Responsible for generating content ideas and managing script creation.",
            instructions="./instructions.md",
            tools=[ContentGenerator, ScriptManager],
            temperature=0.7,
            max_prompt_tokens=25000,
        ) 