"""
MCP Server: document-exporter
Creates formatted export documents (PDF, ZIP, lookbooks)
"""

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any, Sequence
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mcp_servers.document_exporter.pdf_generator import ScreenplayPDFGenerator


# Initialize MCP Server
app = Server("document-exporter")

# Initialize components
pdf_generator = None


def get_pdf_generator():
    """Get or create PDF generator"""
    global pdf_generator
    if pdf_generator is None:
        pdf_generator = ScreenplayPDFGenerator()
    return pdf_generator


# Tool Definitions

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="export_screenplay_pdf",
            description="Exports a screenplay as a formatted PDF document",
            inputSchema={
                "type": "object",
                "properties": {
                    "screenplay": {
                        "type": "string",
                        "description": "The formatted screenplay text"
                    },
                    "format": {
                        "type": "string",
                        "description": "PDF format style",
                        "enum": ["standard", "production", "shooting"],
                        "default": "standard"
                    },
                    "metadata": {
                        "type": "string",
                        "description": "JSON string with title, author, draft info",
                        "default": "{}"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional output path",
                        "default": ""
                    }
                },
                "required": ["screenplay"]
            }
        ),
        Tool(
            name="export_storyboard_pack",
            description="Exports storyboard frames as a ZIP package",
            inputSchema={
                "type": "object",
                "properties": {
                    "frames": {
                        "type": "string",
                        "description": "JSON array of frame data with paths"
                    },
                    "format": {
                        "type": "string",
                        "description": "Package format",
                        "enum": ["zip", "pdf"],
                        "default": "zip"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional output path",
                        "default": ""
                    }
                },
                "required": ["frames"]
            }
        ),
        Tool(
            name="export_lookbook",
            description="Creates a combined lookbook with screenplay and storyboards",
            inputSchema={
                "type": "object",
                "properties": {
                    "screenplay": {
                        "type": "string",
                        "description": "Screenplay text"
                    },
                    "frames": {
                        "type": "string",
                        "description": "JSON array of storyboard frames"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional output path",
                        "default": ""
                    }
                },
                "required": ["screenplay", "frames"]
            }
        ),
        Tool(
            name="generate_shot_list",
            description="Generates a production shot list from screenplay and storyboard",
            inputSchema={
                "type": "object",
                "properties": {
                    "screenplay": {
                        "type": "string",
                        "description": "Screenplay text"
                    },
                    "frames": {
                        "type": "string",
                        "description": "JSON array of storyboard frames"
                    }
                },
                "required": ["screenplay", "frames"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""

    if name == "export_screenplay_pdf":
        return await export_screenplay_pdf(
            screenplay=arguments["screenplay"],
            format=arguments.get("format", "standard"),
            metadata=arguments.get("metadata", "{}"),
            output_path=arguments.get("output_path", "")
        )

    elif name == "export_storyboard_pack":
        return await export_storyboard_pack(
            frames=arguments["frames"],
            format=arguments.get("format", "zip"),
            output_path=arguments.get("output_path", "")
        )

    elif name == "export_lookbook":
        return await export_lookbook(
            screenplay=arguments["screenplay"],
            frames=arguments["frames"],
            output_path=arguments.get("output_path", "")
        )

    elif name == "generate_shot_list":
        return await generate_shot_list(
            screenplay=arguments["screenplay"],
            frames=arguments["frames"]
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


# Tool Implementations

async def export_screenplay_pdf(
    screenplay: str,
    format: str,
    metadata: str,
    output_path: str
) -> Sequence[TextContent]:
    """Export screenplay as PDF"""

    generator = get_pdf_generator()

    # Parse metadata
    try:
        metadata_dict = json.loads(metadata)
    except:
        metadata_dict = {}

    # Generate output path if not provided
    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"screenplay_{timestamp}.pdf")

    # Generate PDF
    result_path = generator.generate_screenplay_pdf(
        screenplay_text=screenplay,
        output_path=output_path,
        metadata=metadata_dict
    )

    result = {
        "success": True,
        "output_path": result_path,
        "format": format,
        "file_size": os.path.getsize(result_path) if os.path.exists(result_path) else 0
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def export_storyboard_pack(
    frames: str,
    format: str,
    output_path: str
) -> Sequence[TextContent]:
    """Export storyboard as ZIP"""

    import zipfile
    import shutil

    # Parse frames
    try:
        frames_data = json.loads(frames)
    except:
        frames_data = []

    # Generate output path
    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"storyboard_{timestamp}.zip")

    # Create ZIP
    try:
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for frame in frames_data:
                image_path = frame.get("image_path")
                if image_path and os.path.exists(image_path):
                    arcname = f"frame_{frame.get('frame_number', 0):03d}.png"
                    zipf.write(image_path, arcname)

        result = {
            "success": True,
            "output_path": output_path,
            "num_frames": len(frames_data),
            "file_size": os.path.getsize(output_path)
        }

    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def export_lookbook(
    screenplay: str,
    frames: str,
    output_path: str
) -> Sequence[TextContent]:
    """Export combined lookbook"""

    # For now, just combine screenplay and frame info
    # Full implementation would create fancy PDF with images

    if not output_path:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"lookbook_{timestamp}.pdf")

    # Parse frames
    try:
        frames_data = json.loads(frames)
    except:
        frames_data = []

    # Create combined document
    combined_text = "LOOKBOOK\n\n"
    combined_text += "="*60 + "\n"
    combined_text += "SCREENPLAY\n"
    combined_text += "="*60 + "\n\n"
    combined_text += screenplay
    combined_text += "\n\n"
    combined_text += "="*60 + "\n"
    combined_text += "STORYBOARD FRAMES\n"
    combined_text += "="*60 + "\n\n"

    for frame in frames_data:
        combined_text += f"\nFrame {frame.get('frame_number', 0)}: {frame.get('description', '')}\n"
        combined_text += f"Scene Reference: {frame.get('scene_reference', 'N/A')}\n"
        combined_text += f"Camera Angle: {frame.get('camera_angle', 'N/A')}\n"
        combined_text += "-"*60 + "\n"

    # Write to file (text fallback)
    txt_path = output_path.replace('.pdf', '.txt')
    with open(txt_path, 'w') as f:
        f.write(combined_text)

    result = {
        "success": True,
        "output_path": txt_path,
        "note": "PDF generation requires additional setup, created text version"
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def generate_shot_list(
    screenplay: str,
    frames: str
) -> Sequence[TextContent]:
    """Generate production shot list"""

    # Parse frames
    try:
        frames_data = json.loads(frames)
    except:
        frames_data = []

    shot_list = []

    for frame in frames_data:
        shot = {
            "shot_number": frame.get("frame_number", 0),
            "scene": frame.get("scene_reference", "N/A"),
            "description": frame.get("description", ""),
            "camera_angle": frame.get("camera_angle", "Medium Shot"),
            "notes": f"Storyboard frame {frame.get('frame_number', 0)}"
        }
        shot_list.append(shot)

    result = {
        "shot_list": shot_list,
        "total_shots": len(shot_list)
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


# Resources

@app.list_resources()
async def list_resources() -> list[Any]:
    """List available resources"""
    return [
        {
            "uri": "exports://recent",
            "name": "Recent Exports",
            "description": "Recently exported documents",
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
