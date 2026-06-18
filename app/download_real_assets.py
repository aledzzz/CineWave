import os
import time
import requests

# Create directories if they don't exist
os.makedirs(r"G:\Antigravity Projects\agy\app\static\images", exist_ok=True)
os.makedirs(r"G:\Antigravity Projects\agy\app\static\images\profiles", exist_ok=True)

# Wikimedia requires a unique, identifiable User-Agent to prevent 429 errors
headers = {
    "User-Agent": "CineWaveMovieHub/1.0 (contact@cinewavehub.org) python-requests/2.34"
}

assets = {
    # Posters (we will try fallbacks for these in the loop)
    r"G:\Antigravity Projects\agy\app\static\images\dune_three_poster.jpg": [
        "https://www.impawards.com/2026/posters/dune_part_three.jpg",
        "https://www.impawards.com/2026/posters/dune_part_three_ver1.jpg",
        "https://www.impawards.com/2026/posters/dune_three.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\spiderman_poster.jpg": [
        "https://www.impawards.com/2026/posters/spiderman_brand_new_day.jpg",
        "https://www.impawards.com/2026/posters/spiderman_brand_new_day_ver1.jpg",
        "https://www.impawards.com/2026/posters/spiderman_four.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\doomsday_poster.jpg": [
        "https://image.tmdb.org/t/p/w500/8HkIe2i4ScpCkcX9SzZ9IPasqWV.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\the_odyssey_poster.jpg": [
        "https://www.impawards.com/2026/posters/the_odyssey.jpg",
        "https://www.impawards.com/2026/posters/the_odyssey_ver1.jpg",
        "https://www.impawards.com/2026/posters/odyssey.jpg"
    ],
    
    # Cast / Director real photos (Wikimedia Commons with Gage Skidmore photography)
    r"G:\Antigravity Projects\agy\app\static\images\profiles\denis_villeneuve.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Denis_Villeneuve_by_Gage_Skidmore.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\timothee_chalamet.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/Timoth%C3%A9e_Chalamet_2021.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\zendaya.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/f/ff/Zendaya_-_MCM_Comic_Con_2017.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\florence_pugh.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/2/22/Florence_Pugh_at_the_2020_Oscars.jpg"
    ],
    
    r"G:\Antigravity Projects\agy\app\static\images\profiles\destin_daniel_cretton.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/0/09/Destin_Daniel_Cretton_by_Gage_Skidmore.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\tom_holland.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/3/3c/Tom_Holland_by_Gage_Skidmore.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\jon_bernthal.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Jon_Bernthal_by_Gage_Skidmore_2.jpg"
    ],
    
    r"G:\Antigravity Projects\agy\app\static\images\profiles\russo_brothers.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/The_Russo_Brothers_by_Gage_Skidmore.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\robert_downey_jr.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Robert_Downey%2C_Jr._SDCC_2014_2_%28cropped%29.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\pedro_pascal.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/c/c5/Pedro_Pascal_by_Gage_Skidmore.jpg"
    ],
    
    r"G:\Antigravity Projects\agy\app\static\images\profiles\christopher_nolan.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/9/95/Christopher_Nolan_Cannes_2018.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\matt_damon.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Matt_Damon_at_the_2015_Jianbing_Event_%28cropped%29.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\anne_hathaway.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/Anne_Hathaway_at_the_2018_Golden_Globe_Awards.jpg"
    ],
    r"G:\Antigravity Projects\agy\app\static\images\profiles\robert_pattinson.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/3/36/Robert_Pattinson_Go_Campaign_2019_%28cropped%29.jpg"
    ]
}

for path, urls in assets.items():
    success = False
    for url in urls:
        try:
            print(f"Trying to download: {url}")
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
        
        # Short pause between failures to be nice to servers
        time.sleep(0.5)
        
    if not success:
        print(f"ERROR: Failed all URLs for {os.path.basename(path)}")
        
    # Rate limit prevention (especially for Wikimedia)
    time.sleep(1.2)

