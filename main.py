from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from imports import module

blog_id = 7302333189972766248
load_dotenv()




#htmlcont =  module.genCont()
htmlcont = open('./file.html','r+')
soup = BeautifulSoup(htmlcont, 'html.parser')
post_title = soup.title.text
Labls = module.genLabels(post_title=post_title)
bannerPath = module.generate_image(post_title=post_title)
newTag = soup.new_tag('img',attrs={
    "src":bannerPath,
    "alt": post_title
})
soup.body.insert(1,newTag)
#soup.body.insert(1,f'<img src="{bannerPath}" alt="{post_title}">')

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/blogger']


def postCont(blog_id, title, content, schedule_post=False, schedule_time=None):
    """
    Posts content to a Blogger blog and optionally schedules weekly posts.

    Parameters:
        blog_id (str): The ID of the Blogger blog.
        title (str): The title of the blog post.
        content (str): The content of the blog post in HTML format.
        schedule_post (bool): Whether to schedule the post weekly. Default is False.
        schedule_time (str): Time to post if scheduling, in HH:MM (24-hour) format. Default is None.
    """


def authenticate():
    """Authenticates the user and returns API credentials."""
    
    # Load service account credentials from the environment
    creds_path = "service_account.json"

    # Write JSON from GitHub Secrets to a temporary file
    with open(creds_path, "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))

    # Authenticate with the service account
    creds = service_account.Credentials.from_service_account_file(creds_path)
    
    return creds



def create_post(service, blog_id, title, content,lbls):
    """Creates a new post on the specified Blogger blog."""
    post = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": lbls
    }
    request = service.posts().insert(blogId=blog_id, body=post)
    response = request.execute()
    print("Post title :"+title)
    print("Post created successfully:", response['url'])

# Authenticate and build the Blogger service
crds = authenticate()
print(f"crds {crds}")
service = build('blogger', 'v3', credentials=crds)
# Post immediately
post_body = str(soup.body)
post_body = post_body.replace('<body>', '')
post_body = post_body.replace('</body>', '')

print(f"Labels : {Labls}")
print(f"Banner Path : {bannerPath}")
print(f"POst body :{post_body}")
create_post(service, blog_id, post_title, post_body,Labls)


