"""
FrameFlow - LLM Prompt Templates
Carefully crafted prompts for screenplay and storyboard generation
"""

# Story Analysis Prompts

STORY_ANALYSIS_PROMPT = """You are an expert story analyst and screenplay consultant. Analyze the following story prompt and extract key elements for screenplay development.

Story Prompt: {prompt}
Genre: {genre}
Act Structure: {act_structure}

Please provide a detailed analysis including:

1. Main Theme: What is the core theme or message?
2. Conflict: What is the central conflict?
3. Protagonist: Who is the main character?
4. Antagonist: Who or what opposes the protagonist?
5. Setting: Where and when does the story take place?
6. Key Plot Points: What are the major story beats?
7. Suggested Acts: How should the story be structured?

Provide your analysis in a structured format that can be used to develop a full screenplay.
"""


# Character Generation Prompts

CHARACTER_CREATION_PROMPT = """You are a character development specialist. Based on the story analysis below, create detailed character profiles for the screenplay.

Story Analysis:
{story_analysis}

Genre: {genre}

For each major character (protagonist, antagonist, and 2-3 supporting characters), provide:

1. Name: Character's full name
2. Age: Approximate age
3. Role: protagonist/antagonist/supporting
4. Description: One-sentence character description
5. Personality Traits: 3-5 key traits
6. Visual Description: Detailed physical appearance for storyboard generation (include: build, hair, clothing style, distinctive features)
7. Motivation: What drives this character?
8. Character Arc: How does this character change?

Make characters feel authentic, complex, and appropriate for the {genre} genre.
"""


# Scene Writing Prompts

SCENE_WRITING_PROMPT = """You are a professional screenwriter. Write a compelling screenplay scene following industry-standard formatting.

Scene Details:
- Scene Number: {scene_number}
- Act: {act}
- Location: {location}
- Time: {time}
- Purpose: {purpose}

Characters in Scene:
{characters}

Plot Context:
{context}

Dialogue Style: {dialogue_style}
Genre: {genre}

Write the scene including:
1. Scene heading (INT/EXT. LOCATION - TIME)
2. Action lines describing what happens
3. Character dialogue with proper formatting
4. Parentheticals for character emotions/actions where needed

Keep the scene focused, visual, and true to the characters. Make every line of dialogue reveal character or advance the plot.
"""


DIALOGUE_GENERATION_PROMPT = """You are a dialogue specialist. Generate authentic dialogue for this screenplay scene.

Characters:
{characters}

Scene Context:
{context}

Dialogue Style: {dialogue_style}
Genre: {genre}

Emotional Tone: {tone}

Generate dialogue that:
1. Sounds natural and authentic to each character
2. Reveals character personality and motivation
3. Advances the plot or deepens conflict
4. Matches the {dialogue_style} style
5. Fits the {genre} genre conventions

Avoid:
- On-the-nose dialogue
- Exposition dumps
- Characters saying what they're doing
- Repetitive patterns

Format as:
CHARACTER NAME
(parenthetical if needed)
Dialogue line
"""


# Storyboard Generation Prompts

KEY_MOMENT_DETECTION_PROMPT = """You are a visual storytelling expert. Identify the key moments in this screenplay that should be visualized as storyboard frames.

Screenplay:
{screenplay}

Number of Frames Needed: {num_frames}

Identify the most visually important, emotionally resonant, and narratively crucial moments. Focus on:
1. Major plot turning points
2. Character reveals or transformations
3. Emotional climaxes
4. Action sequences
5. Establishing shots for new locations
6. Visual metaphors or symbolism

For each selected moment, provide:
- Scene number
- Brief description
- Why this moment is visually important
- Suggested camera angle

Distribute frames evenly across the screenplay's narrative arc.
"""


VISUAL_PROMPT_GENERATION = """You are an expert in visual composition and cinematography. Create a detailed image generation prompt for this storyboard frame.

Scene Description:
{scene_description}

Characters in Frame:
{characters}

Camera Angle: {camera_angle}
Visual Style: {visual_style}
Mood: {mood}

Generate a comprehensive image generation prompt that includes:

1. Main Subject: What/who is the focus?
2. Character Descriptions: Detailed visual appearance (consistent with earlier frames)
3. Setting Details: Environment, props, background
4. Lighting: Light sources, shadows, time of day, atmosphere
5. Camera Angle: {camera_angle} specifics
6. Composition: Rule of thirds, framing, depth
7. Color Palette: Dominant colors and mood
8. Style Modifiers: "{visual_style}" specific techniques
9. Technical Quality: Resolution, clarity specifications

Create a prompt optimized for SDXL/Flux image generation that will produce a professional storyboard frame.
"""


