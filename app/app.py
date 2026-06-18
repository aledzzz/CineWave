import os
import json
import re
import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), 'watchlist.json')

# Rich featured movies database for the requested upcoming blockbusters
FEATURED_MOVIES = [
    {
        "id": "toy-story-5",
        "title": "Toy Story 5",
        "release_date": "June 19, 2026",
        "director": {
            "name": "Andrew Stanton",
            "image": "/static/images/profiles/andrew_stanton.jpg"
        },
        "cast": [
            {
                "name": "Tom Hanks",
                "role": "Woody (voice)",
                "image": "/static/images/profiles/tom_hanks.jpg"
            },
            {
                "name": "Tim Allen",
                "role": "Buzz Lightyear (voice)",
                "image": "/static/images/profiles/tim_allen.jpg"
            },
            {
                "name": "Joan Cusack",
                "role": "Jessie (voice)",
                "image": "/static/images/profiles/joan_cusack.jpg"
            }
        ],
        "synopsis": "Woody, Buzz, and the rest of the gang encounter a brand-new threat to playtime when Bonnie gets obsessed with a high-tech tablet device named Lilypad. Directed by Andrew Stanton.",
        "poster": "/static/images/toy_story_five_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/c51ND9Hdbw0",
        "is_featured": True
    },
    {
        "id": "supergirl-wot",
        "title": "Supergirl: Woman of Tomorrow",
        "release_date": "June 26, 2026",
        "director": {
            "name": "Craig Gillespie",
            "image": "/static/images/profiles/craig_gillespie.jpg"
        },
        "cast": [
            {
                "name": "Milly Alcock",
                "role": "Kara Zor-El / Supergirl",
                "image": "/static/images/profiles/milly_alcock.jpg"
            },
            {
                "name": "Eve Ridley",
                "role": "Ruthye Marye Knoll",
                "image": "/static/images/profiles/eve_ridley.jpg"
            },
            {
                "name": "Matthias Schoenaerts",
                "role": "Krem of the Yellow Hills",
                "image": "/static/images/profiles/matthias_schoenaerts.jpg"
            }
        ],
        "synopsis": "Based on the celebrated DC Comics run, the film follows Supergirl as she travels across the stars alongside a young alien girl named Ruthye seeking justice for the destruction of her world.",
        "poster": "/static/images/supergirl_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/s1-pfiVMKAs",
        "is_featured": True
    },
    {
        "id": "the-odyssey",
        "title": "The Odyssey",
        "release_date": "July 17, 2026",
        "director": {
            "name": "Christopher Nolan",
            "image": "/static/images/profiles/christopher_nolan.jpg"
        },
        "cast": [
            {
                "name": "Matt Damon",
                "role": "Odysseus",
                "image": "/static/images/profiles/matt_damon.jpg"
            },
            {
                "name": "Anne Hathaway",
                "role": "Penelope",
                "image": "/static/images/profiles/anne_hathaway.jpg"
            },
            {
                "name": "Robert Pattinson",
                "role": "Telemachus",
                "image": "/static/images/profiles/robert_pattinson.jpg"
            }
        ],
        "synopsis": "Christopher Nolan directs a mind-bending, IMAX 70mm shot sci-fi reimagining of Homer's epic poem. The legendary Greek hero Odysseus embarks on a cosmic journey to find his way back home to his beloved Penelope.",
        "poster": "/static/images/the_odyssey_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/f_bKjZeJBBI",
        "is_featured": True
    },
    {
        "id": "spiderman-bnd",
        "title": "Spider-Man: Brand New Day",
        "release_date": "July 31, 2026",
        "director": {
            "name": "Destin Daniel Cretton",
            "image": "/static/images/profiles/destin_daniel_cretton.jpg"
        },
        "cast": [
            {
                "name": "Tom Holland",
                "role": "Peter Parker / Spider-Man",
                "image": "/static/images/profiles/tom_holland.jpg"
            },
            {
                "name": "Zendaya",
                "role": "MJ",
                "image": "/static/images/profiles/zendaya.jpg"
            },
            {
                "name": "Jon Bernthal",
                "role": "Frank Castle / Punisher",
                "image": "/static/images/profiles/jon_bernthal.jpg"
            }
        ],
        "synopsis": "Peter Parker struggles to rebuild his life after his identity was erased. However, when his physical powers begin mutating uncontrollably and a dangerous new threat emerges in New York City, he must seek the help of Bruce Banner.",
        "poster": "/static/images/spiderman_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/tLeBDumanoc",
        "is_featured": True
    },
    {
        "id": "avengers-doomsday",
        "title": "Avengers: Doomsday",
        "release_date": "December 18, 2026",
        "director": {
            "name": "Anthony & Joe Russo",
            "image": "/static/images/profiles/russo_brothers.jpg"
        },
        "cast": [
            {
                "name": "Robert Downey Jr.",
                "role": "Victor von Doom / Doctor Doom",
                "image": "/static/images/profiles/robert_downey_jr.jpg"
            },
            {
                "name": "Pedro Pascal",
                "role": "Reed Richards / Mr. Fantastic",
                "image": "/static/images/profiles/pedro_pascal.jpg"
            },
            {
                "name": "Florence Pugh",
                "role": "Yelena Belova / Black Widow",
                "image": "/static/images/profiles/florence_pugh.jpg"
            }
        ],
        "synopsis": "The Avengers face their ultimate challenge yet as Doctor Doom (Robert Downey Jr.) arrives from another dimension with plans of total multiversal domination. Directed by the Russo Brothers.",
        "poster": "/static/images/doomsday_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/399Ez7WHK5s",
        "is_featured": True
    },
    {
        "id": "dune-3",
        "title": "Dune: Part Three",
        "release_date": "December 18, 2026",
        "director": {
            "name": "Denis Villeneuve",
            "image": "/static/images/profiles/denis_villeneuve.jpg"
        },
        "cast": [
            {
                "name": "Timothée Chalamet",
                "role": "Paul Atreides",
                "image": "/static/images/profiles/timothee_chalamet.jpg"
            },
            {
                "name": "Zendaya",
                "role": "Chani",
                "image": "/static/images/profiles/zendaya.jpg"
            },
            {
                "name": "Florence Pugh",
                "role": "Princess Irulan",
                "image": "/static/images/profiles/florence_pugh.jpg"
            }
        ],
        "synopsis": "Paul Atreides grapples with the consequences of his rise to power as he leads the Fremen in a holy war across the universe, finding himself torn between his destiny and his love for Chani. Based on Frank Herbert's Dune Messiah.",
        "poster": "/static/images/dune_three_poster.jpg",
        "trailer_url": "https://www.youtube.com/embed/3_9vCamtuPY",
        "is_featured": True
    }
]

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    try:
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading watchlist: {e}")
        return []

