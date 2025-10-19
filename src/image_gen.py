from diffusers import StableDiffusionPipeline
from PIL import Image, ImageFont, ImageDraw
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
import torch
import time
import os
import config
import tempfile




def generate_image(prompt, model_id):
    model_id = model_id
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cpu")

    image = pipe(prompt).images[0]
    return image

# Initialize Vertex AI with your project
def init_vertex_ai():
    """Initialize Vertex AI with authentication."""
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION')
    print(location)
    # # This will use GOOGLE_APPLICATION_CREDENTIALS environment variable
    vertexai.init(project=project_id, location=location)

def generate_image_vertexAI(prompt, model_id="imagen-3.0-generate-001", max_retries=5, retry_delay=5):
    model = ImageGenerationModel.from_pretrained(model_id)
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}: Generating image...")
            generated_image = model.generate_images(prompt=prompt)
            print("Image generated successfully!")
        
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                generated_image[0].save(tmp.name)
                pil_image = Image.open(tmp.name)
                pil_image.load()  # Load image data before file is deleted
            
            print("Image generated successfully!")
            return pil_image
            
        except Exception as e:
            print(f"ERROR on attempt {attempt + 1}: {e}")
            print(f"Error type: {type(e).__name__}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed after {max_retries} attempts")
                import traceback
                traceback.print_exc()
                return None

def add_text(image, text, x_axis=50, y_axis=50, font_size=16, 
                         text_color=(0, 0, 0), border_color=(255, 255, 255), 
                         border_width=2):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Fonts/OpenSansEmoji.ttf', font_size, encoding='unic')
    draw.text((x_axis, y_axis), text, fill=text_color, font=font, stroke_width=border_width, stroke_fill=border_color)
    return image

