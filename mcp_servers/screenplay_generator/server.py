"""
MCP Server: screenplay-generator
Handles story structure, character arcs, scene breakdown, and dialogue generation
"""

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any, Sequence
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from integrations.sambanova import SambaNovaClient
from core.prompts import (
    create_story_analysis_prompt,
    create_character_prompt,
    create_scene_prompt,
    SYSTEM_PROMPT_CREATIVE
)
from core.schemas import StoryAnalysis, CharacterProfile


# Initialize MCP Server
app = Server("screenplay-generator")

# Initialize LLM client
llm_client = None


def get_llm_client():
    """Get or create LLM client"""
    global llm_client
    if llm_client is None:
        llm_client = SambaNovaClient()
    return llm_client


# Tool Definitions

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="analyze_story",
            description="Analyzes a story prompt and extracts key elements for screenplay development",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The story idea or prompt to analyze"
                    },
                    "genre": {
                        "type": "string",
                        "description": "The genre of the story",
                        "enum": ["Drama", "Comedy", "Thriller", "Sci-Fi", "Horror", "Romance", "Action", "Mystery"]
                    },
                    "act_structure": {
                        "type": "string",
                        "description": "The desired story structure",
                        "enum": ["Three-Act", "Five-Act", "Hero's Journey"],
                        "default": "Three-Act"
                    }
                },
                "required": ["prompt", "genre"]
            }
        ),
        Tool(
            name="create_characters",
            description="Generates detailed character profiles based on story analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "story_analysis": {
                        "type": "string",
                        "description": "JSON string of story analysis from analyze_story tool"
                    },
                    "genre": {
                        "type": "string",
                        "description": "The genre of the story"
                    },
                    "num_characters": {
                        "type": "integer",
                        "description": "Number of main characters to create",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["story_analysis", "genre"]
            }
        ),
        Tool(
            name="write_scene",
            description="Writes a formatted screenplay scene with dialogue and action",
            inputSchema={
                "type": "object",
                "properties": {
                    "scene_number": {
                        "type": "integer",
                        "description": "The scene number"
                    },
                    "scene_outline": {
                        "type": "string",
                        "description": "Brief outline of what happens in the scene"
                    },
                    "characters": {
                        "type": "string",
                        "description": "JSON array of character profiles in the scene"
                    },
                    "location": {
                        "type": "string",
                        "description": "Scene location (e.g., 'INT. COFFEE SHOP - DAY')"
                    },
                    "dialogue_style": {
                        "type": "string",
                        "description": "Style of dialogue",
                        "enum": ["Realistic", "Stylized", "Period-Specific", "Witty", "Minimal"],
                        "default": "Realistic"
                    },
                    "genre": {
                        "type": "string",
                        "description": "Genre for context"
                    }
                },
                "required": ["scene_number", "scene_outline", "characters", "location", "genre"]
            }
        ),
        Tool(
            name="generate_dialogue",
            description="Generates character-specific dialogue for a scene context",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "The scene context and what's happening"
                    },
                    "characters": {
                        "type": "string",
                        "description": "JSON array of characters in the conversation"
                    },
                    "style": {
                        "type": "string",
                        "description": "Dialogue style",
                        "enum": ["Realistic", "Stylized", "Period-Specific", "Witty", "Minimal"],
                        "default": "Realistic"
                    },
                    "tone": {
                        "type": "string",
                        "description": "Emotional tone of the dialogue",
                        "default": "neutral"
                    },
                    "num_exchanges": {
                        "type": "integer",
                        "description": "Number of dialogue exchanges",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["context", "characters"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""

    if name == "analyze_story":
        return await analyze_story(
            prompt=arguments["prompt"],
            genre=arguments["genre"],
            act_structure=arguments.get("act_structure", "Three-Act")
        )

    elif name == "create_characters":
        return await create_characters(
            story_analysis=arguments["story_analysis"],
            genre=arguments["genre"],
            num_characters=arguments.get("num_characters", 3)
        )

    elif name == "write_scene":
        return await write_scene(
            scene_number=arguments["scene_number"],
            scene_outline=arguments["scene_outline"],
            characters=arguments["characters"],
            location=arguments["location"],
            dialogue_style=arguments.get("dialogue_style", "Realistic"),
            genre=arguments["genre"]
        )

    elif name == "generate_dialogue":
        return await generate_dialogue(
            context=arguments["context"],
            characters=arguments["characters"],
            style=arguments.get("style", "Realistic"),
            tone=arguments.get("tone", "neutral"),
            num_exchanges=arguments.get("num_exchanges", 5)
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


# Tool Implementations

async def analyze_story(prompt: str, genre: str, act_structure: str) -> Sequence[TextContent]:
    """Analyze story prompt and extract key elements"""

    client = get_llm_client()

    # Create analysis prompt
    analysis_prompt = create_story_analysis_prompt(
        prompt=prompt,
        genre=genre,
        act_structure=act_structure
    )

    # Generate analysis
    response = await client.generate_structured(
        prompt=analysis_prompt,
        system_prompt=SYSTEM_PROMPT_CREATIVE,
        temperature=0.7
    )

    # Return as JSON
    return [TextContent(
        type="text",
        text=json.dumps(response, indent=2)
    )]


async def create_characters(
    story_analysis: str,
    genre: str,
    num_characters: int
) -> Sequence[TextContent]:
    """Create character profiles"""

    client = get_llm_client()

    # Create character prompt
    char_prompt = create_character_prompt(
        story_analysis=story_analysis,
        genre=genre
    )

    char_prompt += f"\n\nCreate {num_characters} main characters."

    # Generate characters
    response = await client.generate(
        prompt=char_prompt,
        system_prompt=SYSTEM_PROMPT_CREATIVE,
        temperature=0.8
    )

    return [TextContent(
        type="text",
        text=response
    )]


async def write_scene(
    scene_number: int,
    scene_outline: str,
    characters: str,
    location: str,
    dialogue_style: str,
    genre: str
) -> Sequence[TextContent]:
    """Write a complete screenplay scene"""

    client = get_llm_client()

    # Parse act from scene number (simple estimation)
    if scene_number <= 3:
        act = "Act 1"
    elif scene_number <= 7:
        act = "Act 2"
    else:
        act = "Act 3"

    # Create scene prompt
    scene_prompt = create_scene_prompt(
        scene_number=scene_number,
        act=act,
        location=location,
        time="DAY",  # Could be extracted from location
        purpose=scene_outline,
        characters=characters,
        context=scene_outline,
        dialogue_style=dialogue_style,
        genre=genre
    )

    # Generate scene
    response = await client.generate(
        prompt=scene_prompt,
        system_prompt=SYSTEM_PROMPT_CREATIVE,
        temperature=0.75,
        max_tokens=2000
    )

    return [TextContent(
        type="text",
        text=response
    )]


async def generate_dialogue(
    context: str,
    characters: str,
    style: str,
    tone: str,
    num_exchanges: int
) -> Sequence[TextContent]:
    """Generate dialogue for characters"""

    client = get_llm_client()

    from core.prompts import DIALOGUE_GENERATION_PROMPT, format_prompt

    # Create dialogue prompt
    dialogue_prompt = format_prompt(
        DIALOGUE_GENERATION_PROMPT,
        characters=characters,
        context=context,
        dialogue_style=style,
        genre="Drama",  # Could be passed as parameter
        tone=tone
    )

    dialogue_prompt += f"\n\nGenerate approximately {num_exchanges} exchanges of dialogue."

    # Generate dialogue
    response = await client.generate(
        prompt=dialogue_prompt,
        system_prompt=SYSTEM_PROMPT_CREATIVE,
        temperature=0.85,
        max_tokens=1500
    )

    return [TextContent(
        type="text",
        text=response
    )]


# Resources

@app.list_resources()
async def list_resources() -> list[Any]:
    """List available resources"""
    return [
        {
            "uri": "screenplay://current",
            "name": "Current Screenplay",
            "description": "The current screenplay being generated",
            "mimeType": "text/plain"
        },
        {
            "uri": "screenplay://characters",
            "name": "Character Database",
            "description": "All characters in the current screenplay",
            "mimeType": "application/json"
        },
        {
            "uri": "screenplay://structure",
            "name": "Story Structure",
            "description": "The story structure template being used",
            "mimeType": "application/json"
        }
    ]


# Main entry point
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(main())