def save_watchlist(data):
    try:
        with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing watchlist: {e}")
        return False

def fetch_news():
    url = "https://variety.com/v/film/feed/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    news_items = []
    
    # Heuristics for movie-related content
    MOVIE_KEYWORDS = [
        r'\bmovie\b', r'\bmovies\b', r'\bfilm\b', r'\bfilms\b', r'\bcinema\b', r'\bcinemas\b',
        r'\bbox office\b', r'\btheatrical\b', r'\btheater\b', r'\btheaters\b', r'\btheatre\b', r'\btheatres\b',
        r'\bdirector\b', r'\bdirectors\b', r'\bdirected\b', r'\bactor\b', r'\bactors\b', r'\bactress\b',
        r'\bactresses\b', r'\bcast\b', r'\bcasting\b', r'\bscreenplay\b', r'\bscreenwriter\b',
        r'\banimation\b', r'\banimated\b', r'\btrailer\b', r'\btrailers\b', r'\bsundance\b',
        r'\bcannes\b', r'\boscars\b', r'\boscar\b', r'\bacademy award\b', r'\bacademy awards\b',
        r'\bstudio\b', r'\bstudios\b', r'\bsequel\b', r'\bprequel\b', r'\bfranchise\b',
        r'\bblockbuster\b', r'\bpixar\b', r'\bdisney\b', r'\bmarvel\b', r'\bdc studios\b',
        r'\bwarner bros\b', r'\bsony pictures\b', r'\buniversal pictures\b', r'\bparamount\b',
        r'\btoy story\b', r'\bsupergirl\b', r'\bodyssey\b', r'\bspider-man\b', r'\bspiderman\b',
        r'\bavengers\b', r'\bdune\b', r'\bdoomsday\b', r'\bwoman of tomorrow\b'
    ]
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            channel = root.find("channel")
            if channel is not None:
                items = channel.findall("item")
                count = 0
                for item in items:
                    if count >= 10:
                        break
                    
                    title = item.find("title").text if item.find("title") is not None else "Movie News Update"
                    link = item.find("link").text if item.find("link") is not None else "#"
                    pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                    description = item.find("description").text if item.find("description") is not None else ""
                    categories = [cat.text for cat in item.findall("category") if cat.text]
                    
                    # Heuristic movie-only check
                    text_to_check = (title + " " + description + " " + " ".join(categories)).lower()
                    text_to_check = re.sub('<[^<]+?>', '', text_to_check)
                    
                    is_movie_related = any(re.search(kw, text_to_check) for kw in MOVIE_KEYWORDS)
                    if not is_movie_related:
                        continue
                    
                    # Extract image url from media namespace tags
                    image_url = ""
                    thumb_el = item.find("{http://search.yahoo.com/mrss/}thumbnail")
                    if thumb_el is not None and "url" in thumb_el.attrib:
                        image_url = thumb_el.attrib["url"]
                    else:
                        content_el = item.find("{http://search.yahoo.com/mrss/}content")
                        if content_el is not None and "url" in content_el.attrib:
                            image_url = content_el.attrib["url"]

                    # Fallback to Unsplash if no image URL found
                    if not image_url:
                        fallbacks = [
                            "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=80",
                            "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=500&auto=format&fit=crop&q=80",
                            "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&auto=format&fit=crop&q=80",
                            "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=500&auto=format&fit=crop&q=80"
                        ]
                        image_url = fallbacks[count % len(fallbacks)]
                    
                    # Clean up description (strip HTML tags and resolve entities)
                    if description:
                        description = re.sub('<[^<]+?>', '', description)
                        description = description.replace("&amp;", "&").replace("&quot;", '"').replace("&#8217;", "'").replace("&#8220;", '"').replace("&#8221;", '"').replace("&#038;", "&").replace("&#8211;", "-")
                        if len(description) > 150:
                            description = description[:150].strip() + "..."
                    
                    # Clean up date to read nicer
                    clean_date = pub_date
                    if pub_date:
                        match = re.match(r"\w+,\s+(\d+\s+\w+\s+\d+)", pub_date)
                        if match:
                            clean_date = match.group(1)

                    news_items.append({
                        "id": f"news-{count}",
                        "title": title,
                        "link": link,
                        "release_date": clean_date,  # mapping date field consistently
                        "description": description,
                        "poster": image_url,
                        "is_featured": False
                    })
                    count += 1
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        # Fallback news items if offline/network error
        news_items = [
            {
                "id": "news-fallback-1",
                "title": "Hollywood Studios Eye Major Release Date Adjustments for 2026/2027",
                "link": "https://variety.com",
                "release_date": "18 Jun 2026",
                "description": "Studio executives are meeting to coordinate high-profile release dates to avoid box office clashes, with special emphasis on summer and holiday release windows.",
                "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=80",
                "is_featured": False
            },
            {
                "id": "news-fallback-2",
                "title": "IMAX Reports Surging Bookings for Christopher Nolan's Next Epic",
                "link": "https://variety.com",
                "release_date": "17 Jun 2026",
                "description": "Pre-sales and theater chain commitments for Christopher Nolan's upcoming release have reached record-breaking figures, fueling projections for the 2026 box office.",
                "poster": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=500&auto=format&fit=crop&q=80",
                "is_featured": False
            },
            {
                "id": "news-fallback-3",
                "title": "Marvel Studios Gears Up for Avengers: Doomsday Pre-Production",
                "link": "https://variety.com",
                "release_date": "16 Jun 2026",
                "description": "Leaked schedules show massive production design setups in London as the Russo Brothers assemble the massive cast for the Doctor Doom conflict.",
                "poster": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&auto=format&fit=crop&q=80",
                "is_featured": False
            }
        ]
    return news_items

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies')
def get_movies():
    news = fetch_news()
    return jsonify({
        "featured": FEATURED_MOVIES,
        "news": news
    })

