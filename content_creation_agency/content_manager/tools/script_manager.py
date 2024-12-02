from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from datetime import datetime

class ScriptManager(BaseTool):
    """
    A tool to write and edit scripts in Markdown format.
    """
    content: str = Field(
        ..., description="The content of the script in Markdown format."
    )
    filename: str = Field(
        None, description="The filename for the script. If not provided, a timestamp will be used."
    )
    mode: str = Field(
        "write", description="The mode of operation: 'write' for new scripts or 'edit' for existing ones."
    )

    def run(self):
        """Write or edit a script file in Markdown format."""
        try:
            # Create scripts directory if it doesn't exist
            scripts_dir = "scripts"
            os.makedirs(scripts_dir, exist_ok=True)

            # Generate filename if not provided
            if not self.filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.filename = f"script_{timestamp}.md"

            filepath = os.path.join(scripts_dir, self.filename)

            if self.mode == "write":
                with open(filepath, "w") as f:
                    f.write(self.content)
                return f"Script successfully written to {filepath}"
            elif self.mode == "edit":
                if not os.path.exists(filepath):
                    return f"Error: File {filepath} does not exist"
                with open(filepath, "w") as f:
                    f.write(self.content)
                return f"Script successfully edited at {filepath}"
            else:
                return "Error: Invalid mode. Use 'write' or 'edit'"
        except Exception as e:
            return f"Error managing script: {str(e)}"

if __name__ == "__main__":
    tool = ScriptManager(
        content="# Test Script\n\nThis is a test script.",
        filename="test_script.md"
    )
    print(tool.run()) 