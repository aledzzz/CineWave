import os
import re
import requests

# Target profiles directory
profiles_dir = r"G:\Antigravity Projects\agy\app\static\images\profiles"
os.makedirs(profiles_dir, exist_ok=True)

headers = {
    "User-Agent": "CineWaveMovieHub/1.0 (contact@cinewavehub.org) python-requests/2.34"
}

# Mapping of file names to TMDB IDs
tmdb_people = {
    "denis_villeneuve.jpg": 13742,
    "timothee_chalamet.jpg": 1190668,
    "zendaya.jpg": 505710,
    "florence_pugh.jpg": 1373737,
    "destin_daniel_cretton.jpg": 1038084,
    "jon_bernthal.jpg": 46841,
    "russo_brothers.jpg": 19273,       # Anthony Russo
    "robert_downey_jr.jpg": 3223,
    "matt_damon.jpg": 1892,
    "anne_hathaway.jpg": 1810,
    "robert_pattinson.jpg": 11288
}

for filename, tmdb_id in tmdb_people.items():
    url = f"https://www.themoviedb.org/person/{tmdb_id}"
    try:
        print(f"Fetching TMDB page for ID {tmdb_id} ({filename})...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Look for og:image meta tag content
            html = response.text
            match = re.search(r'<meta[^>]*property="og:image"[^>]*content="(https://image\.tmdb\.org/t/p/[^"]+)"', html)
            if not match:
                # Try search with single quotes or different attribute order
                match = re.search(r'content="(https://image\.tmdb\.org/t/p/[^"]+)"[^>]*property="og:image"', html)
                
            if match:
                image_url = match.group(1)
                # We can request w500 or keep it as is
                # w600_and_h900_bestv2 -> w300
                image_url = image_url.replace("w600_and_h900_bestv2", "w300")
                
                print(f"Found image URL: {image_url}")
                img_res = requests.get(image_url, headers=headers, timeout=15)
                if img_res.status_code == 200:
                    dest_path = os.path.join(profiles_dir, filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_res.content)
                    print(f"Successfully saved to {dest_path}")
                else:
                    print(f"Failed to download image from {image_url} (status {img_res.status_code})")
            else:
                print(f"Could not find og:image in HTML for ID {tmdb_id}")
        else:
            print(f"Failed to fetch TMDb page (status {response.status_code}) for ID {tmdb_id}")
    except Exception as e:
        print(f"Error processing ID {tmdb_id}: {e}")
