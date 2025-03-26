from flask import Flask, request, jsonify
import torch
from diffusers import StableDiffusionPipeline
import os
from PIL import Image
import requests

app = Flask(__name__)

# Load Stable Diffusion Model (Optimized for Railway)
model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
model.to("cuda" if torch.cuda.is_available() else "cpu")

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "A beautiful landscape")

    # Generate Image
    image = model(prompt).images[0]

    # Save Image Locally
    filename = "generated_image.png"
    image.save(filename)

    # Upload Image to Imgur (or Cloud Storage)
    public_url = upload_to_imgur(filename)

    return jsonify({"image_url": public_url})

def upload_to_imgur(filepath):
    """Uploads image to Imgur and returns a public URL."""
    headers = {"Authorization": "Client-ID YOUR_IMGUR_CLIENT_ID"}
    with open(filepath, "rb") as file:
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": file})
        return response.json()["data"]["link"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