CAMERA_ANGLE_SUGGESTION_PROMPT = """You are a cinematographer. Suggest the best camera angle for this story moment.

Scene Description:
{scene_description}

Emotional Tone: {tone}
Genre: {genre}
Narrative Purpose: {purpose}

Consider:
1. What emotion should this shot convey?
2. What's the power dynamic between characters?
3. What information needs to be visible?
4. What's the genre's visual language?

Suggest:
- Primary camera angle (Wide Shot, Medium Shot, Close-Up, etc.)
- Reasoning for this choice
- Alternative angle if needed
- Any special camera movements or techniques
"""


# Export and Formatting Prompts

SCREENPLAY_TITLE_GENERATION = """You are a title expert. Generate 5 compelling screenplay titles based on this story.

Story Summary:
{summary}

Genre: {genre}
Theme: {theme}

Generate titles that are:
1. Memorable and intriguing
2. Genre-appropriate
3. Not too generic
4. Hint at the story without spoiling
5. Marketable

Provide 5 options with brief explanations.
"""


LOGLINE_GENERATION = """You are a logline specialist. Create a compelling one-sentence logline for this screenplay.

Story:
{story_summary}

Genre: {genre}
Protagonist: {protagonist}
Conflict: {conflict}

A good logline includes:
1. The protagonist (with adjective)
2. The inciting incident
3. The goal/quest
4. The obstacle/antagonist
5. The stakes

Make it intriguing, specific, and under 35 words.
"""


# Consistency Prompts

CHARACTER_CONSISTENCY_PROMPT = """Ensure visual consistency for this character across storyboard frames.

Character Profile:
Name: {name}
Visual Description: {visual_description}
Previous Frame Descriptions: {previous_descriptions}

Generate a consistent visual description for the next frame that maintains:
1. Physical features (height, build, hair, eyes)
2. Clothing (unless scene requires change)
3. Distinctive characteristics
4. Age appearance
5. General demeanor

This description will be used in image generation - be specific and consistent.
"""


# System Prompts for Different LLMs

SYSTEM_PROMPT_CREATIVE = """You are FrameFlow, an AI agent specialized in screenplay writing and visual storytelling. You have expert knowledge of:

- Industry-standard screenplay formatting
- Story structure and narrative theory
- Character development and dialogue
- Visual composition and cinematography
- Genre conventions and tropes

Your responses should be:
- Professional and industry-standard
- Creative but focused
- Detailed and specific
- Formatted properly for screenplays

You are helping transform story ideas into production-ready screenplays and storyboards.
"""


SYSTEM_PROMPT_TECHNICAL = """You are a technical assistant for the FrameFlow screenplay generation system. Your role is to:

- Parse and structure screenplay data
- Ensure proper formatting compliance
- Validate character and scene consistency
- Generate structured outputs for the MCP pipeline
- Handle edge cases and errors gracefully

Prioritize accuracy, consistency, and technical correctness.
"""


# Utility function to format prompts

def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with provided arguments

    Args:
        template: Prompt template string
        **kwargs: Values to insert into template

    Returns:
        Formatted prompt string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt argument: {e}")


def create_story_analysis_prompt(prompt: str, genre: str, act_structure: str) -> str:
    """Create formatted story analysis prompt"""
    return format_prompt(
        STORY_ANALYSIS_PROMPT,
        prompt=prompt,
        genre=genre,
        act_structure=act_structure
    )


def create_character_prompt(story_analysis: str, genre: str) -> str:
    """Create formatted character creation prompt"""
    return format_prompt(
        CHARACTER_CREATION_PROMPT,
        story_analysis=story_analysis,
        genre=genre
    )


def create_scene_prompt(
    scene_number: int,
    act: str,
    location: str,
    time: str,
    purpose: str,
    characters: str,
    context: str,
    dialogue_style: str,
    genre: str
) -> str:
    """Create formatted scene writing prompt"""
    return format_prompt(
        SCENE_WRITING_PROMPT,
        scene_number=scene_number,
        act=act,
        location=location,
        time=time,
        purpose=purpose,
        characters=characters,
        context=context,
        dialogue_style=dialogue_style,
        genre=genre
    )


def create_visual_prompt(
    scene_description: str,
    characters: str,
    camera_angle: str,
    visual_style: str,
    mood: str
) -> str:
    """Create formatted visual prompt for image generation"""
    return format_prompt(
        VISUAL_PROMPT_GENERATION,
        scene_description=scene_description,
        characters=characters,
        camera_angle=camera_angle,
        visual_style=visual_style,
        mood=mood
    )
