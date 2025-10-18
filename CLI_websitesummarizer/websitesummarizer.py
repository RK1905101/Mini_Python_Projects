import time
import sys
from dotenv import load_dotenv
import os
import google.generativeai as genai
from IPython.display import Markdown, display,clear_output
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url=""
msg=""
# Step 1: Fetch the webpage
def fetchingsoup(url1):
     url=url1
     headers = {"User-Agent": "Mozilla/5.0"}
     response = requests.get(url, headers=headers)
     soup = BeautifulSoup(response.text, 'html.parser')
     return soup,url
     
def textfetching(url1):
    soup,url=fetchingsoup(url1)
    msg=soup.get_text(separator=' ',strip=True)
    return msg,url
load_dotenv()  # This loads the .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)
model=genai.GenerativeModel('gemini-2.0-flash')

sysprompt="Generate a beautiful summary of the given site in markdown with proper heading in structured format."
def summarygen(msg):
    try:
        response1=model.generate_content(sysprompt+" "+msg)
        return response1.text
    except Exception as e:
        return f"Error:{str(e)}"

os.makedirs("summaries", exist_ok=True)

def writer(text,delay=0.02):
    displayed_text = ""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


print("Hello I am your chatbot. To exit write Quit")
while True:
    url1=input("Enter URL or quit to exit")
    if(url1.lower()=="quit"):
        print("thankyou for visiting")
        break
    msg, url=textfetching(url1)
    summary = summarygen(msg)
    writer(summary)
    domain = urlparse(url).netloc.replace('.', '_')
    filename = f"summaries/{domain}_summary.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(sysprompt+" for the site "+domain+"\n"+summary)
    print("✅ Summary saved to 'summary.md'")




