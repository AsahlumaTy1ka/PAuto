import google.generativeai as genai
import os
import string 
import random
import requests
myk = os.getenv('API_KEY')
genai.configure(api_key=myk)

# Generate an image
def generate_image(post_title,guidance_scale=4, height=512, width=512, max_sequence_length=256, num_images=1, num_inference_steps=15, seed=1):
    """
    Generates an image using the Mystic AI pipeline.

    Args:
        prompt (str): The text prompt for image generation.
        token (str): The API token for authorization.
        guidance_scale (int): Guidance scale for image generation. Default is 4.
        height (int): Height of the generated image. Default is 512.
        width (int): Width of the generated image. Default is 512.
        max_sequence_length (int): Maximum sequence length for generation. Default is 256.
        num_images (int): Number of images to generate. Default is 1.
        num_inference_steps (int): Number of inference steps. Default is 15.
        seed (int): Seed for deterministic output. Default is 1.

    Returns:
        dict: The JSON response from the API.
    """
    output_path = './banners/'+str(''.join(random.choices(string.ascii_letters,k=7)))+ '.jpg'
    token = os.getenv("AI_AKEY")
    prompt = f"A blog post banner with title '{post_title}'"
    url = "https://www.mystic.ai/v4/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "pipeline": "black-forest-labs/flux1-dev:v1",
        "inputs": [
            {
                "type": "string",
                "value": prompt
            },
            {
                "type": "dictionary",
                "value": {
                    "guidance_scale": guidance_scale,
                    "height": height,
                    "max_sequence_length": max_sequence_length,
                    "num_images_per_prompt": num_images,
                    "num_inference_steps": num_inference_steps,
                    "seed": seed,
                    "width": width
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        r = response.json()
        imgUrl = r['outputs'][0]['value'][0]['file']['url']
        img_data = requests.get(imgUrl).content
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
        return output_path
        #return response.json()
    else:
        return {"error": response.status_code, "message": response.text}



def genCont():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = '''Generate me a blog post about a random coding tutorial people or coders usually search about,in html format and make it as long as possible and do not take this as a chat plus dont put the html in a codeblock just return plain html and use <pre style="background: rgb(238, 238, 238); border-radius: 10px; border: 1px solid rgb(221, 221, 221); font-family: 'Courier New', Courier, monospace; padding: 12px;"></pre> as codeblocks instead of code tags'''
    resp = model.generate_content(prompt)
    return resp.text



def genLabels(post_title):
    lblPrompt = f'Generate me labels for post with title {post_title} and return me a list,do not put it on code blocks ,return it like this example : Label1,Label2,Labeln . and it should not be greater than 5'
    model = genai.GenerativeModel('gemini-1.5-flash')
    labels = model.generate_content(lblPrompt)
    return labels.text


