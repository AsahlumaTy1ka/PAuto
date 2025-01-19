from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
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
bannerPath = ""
#bannerPath = module.generate_image(post_title=post_title)
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
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    creds = None

    # Check if token exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token_file:
            creds = pickle.load(token_file)

    # Authenticate if credentials are not valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_console()  # Use console-based authentication

        # Save the credentials for reuse
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)
    
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
#print(f"Banner Path : {bannerPath}")
#print(f"POst body :{post_body}")
create_post(service, blog_id, post_title, post_body,Labls)


