# CineWave

An upcoming blockbuster movie hub and real-time news pipeline dashboard built to display highly anticipated blockbusters, stream official teaser trailers, and track film industry headlines. Designed with rich glassmorphism aesthetics, this Flask web application vaults user watchlist selections into a local JSON database and automatically curates film-only press coverage from Variety.

# Prerequisites
- Python 3.11+
- Virtual Environment manager (`venv`)
- Modern Web Browser (Google Chrome recommended)
- pip package manager

# Key Features
- **Curated Blockbusters:** Showcases highly anticipated titles (Toy Story 5, Supergirl, The Odyssey, Spider-Man, Avengers, Dune 3) sorted chronologically.
- **Film Industry News:** Curates and filters live Variety RSS news feed items, strictly rendering movie-focused updates.
- **Interactive Trailers:** Plays high-definition trailers via a dedicated YouTube embed overlay modal.
- **Circular Cast Profiles:** Renders detailed cast and director bios with real headshots inside interactive overlay modals.
- **Local Watchlist Database:** Saves and deletes selected titles/news from a persistent local JSON database.

# Architecture & API Limitations
To bypass rate limiting from standard search engines and Wikipedia's media endpoints, CineWave utilizes a hybrid asset retrieval pipeline. 

If you are running this repository locally:
1. **Pre-Cached Assets:** Cast headshots and theatrical posters are pre-downloaded and stored locally in the [static/images/](file:///G:/Antigravity Projects/agy/app/static/images) directory.
2. **RSS Filtering & Recovery:** If Variety's RSS feed is unreachable, the system automatically recovers and presents stored fallback articles. If active, a custom keyword regex checks article headings to suppress television, music, and sports posts.

# Setup
1.) Clone the repository
```
https://github.com/aledzzz/CineWave.git
```
2.) Navigate to the app folder
```
cd app
```
3.) Create a virtual environment
```
python -m venv venv
```
4.) Install dependencies
```
pip install -r requirements.txt
```
5.) Run
```
python app.py
```
*(Once running, navigate to `http://127.0.0.1:8080` in your web browser.)*
