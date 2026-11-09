import asyncio
import base64
import os
import requests
from random import randint
from time import sleep
from dotenv import get_key
from PIL import Image

# Ensure Data folder exists
os.makedirs("Data", exist_ok=True)

def open_images(prompt):  
    folder_path = "Data"  # Ensure directory exists
    prompt = prompt.replace(" ", "_")  # Format prompt
    
    # Generate filenames  
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]  

    for jpg_file in Files:  
        image_path = os.path.join(folder_path, jpg_file)  
        try:  
            img = Image.open(image_path)  
            print(f"Opening image: {image_path}")  
            img.show()
            sleep(1)  # Pause before showing next image  
        except IOError:  
            print(f"Unable to open {image_path}")  

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"  
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}  

# Async function to send a query to the Hugging Face API  
async def query(payload):  
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)  
    json_data = response.json()  # Convert response to JSON  

    if "image" in json_data:
        return base64.b64decode(json_data["image"])  # Decode Base64
    else:
        print("Error:", json_data)
        return None  

# Async function to generate images  
async def generate_images(prompt: str):  
    tasks = []  

    for _ in range(4):  
        payload = {  
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",  
        }  
        tasks.append(asyncio.create_task(query(payload)))  

    image_bytes_list = await asyncio.gather(*tasks)  

    for i, image_bytes in enumerate(image_bytes_list):  
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
            with open(file_path, "wb") as f:  
                f.write(image_bytes)  

def GenerateImages(prompt: str):  
    asyncio.run(generate_images(prompt))  # Run async image generation  
    open_images(prompt)  # Open generated images  

# Main loop to monitor image generation requests  
while True:  
    try:  
        with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "r") as f:  
            Data = f.read().strip()

        prompt, Status = Data.split(",")

        if Status.strip().lower() == "true":  
            print("Generating Images ...")  
            GenerateImages(prompt.strip())  

            # Reset status
            with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as f:  
                f.write("False,False")  
            break  
        else:  
            sleep(1)  

    except Exception as e:
        print("Error:", e)
        sleep(1)  
