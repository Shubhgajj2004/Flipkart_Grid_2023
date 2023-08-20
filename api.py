import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

def scrape_images(query):
    base_url = "https://www.xyzabc.com" #Base URL from which letest trending fashion images should be webscraped
    search_url = f"{base_url}/search/pins/?q={query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Your User Agent"  # Set your user agent here
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        image_tags = soup.find_all("img", class_="hCL kVc")
        
        image_links = [img["src"] for img in image_tags]
        print(image_links)
        return image_links[:10]  # Return top 10 image links
    else:
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        image_links = scrape_images(query)
        download_images(image_links)
        
    return render_template("index.html")

def download_images(image_links):
    folder_path = "images"
    os.makedirs(folder_path, exist_ok=True)
    
    for index, link in enumerate(image_links):
        response = requests.get(link)
        if response.status_code == 200:
            image_path = os.path.join(folder_path, f"image{index+1}.jpg")
            with open(image_path, "wb") as f:
                f.write(response.content)

if __name__ == "__main__":
    app.run(debug=True)