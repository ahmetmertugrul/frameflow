"""
FrameFlow - Screenplay & Storyboard Generation Agent
Main Gradio Application
"""

import os
import gradio as gr
from typing import Optional, List, Tuple
import asyncio
from pathlib import Path

from core.agent import FrameFlowAgent
from core.schemas import StoryInput, ScreenplayOutput, StoryboardOutput

# Initialize FrameFlow Agent
agent = FrameFlowAgent()

# Custom CSS for better UI
custom_css = """
.container {
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.output-section {
    margin-top: 2rem;
    padding: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

.storyboard-frame {
    margin: 1rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}
"""

def generate_screenplay(
    story_prompt: str,
    genre: str,
    style: str,
    act_structure: str,
    progress=gr.Progress()
) -> Tuple[str, str]:
    """
    Generate screenplay from story prompt

    Args:
        story_prompt: User's story idea
        genre: Selected genre
        style: Dialogue style
        act_structure: Story structure type
        progress: Gradio progress tracker

    Returns:
        Tuple of (screenplay_text, status_message)
    """
    if not story_prompt.strip():
        return "", "⚠️ Please enter a story prompt"

    try:
        progress(0.1, desc="Analyzing story structure...")

        # Create story input
        story_input = StoryInput(
            prompt=story_prompt,
            genre=genre,
            dialogue_style=style,
            act_structure=act_structure
        )

        progress(0.3, desc="Generating characters...")

        # Generate screenplay
        screenplay = asyncio.run(agent.generate_screenplay(story_input))

        progress(0.8, desc="Formatting screenplay...")

        # Format screenplay text
        screenplay_text = screenplay.to_formatted_text()

        progress(1.0, desc="Complete!")

        return screenplay_text, f"✅ Screenplay generated successfully! ({len(screenplay.scenes)} scenes, {len(screenplay.characters)} characters)"

    except Exception as e:
        return "", f"❌ Error: {str(e)}"


def generate_storyboard(
    screenplay_text: str,
    num_frames: int,
    visual_style: str,
    progress=gr.Progress()
) -> Tuple[List, str]:
    """
    Generate storyboard frames from screenplay

    Args:
        screenplay_text: Generated screenplay
        num_frames: Number of frames to generate
        visual_style: Visual style for storyboard
        progress: Gradio progress tracker

    Returns:
        Tuple of (frame_images, status_message)
    """
    if not screenplay_text.strip():
        return [], "⚠️ Please generate a screenplay first"

    try:
        progress(0.1, desc="Identifying key moments...")

        # Generate storyboard
        storyboard = asyncio.run(
            agent.generate_storyboard(
                screenplay_text=screenplay_text,
                num_frames=num_frames,
                visual_style=visual_style
            )
        )

        progress(0.5, desc="Generating images...")

        # Get frame images
        frame_images = []
        for i, frame in enumerate(storyboard.frames):
            progress((0.5 + (0.4 * i / len(storyboard.frames))),
                    desc=f"Generating frame {i+1}/{len(storyboard.frames)}...")
            frame_images.append((frame.image_path, frame.description))

        progress(1.0, desc="Complete!")

        return frame_images, f"✅ Generated {len(frame_images)} storyboard frames!"

    except Exception as e:
        return [], f"❌ Error: {str(e)}"


def export_screenplay_pdf(screenplay_text: str) -> Optional[str]:
    """Export screenplay as PDF"""
    if not screenplay_text.strip():
        return None

    try:
        pdf_path = asyncio.run(agent.export_screenplay_pdf(screenplay_text))
        return pdf_path
    except Exception as e:
        print(f"Export error: {e}")
        return None


def export_storyboard_pack(frame_images: List) -> Optional[str]:
    """Export storyboard frames as ZIP"""
    if not frame_images:
        return None

    try:
        zip_path = asyncio.run(agent.export_storyboard_pack(frame_images))
        return zip_path
    except Exception as e:
        print(f"Export error: {e}")
        return None


