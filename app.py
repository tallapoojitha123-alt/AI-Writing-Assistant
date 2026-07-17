# ==========================================================
# AI BLOG GENERATOR (GEMINI + GRADIO)
# SAFE VERSION FOR GITHUB & DEPLOYMENT
# ==========================================================

import os
import gradio as gr
from google import genai

# ==========================================================
# LOAD API KEY FROM ENVIRONMENT
# ==========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not set!")

client = genai.Client(api_key=API_KEY)

# ==========================================================
# BLOG GENERATION FUNCTION
# ==========================================================

def generate_blog(topic, audience, tone, language, words):

    if not topic.strip():
        return "❌ Please enter a topic."

    if not API_KEY:
        return "❌ API Key not found. Set GEMINI_API_KEY."

    prompt = f"""
    Write a {words}-word blog.

    Topic: {topic}
    Audience: {audience}
    Tone: {tone}
    Language: {language}

    Include:
    - Title
    - Introduction
    - Key points
    - Examples
    - Disadvantages
    - Conclusion
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==========================================================
# GRADIO UI
# ==========================================================

demo = gr.Interface(
    fn=generate_blog,
    inputs=[
        gr.Textbox(label="Topic", placeholder="Enter blog topic..."),
        gr.Textbox(label="Audience", placeholder="Students, Developers, etc."),
        gr.Dropdown(
            ["Professional", "Casual", "Funny", "Technical", "Inspirational"],
            label="Tone",
        ),
        gr.Dropdown(
            ["English", "Telugu", "Hindi", "Tamil"],
            label="Language",
            value="English"
        ),
        gr.Slider(200, 1000, value=500, step=50, label="Word Count")
    ],
    outputs=gr.Markdown(label="Generated Blog"),
    title="🤖 AI Blog Generator (Gemini)",
    description="Generate blogs using Google's Gemini AI",
)

# ==========================================================
# LAUNCH APP
# ==========================================================

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
