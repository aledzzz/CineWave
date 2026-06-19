import os
import time
import requests

# Target directories relative to this script
base_dir = os.path.dirname(os.path.abspath(__file__))
profiles_dir = os.path.join(base_dir, 'static', 'images', 'profiles')
posters_dir = os.path.join(base_dir, 'static', 'images')
os.makedirs(profiles_dir, exist_ok=True)
os.makedirs(posters_dir, exist_ok=True)

headers = {
    "User-Agent": "CineWaveMovieHub/1.0 (contact@cinewavehub.org) python-requests/2.34"
}

# New posters to download
posters = {
    os.path.join(posters_dir, "toy_story_five_poster.jpg"): [
        "https://www.impawards.com/2026/posters/toy_story_five.jpg",
        "https://www.impawards.com/2026/posters/toy_story_five_ver1.jpg"
    ],
    os.path.join(posters_dir, "supergirl_poster.jpg"): [
        "https://www.impawards.com/2026/posters/supergirl.jpg",
        "https://www.impawards.com/2026/posters/supergirl_ver1.jpg"
    ]
}

# New cast / director Wikipedia pages
wiki_people = {
    "andrew_stanton.jpg": "Andrew Stanton",
    "tom_hanks.jpg": "Tom Hanks",
    "tim_allen.jpg": "Tim Allen",
    "joan_cusack.jpg": "Joan Cusack",
    "craig_gillespie.jpg": "Craig Gillespie",
    "milly_alcock.jpg": "Milly Alcock",
    "eve_ridley.jpg": "Eve Ridley",
    "matthias_schoenaerts.jpg": "Matthias Schoenaerts"
}

# 1. Download Posters
for path, urls in posters.items():
    success = False
    for url in urls:
        try:
            print(f"Trying to download poster: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                with open(path, "wb") as f:
                    f.write(response.content)
                print(f"Success: Saved to {os.path.basename(path)}")
                success = True
                break
            else:
                print(f"HTTP Status {response.status_code} for {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        time.sleep(0.5)
    if not success:
        print(f"ERROR: Failed to download poster for {os.path.basename(path)}")
    time.sleep(1.0)

# 2. Download Portraits
for filename, title in wiki_people.items():
    print(f"Querying Wikipedia PageImages API for: {title}...")
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=pageimages&format=json&pithumbsize=300"
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            page_id = list(pages.keys())[0]
            page_info = pages[page_id]
            
            if "thumbnail" in page_info:
                image_url = page_info["thumbnail"]["source"]
                print(f"Found image: {image_url}")
                
                # Download the image
                img_res = requests.get(image_url, headers=headers, timeout=15)
                if img_res.status_code == 200:
                    dest_path = os.path.join(profiles_dir, filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_res.content)
                    print(f"Success: Saved to {dest_path}")
                else:
                    print(f"Failed to download image (status {img_res.status_code})")
            else:
                print(f"No thumbnail image found for page title: {title}")
        else:
            print(f"Wikipedia API request failed (status {response.status_code})")
    except Exception as e:
        print(f"Error querying Wikipedia for {title}: {e}")
    time.sleep(1.0)
