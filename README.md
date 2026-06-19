# CineWave

An upcoming blockbuster movie hub and real-time news pipeline dashboard built to display highly anticipated blockbusters, stream official teaser trailers, and track film industry headlines. Designed with rich glassmorphism aesthetics, this Flask web application vaults user watchlist selections into a local JSON database and automatically curates film-only press coverage from Variety.

# Prerequisites
- Python 3.11+
- Virtual Environment manager (`venv`)
- Google Chrome (Incognito Mode Recommended)
- pip package manager

# Key Features
- **Upcoming Blockbusters:** Showcases highly anticipated titles (Toy Story 5, Supergirl, The Odyssey, Spider-Man, Avengers, Dune 3).
- **Film Industry News:** Curates and filters live Variety RSS news feed items, strictly rendering movie-focused updates.
- **Interactive Trailers:** Plays high-definition trailers via a dedicated YouTube embed overlay model.
- **Circular Cast Profiles:** Renders detailed cast and director bios inside interactive overlay models.
- **Local Watchlist Database:** Saves and deletes selected titles/news from a persistent local JSON database.

# Architecture & API Limitations
To bypass rate limiting from standard search engines and Wikipedia's media endpoints, CineWave utilizes a hybrid asset retrieval pipeline. 

If you are running this repository locally:
1. **Pre-Cached Assets:** Cast headshots and theatrical posters are pre-downloaded and stored locally in the [static/images/](file:///G:/Antigravity Projects/agy/app/static/images) directory.
2. **RSS Filtering & Recovery:** If Variety's RSS feed is unreachable, the system automatically recovers and presents stored fallback articles. If active, a custom keyword regex checks article headings to suppress television, music, and sports posts.

# Setup & Installation (Via Terminal / Command Line)

To run the CineWave application locally, you will need to execute the following commands in your computer's terminal (Command Prompt/PowerShell on Windows, or Terminal on macOS/Linux).

### 1. Open your Terminal / Command Line
*   **Windows:** Press `Win + R`, type `powershell` (or `cmd`), and press Enter.
*   **macOS:** Press `Cmd + Space`, type `Terminal`, and press Enter.

### 2. Clone the Repository
Download the project files onto your local computer and navigate into the project directory:
```bash
git clone https://github.com/aledzzz/CineWave.git
cd CineWave/app
```

### 3. Initialize a Python Virtual Environment
Creating a virtual environment ensures that the application's packages do not interfere with your system-wide Python installation:
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment
Before installing packages, you must activate the environment:
*   **Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
*   **Windows (Command Prompt / CMD):**
    ```cmd
    .\venv\Scripts\activate.bat
    ```
*   **macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```

### 5. Install Project Dependencies
Use `pip` to install all the dependencies listed in the requirements file:
```bash
pip install -r requirements.txt
```

### 6. Run the Application
Launch the Flask local web server:
```bash
python app.py
```
Once the server starts up, open google chrome (incognito) and go to:
**[http://127.0.0.1:8080/](http://127.0.0.1:8080/)**
