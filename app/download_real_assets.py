import os
import time
import requests

# Target directories relative to this script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'static', 'images')
profiles_dir = os.path.join(images_dir, 'profiles')

# Create directories if they don't exist
os.makedirs(images_dir, exist_ok=True)
os.makedirs(profiles_dir, exist_ok=True)

# Wikimedia requires a unique, identifiable User-Agent to prevent 429 errors
headers = {
    "User-Agent": "CineWaveMovieHub/1.0 (contact@cinewavehub.org) python-requests/2.34"
}

assets = {
    # Posters (we will try fallbacks for these in the loop)
    os.path.join(images_dir, "dune_three_poster.jpg"): [
        "https://www.impawards.com/2026/posters/dune_part_three.jpg",
        "https://www.impawards.com/2026/posters/dune_part_three_ver1.jpg",
        "https://www.impawards.com/2026/posters/dune_three.jpg"
    ],
    os.path.join(images_dir, "spiderman_poster.jpg"): [
        "https://www.impawards.com/2026/posters/spiderman_brand_new_day.jpg",
        "https://www.impawards.com/2026/posters/spiderman_brand_new_day_ver1.jpg",
        "https://www.impawards.com/2026/posters/spiderman_four.jpg"
    ],
    os.path.join(images_dir, "doomsday_poster.jpg"): [
        "https://image.tmdb.org/t/p/w500/8HkIe2i4ScpCkcX9SzZ9IPasqWV.jpg"
    ],
    os.path.join(images_dir, "the_odyssey_poster.jpg"): [
        "https://www.impawards.com/2026/posters/the_odyssey.jpg",
        "https://www.impawards.com/2026/posters/the_odyssey_ver1.jpg",
        "https://www.impawards.com/2026/posters/odyssey.jpg"
    ],
    
    # Cast / Director real photos (Wikimedia Commons with Gage Skidmore photography)
    os.path.join(profiles_dir, "denis_villeneuve.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Denis_Villeneuve_by_Gage_Skidmore.jpg"
    ],
    os.path.join(profiles_dir, "timothee_chalamet.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/Timoth%C3%A9e_Chalamet_2021.jpg"
    ],
    os.path.join(profiles_dir, "zendaya.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/f/ff/Zendaya_-_MCM_Comic_Con_2017.jpg"
    ],
    os.path.join(profiles_dir, "florence_pugh.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/2/22/Florence_Pugh_at_the_2020_Oscars.jpg"
    ],
    
    os.path.join(profiles_dir, "destin_daniel_cretton.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/0/09/Destin_Daniel_Cretton_by_Gage_Skidmore.jpg"
    ],
    os.path.join(profiles_dir, "tom_holland.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/3/3c/Tom_Holland_by_Gage_Skidmore.jpg"
    ],
    os.path.join(profiles_dir, "jon_bernthal.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Jon_Bernthal_by_Gage_Skidmore_2.jpg"
    ],
    
    os.path.join(profiles_dir, "russo_brothers.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/The_Russo_Brothers_by_Gage_Skidmore.jpg"
    ],
    os.path.join(profiles_dir, "robert_downey_jr.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Robert_Downey%2C_Jr._SDCC_2014_2_%28cropped%29.jpg"
    ],
    os.path.join(profiles_dir, "pedro_pascal.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/c/c5/Pedro_Pascal_by_Gage_Skidmore.jpg"
    ],
    
    os.path.join(profiles_dir, "christopher_nolan.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/9/95/Christopher_Nolan_Cannes_2018.jpg"
    ],
    os.path.join(profiles_dir, "matt_damon.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Matt_Damon_at_the_2015_Jianbing_Event_%28cropped%29.jpg"
    ],
    os.path.join(profiles_dir, "anne_hathaway.jpg"): [
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/Anne_Hathaway_at_the_2018_Golden_Globe_Awards.jpg"
    ],
    os.path.join(profiles_dir, "robert_pattinson.jpg"): [
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

