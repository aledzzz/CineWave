// Global state variables
let movieData = { featured: [], news: [] };
let watchlist = [];
let activeTrailerMovie = null;

// DOM Elements
const featuredMoviesGrid = document.getElementById('featured-movies-grid');
const newsFeedContainer = document.getElementById('news-feed-container');
const watchlistSection = document.getElementById('watchlist-section');
const watchlistGrid = document.getElementById('watchlist-grid');
const watchlistEmptyState = document.getElementById('watchlist-empty-state');
const watchlistBadge = document.getElementById('watchlist-badge');
const refreshTrigger = document.getElementById('refresh-trigger');
const spinnerIcon = document.getElementById('spinner-icon');
const goWatchlistBtn = document.getElementById('go-watchlist-btn');
const closeWatchlistBtn = document.getElementById('close-watchlist-btn');
const heroScrollBtn = document.getElementById('hero-scroll-btn');
const logoLink = document.getElementById('logo-link');

// Modal Elements
const trailerModal = document.getElementById('trailer-modal');
const trailerIframe = document.getElementById('trailer-iframe');
const modalMovieTitle = document.getElementById('modal-movie-title');
const modalMovieDate = document.getElementById('modal-movie-date');
const modalCloseBtn = document.getElementById('modal-close-btn');

const detailsModal = document.getElementById('details-modal');
const detailsCloseBtn = document.getElementById('details-close-btn');
const detailsPoster = document.getElementById('details-poster');
const detailsTitle = document.getElementById('details-title');
const detailsDate = document.getElementById('details-date');
const detailsSynopsis = document.getElementById('details-synopsis');
const detailsDirectorContainer = document.getElementById('details-director-container');
const detailsCastContainer = document.getElementById('details-cast-container');
const detailsTrailerBtn = document.getElementById('details-trailer-btn');
const detailsWatchlistBtn = document.getElementById('details-watchlist-btn');

// Toast Notification
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    fetchMoviesAndNews();
    fetchWatchlist();
    setupEventListeners();
});

// Setup Events
function setupEventListeners() {
    // Refresh feed
    refreshTrigger.addEventListener('click', () => {
        if (!refreshTrigger.classList.contains('loading')) {
            fetchMoviesAndNews();
        }
    });

    // Watchlist visibility toggles
    goWatchlistBtn.addEventListener('click', () => {
        watchlistSection.classList.remove('hidden');
        watchlistSection.scrollIntoView({ behavior: 'smooth' });
    });
    
    closeWatchlistBtn.addEventListener('click', () => {
        watchlistSection.classList.add('hidden');
    });

    // Scroll button in hero
    heroScrollBtn.addEventListener('click', () => {
        document.getElementById('blockbusters-section').scrollIntoView({ behavior: 'smooth' });
    });

    // Logo click home
    logoLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        watchlistSection.classList.add('hidden');
    });

    // Trailer modal close events
    modalCloseBtn.addEventListener('click', closeTrailerModal);
    trailerModal.addEventListener('click', (e) => {
        if (e.target === trailerModal) {
            closeTrailerModal();
        }
    });

    // Details modal close events
    detailsCloseBtn.addEventListener('click', closeDetailsModal);
    detailsModal.addEventListener('click', (e) => {
        if (e.target === detailsModal) {
            closeDetailsModal();
        }
    });

    // Details Modal trailer & watchlist triggers
    detailsTrailerBtn.addEventListener('click', () => {
        if (activeTrailerMovie) {
            closeDetailsModal();
            openTrailerModal(activeTrailerMovie);
        }
    });

    detailsWatchlistBtn.addEventListener('click', () => {
        if (activeTrailerMovie) {
            addToWatchlist(activeTrailerMovie);
        }
    });

    // Global escape key close modals
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeTrailerModal();
            closeDetailsModal();
        }
    });
}

