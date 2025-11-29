"""
MCP Server: storyboard-visualizer
Handles visual generation and composition for storyboard frames
"""

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any, Sequence
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mcp_servers.storyboard_visualizer.moment_detector import KeyMomentDetector
from mcp_servers.storyboard_visualizer.prompt_generator import VisualPromptGenerator


# Initialize MCP Server
app = Server("storyboard-visualizer")

# Initialize components
moment_detector = None
prompt_generator = None


def get_components():
    """Get or create components"""
    global moment_detector, prompt_generator

    if moment_detector is None:
        moment_detector = KeyMomentDetector()

    if prompt_generator is None:
        prompt_generator = VisualPromptGenerator()

    return moment_detector, prompt_generator


# Tool Definitions

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="identify_key_moments",
            description="Identifies key visual moments in a screenplay for storyboard frames",
            inputSchema={
                "type": "object",
                "properties": {
                    "screenplay": {
                        "type": "string",
                        "description": "The full screenplay text"
                    },
                    "num_frames": {
                        "type": "integer",
                        "description": "Number of storyboard frames to generate",
                        "default": 8,
                        "minimum": 4,
                        "maximum": 16
                    }
                },
                "required": ["screenplay"]
            }
        ),
        Tool(
            name="generate_visual_prompt",
            description="Generates a detailed image generation prompt for a storyboard frame",
            inputSchema={
                "type": "object",
                "properties": {
                    "scene": {
                        "type": "string",
                        "description": "Scene description or moment"
                    },
                    "characters": {
                        "type": "string",
                        "description": "JSON array of character visual descriptions",
                        "default": "[]"
                    },
                    "visual_style": {
                        "type": "string",
                        "description": "Visual style for the storyboard",
                        "enum": ["Realistic", "Noir", "Illustrated", "Anime", "Sketch"],
                        "default": "Realistic"
                    },
                    "camera_angle": {
                        "type": "string",
                        "description": "Camera angle for the frame",
                        "enum": ["Wide Shot", "Medium Shot", "Close-Up", "Extreme Close-Up", "POV (Point of View)", "Over the Shoulder", "Bird's Eye View", "Low Angle", "High Angle"],
                        "default": "Medium Shot"
                    },
                    "mood": {
                        "type": "string",
                        "description": "Emotional mood of the scene",
                        "default": "dramatic"
                    }
                },
                "required": ["scene"]
            }
        ),
        Tool(
            name="suggest_camera_angle",
            description="Suggests the best camera angle for a scene based on its content and emotional tone",
            inputSchema={
                "type": "object",
                "properties": {
                    "scene_type": {
                        "type": "string",
                        "description": "Type or description of the scene"
                    },
                    "tone": {
                        "type": "string",
                        "description": "Emotional tone of the scene",
                        "default": "dramatic"
                    },
                    "num_characters": {
                        "type": "integer",
                        "description": "Number of characters in the scene",
                        "default": 1
                    }
                },
                "required": ["scene_type"]
            }
        ),
        Tool(
            name="create_frame",
            description="Creates a complete storyboard frame with visual prompt and metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "visual_prompt": {
                        "type": "string",
                        "description": "The visual generation prompt"
                    },
                    "style": {
                        "type": "string",
                        "description": "Visual style",
                        "default": "Realistic"
                    },
                    "frame_number": {
                        "type": "integer",
                        "description": "Frame number in sequence"
                    },
                    "scene_reference": {
                        "type": "integer",
                        "description": "Reference to screenplay scene number"
                    },
                    "description": {
                        "type": "string",
                        "description": "Frame description"
                    }
                },
                "required": ["visual_prompt", "frame_number"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""

    detector, generator = get_components()

    if name == "identify_key_moments":
        return await identify_key_moments(
            screenplay=arguments["screenplay"],
            num_frames=arguments.get("num_frames", 8),
            detector=detector
        )

    elif name == "generate_visual_prompt":
        return await generate_visual_prompt(
            scene=arguments["scene"],
            characters=arguments.get("characters", "[]"),
            visual_style=arguments.get("visual_style", "Realistic"),
            camera_angle=arguments.get("camera_angle", "Medium Shot"),
            mood=arguments.get("mood", "dramatic"),
            generator=generator
        )

    elif name == "suggest_camera_angle":
        return await suggest_camera_angle(
            scene_type=arguments["scene_type"],
            tone=arguments.get("tone", "dramatic"),
            num_characters=arguments.get("num_characters", 1),
            detector=detector
        )

    elif name == "create_frame":
        return await create_frame(
            visual_prompt=arguments["visual_prompt"],
            style=arguments.get("style", "Realistic"),
            frame_number=arguments["frame_number"],
            scene_reference=arguments.get("scene_reference"),
            description=arguments.get("description")
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


# Tool Implementations

async def identify_key_moments(
    screenplay: str,
    num_frames: int,
    detector: KeyMomentDetector
) -> Sequence[TextContent]:
    """Identify key moments in screenplay"""

    moments = detector.identify_key_moments(screenplay, num_frames)

    return [TextContent(
        type="text",
        text=json.dumps(moments, indent=2)
    )]


async def generate_visual_prompt(
    scene: str,
    characters: str,
    visual_style: str,
    camera_angle: str,
    mood: str,
    generator: VisualPromptGenerator
) -> Sequence[TextContent]:
    """Generate visual prompt for frame"""

    # Parse characters JSON
    try:
        char_data = json.loads(characters)
    except:
        char_data = None

    # Create moment dict
    moment = {
        "description": scene,
        "emotional_tone": mood,
        "characters": []
    }

    # Generate prompt
    prompt = generator.generate_visual_prompt(
        moment=moment,
        visual_style=visual_style,
        camera_angle=camera_angle,
        characters=char_data
    )

    return [TextContent(
        type="text",
        text=prompt
    )]


async def suggest_camera_angle(
    scene_type: str,
    tone: str,
    num_characters: int,
    detector: KeyMomentDetector
) -> Sequence[TextContent]:
    """Suggest camera angle for scene"""

    # Create moment dict
    moment = {
        "description": scene_type,
        "emotional_tone": tone,
        "characters": ["CHAR"] * num_characters  # Dummy characters for count
    }

    # Get suggestion
    angle = detector.suggest_camera_angles(moment)

    result = {
        "suggested_angle": angle,
        "reasoning": f"Based on {tone} tone and {num_characters} character(s)"
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def create_frame(
    visual_prompt: str,
    style: str,
    frame_number: int,
    scene_reference: int = None,
    description: str = None
) -> Sequence[TextContent]:
    """Create storyboard frame metadata"""

    frame_data = {
        "frame_number": frame_number,
        "scene_reference": scene_reference,
        "visual_prompt": visual_prompt,
        "visual_style": style,
        "description": description or "Storyboard frame",
        "status": "ready_for_generation"
    }

    return [TextContent(
        type="text",
        text=json.dumps(frame_data, indent=2)
    )]


# Resources

@app.list_resources()
async def list_resources() -> list[Any]:
    """List available resources"""
    return [
        {
            "uri": "storyboard://frames",
            "name": "Generated Frames",
            "description": "Collection of generated storyboard frames",
            "mimeType": "application/json"
        },
        {
            "uri": "storyboard://styles",
            "name": "Available Styles",
            "description": "Visual styles available for storyboard generation",
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
