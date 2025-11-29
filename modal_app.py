"""
Modal Deployment Configuration for FrameFlow
Deploys Gradio app with GPU support for image generation
"""

import modal
from pathlib import Path

# Create Modal app
app = modal.App("frameflow")

# Mount the entire project directory
project_root = Path(__file__).parent
mounts = [
    modal.Mount.from_local_dir(
        project_root / "core",
        remote_path="/root/core"
    ),
    modal.Mount.from_local_dir(
        project_root / "integrations",
        remote_path="/root/integrations"
    ),
    modal.Mount.from_local_dir(
        project_root / "mcp_servers",
        remote_path="/root/mcp_servers"
    ),
    modal.Mount.from_local_file(
        project_root / "app.py",
        remote_path="/root/app.py"
    ),
]

# Define image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "gradio>=6.0.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.25.0",
        "Pillow>=10.1.0",
        "numpy>=1.24.0",
        "reportlab>=4.0.0",
        "mcp>=0.9.0",
        "chromadb>=0.4.0",
    )
)

# Define secrets - all API keys in one secret
secrets = [modal.Secret.from_name("frameflow-secrets")]


# GPU function for image generation
@app.function(
    image=image,
    gpu="T4",  # Use T4 GPU for image generation
    timeout=600,  # 10 minute timeout
    secrets=secrets,
    mounts=mounts
)
async def generate_storyboard_frame(prompt: str, style: str):
    """Generate a single storyboard frame using GPU"""
    from integrations.hyperbolic import HyperbolicClient

    client = HyperbolicClient()

    image_bytes = await client.generate_storyboard_frame(
        prompt=prompt,
        style=style,
        aspect_ratio="16:9",
        quality="high"
    )

    return image_bytes


# Main Gradio app
@app.function(
    image=image,
    secrets=secrets,
    min_containers=1,  # Keep one instance warm (updated from keep_warm)
    timeout=1800,  # 30 minute timeout for long screenplay generation
    mounts=mounts
)
@modal.asgi_app()
def gradio_app():
    """Gradio web interface"""
    import sys
    sys.path.insert(0, "/root")  # Add project root to Python path

    from app import demo  # Import the Gradio demo from app.py
    return demo


# CLI for local development
@app.local_entrypoint()
def main():
    """Run the app locally"""
    print("🚀 Deploying FrameFlow to Modal...")
    print("Visit the URL below to access your app:")
    print()
    gradio_app.remote()