// Fetch Blockbusters and News Feed from API
async function fetchMoviesAndNews() {
    // Show spinner & loading state
    refreshTrigger.classList.add('loading');
    spinnerIcon.classList.add('animate-spin'); // fallback or helper class

    try {
        const response = await fetch('/api/movies');
        if (!response.ok) throw new Error("Failed to fetch movies.");
        
        movieData = await response.json();
        
        // Render lists
        renderFeaturedMovies(movieData.featured);
        renderNewsFeed(movieData.news);
        
        showToast("Feed updated successfully!");
    } catch (error) {
        console.error("Error fetching movies/news:", error);
        showToast("Error updating feed. Using offline fallbacks.");
    } finally {
        // Stop spinner
        setTimeout(() => {
            refreshTrigger.classList.remove('loading');
            spinnerIcon.classList.remove('animate-spin');
        }, 600); // smooth animation transition
    }
}

// Fetch Watchlist items from API
async function fetchWatchlist() {
    try {
        const response = await fetch('/api/watchlist');
        if (!response.ok) throw new Error("Failed to load watchlist.");
        
        watchlist = await response.json();
        renderWatchlist();
    } catch (error) {
        console.error("Error loading watchlist:", error);
    }
}

// Render Featured Blockbuster Grid
function renderFeaturedMovies(movies) {
    featuredMoviesGrid.innerHTML = '';
    
    movies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        
        // Check if item is already in watchlist
        const isInWatchlist = watchlist.some(item => item.id === movie.id);
        const watchlistBtnText = isInWatchlist ? 'Saved' : 'Watchlist';
        const watchlistBtnIcon = isInWatchlist ? 'check' : 'bookmark';
        const watchlistBtnClass = isInWatchlist ? 'btn-outline' : 'btn-primary';

        movieCard.innerHTML = `
            <div class="movie-poster-wrapper" onclick="openDetailsModal('${movie.id}')">
                <img class="movie-poster" src="${movie.poster}" alt="${movie.title}">
                <div class="movie-overlay-actions">
                    <div class="overlay-btn-row">
                        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); openTrailer('${movie.id}')">
                            <i data-lucide="play" class="icon-xs"></i> Trailer
                        </button>
                    </div>
                </div>
            </div>
            <div class="movie-info">
                <div class="movie-meta-row">
                    <i data-lucide="calendar" class="icon-xs"></i>
                    <span>${movie.release_date}</span>
                </div>
                <h3 class="movie-card-title" onclick="openDetailsModal('${movie.id}')">${movie.title}</h3>
                <p class="movie-card-synopsis">${movie.synopsis}</p>
                <div class="movie-card-footer">
                    <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); openDetailsModal('${movie.id}')">
                        Details
                    </button>
                    <button class="btn ${watchlistBtnClass} btn-sm" style="flex-grow: 1;" onclick="event.stopPropagation(); toggleWatchlistMovie('${movie.id}')">
                        <i data-lucide="${watchlistBtnIcon}" class="icon-xs"></i> <span>${watchlistBtnText}</span>
                    </button>
                </div>
            </div>
        `;
        
        featuredMoviesGrid.appendChild(movieCard);
    });
    
    lucide.createIcons();
}

// Render News Feed
function renderNewsFeed(newsItems) {
    newsFeedContainer.innerHTML = '';
    
    newsItems.forEach(item => {
        const isInWatchlist = watchlist.some(w => w.id === item.id);
        const watchlistIcon = isInWatchlist ? 'check' : 'bookmark';
        const watchlistTitle = isInWatchlist ? 'Remove from Watchlist' : 'Add to Watchlist';
        
        const newsCard = document.createElement('div');
        newsCard.className = 'news-item';
        
        newsCard.innerHTML = `
            <div class="news-thumbnail-wrapper">
                <img class="news-thumbnail" src="${item.poster}" alt="News Image">
            </div>
            <div class="news-info">
                <div class="news-date">
                    <i data-lucide="calendar" class="icon-xs"></i>
                    <span>${item.release_date}</span>
                </div>
                <h3 class="news-title">${item.title}</h3>
                <p class="news-description">${item.description}</p>
                <div class="news-actions">
                    <a href="${item.link}" target="_blank" class="read-more-link">
                        Read Full Article <i data-lucide="arrow-up-right" class="icon-xs"></i>
                    </a>
                    <button class="btn-icon-only" title="${watchlistTitle}" onclick="toggleWatchlistNews('${item.id}')">
                        <i data-lucide="${watchlistIcon}"></i>
                    </button>
                </div>
            </div>
        `;
        
        newsFeedContainer.appendChild(newsCard);
    });
    
    lucide.createIcons();
}

