# FrameFlow

**Screenplay & Storyboard Generation Agent**

MCP 1st Birthday Hackathon | November 2025

---

## 1. Executive Summary

FrameFlow is an intelligent agent that transforms simple story ideas into complete screenplays with accompanying visual storyboards. The system leverages multiple AI services through MCP (Model Context Protocol) to provide a seamless creative workflow from concept to production-ready materials.

The project targets the **MCP in Action - Multimodal** track, combining text generation, image synthesis, and document creation in an autonomous agent workflow.

---

## 2. Project Overview

### 2.1 Problem Statement

Content creators, filmmakers, and storytellers face significant barriers in the pre-production phase. Professional screenplay writing requires expertise in formatting and structure, while storyboard creation demands both artistic skills and understanding of visual storytelling. This creates a gap between creative vision and executable production materials.

### 2.2 Solution

FrameFlow bridges this gap by providing an end-to-end solution that takes a simple story prompt and generates a formatted screenplay with scene breakdowns, character development, dialogue, and visual storyboard frames for each key scene.

### 2.3 Target Track

- **Track:** MCP in Action
- **Category:** Multimodal
- **Tag:** `mcp-in-action-track-multimodal`

---

## 3. Platform Credits & Resource Allocation

| Platform | Credit | Usage in Project |
|----------|--------|------------------|
| **Modal.com** | $250 | Main infrastructure - Gradio app hosting, GPU compute for image generation, serverless functions for MCP servers |
| **Blaxel.ai** | $250 | MCP server deployment platform, agent orchestration layer, eligible for $2,500 Blaxel Choice Award |
| **Nebius.com** | $50 | Secondary LLM inference, embedding generation for semantic consistency, character/scene memory |
| **Hyperbolic.ai** | $25 | Storyboard image generation using SDXL/Flux models |
| **SambaNova.ai** | $5 | Fast LLM inference for real-time screenplay generation, dialogue refinement |

**Total Credits: $580**

---

## 4. Technical Architecture

### 4.1 System Components

#### 4.1.1 Frontend Layer (Gradio 6)

- Story input interface with genre/style selection
- Real-time screenplay preview with syntax highlighting
- Storyboard gallery with zoom and navigation
- Export options (PDF screenplay, image pack, combined document)
- Mobile-responsive design for on-the-go creativity

#### 4.1.2 MCP Server Layer

**screenplay-generator MCP Server:** Handles story structure, character arcs, scene breakdown, and dialogue generation using LLM inference.

**storyboard-visualizer MCP Server:** Converts scene descriptions to visual prompts and generates storyboard images.

**document-exporter MCP Server:** Creates formatted PDF/DOCX outputs with proper screenplay formatting.

**character-consistency MCP Server:** Maintains character visual and personality consistency across scenes using embeddings.

#### 4.1.3 Backend Services

- **Modal.com:** Gradio app hosting, GPU functions, async job processing
- **Blaxel.ai:** MCP server deployment and management
- **Nebius.com:** Vector database for character/scene consistency

### 4.2 Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INPUT                                  │
│                    (Story idea, genre, preferences)                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FRAMEFLOW - GRADIO 6 INTERFACE                      │
│                        (Modal.com - $250 credit)                         │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      MCP ORCHESTRATION LAYER                             │
│                     (Blaxel.ai - $250 credit)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│  │  screenplay-    │  │  storyboard-    │  │  character-consistency  │  │
│  │  generator      │  │  visualizer     │  │  (Nebius embeddings)    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────────┬────────────┘  │
│           │                    │                        │               │
└───────────┼────────────────────┼────────────────────────┼───────────────┘
            │                    │                        │
            ▼                    ▼                        ▼
┌───────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐
│   SambaNova.ai    │  │   Hyperbolic.ai     │  │      Nebius.com         │
│   ($5 credit)     │  │   ($25 credit)      │  │      ($50 credit)       │
│                   │  │                     │  │                         │
│   Fast LLM for    │  │   SDXL/Flux for     │  │   Embeddings for        │
│   screenplay      │  │   storyboard        │  │   character             │
│   generation      │  │   images            │  │   consistency           │
└───────────────────┘  └─────────────────────┘  └─────────────────────────┘
            │                    │                        │
            └────────────────────┼────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRAMEFLOW OUTPUT                                 │
