from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import json
from bs4 import BeautifulSoup
from google.auth import credentials
from mods import module

blog_id = 7302333189972766248




htmlcont =  module.genCont()
#htmlcont = open('./file.html','r+')
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
    """Authenticates the user and returns API credentials."""
    creds = None
    
    # Check if token.json exists
    if os.path.exists('token.json'):
        try:
            # Load credentials from token.json
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except (json.JSONDecodeError, ValueError):
            print("token.json is corrupted or invalid. Regenerating credentials...")
    
    # If no valid credentials, run the OAuth flow
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json',
                scopes=SCOPES
            )
            # Set redirect URI
            flow.redirect_uri = "https://ideal-succotash-7gg7vg9jr5gcrjpr.github.dev/oauth2callback"
            
            # Generate the authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline', prompt='consent'
            )
            print('Please go to this URL to authorize the app: {}'.format(auth_url))
            
            # Manually fetch the authorization code
            code = input('Enter the authorization code: ')
            
            # Exchange the authorization code for tokens
            flow.fetch_token(code=code)
            creds = flow.credentials
            # Save credentials to token.json
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    
    return creds

  
            
def get_authenticated_service():
  """
  Gets authenticated service using refresh token.

  Returns:
    The authenticated Blogger API service object.
  """
  try:
    with open('token.json', 'r') as token_file:
      creds_data = json.load(token_file)
      creds = credentials.Credentials(**creds_data, scopes=SCOPES)

    if not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        raise Exception('Invalid credentials. Please re-authenticate.')

    return build('blogger', 'v3', credentials=creds)

  except FileNotFoundError:
    print("Error: 'token.json' file not found.")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

# Example usage:


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
#print(f"crds {crds}")
sevice = build('blogger', 'v3', credentials=crds)
#sevice = get_authenticated_service()
# Post immediately
post_body = str(soup.body)
post_body = post_body.replace('<body>', '')
post_body = post_body.replace('</body>', '')

print(f"Labels : {Labls}")
#print(f"Banner Path : {bannerPath}")
#print(f"POst body :{post_body}")
create_post(sevice, blog_id, post_title, post_body,Labls)


