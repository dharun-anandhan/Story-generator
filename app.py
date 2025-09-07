from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
import asyncio
from fpdf import FPDF

# Initialize text generation on CPU with distilgpt2 or GPT-Neo 125M if available
text_generator = pipeline(
    "text-generation",
    model="distilgpt2",  # Swap for "EleutherAI/gpt-neo-125M" if possible
    device=-1,
    max_length=300,
    max_new_tokens=200,  # Reduced to ensure we get clean output
    do_sample=True,
    temperature=0.95,
    top_p=0.9,
    pad_token_id=50256  # Add pad token to avoid warnings
)

# Initialize image generation on GPU with smaller resolution for 4GB VRAM
device = "cuda" if torch.cuda.is_available() else "cpu"
image_generator = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-base"
).to(device)

def scene_to_prompt(scene_text, style):
    # Take only first 100 characters to avoid overly long prompts
    clean_text = scene_text[:100].strip()
    return f"{clean_text}. Illustration, {style} style."

async def generate_scene(scene_number, previous_text, genre, audience, tone, story_idea, art_style):
    # Compose prompt with scene-specific instructions and prior scene context
    prompt = (
        f"Write Scene {scene_number} of a {genre} story for {audience} with {tone} tone.\n"
        f"Story idea: {story_idea}\n"
        f"Previous scene summary: {previous_text}\n"
        f"Scene {scene_number}:"
    )
    
    print(f"Generating text for Scene {scene_number}...")
    
    # Generate story text on CPU
    output = text_generator(prompt, return_full_text=False)[0]["generated_text"]
    
    # Clean up the generated text
    scene_text = output.strip()
    
    # Remove any remaining prompt artifacts
    if scene_text.startswith("Scene"):
        # Find the first sentence or paragraph after "Scene X:"
        lines = scene_text.split('\n')
        clean_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith("Scene") and not line.strip().startswith("Write"):
                clean_lines.append(line.strip())
        scene_text = ' '.join(clean_lines) if clean_lines else scene_text
    
    # Ensure we have actual content
    if len(scene_text.strip()) < 20:
        scene_text = f"In this scene of our {genre} story, the adventure continues with new developments and characters facing challenges."
    
    print(f"Generated text: {scene_text[:100]}...")
    
    # Generate image on GPU with smaller resolution
    print(f"Generating image for Scene {scene_number}...")
    img_prompt = scene_to_prompt(scene_text, art_style)
    print(f"Image prompt: {img_prompt}")
    
    try:
        image = image_generator(img_prompt, height=256, width=256, num_inference_steps=20).images[0]
        img_path = f"scene_{scene_number}.png"
        image.save(img_path)
        print(f"Saved image: {img_path}")
    except Exception as e:
        print(f"Error generating image: {e}")
        img_path = None
    
    print(f"Completed Scene {scene_number}")
    
    # Return scene text and image path
    return scene_text, img_path

async def main():
    print("=== AI Storybook Generator ===")
    story_idea = input("Enter your story idea: ")
    genre = input("Genre (fantasy/sci-fi/mystery/comedy): ")
    tone = input("Tone (dark/lighthearted/epic): ")
    audience = input("Audience (kids/teens/adults): ")
    num_scenes = int(input("How many scenes (e.g. 4): "))
    art_style = input("Art style (realistic/cartoon/anime/watercolor/digital painting): ")
    
    previous_text = "This is the beginning of the story"
    scenes_results = []
    
    print(f"\nGenerating {num_scenes} scenes...")
    
    for i in range(1, num_scenes + 1):
        scene_text, img_path = await generate_scene(
            i, previous_text, genre, audience, tone, story_idea, art_style
        )
        # Use only the last 100 characters as context to avoid overwhelming the next prompt
        previous_text = scene_text[-100:] if len(scene_text) > 100 else scene_text
        scenes_results.append((scene_text, img_path))
        print(f"Scene {i} complete\n")
    
    # Export results to PDF picture book
    print("Creating PDF...")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Add title page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AI Generated Storybook", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Story: {story_idea}")
    pdf.multi_cell(0, 10, f"Genre: {genre} | Tone: {tone} | Audience: {audience}")
    pdf.ln(10)
    
    # Add scenes
    for idx, (text, img_path) in enumerate(scenes_results, 1):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Scene {idx}", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, text)
        pdf.ln(10)
        
        if img_path:
            try:
                pdf.image(img_path, x=45, w=120)
            except Exception as e:
                print(f"Error adding image {img_path} to PDF: {e}")
    
    pdf.output("storybook.pdf")
    print("Storybook generated successfully: storybook.pdf")

if __name__ == "__main__":
    asyncio.run(main())