│         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│         │  Formatted   │  │  Storyboard  │  │   Combined   │            │
│         │  Screenplay  │  │   Images     │  │   Lookbook   │            │
│         │    (PDF)     │  │    (ZIP)     │  │    (PDF)     │            │
│         └──────────────┘  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Data Flow Steps

1. User inputs story idea, genre, and preferences
2. FrameFlow agent analyzes input and creates story structure
3. Character profiles generated with visual descriptions
4. Scene-by-scene screenplay written with proper formatting
5. Key moments identified for storyboard frames
6. Visual prompts generated with character consistency
7. Storyboard images created via image generation API
8. Final package assembled with screenplay + storyboards

---

## 5. Core Features

### 5.1 Screenplay Generation

- Industry-standard formatting (INT/EXT, character cues, action lines)
- Multiple genre templates (Drama, Comedy, Thriller, Sci-Fi, Horror)
- Act structure guidance (Three-Act, Five-Act, Hero's Journey)
- Character arc development with motivation tracking
- Dialogue style customization (realistic, stylized, period-specific)

### 5.2 Storyboard Generation

- Automatic key moment detection from screenplay
- Camera angle suggestions (wide, medium, close-up, POV)
- Character visual consistency across frames
- Style presets (realistic, illustrated, noir, anime)
- Scene composition and lighting descriptions

### 5.3 Export & Integration

- PDF export with proper screenplay formatting
- Image pack download (ZIP with numbered frames)
- Combined lookbook document (screenplay + storyboards)
- Shot list generation for production planning

---

## 6. Implementation Timeline

### Phase 1: Foundation (Days 1-3)

| Task | Description | Platform |
|------|-------------|----------|
| 1 | Set up development environment and repository | Local |
| 2 | Configure Modal.com account and Gradio app skeleton | Modal |
| 3 | Set up Blaxel.ai for MCP server hosting | Blaxel |
| 4 | Integrate SambaNova API for fast LLM inference | SambaNova |
| 5 | Create basic MCP server structure | Blaxel |

### Phase 2: Core Agent (Days 4-7)

| Task | Description | Platform |
|------|-------------|----------|
| 1 | Implement screenplay-generator MCP server | Blaxel |
| 2 | Build story structure analysis module | SambaNova |
| 3 | Develop character profile generation | SambaNova |
| 4 | Create scene breakdown logic | SambaNova |
| 5 | Implement dialogue generation with style options | SambaNova |

### Phase 3: Visual Pipeline (Days 8-11)

| Task | Description | Platform |
|------|-------------|----------|
| 1 | Set up Hyperbolic.ai image generation integration | Hyperbolic |
| 2 | Implement storyboard-visualizer MCP server | Blaxel |
| 3 | Build visual prompt generation from scenes | Nebius |
| 4 | Configure Nebius embeddings for character consistency | Nebius |
| 5 | Create camera angle and composition logic | Local |

### Phase 4: Integration & Polish (Days 12-16)

| Task | Description | Platform |
|------|-------------|----------|
| 1 | Build complete Gradio 6 interface | Modal |
| 2 | Implement export functionality (PDF, images, combined) | Modal |
| 3 | Add error handling and loading states | Modal |
| 4 | Create demo video and documentation | Local |
| 5 | Test end-to-end workflow | All |
| 6 | Submit to HuggingFace Spaces | HuggingFace |

---

## 7. Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Gradio 6, HTML/CSS, JavaScript |
| **Backend** | Python 3.11+, FastAPI, Modal Functions |
| **MCP Framework** | mcp-server-python, Blaxel SDK |
| **LLM Inference** | SambaNova API, Nebius AI Studio |
| **Image Generation** | Hyperbolic.ai (SDXL/Flux), Modal GPU |
| **Storage** | Modal Volumes, HuggingFace Datasets |
| **Export** | ReportLab (PDF), Pillow, python-docx |

---

## 8. MCP Server Specifications

### 8.1 screenplay-generator

Primary MCP server for screenplay creation and story structure.

**Tools:**

| Tool | Parameters | Description |
|------|------------|-------------|
| `analyze_story` | `prompt`, `genre` | Extracts story elements and suggests structure |
| `create_characters` | `story_analysis` | Generates character profiles with descriptions |
| `write_scene` | `scene_outline`, `characters` | Writes formatted screenplay scene |
| `generate_dialogue` | `context`, `characters`, `style` | Creates character-specific dialogue |

**Resources:**

- `screenplay://current` - Current screenplay state
- `screenplay://characters` - Character database
- `screenplay://structure` - Story structure template

### 8.2 storyboard-visualizer

Handles visual generation and composition for storyboard frames.

**Tools:**

| Tool | Parameters | Description |
|------|------------|-------------|
| `identify_key_moments` | `screenplay` | Selects scenes for storyboard frames |
| `generate_visual_prompt` | `scene`, `characters` | Creates detailed image generation prompt |
| `create_frame` | `visual_prompt`, `style` | Generates storyboard image |
| `suggest_camera_angle` | `scene_type` | Recommends composition and framing |

**Resources:**

- `storyboard://frames` - Generated frame collection
- `storyboard://styles` - Available visual styles

### 8.3 character-consistency

Maintains visual and personality consistency across the project.

**Tools:**

| Tool | Parameters | Description |
|------|------------|-------------|
| `store_character_embedding` | `character_profile` | Saves character visual signature |
| `get_character_prompt` | `character_name` | Retrieves consistent visual description |
| `validate_consistency` | `new_frame`, `character` | Checks frame against character profile |

**Resources:**

- `characters://embeddings` - Character embedding database
- `characters://profiles` - Full character profiles

### 8.4 document-exporter

Creates formatted export documents.

**Tools:**

| Tool | Parameters | Description |
|------|------------|-------------|
| `export_screenplay_pdf` | `screenplay`, `format` | Creates industry-standard PDF |
| `export_storyboard_pack` | `frames`, `format` | Creates image ZIP package |
| `export_lookbook` | `screenplay`, `frames` | Creates combined document |
| `generate_shot_list` | `screenplay`, `frames` | Creates production shot list |

---

## 9. Alignment with Judging Criteria

| Criteria | How FrameFlow Addresses It |
|----------|----------------------------|
| **Design/UI-UX** | Clean, intuitive Gradio 6 interface with mobile support. Clear workflow from input to export. Real-time progress indicators. |
| **Functionality** | Full MCP integration with multiple servers. Uses Gradio 6 agentic features. Demonstrates planning, reasoning, and execution. |
| **Creativity** | Novel combination of screenplay writing and visual generation. Character consistency via embeddings. Multi-modal output. |
| **Documentation** | Comprehensive README with architecture diagrams. Demo video walkthrough. Clear API documentation for MCP servers. |
| **Real-world Impact** | Practical tool for indie filmmakers, content creators, and storytellers. Reduces pre-production barriers significantly. |

---

## 10. Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Image generation quality inconsistency | Medium | High | Multiple style presets, regeneration option, prompt optimization |
| Credit exhaustion during development | Medium | High | Local testing with smaller models, caching, efficient batching |
| Character consistency failures | Medium | Medium | Strong embedding system via Nebius, validation checks, manual override |
| Time constraints for full feature set | High | Medium | MVP-first approach, prioritized feature list, modular architecture |
| API rate limits or downtime | Low | High | Fallback providers, graceful degradation, error handling |
| Complex MCP integration issues | Medium | Medium | Incremental development, extensive testing, Blaxel support |

---

## 11. Success Metrics

| Metric | Target |
|--------|--------|
| Screenplay generation time | < 2 minutes for short screenplay |
| Storyboard frames per screenplay | 8-12 frames minimum |
| Character visual consistency | > 80% similarity across frames |
| Export formats supported | PDF, ZIP (images), Combined PDF |
| Mobile responsiveness | Full functionality on mobile devices |
| Platform credit utilization | All 5 platforms used in production |

---

## 12. Final Deliverables

### Required Submissions

- [ ] HuggingFace Space with deployed Gradio application
- [ ] GitHub repository with complete source code
- [ ] 3-5 minute demo video showcasing full workflow
- [ ] Comprehensive README with setup instructions
- [ ] MCP server documentation with tool specifications
- [ ] Social media post with project highlights
- [ ] Sample outputs (screenplay + storyboard examples)

### Submission Checklist

- [ ] Space published to MCP-1st-Birthday organization
- [ ] README includes `mcp-in-action-track-multimodal` tag
- [ ] Social media link included in README
- [ ] Demo video linked in Space description
- [ ] All work completed between Nov 14-30, 2025

---

## 13. Repository Structure

```
frameflow/
├── README.md
├── requirements.txt
├── app.py                      # Main Gradio application
├── modal_app.py                # Modal deployment configuration
│
├── mcp_servers/
│   ├── screenplay_generator/
│   │   ├── __init__.py
│   │   ├── server.py           # MCP server implementation
│   │   ├── story_analyzer.py
│   │   ├── character_creator.py
│   │   └── scene_writer.py
│   │
│   ├── storyboard_visualizer/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── moment_detector.py
│   │   ├── prompt_generator.py
│   │   └── image_creator.py
│   │
│   ├── character_consistency/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── embedding_manager.py
│   │
│   └── document_exporter/
│       ├── __init__.py
│       ├── server.py
│       ├── pdf_generator.py
│       └── lookbook_creator.py
│
├── core/
│   ├── __init__.py
│   ├── agent.py                # Main FrameFlow agent orchestration
│   ├── prompts.py              # LLM prompt templates
│   └── schemas.py              # Pydantic models
│
├── integrations/
│   ├── __init__.py
│   ├── sambanova.py            # SambaNova API client
│   ├── hyperbolic.py           # Hyperbolic API client
│   ├── nebius.py               # Nebius API client
│   └── blaxel.py               # Blaxel SDK wrapper
│
├── templates/
│   ├── screenplay_formats/
│   │   ├── standard.py
│   │   └── short_film.py
│   └── storyboard_styles/
│       ├── realistic.py
│       ├── illustrated.py
│       └── noir.py
│
├── static/
│   ├── css/
│   └── images/
│
├── tests/
│   ├── test_screenplay.py
│   ├── test_storyboard.py
│   └── test_integration.py
│
├── docs/
│   ├── API.md
│   ├── SETUP.md
│   └── EXAMPLES.md
│
└── examples/
    ├── sample_screenplay.pdf
    ├── sample_storyboard/
    └── sample_lookbook.pdf
```

---

## 14. Quick Start Commands

```bash
# Clone repository
git clone https://github.com/username/frameflow.git
cd frameflow

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SAMBANOVA_API_KEY="your-key"
export HYPERBOLIC_API_KEY="your-key"
export NEBIUS_API_KEY="your-key"
export BLAXEL_API_KEY="your-key"

# Run locally
python app.py

# Deploy to Modal
modal deploy modal_app.py

# Deploy MCP servers to Blaxel
blaxel deploy mcp_servers/
```

---

## 15. Project Information

| Field | Value |
|-------|-------|
| **Project Name** | FrameFlow |
| **Tagline** | From idea to storyboard in minutes |
| **Track** | MCP in Action - Multimodal |
| **Submission Tag** | `mcp-in-action-track-multimodal` |
| **Deadline** | November 30, 2025, 11:59 PM UTC |
| **Team Size** | Solo / 2-5 members |
| **Eligible Awards** | Main Prize ($2,500/$1,000/$500), Blaxel Choice ($2,500), Community Choice ($1,000) |

---

## 16. References & Resources

### Official Documentation

- [Gradio 6 Documentation](https://www.gradio.app/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Getting Started with MCP in Gradio](https://huggingface.co/blog/gradio-mcp)
- [Modal.com Documentation](https://modal.com/docs)
- [Blaxel.ai Documentation](https://docs.blaxel.ai)

### Platform APIs

- [SambaNova API Reference](https://docs.sambanova.ai)
- [Hyperbolic.ai API Reference](https://docs.hyperbolic.ai)
- [Nebius AI Studio](https://studio.nebius.ai)

### Hackathon Resources

- [MCP 1st Birthday Hackathon](https://huggingface.co/MCP-1st-Birthday)
- [Discord Community](https://discord.gg/fveShqytyh)
- [Submission Guidelines](https://huggingface.co/MCP-1st-Birthday)

---

## 17. License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>FrameFlow</b> - From idea to storyboard in minutes 🎬
</p>

<p align="center">
  Built for MCP 1st Birthday Hackathon | November 2025
</p>

---

*Last Updated: November 2025*
