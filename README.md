📖 AI Storybook Generator

An AI-powered application that generates short illustrated storybooks from a simple idea.
The system uses lightweight text and image models optimized for low-end GPUs (4GB VRAM) to generate scene-by-scene narratives and illustrations, and compiles them into a PDF storybook.

🎯 Aim

To create an AI-based story generator that can automatically expand a simple idea into a multi-scene illustrated storybook, suitable for kids, teens, or adults.

📝 Problem Statement

Storytelling is a powerful medium for education and entertainment, but many people lack the time or resources to write and illustrate stories.
This project solves the problem by enabling anyone to quickly generate custom storybooks with both text and visuals.

📌 Scope of the Solution

Takes a story idea as input.

Expands the idea into multiple scenes with coherent text.

Generates a unique illustration for each scene.

Compiles the scenes and images into a PDF storybook.

Works on low-end GPUs (4GB VRAM) with reduced image sizes and smaller text models.

⚙️ Required Components
🖥 Software

Python 3.9+

Transformers (Hugging Face)

Diffusers

Torch

FPDF

Install requirements with:

pip install torch transformers diffusers fpdf

💻 Hardware

CPU: Ryzen 5 (or equivalent)

GPU: NVIDIA RTX 3050/3060 or similar (4GB VRAM supported)

RAM: 8GB minimum

🛠 IDE

VS Code / PyCharm / Jupyter Notebook

🚀 Usage Instructions

Clone or download this repository.

Install dependencies:

pip install -r requirements.txt


Run the program:

python app.py


Provide the inputs interactively when prompted:

Story idea

Genre (fantasy/sci-fi/mystery/comedy)

Tone (dark/lighthearted/epic)

Audience (kids/teens/adults)

Number of scenes

Art style (cartoon/anime/realistic/digital painting)

After generation, check the output file:

storybook.pdf

📌 Special Note on Models

⚠️ Due to system restrictions (4GB GPU VRAM), we used lightweight models:

Text: distilgpt2 (or EleutherAI/gpt-neo-125M if available)

Images: stabilityai/stable-diffusion-2-base (small resolution 256×256)

👉 If you have access to higher-end hardware, we recommend updating to:

Text Models: mistralai/Mistral-7B-Instruct, Llama-2-7B, or GPT-4 APIs

Image Models: runwayml/stable-diffusion-v1-5 or SDXL for better illustrations

Update the code accordingly for higher performance and quality.

demo_video : https://drive.google.com/file/d/1FueEQJeCP8AnYzHAqqAQKi2BccurELvG/view?usp=drivesdk


## 👥 Collaborators

* **Dharun A /dharun-anandhan** → *Team Lead, Backend & Model Integration*
* **\[Saravanakumar B / sarvx-gh]** → *Frontend & UI Development*
* **\[Rahul Ramana V / rahul-ramana]** → *Model Optimization & Testing*

📂 Project Structure
📦 AI-Storybook-Generator
 ┣ 📜 app.py              # Main script (interactive generator)
 ┣ 📜 requirements.txt    # Python dependencies
 ┗ 📜 README.md           # Project documentation

✅ Results

Generates scene-by-scene text with context awareness.

Produces unique illustrations for each scene.

Compiles everything into a PDF storybook automatically.