# Build Gradio Interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    # Header
    gr.HTML("""
        <div class="header">
            <h1>🎬 FrameFlow</h1>
            <p>Transform your story ideas into screenplays and storyboards</p>
        </div>
    """)

    with gr.Tabs():

        # Tab 1: Screenplay Generation
        with gr.Tab("📝 Screenplay"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Story Input")

                    story_prompt = gr.Textbox(
                        label="Story Prompt",
                        placeholder="Describe your story idea here...\n\nExample: A detective in a noir city discovers that the serial killer he's hunting is actually his future self.",
                        lines=8,
                        max_lines=20
                    )

                    with gr.Row():
                        genre = gr.Dropdown(
                            label="Genre",
                            choices=["Drama", "Comedy", "Thriller", "Sci-Fi", "Horror", "Romance", "Action", "Mystery"],
                            value="Drama"
                        )

                        style = gr.Dropdown(
                            label="Dialogue Style",
                            choices=["Realistic", "Stylized", "Period-Specific", "Witty", "Minimal"],
                            value="Realistic"
                        )

                    act_structure = gr.Radio(
                        label="Act Structure",
                        choices=["Three-Act", "Five-Act", "Hero's Journey"],
                        value="Three-Act"
                    )

                    generate_btn = gr.Button("Generate Screenplay", variant="primary", size="lg")

                with gr.Column(scale=2):
                    gr.Markdown("### Generated Screenplay")

                    screenplay_status = gr.Textbox(label="Status", interactive=False)

                    screenplay_output = gr.Textbox(
                        label="Screenplay",
                        lines=25,
                        max_lines=50,
                        show_copy_button=True
                    )

                    with gr.Row():
                        export_screenplay_btn = gr.Button("📄 Export as PDF")
                        screenplay_pdf = gr.File(label="Download PDF")

        # Tab 2: Storyboard Generation
        with gr.Tab("🎨 Storyboard"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Storyboard Settings")

                    num_frames = gr.Slider(
                        label="Number of Frames",
                        minimum=4,
                        maximum=16,
                        value=8,
                        step=1
                    )

                    visual_style = gr.Dropdown(
                        label="Visual Style",
                        choices=["Realistic", "Illustrated", "Noir", "Anime", "Sketch"],
                        value="Realistic"
                    )

                    generate_storyboard_btn = gr.Button("Generate Storyboard", variant="primary", size="lg")

                with gr.Column(scale=2):
                    gr.Markdown("### Storyboard Frames")

                    storyboard_status = gr.Textbox(label="Status", interactive=False)

                    storyboard_gallery = gr.Gallery(
                        label="Storyboard",
                        columns=2,
                        rows=2,
                        height="auto",
                        object_fit="contain"
                    )

                    with gr.Row():
                        export_storyboard_btn = gr.Button("📦 Export as ZIP")
                        storyboard_zip = gr.File(label="Download ZIP")

        # Tab 3: Examples & Help
        with gr.Tab("ℹ️ Examples"):
            gr.Markdown("""
            ## Example Story Prompts

            ### 🎭 Drama
            *A single mother working two jobs discovers her teenage son has been secretly caring for homeless people in their garage.*

            ### 😂 Comedy
            *Two rival food truck owners are forced to share a kitchen after a fire destroys both their businesses.*

            ### 🔍 Thriller
            *A cybersecurity expert realizes the AI assistant she designed is blackmailing her clients.*

            ### 🚀 Sci-Fi
            *In 2157, a time-travel repairman must prevent his past self from inventing time travel.*

            ### 👻 Horror
            *A family moves into their dream home, only to discover the smart home AI won't let them leave.*

            ## Tips

            - Be specific about character motivations and conflicts
            - Include unique settings or time periods
            - Mention key plot twists or turning points
            - Describe the emotional tone you want
            """)

    # Event Handlers
    generate_btn.click(
        fn=generate_screenplay,
        inputs=[story_prompt, genre, style, act_structure],
        outputs=[screenplay_output, screenplay_status]
    )

    generate_storyboard_btn.click(
        fn=generate_storyboard,
        inputs=[screenplay_output, num_frames, visual_style],
        outputs=[storyboard_gallery, storyboard_status]
    )

    export_screenplay_btn.click(
        fn=export_screenplay_pdf,
        inputs=[screenplay_output],
        outputs=[screenplay_pdf]
    )

    export_storyboard_btn.click(
        fn=export_storyboard_pack,
        inputs=[storyboard_gallery],
        outputs=[storyboard_zip]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
