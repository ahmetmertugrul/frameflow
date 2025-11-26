# 🎬 FrameFlow

**From idea to storyboard in minutes**

[![MCP 1st Birthday Hackathon](https://img.shields.io/badge/MCP-1st%20Birthday%20Hackathon-blue)](https://huggingface.co/MCP-1st-Birthday)
[![Track: Multimodal](https://img.shields.io/badge/Track-Multimodal-purple)](https://huggingface.co/MCP-1st-Birthday)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FrameFlow is an intelligent AI agent that transforms simple story ideas into complete screenplays with accompanying visual storyboards. Built for the MCP 1st Birthday Hackathon, it leverages multiple AI services through the Model Context Protocol (MCP) to provide a seamless creative workflow from concept to production-ready materials.

## ✨ Features

### 📝 Screenplay Generation
- **Industry-Standard Formatting**: INT/EXT, character cues, action lines
- **Multiple Genre Templates**: Drama, Comedy, Thriller, Sci-Fi, Horror, Romance, Action, Mystery
- **Story Structure**: Three-Act, Five-Act, Hero's Journey templates
- **Character Development**: Automated character arc and motivation tracking
- **Dialogue Customization**: Realistic, stylized, period-specific, witty, or minimal styles

### 🎨 Storyboard Generation
- **Automatic Key Moment Detection**: Identifies the most visually important scenes
- **Camera Angle Suggestions**: Wide, medium, close-up, POV, and more
- **Character Consistency**: Maintains visual consistency across all frames using embeddings
- **Multiple Visual Styles**: Realistic, illustrated, noir, anime, sketch
- **Professional Composition**: Scene layout, lighting, and framing descriptions

### 📦 Export & Integration
- **PDF Screenplay Export**: Industry-standard screenplay formatting
- **Image Pack Download**: ZIP file with numbered storyboard frames
- **Combined Lookbook**: Screenplay + storyboards in one document
- **Shot List Generation**: Production-ready shot lists

## 🏗️ Architecture

FrameFlow uses a multi-agent architecture powered by MCP (Model Context Protocol):

```
┌─────────────────────────────────────────────────────────┐
│                   Gradio 6 Interface                    │
│                    (Modal.com)                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              MCP Orchestration Layer                    │
│                   (Blaxel.ai)                           │
├─────────────────────────────────────────────────────────┤
│  • screenplay-generator      • storyboard-visualizer    │
│  • character-consistency     • document-exporter        │
└──────────┬─────────────┬─────────────┬──────────────────┘
           │             │             │
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │SambaNova │  │Hyperbolic│  │ Nebius   │
    │   LLM    │  │  Images  │  │Embeddings│
    └──────────┘  └──────────┘  └──────────┘
```

### MCP Servers

1. **screenplay-generator**: Story structure, character creation, scene writing, dialogue generation
2. **storyboard-visualizer**: Visual prompt generation, image creation, camera angles
3. **character-consistency**: Character embeddings, consistency validation
4. **document-exporter**: PDF/DOCX export, lookbook creation

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- API keys for:
  - SambaNova AI (LLM generation)
  - Hyperbolic AI (image generation)
  - Nebius AI (embeddings)
  - Blaxel AI (MCP hosting)
  - Modal.com (deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahmetmertugrul/frameflow.git
   cd frameflow
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run locally**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:7860
   ```

## 🔑 Environment Variables

Create a `.env` file with the following:

```env
# LLM Inference
SAMBANOVA_API_KEY=your_sambanova_key_here

# Image Generation
HYPERBOLIC_API_KEY=your_hyperbolic_key_here

# Embeddings
NEBIUS_API_KEY=your_nebius_key_here

# MCP Hosting
BLAXEL_API_KEY=your_blaxel_key_here

# Deployment
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
```

## 📖 Usage

### Basic Workflow

1. **Enter Story Prompt**
   ```
   A detective in a noir city discovers that the serial killer
   he's hunting is actually his future self.
   ```

2. **Select Preferences**
   - Genre: Thriller
   - Dialogue Style: Realistic
   - Act Structure: Three-Act

3. **Generate Screenplay**
   - Click "Generate Screenplay"
   - Wait for AI to analyze, create characters, and write scenes
   - Review the formatted screenplay

4. **Generate Storyboard**
   - Set number of frames (4-16)
   - Choose visual style (Realistic, Noir, etc.)
   - Click "Generate Storyboard"
   - View and navigate through frames

5. **Export**
   - Export screenplay as PDF
   - Download storyboard frames as ZIP
   - Create combined lookbook

### Example Prompts

**Drama**
```
A single mother working two jobs discovers her teenage son
has been secretly caring for homeless people in their garage.
```

**Comedy**
```
Two rival food truck owners are forced to share a kitchen
after a fire destroys both their businesses.
```

**Sci-Fi**
```
In 2157, a time-travel repairman must prevent his past self
from inventing time travel.
```

## 🛠️ Development

### Project Structure

```
frameflow/
├── app.py                      # Main Gradio application
├── requirements.txt            # Python dependencies
│
├── core/
│   ├── agent.py               # Main FrameFlow agent
│   ├── schemas.py             # Pydantic models
│   └── prompts.py             # LLM prompt templates
│
├── mcp_servers/
│   ├── screenplay_generator/  # Screenplay MCP server
│   ├── storyboard_visualizer/ # Storyboard MCP server
│   ├── character_consistency/ # Consistency MCP server
│   └── document_exporter/     # Export MCP server
│
├── integrations/
│   ├── sambanova.py           # SambaNova API client
│   ├── hyperbolic.py          # Hyperbolic API client
│   └── nebius.py              # Nebius API client
│
├── templates/                 # Screenplay & storyboard templates
├── static/                    # Static assets (CSS, images)
├── tests/                     # Unit and integration tests
└── docs/                      # Documentation
```

### Running Tests

FrameFlow includes a comprehensive test suite with 110+ test cases covering all core functionality.

**Run all tests:**
```bash
pytest tests/
```

**Run with coverage report:**
```bash
pytest tests/ --cov=core --cov=integrations --cov=mcp_servers --cov-report=html
```

**Run specific test files:**
```bash
# Schema tests only
pytest tests/test_schemas.py -v

# Prompt tests only
pytest tests/test_prompts.py -v

# Agent tests only
pytest tests/test_agent.py -v

# Integration tests only
pytest tests/test_integrations.py -v
```

**Run with markers:**
```bash
# Run only unit tests (exclude integration tests)
pytest tests/ -m "not integration"

# Run only integration tests (requires API keys)
pytest tests/ -m integration

# Run only async tests
pytest tests/ -m asyncio
```

**Test Coverage:**
- ✅ **Core**: schemas, prompts, agent orchestration
- ✅ **Integrations**: SambaNova, Hyperbolic, Nebius clients
- ✅ **MCP Servers**: screenplay generator tools
- ✅ **Edge Cases**: validation, error handling, async operations

**View HTML coverage report:**
```bash
pytest tests/ --cov-report=html
open htmlcov/index.html  # Opens in browser
```

### Deploying to Modal

```bash
modal deploy modal_app.py
```

### Deploying MCP Servers to Blaxel

```bash
blaxel deploy mcp_servers/
```

## 🎯 Technical Details

### Technologies Used

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Gradio 6, HTML/CSS, JavaScript |
| **Backend** | Python 3.11+, FastAPI, Modal Functions |
| **MCP Framework** | mcp-server-python, Blaxel SDK |
| **LLM Inference** | SambaNova API, Nebius AI Studio |
| **Image Generation** | Hyperbolic.ai (SDXL/Flux) |
| **Vector DB** | ChromaDB, Sentence Transformers |
| **Export** | ReportLab (PDF), Pillow, python-docx |

### Platform Credits

| Platform | Credit | Usage |
|----------|--------|-------|
| **Modal.com** | $250 | Gradio hosting, GPU compute |
| **Blaxel.ai** | $250 | MCP server deployment |
| **Nebius.com** | $50 | LLM inference, embeddings |
| **Hyperbolic.ai** | $25 | Image generation |
| **SambaNova.ai** | $5 | Fast LLM inference |

## 🏆 Hackathon Submission

This project is submitted to the **MCP 1st Birthday Hackathon** in the **MCP in Action - Multimodal** track.

**Tag**: `mcp-in-action-track-multimodal`

### Deliverables

- ✅ HuggingFace Space with deployed Gradio application
- ✅ Complete source code on GitHub
- ✅ Demo video (3-5 minutes)
- ✅ Comprehensive documentation
- ✅ MCP server specifications
- ✅ Sample outputs

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- MCP 1st Birthday Hackathon organizers
- SambaNova, Hyperbolic, Nebius, Blaxel, and Modal for platform credits
- The MCP and Gradio communities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Project Link: [https://github.com/ahmetmertugrul/frameflow](https://github.com/ahmetmertugrul/frameflow)

## 🌟 Show Your Support

If you find FrameFlow useful, please give it a ⭐️ on GitHub!

---

<p align="center">
  <b>FrameFlow</b> - Transforming ideas into visual stories 🎬✨
</p>

<p align="center">
  Built for MCP 1st Birthday Hackathon | November 2025
</p>
