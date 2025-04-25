import google.generativeai as genai
import os
from dotenv import load_dotenv
import string 
import random
import requests
load_dotenv()
myk = os.getenv('API_KEY')
genai.configure(api_key='AIzaSyAMd-EzTIfn7rh0juAwBFJk3LR6pYOUA6E')

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
    print('AI_KEY : '+ token)
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
    prompt = '''
You’re a tech blogger using Beautiful Jekyll by deanatalli. Generate one fresh, original blog post in plain Markdown (no fenced code blocks), with these rules:

1. Title  
   - On the very first line, output only the post title (plain text, no commas/slashes/colons).

2. Length & Markup  
   - At least 1,500 words.  
   - Use `{% highlight <language> linenos %}` … `{% endhighlight %}` for code.  
   - Don’t wrap the whole thing in a code-block.

3. Topic Selection (pick exactly one)  
   - 🔲 **Emerging AI & ML** (new open-source models, fine-tuning, ethical implications)  
   - 🔲 **JavaScript Frameworks** (React/Next.js tips, Svelte, real-world case studies)  
   - 🔲 **Cloud & DevOps** (Kubernetes patterns, serverless best practices, CI/CD pipelines)  
   - 🔲 **Mobile Development** (Flutter, React Native, PWA tricks)  
   - 🔲 **Cybersecurity** (hands-on pentesting, DevSecOps, secure coding)  
   - 🔲 **Data Science & Visualization** (Pandas alternatives, interactive dashboards)  
   - 🔲 **IoT & Hardware Hacks** (Raspberry Pi, Arduino projects)  

   _Only one in every three posts may be Python automation._  

4. Structure  
   - **Introduction**: Hook with a real problem or question.  
   - **Sections**: Use `##`/`###` headings.  
   - **Code Snippets**: Ready-to-copy with `{% highlight %}`.  
   - **Internal Links**: When you refer to something you’ve covered on GTec, link to it (e.g. `[See our React hooks guide](https://gtec0.github.io/2025-04-20-hooks-react-guide/)`).  

5. SEO & Engagement  
   - Sprinkle 2–3 relevant keywords in headings/body.  
   - Vary verbs: “Exploring,” “Building,” “Automating,” “Understanding.”  
   - End with a **Conclusion + Call to Action**.

6. Originality  
   - Never repeat an existing GTec topic.  
   - Bring fresh examples or data.

Produce the Markdown output directly.  
    '''
    
    resp = model.generate_content(prompt)
    return resp.text



def genLabels(post_title):
    lblPrompt = f'Generate me labels for post with title {post_title} and return me a list,do not put it on code blocks ,return it like this example : Label1,Label2,Labeln . and it should not be greater than 5'
    model = genai.GenerativeModel('gemini-1.5-flash')
    labels = model.generate_content(lblPrompt)
    return labels.text


