# 🎵 AI Mood-Based Music Recommender

**An Educational Journey Through Python: From Basics to Advanced**

This project demonstrates three progressively advanced implementations of an AI-powered music recommendation system that analyzes your mood and suggests songs. Perfect for learning Python development from beginner to advanced levels.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Level Comparison](#level-comparison)
- [Installation Guide](#installation-guide)
- [Level 1: Basic (Beginner-Friendly)](#level-1-basic-beginner-friendly)
- [Level 2: Intermediate (API Integration)](#level-2-intermediate-api-integration)
- [Level 3: Advanced (Production-Ready)](#level-3-advanced-production-ready)
- [Educational Progression](#educational-progression)
- [Core Python Concepts](#core-python-concepts)
- [API Setup](#api-setup)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Each version analyzes text describing your mood and recommends music accordingly:

```
User Input: "I'm feeling really happy and energetic today!"
         ↓
   Mood Analysis (NLP)
         ↓
   Song Recommendations
```

**What it teaches:**

- Natural Language Processing (NLP)
- Sentiment Analysis
- API Integration
- Object-Oriented Programming
- Async Programming
- Caching Strategies
- Software Architecture

---

## 📊 Level Comparison

| Feature            | Basic         | Intermediate        | Advanced          |
| ------------------ | ------------- | ------------------- | ----------------- |
| **Lines of Code**  | ~150          | ~250                | ~600              |
| **Difficulty**     | ⭐ Beginner   | ⭐⭐ Intermediate   | ⭐⭐⭐ Advanced   |
| **NLP Engine**     | TextBlob only | TextBlob only       | TextBlob + VADER  |
| **Music Source**   | Local DB      | Spotify API + Local | Multi-API + Cache |
| **Architecture**   | Single class  | Multi-class         | Modular + Async   |
| **Error Handling** | Basic         | Good                | Production-grade  |
| **Performance**    | Simple        | Standard            | Optimized         |
| **Type Hints**     | ❌ No         | ❌ No               | ✅ Yes            |
| **Caching**        | ❌ No         | ❌ No               | ✅ Yes            |
| **Async Support**  | ❌ No         | ❌ No               | ✅ Yes            |
| **Audio Features** | ❌ No         | ❌ No               | ✅ Yes            |

---

## 🚀 Installation Guide

### Prerequisites

```bash
# Python 3.8 or higher required
python --version
```

### Step 1: Install Dependencies

#### For Basic Version

```bash
pip install textblob
python -m textblob.download_corpora
```

#### For Intermediate Version

```bash
pip install textblob spotipy
python -m textblob.download_corpora
```

#### For Advanced Version

```bash
pip install textblob spotipy aiohttp vaderSentiment
python -m textblob.download_corpora
```

### Step 2: Download the Code

Save the respective version as:

- `basic_recommender.py`
- `intermediate_recommender.py`
- `advanced_recommender.py`

---

## 🌟 Level 1: Basic (Beginner-Friendly)

### 🎓 Learning Goals

- Understanding classes and methods
- Basic string manipulation
- Dictionary operations
- Simple sentiment analysis
- User input/output

### 🔧 Core Python Concepts Used

#### 1. **Class-Based Design**

```python
class MoodMusicRecommender:
    def __init__(self):
        # Initialize data

    def analyze_mood(self, text):
        # Analyze text

    def recommend_songs(self, mood):
        # Return songs
```

#### 2. **Dictionary for Data Storage**

```python
self.moods = {
    'happy': ['happy', 'joy', 'excited'],
    'sad': ['sad', 'down', 'unhappy']
}
```

#### 3. **List Comprehension**

```python
mood_scores = {
    mood: sum(1 for word in keywords if word in text)
    for mood, keywords in self.moods.items()
}
```

#### 4. **TextBlob Sentiment**

```python
sentiment = TextBlob(text).sentiment.polarity
# Returns: -1.0 (very negative) to +1.0 (very positive)
```

### 📋 Usage

```bash
python basic_recommender.py
```

**Example Session:**

```
🎵  AI MOOD-BASED MUSIC RECOMMENDER  🎵

💭 How are you feeling? Describe your mood:
> I'm feeling really happy and excited today!

--------------------------------------------------
🎭 Detected Mood: HAPPY
📊 Confidence: 75.0%
😊 Sentiment: 0.65
--------------------------------------------------

🎵 RECOMMENDED SONGS:
1. Happy - Pharrell Williams
2. Don't Stop Me Now - Queen
3. Walking on Sunshine - Katrina and the Waves
```

### 🎯 Key Takeaways

- **Simple but functional** - Does the job with minimal complexity
- **Easy to understand** - Perfect for beginners
- **No external dependencies** (except TextBlob)
- **Fast execution** - Instant results

---

## 🚀 Level 2: Intermediate (API Integration)

### 🎓 Learning Goals

- RESTful API integration
- OAuth authentication
- Environment variables
- Error handling patterns
- Multi-class architecture
- Fallback strategies

### 🔧 Core Python Concepts Used

#### 1. **Environment Variables**

```python
import os

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
```

#### 2. **API Authentication**

```python
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
spotify = spotipy.Spotify(auth_manager=auth_manager)
```

#### 3. **API Request Structure**

```python
results = self.spotify.recommendations(
    seed_genres=['pop', 'dance'],
    limit=5,
    target_valence=0.8,  # Happiness level
    target_energy=0.7,   # Energy level
    target_tempo=120     # Beats per minute
)
```

#### 4. **Graceful Fallback**

```python
if self.use_spotify:
    songs = self.get_spotify_recommendations(mood, count)
    if songs:
        return songs, 'Spotify'

# Fallback to local database
return self.get_local_recommendations(mood, count), 'Local'
```

#### 5. **Error Handling**

```python
try:
    # API call
    results = self.spotify.recommendations(...)
except Exception as e:
    print(f"⚠️  Spotify error: {e}")
    return None
```

### 📋 Setup & Usage

#### Step 1: Get Spotify Credentials

1. Go to https://developer.spotify.com/dashboard
2. Click "Create an App"
3. Note your **Client ID** and **Client Secret**

#### Step 2: Set Environment Variables

**macOS/Linux:**

```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```

**Windows (Command Prompt):**

```cmd
set SPOTIFY_CLIENT_ID=your_client_id_here
set SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

**Windows (PowerShell):**

```powershell
$env:SPOTIFY_CLIENT_ID="your_client_id_here"
$env:SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```

#### Step 3: Run the Program

```bash
python intermediate_recommender.py
```

**Example Session:**

```
✅ Connected to Spotify API

🎵  AI MOOD-BASED MUSIC RECOMMENDER  🎵

💭 How are you feeling right now?
> I'm feeling energetic and ready to workout!

🔄 Analyzing your mood...

============================================================
📊 MOOD ANALYSIS
============================================================
🎭 Detected Mood: ENERGETIC
📈 Confidence: 85.0%
😊 Sentiment Score: 0.625
============================================================

🎵 RECOMMENDED SONGS (Spotify):
------------------------------------------------------------

1. 🎵 Blinding Lights
   👤 The Weeknd
   🔗 https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b

2. 🎵 Lose Yourself
   👤 Eminem
   🔗 https://open.spotify.com/track/5Z01UMMf7V1o0MzF86s6WJ
```

### 🎯 Key Takeaways

- **Real API integration** - Works with actual Spotify data
- **Professional patterns** - Environment variables, error handling
- **Smart fallback** - Works without API credentials
- **Better recommendations** - Uses Spotify's music knowledge

---

## 🔥 Level 3: Advanced (Production-Ready)

### 🎓 Learning Goals

- Asynchronous programming
- Custom caching implementation
- Type hints and data classes
- Ensemble machine learning
- Performance optimization
- Advanced OOP patterns
- Production-ready architecture

### 🔧 Core Python Concepts Used

#### 1. **Data Classes**

```python
from dataclasses import dataclass

@dataclass
class MoodAnalysis:
    mood: str
    confidence: float
    sentiment_score: float
    subjectivity: float
    intensity: float
    timestamp: str
    keyword_matches: Dict[str, int]

# Auto-generates __init__, __repr__, __eq__, etc.
```

#### 2. **Type Hints**

```python
from typing import List, Dict, Optional, Tuple

def get_recommendations(
    self,
    mood: str,
    intensity: float,
    count: int = 5
) -> List[Song]:
    # Function body
```

#### 3. **Async/Await Programming**

```python
async def get_recommendations_async(self, mood: str) -> List[Song]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
    return songs

# Run with:
await get_recommendations_async('happy')
```

#### 4. **Custom LRU Cache with TTL**

```python
class CacheManager:
    def __init__(self, max_size: int = 100, ttl_minutes: int = 60):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self, key: str) -> Optional[any]:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return value  # Still valid
            del self.cache[key]  # Expired
        return None
```

#### 5. **Hash-Based Cache Keys**

```python
import hashlib

def _generate_key(self, *args) -> str:
    key_str = ''.join(str(arg) for arg in args)
    return hashlib.md5(key_str.encode()).hexdigest()
```

#### 6. **Ensemble Sentiment Analysis**

```python
def _ensemble_sentiment(self, textblob: Dict, vader: Dict) -> float:
    # Combine multiple algorithms for better accuracy
    return (textblob['polarity'] * 0.4 + vader['compound'] * 0.6)
```

#### 7. **Dynamic Parameter Tuning**

```python
def _get_audio_params(self, mood: str, intensity: float) -> Dict:
    params = base_params[mood]

    # Adjust energy based on intensity (0-100)
    intensity_factor = intensity / 100
    params['target_energy'] = min(
        1.0,
        params['target_energy'] * (0.8 + intensity_factor * 0.4)
    )

    return params
```

#### 8. **Context Managers**

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        return await response.json()
```

### 📋 Setup & Usage

#### Step 1: Install All Dependencies

```bash
pip install textblob spotipy aiohttp vaderSentiment
python -m textblob.download_corpora
```

#### Step 2: Set Environment Variables

```bash
# Spotify (required for best results)
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"

# Last.fm (optional - provides fallback)
export LASTFM_API_KEY="your_lastfm_key"
```

#### Step 3: Run the Program

```bash
python advanced_recommender.py
```

**Example Session:**

```
✅ Spotify API connected
✅ Last.fm API ready

🎵  ADVANCED AI MOOD-BASED MUSIC RECOMMENDER  🎵

Features: Multi-API, Caching, Advanced NLP, Audio Analysis
Type 'exit' or 'quit' to stop

💭 Describe your current mood in detail:
> I'm feeling incredibly happy and energetic after my workout!

🔄 Analyzing mood with advanced NLP...

======================================================================
📊 ADVANCED MOOD ANALYSIS
======================================================================
🎭 Mood: ENERGETIC
📈 Confidence: 92.50%
😊 Sentiment: 0.685
🎯 Subjectivity: 0.450
⚡ Intensity: 68.50%
🕐 Timestamp: 2024-10-13T15:30:45.123456

🔍 Keyword Matches:
   • energetic: 2 matches
   • happy: 1 matches
======================================================================

🎵 RECOMMENDATIONS FROM SPOTIFY
----------------------------------------------------------------------

1. 🎵 Blinding Lights
   👤 The Weeknd
   💿 Album: After Hours
   📊 Popularity: 95/100
   🎚️  Audio: Energy=0.88, Valence=0.62, Tempo=171
   🔗 https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b

2. 🎵 Don't Start Now
   👤 Dua Lipa
   💿 Album: Future Nostalgia
   📊 Popularity: 92/100
   🎚️  Audio: Energy=0.79, Valence=0.68, Tempo=124
   🔗 https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62

⏱️  Processing time: 0.85s
```

### 🎯 Key Takeaways

- **Production-ready code** - Enterprise-level patterns
- **Performance optimized** - Caching reduces API calls
- **Type-safe** - Full type hints for better IDE support
- **Async architecture** - Non-blocking I/O
- **Multiple ML models** - Ensemble approach
- **Detailed analytics** - Audio features, timestamps
- **Scalable design** - Easy to extend and maintain

---

## 📈 Educational Progression

### Level 1 → Level 2: What Changes?

| Concept            | Basic          | Intermediate          |
| ------------------ | -------------- | --------------------- |
| **Data Source**    | Hardcoded list | Live API              |
| **Classes**        | 1 class        | 2+ classes            |
| **Error Handling** | Minimal        | Try-except blocks     |
| **Configuration**  | None           | Environment variables |
| **Song Quality**   | Fixed 4 songs  | Dynamic, real songs   |
| **Complexity**     | ~150 lines     | ~250 lines            |

**Key Learning:**

- How to work with external APIs
- OAuth2 authentication flow
- Graceful degradation (fallbacks)
- Separation of concerns

### Level 2 → Level 3: What Changes?

| Concept          | Intermediate | Advanced         |
| ---------------- | ------------ | ---------------- |
| **Execution**    | Synchronous  | Asynchronous     |
| **Caching**      | None         | Custom LRU + TTL |
| **Type Safety**  | No types     | Full type hints  |
| **Data Models**  | Dictionaries | Data classes     |
| **ML Models**    | 1 (TextBlob) | 2 (Ensemble)     |
| **Performance**  | Standard     | Optimized        |
| **Architecture** | Simple       | Modular          |
| **Complexity**   | ~250 lines   | ~600 lines       |

**Key Learning:**

- Async programming patterns
- Cache implementation strategies
- Type systems in Python
- Professional code organization
- Performance optimization
- Production-ready patterns

---

## 🧠 Core Python Concepts

### 1. Object-Oriented Programming (All Levels)

```python
class MoodAnalyzer:
    def __init__(self):
        # Constructor - runs when object is created
        self.mood_keywords = {...}

    def analyze(self, text):
        # Instance method - operates on self
        return self._process(text)

    def _process(self, text):
        # Private method - internal use only
        pass
```

### 2. List Comprehensions (All Levels)

```python
# Traditional way
scores = {}
for mood, keywords in self.moods.items():
    count = 0
    for word in keywords:
        if word in text:
            count += 1
    scores[mood] = count

# Pythonic way
scores = {
    mood: sum(1 for word in keywords if word in text)
    for mood, keywords in self.moods.items()
}
```

### 3. Dictionary Methods (All Levels)

```python
# Get with default
mood_data = self.database.get(mood, self.database['neutral'])

# Max by value
best_mood = max(mood_scores, key=mood_scores.get)

# Filter dictionary
active_moods = {k: v for k, v in scores.items() if v > 0}
```

### 4. Exception Handling (Level 2+)

```python
try:
    results = api.fetch_data()
except ConnectionError:
    # Handle network issues
    return fallback_data
except ValueError:
    # Handle bad data
    return None
except Exception as e:
    # Catch all other errors
    print(f"Unexpected error: {e}")
finally:
    # Always runs (cleanup)
    api.close()
```

### 5. Environment Variables (Level 2+)

```python
import os

# Read environment variable
api_key = os.getenv('API_KEY')

# With default value
api_key = os.getenv('API_KEY', 'default_key')

# Check if exists
if 'API_KEY' in os.environ:
    # Use the key
    pass
```

### 6. Type Hints (Level 3)

```python
from typing import List, Dict, Optional, Tuple

def process_songs(
    songs: List[str],           # List of strings
    metadata: Dict[str, int],   # Dict with str keys, int values
    limit: Optional[int] = None # Optional integer
) -> Tuple[List[str], int]:    # Returns tuple of list and int
    return filtered_songs, count
```

### 7. Data Classes (Level 3)

```python
from dataclasses import dataclass

# Instead of:
class Song:
    def __init__(self, title, artist, url):
        self.title = title
        self.artist = artist
        self.url = url

    def __repr__(self):
        return f"Song({self.title}, {self.artist})"

# Use dataclass:
@dataclass
class Song:
    title: str
    artist: str
    url: str
    # Auto-generates __init__, __repr__, __eq__, etc.
```

### 8. Async/Await (Level 3)

```python
import asyncio
import aiohttp

# Async function
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Run async function
async def main():
    data = await fetch_data('https://api.example.com')
    print(data)

# Execute
asyncio.run(main())
```

### 9. Context Managers (Level 3)

```python
# File handling
with open('data.txt', 'r') as f:
    content = f.read()
# File automatically closed

# Custom context manager
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print(f"Took {self.end - self.start}s")

with Timer():
    # Code to time
    pass
```

### 10. Decorators (Advanced Concept)

```python
# LRU Cache decorator
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(n):
    # Results are cached automatically
    return complex_calculation(n)
```

---

## 🔑 API Setup

### Spotify API

1. **Go to Spotify Dashboard**

   - Visit: https://developer.spotify.com/dashboard
   - Log in with your Spotify account

2. **Create an App**

   - Click "Create an App"
   - Enter app name: "Mood Music Recommender"
   - Enter description: "Educational project"
   - Accept terms and create

3. **Get Credentials**

   - Click on your app
   - Copy **Client ID**
   - Click "Show Client Secret"
   - Copy **Client Secret**

4. **Set Environment Variables**
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id_here"
   export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
   ```

### Last.fm API (Optional - Level 3)

1. **Create Account**

   - Visit: https://www.last.fm/api/account/create
   - Fill in details

2. **Get API Key**

   - Copy your API key
   - No secret needed for non-commercial use

3. **Set Environment Variable**
   ```bash
   export LASTFM_API_KEY="your_api_key_here"
   ```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'textblob'"

**Solution:**

```bash
pip install textblob
python -m textblob.download_corpora
```

#### 2. "ModuleNotFoundError: No module named 'spotipy'"

**Solution:**

```bash
pip install spotipy
```

#### 3. Spotify Authentication Failed

**Causes:**

- Wrong credentials
- Credentials not set in environment

**Solution:**

```bash
# Check if variables are set
echo $SPOTIFY_CLIENT_ID
echo $SPOTIFY_CLIENT_SECRET

# If empty, set them again
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
```

#### 4. "LookupError: Resource 'corpora/brown' not found"

**Solution:**

```bash
python -m textblob.download_corpora
```

#### 5. Advanced Version: "ModuleNotFoundError: No module named 'aiohttp'"

**Solution:**

```bash
pip install aiohttp vaderSentiment
```

#### 6. No Recommendations Returned

**Possible Causes:**

- API rate limit exceeded
- Network connection issue
- Invalid mood detected

**Solution:**

- Wait a few minutes (rate limit)
- Check internet connection
- Try more descriptive mood text

---

## 🎓 Learning Path Recommendation

### For Complete Beginners

1. **Start with Basic Version**

   - Understand classes and methods
   - Learn dictionary operations
   - Practice with string manipulation

2. **Study the Code**

   - Add print statements to see what's happening
   - Modify the mood keywords
   - Add your own songs to the database

3. **Experiment**
   - Change confidence calculation
   - Add new moods
   - Modify output formatting

### For Intermediate Learners

1. **Move to Intermediate Version**

   - Learn API integration
   - Understand OAuth2 flow
   - Practice error handling

2. **Enhance the Code**

   - Add more audio features
   - Implement song ratings
   - Create a history feature

3. **Explore APIs**
   - Read Spotify API docs
   - Try different endpoints
   - Experiment with parameters

### For Advanced Learners

1. **Study Advanced Version**

   - Master async programming
   - Implement custom cache
   - Use type hints everywhere

2. **Production Features**

   - Add logging system
   - Implement rate limiting
   - Create unit tests
   - Add configuration files

3. **Extend Functionality**
   - Add database storage (SQLite)
   - Create web interface (Flask/FastAPI)
   - Build playlist generation
   - Add user preferences

---

## 📚 Additional Resources

### Python Fundamentals

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

### NLP & Sentiment Analysis

- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)

### API Integration

- [Spotify API Docs](https://developer.spotify.com/documentation/web-api/)
- [Requests Library](https://requests.readthedocs.io/)

### Advanced Topics

- [Async/Await in Python](https://realpython.com/async-io-python/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [Data Classes](https://docs.python.org/3/library/dataclasses.html)

---

## 🤝 Contributing

This is an educational project. Feel free to:

- Add new features
- Improve documentation
- Fix bugs
- Create tutorials

---

## 📝 License

This project is for educational purposes. Use freely for learning!

---

## 🎉 Conclusion

You've now seen three different approaches to the same problem:

1. **Basic** - Clean, simple, functional
2. **Intermediate** - Professional, API-integrated
3. **Advanced** - Production-ready, optimized

Each level builds on the previous one, demonstrating how Python code evolves from simple scripts to production systems.

**Happy Learning! 🚀**

---

_Last Updated: October 2024_
