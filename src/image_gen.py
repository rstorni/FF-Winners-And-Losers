from diffusers import StableDiffusionPipeline
from PIL import Image, ImageFont, ImageDraw
import torch
import time

def generate_image(prompt, model_id):
    model_id = model_id
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cpu")

    image = pipe(prompt).images[0]
    return image

def add_text(image, text, x_axis=50, y_axis=50, font_size=16, 
                         text_color=(0, 0, 0), border_color=(255, 255, 255), 
                         border_width=2):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Fonts/OpenSansEmoji.ttf', font_size, encoding='unic')
    draw.text((x_axis, y_axis), text, fill=text_color, font=font, stroke_width=border_width, stroke_fill=border_color)
    return image

