from diffusers import StableDiffusionPipeline
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import torch
import time

def generate_image(prompt, model_id):
    model_id = model_id
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cpu")

    image = pipe(prompt).images[0]
    return image


def add_text(image, top_text, bottom_text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Fonts/OpenSansEmoji.ttf', 20, encoding='unic')
    draw.text((50, 50),top_text,(000,000,000),font=font)
    draw.text((125, 450),bottom_text,(000,000,000),font=font)
    
    return image