@app.route('/api/watchlist', methods=['GET', 'POST'])
def watchlist():
    watchlist_data = load_watchlist()
    if request.method == 'GET':
        return jsonify(watchlist_data)
    
    elif request.method == 'POST':
        movie = request.json
        if not movie or 'id' not in movie:
            return jsonify({"success": False, "message": "Invalid movie data"}), 400
        
        # Check if already exists in watchlist
        if any(item['id'] == movie['id'] for item in watchlist_data):
            return jsonify({"success": True, "message": "Already in watchlist", "watchlist": watchlist_data})
        
        watchlist_data.append(movie)
        if save_watchlist(watchlist_data):
            return jsonify({"success": True, "message": "Added to watchlist", "watchlist": watchlist_data})
        else:
            return jsonify({"success": False, "message": "Failed to save watchlist"}), 500

@app.route('/api/watchlist/<movie_id>', methods=['DELETE'])
def remove_from_watchlist(movie_id):
    watchlist_data = load_watchlist()
    new_watchlist = [item for item in watchlist_data if item['id'] != movie_id]
    
    if len(new_watchlist) == len(watchlist_data):
        return jsonify({"success": False, "message": "Movie not found in watchlist"}), 404
        
    if save_watchlist(new_watchlist):
        return jsonify({"success": True, "message": "Removed from watchlist", "watchlist": new_watchlist})
    else:
        return jsonify({"success": False, "message": "Failed to save watchlist"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
