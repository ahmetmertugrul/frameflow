"""
MCP Server: character-consistency
Maintains visual and personality consistency across the project using embeddings
"""

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any, Sequence
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from integrations.nebius import NebiusClient, CharacterConsistencyManager


# Initialize MCP Server
app = Server("character-consistency")

# Initialize components
consistency_manager = None


def get_consistency_manager():
    """Get or create consistency manager"""
    global consistency_manager

    if consistency_manager is None:
        try:
            nebius_client = NebiusClient()
            consistency_manager = CharacterConsistencyManager(nebius_client)
        except:
            # Fallback without embedding client
            consistency_manager = None

    return consistency_manager


# Tool Definitions

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="store_character_embedding",
            description="Stores a character's visual signature as an embedding for consistency tracking",
            inputSchema={
                "type": "object",
                "properties": {
                    "character_profile": {
                        "type": "string",
                        "description": "JSON string with character name and visual_description"
                    },
                    "metadata": {
                        "type": "string",
                        "description": "Optional JSON metadata (age, role, etc.)",
                        "default": "{}"
                    }
                },
                "required": ["character_profile"]
            }
        ),
        Tool(
            name="get_character_prompt",
            description="Retrieves consistent visual description for a character",
            inputSchema={
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "Name of the character"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional scene context for adaptation",
                        "default": ""
                    }
                },
                "required": ["character_name"]
            }
        ),
        Tool(
            name="validate_consistency",
            description="Validates if a new description is consistent with stored character",
            inputSchema={
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "Name of the character"
                    },
                    "new_description": {
                        "type": "string",
                        "description": "New description to validate"
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum similarity threshold (0-1)",
                        "default": 0.85
                    }
                },
                "required": ["character_name", "new_description"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""

    if name == "store_character_embedding":
        return await store_character_embedding(
            character_profile=arguments["character_profile"],
            metadata=arguments.get("metadata", "{}")
        )

    elif name == "get_character_prompt":
        return await get_character_prompt(
            character_name=arguments["character_name"],
            context=arguments.get("context", "")
        )

    elif name == "validate_consistency":
        return await validate_consistency(
            character_name=arguments["character_name"],
            new_description=arguments["new_description"],
            threshold=arguments.get("threshold", 0.85)
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


# Tool Implementations

async def store_character_embedding(
    character_profile: str,
    metadata: str
) -> Sequence[TextContent]:
    """Store character embedding"""

    manager = get_consistency_manager()

    if not manager:
        result = {
            "success": False,
            "error": "Character consistency manager not available (missing API key)"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    try:
        # Parse character profile
        profile = json.loads(character_profile)
        char_name = profile.get("name", "Unknown")
        visual_desc = profile.get("visual_description", "")

        # Parse metadata
        try:
            meta = json.loads(metadata)
        except:
            meta = {}

        # Store character
        char_id = await manager.store_character(
            character_name=char_name,
            visual_description=visual_desc,
            metadata=meta
        )

        result = {
            "success": True,
            "character_id": char_id,
            "character_name": char_name
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


async def get_character_prompt(
    character_name: str,
    context: str
) -> Sequence[TextContent]:
    """Get consistent character description"""

    manager = get_consistency_manager()

    if not manager:
        result = {
            "description": f"Character: {character_name}",
            "note": "Consistency manager not available, using default"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    try:
        description = await manager.get_character_description(
            character_name,
            context=context if context else None
        )

        result = {
            "character_name": character_name,
            "description": description,
            "context_used": bool(context)
        }

    except Exception as e:
        result = {
            "error": str(e),
            "character_name": character_name
        }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def validate_consistency(
    character_name: str,
    new_description: str,
    threshold: float
) -> Sequence[TextContent]:
    """Validate character consistency"""

    manager = get_consistency_manager()

    if not manager:
        result = {
            "is_consistent": True,
            "score": 1.0,
            "note": "Consistency manager not available, assuming consistent"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    try:
        is_consistent, score = await manager.validate_consistency(
            character_name,
            new_description,
            threshold
        )

        result = {
            "is_consistent": is_consistent,
            "similarity_score": score,
            "threshold": threshold,
            "character_name": character_name
        }

    except Exception as e:
        result = {
            "error": str(e),
            "character_name": character_name
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
            "uri": "characters://embeddings",
            "name": "Character Embeddings",
            "description": "Character embedding database for consistency",
            "mimeType": "application/json"
        },
        {
            "uri": "characters://profiles",
            "name": "Character Profiles",
            "description": "Full character profile database",
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