// Render Watchlist Grid
function renderWatchlist() {
    watchlistGrid.innerHTML = '';
    
    // Update navbar badge
    watchlistBadge.textContent = watchlist.length;
    
    if (watchlist.length === 0) {
        watchlistEmptyState.classList.remove('hidden');
        watchlistGrid.classList.add('hidden');
        return;
    }
    
    watchlistEmptyState.classList.add('hidden');
    watchlistGrid.classList.remove('hidden');
    
    watchlist.forEach(movie => {
        const watchlistCard = document.createElement('div');
        watchlistCard.className = 'movie-card';
        
        // Blockbusters and News look slightly different but share cards
        let isFeatured = movie.is_featured;
        let actionButtonsHtml = '';
        
        if (isFeatured) {
            actionButtonsHtml = `
                <button class="btn btn-outline btn-sm" onclick="openDetailsModal('${movie.id}')">Details</button>
                <button class="btn btn-outline btn-sm" title="Remove" onclick="removeFromWatchlist('${movie.id}')">
                    <i data-lucide="trash-2" class="icon-xs text-red"></i>
                </button>
            `;
        } else {
            actionButtonsHtml = `
                <a href="${movie.link}" target="_blank" class="btn btn-outline btn-sm" style="flex-grow: 1;">Read Article</a>
                <button class="btn btn-outline btn-sm" title="Remove" onclick="removeFromWatchlist('${movie.id}')">
                    <i data-lucide="trash-2" class="icon-xs text-red"></i>
                </button>
            `;
        }

        watchlistCard.innerHTML = `
            <div class="movie-poster-wrapper" onclick="${isFeatured ? `openDetailsModal('${movie.id}')` : `window.open('${movie.link}', '_blank')`}">
                <img class="movie-poster" src="${movie.poster}" alt="${movie.title}">
                ${isFeatured ? `
                <div class="movie-overlay-actions">
                    <div class="overlay-btn-row">
                        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); openTrailer('${movie.id}')">
                            <i data-lucide="play" class="icon-xs"></i> Play
                        </button>
                    </div>
                </div>` : ''}
            </div>
            <div class="movie-info">
                <div class="movie-meta-row">
                    <i data-lucide="calendar" class="icon-xs"></i>
                    <span>${movie.release_date}</span>
                </div>
                <h3 class="movie-card-title" onclick="${isFeatured ? `openDetailsModal('${movie.id}')` : `window.open('${movie.link}', '_blank')`}">${movie.title}</h3>
                <p class="movie-card-synopsis">${movie.description || movie.synopsis}</p>
                <div class="movie-card-footer" style="justify-content: space-between;">
                    ${actionButtonsHtml}
                </div>
            </div>
        `;
        
        watchlistGrid.appendChild(watchlistCard);
    });
    
    lucide.createIcons();
}

// Watchlist API calls
async function addToWatchlist(item) {
    try {
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        });
        
        if (!response.ok) throw new Error("Failed to save watchlist.");
        
        const data = await response.json();
        watchlist = data.watchlist;
        
        renderWatchlist();
        renderFeaturedMovies(movieData.featured);
        renderNewsFeed(movieData.news);
        
        // Refresh details modal watchlist button if it's active
        if (detailsModal.classList.contains('active') && activeTrailerMovie && activeTrailerMovie.id === item.id) {
            updateDetailsModalWatchlistBtn(true);
        }

        showToast(`"${item.title}" saved to local Watchlist!`);
    } catch (error) {
        console.error("Error adding to watchlist:", error);
        showToast("Error saving item to watchlist.");
    }
}

