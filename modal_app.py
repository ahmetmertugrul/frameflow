"""
Modal Deployment Configuration for FrameFlow
Deploys Gradio app with GPU support for image generation
"""

import modal

# Create Modal app
app = modal.App("frameflow")

# Define image with all dependencies AND project files
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
    # Copy project files into the image
    .copy_local_dir("core", "/root/core")
    .copy_local_dir("integrations", "/root/integrations")
    .copy_local_dir("mcp_servers", "/root/mcp_servers")
    .copy_local_file("app.py", "/root/app.py")
)

# Define secrets - all API keys in one secret
secrets = [modal.Secret.from_name("frameflow-secrets")]


# GPU function for image generation
@app.function(
    image=image,
    gpu="T4",  # Use T4 GPU for image generation
    timeout=600,  # 10 minute timeout
    secrets=secrets
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
    min_containers=1,  # Keep one instance warm
    timeout=1800,  # 30 minute timeout for long screenplay generation
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
