"""
Modal Deployment Configuration for FrameFlow
Deploys Gradio app with GPU support for image generation
"""

import modal

# Create Modal app
app = modal.App("frameflow")

# Define image: Install dependencies and clone the GitHub repo
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Install git
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
    .run_commands(
        "cd /root && git clone https://github.com/ahmetmertugrul/frameflow.git",
        "cd /root/frameflow && git checkout claude/start-frameflow-project-01U4FinfxJYU2wCM8sTGaVAT"
    )
)

# Define secrets - all API keys in one secret
secrets = [modal.Secret.from_name("frameflow-secrets")]


# Main Gradio app
@app.function(
    image=image,
    secrets=secrets,
    min_containers=1,  # Keep one instance warm
    timeout=1800,  # 30 minute timeout for long screenplay generation
    gpu="T4",  # Add GPU for the main app
)
@modal.asgi_app()
def gradio_app():
    """Gradio web interface"""
    import sys
    sys.path.insert(0, "/root/frameflow")  # Add cloned repo to Python path

    # Import and return the Gradio demo
    from app import demo
    return demo


# CLI for local development
@app.local_entrypoint()
def main():
    """Run the app locally"""
    print("🚀 Deploying FrameFlow to Modal...")
    print("Visit the URL below to access your app:")
    print()
    gradio_app.remote()