async function removeFromWatchlist(itemId) {
    try {
        const response = await fetch(`/api/watchlist/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error("Failed to delete from watchlist.");
        
        const data = await response.json();
        watchlist = data.watchlist;
        
        renderWatchlist();
        renderFeaturedMovies(movieData.featured);
        renderNewsFeed(movieData.news);
        
        // Refresh details modal watchlist button if it's active
        if (detailsModal.classList.contains('active') && activeTrailerMovie && activeTrailerMovie.id === itemId) {
            updateDetailsModalWatchlistBtn(false);
        }
        
        showToast("Removed from watchlist.");
    } catch (error) {
        console.error("Error removing from watchlist:", error);
        showToast("Error deleting item.");
    }
}

// Toggle functionality for buttons
function toggleWatchlistMovie(movieId) {
    const movie = movieData.featured.find(m => m.id === movieId);
    if (!movie) return;
    
    const index = watchlist.findIndex(item => item.id === movieId);
    if (index === -1) {
        addToWatchlist(movie);
    } else {
        removeFromWatchlist(movieId);
    }
}

function toggleWatchlistNews(newsId) {
    const item = movieData.news.find(n => n.id === newsId);
    if (!item) return;
    
    const index = watchlist.findIndex(w => w.id === newsId);
    if (index === -1) {
        addToWatchlist(item);
    } else {
        removeFromWatchlist(newsId);
    }
}

// Trailer Popup Modal Controls
function openTrailer(movieId) {
    const movie = movieData.featured.find(m => m.id === movieId) || watchlist.find(m => m.id === movieId);
    if (!movie) return;
    openTrailerModal(movie);
}

function openTrailerModal(movie) {
    modalMovieTitle.textContent = movie.title;
    modalMovieDate.textContent = `Release Date: ${movie.release_date}`;
    
    // Set Youtube source URL (ensure auto-play settings)
    trailerIframe.src = `${movie.trailer_url}?autoplay=1&rel=0`;
    
    trailerModal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Lock background scroll
}

function closeTrailerModal() {
    trailerModal.classList.remove('active');
    trailerIframe.src = ''; // Clear source to stop video playback
    document.body.style.overflow = ''; // Unlock scroll
}

// Detailed Information Modal Controls
function openDetailsModal(movieId) {
    const movie = movieData.featured.find(m => m.id === movieId) || watchlist.find(m => m.id === movieId);
    if (!movie) return;
    
    activeTrailerMovie = movie; // save movie context for details actions
    
    detailsPoster.src = movie.poster;
    detailsPoster.alt = movie.title;
    detailsTitle.textContent = movie.title;
    detailsDate.textContent = `Releasing ${movie.release_date}`;
    detailsSynopsis.textContent = movie.synopsis;
    
    // Render Director
    detailsDirectorContainer.innerHTML = `
        <img class="avatar" src="${movie.director.image}" alt="${movie.director.name}">
        <div class="profile-info">
            <h4>${movie.director.name}</h4>
            <p>Director</p>
        </div>
    `;
    
    // Render Cast Profiles
    detailsCastContainer.innerHTML = '';
    movie.cast.forEach(actor => {
        const actorEl = document.createElement('div');
        actorEl.className = 'cast-profile';
        actorEl.innerHTML = `
            <img class="avatar avatar-md" src="${actor.image}" alt="${actor.name}">
            <div class="profile-info">
                <h4>${actor.name}</h4>
                <p>as ${actor.role}</p>
            </div>
        `;
        detailsCastContainer.appendChild(actorEl);
    });
    
    // Setup Watchlist Action Button state
    const isInWatchlist = watchlist.some(item => item.id === movie.id);
    updateDetailsModalWatchlistBtn(isInWatchlist);
    
    detailsModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function updateDetailsModalWatchlistBtn(isInWatchlist) {
    if (isInWatchlist) {
        detailsWatchlistBtn.className = 'btn btn-outline btn-md';
        detailsWatchlistBtn.innerHTML = '<i data-lucide="check"></i> Saved in Watchlist';
    } else {
        detailsWatchlistBtn.className = 'btn btn-outline btn-md';
        detailsWatchlistBtn.innerHTML = '<i data-lucide="bookmark"></i> Save to Watchlist';
    }
    lucide.createIcons();
}

function closeDetailsModal() {
    detailsModal.classList.remove('active');
    document.body.style.overflow = '';
}

// Toast System
function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3500);
}
