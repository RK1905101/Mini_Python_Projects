"""
AI Mood-Based Music Recommender - Advanced Edition
Features: Multi-API integration, caching, async requests, ML sentiment analysis
"""

import asyncio
import aiohttp
from textblob import TextBlob
import random
import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from functools import lru_cache
import hashlib

# Spotify imports
try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False

# Optional ML-based sentiment
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


@dataclass
class MoodAnalysis:
    """Data class for mood analysis results"""
    mood: str
    confidence: float
    sentiment_score: float
    subjectivity: float
    intensity: float
    timestamp: str
    keyword_matches: Dict[str, int]


@dataclass
class Song:
    """Data class for song recommendations"""
    title: str
    artist: str
    url: Optional[str] = None
    preview_url: Optional[str] = None
    album: Optional[str] = None
    popularity: Optional[int] = None
    audio_features: Optional[Dict] = None
    source: str = "Unknown"


class CacheManager:
    """LRU cache with expiration for API responses"""

    def __init__(self, max_size: int = 100, ttl_minutes: int = 60):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)

    def _generate_key(self, *args) -> str:
        """Generate cache key from arguments"""
        key_str = ''.join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[any]:
        """Get cached value if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: any):
        """Set cache value with timestamp"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(),
                             key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]

        self.cache[key] = (value, datetime.now())

    def clear(self):
        """Clear all cache"""
        self.cache.clear()


class AdvancedMoodAnalyzer:
    """Advanced mood analyzer with multiple sentiment engines"""

    def __init__(self, use_vader: bool = True):
        self.use_vader = use_vader and VADER_AVAILABLE
        self.vader_analyzer = SentimentIntensityAnalyzer() if self.use_vader else None

        # Enhanced mood keywords with weights
        self.mood_patterns = {
            'happy': {
                'keywords': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing',
                             'fantastic', 'cheerful', 'delighted', 'thrilled', 'ecstatic'],
                'weight': 1.0
            },
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'unhappy', 'crying', 'hurt',
                             'lonely', 'heartbroken', 'miserable', 'devastated'],
                'weight': 1.0
            },
            'energetic': {
                'keywords': ['energetic', 'pumped', 'motivated', 'workout', 'active',
                             'hyped', 'party', 'wild', 'fierce', 'intense'],
                'weight': 1.2
            },
            'calm': {
                'keywords': ['calm', 'peaceful', 'relaxed', 'chill', 'quiet', 'tranquil',
                             'serene', 'meditate', 'zen', 'gentle'],
                'weight': 0.9
            },
            'angry': {
                'keywords': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'upset',
                             'rage', 'irritated', 'pissed', 'bitter'],
                'weight': 1.1
            },
            'romantic': {
                'keywords': ['love', 'romantic', 'date', 'crush', 'valentine', 'affection',
                             'intimate', 'passionate', 'caring', 'tender'],
                'weight': 1.0
            },
            'anxious': {
                'keywords': ['anxious', 'worried', 'stressed', 'nervous', 'tense',
                             'overwhelmed', 'panic', 'afraid', 'uneasy'],
                'weight': 1.0
            },
            'melancholic': {
                'keywords': ['melancholic', 'nostalgic', 'wistful', 'bittersweet',
                             'contemplative', 'longing', 'yearning', 'reflective'],
                'weight': 0.95
            }
        }

        # Negation words
        self.negations = {'not', 'no', 'never',
                          "n't", 'neither', 'nobody', 'nothing'}

    def _handle_negation(self, text: str) -> str:
        """Handle negations in text"""
        words = text.lower().split()
        modified = []
        negate_next = False

        for word in words:
            if word in self.negations:
                negate_next = True
                modified.append(word)
            elif negate_next:
                modified.append(f"NOT_{word}")
                negate_next = False
            else:
                modified.append(word)

        return ' '.join(modified)

    def _calculate_keyword_scores(self, text: str) -> Dict[str, int]:
        """Calculate weighted keyword scores for each mood"""
        text_processed = self._handle_negation(text)
        scores = {}
        matches = {}

        for mood, pattern in self.mood_patterns.items():
            count = 0
            for keyword in pattern['keywords']:
                if keyword in text_processed and f"NOT_{keyword}" not in text_processed:
                    count += 1

            scores[mood] = count * pattern['weight']
            matches[mood] = count

        return scores, matches

    def _get_textblob_sentiment(self, text: str) -> Dict:
        """Get TextBlob sentiment analysis"""
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }

    def _get_vader_sentiment(self, text: str) -> Optional[Dict]:
        """Get VADER sentiment scores"""
        if not self.use_vader:
            return None

        scores = self.vader_analyzer.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }

    def _ensemble_sentiment(self, textblob: Dict, vader: Optional[Dict]) -> float:
        """Combine multiple sentiment scores"""
        if vader:
            # Weighted average of TextBlob and VADER
            return (textblob['polarity'] * 0.4 + vader['compound'] * 0.6)
        return textblob['polarity']

    def _determine_mood(self, keyword_scores: Dict, sentiment: float,
                        subjectivity: float) -> Tuple[str, float]:
        """Determine final mood with confidence score"""
        max_score = max(keyword_scores.values())

        # If clear keyword match
        if max_score > 0:
            top_mood = max(keyword_scores, key=keyword_scores.get)
            confidence = min(95, max_score * 20 + abs(sentiment) * 30)
            return top_mood, confidence

        # Fallback to sentiment-based detection
        if sentiment > 0.5:
            return 'happy', abs(sentiment) * 80
        elif sentiment > 0.2:
            return 'calm', abs(sentiment) * 60
        elif sentiment < -0.5:
            return 'sad', abs(sentiment) * 80
        elif sentiment < -0.2:
            return 'melancholic', abs(sentiment) * 60
        else:
            return 'neutral', 30

    def analyze(self, text: str) -> MoodAnalysis:
        """Main analysis method with ensemble approach"""
        if not text or len(text.strip()) < 2:
            return MoodAnalysis(
                mood='neutral',
                confidence=0.0,
                sentiment_score=0.0,
                subjectivity=0.0,
                intensity=0.0,
                timestamp=datetime.now().isoformat(),
                keyword_matches={}
            )

        # Calculate scores
        keyword_scores, matches = self._calculate_keyword_scores(text)
        textblob_sentiment = self._get_textblob_sentiment(text)
        vader_sentiment = self._get_vader_sentiment(text)

        # Ensemble sentiment
        final_sentiment = self._ensemble_sentiment(
            textblob_sentiment, vader_sentiment)

        # Determine mood and confidence
        mood, confidence = self._determine_mood(
            keyword_scores,
            final_sentiment,
            textblob_sentiment['subjectivity']
        )

        # Calculate intensity (how strong the emotion is)
        intensity = abs(final_sentiment) * 100

        return MoodAnalysis(
            mood=mood,
            confidence=round(confidence, 2),
            sentiment_score=round(final_sentiment, 3),
            subjectivity=round(textblob_sentiment['subjectivity'], 3),
            intensity=round(intensity, 2),
            timestamp=datetime.now().isoformat(),
            keyword_matches=matches
        )


class SpotifyAdvancedRecommender:
    """Advanced Spotify recommender with audio feature analysis"""

    def __init__(self, client_id: str, client_secret: str):
        self.available = False

        if not SPOTIFY_AVAILABLE:
            return

        try:
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            self.available = True
            print("✅ Spotify API connected")
        except Exception as e:
            print(f"⚠️  Spotify failed: {e}")

    def _get_audio_params(self, mood: str, intensity: float) -> Dict:
        """Get dynamic audio parameters based on mood and intensity"""
        base_params = {
            'happy': {
                'seed_genres': ['pop', 'dance', 'happy'],
                'target_valence': 0.8,
                'target_energy': 0.7,
                'target_tempo': 120
            },
            'sad': {
                'seed_genres': ['sad', 'acoustic', 'piano'],
                'target_valence': 0.2,
                'target_energy': 0.3,
                'target_tempo': 70
            },
            'energetic': {
                'seed_genres': ['rock', 'workout', 'edm'],
                'target_valence': 0.7,
                'target_energy': 0.95,
                'target_tempo': 140
            },
            'calm': {
                'seed_genres': ['ambient', 'chill', 'jazz'],
                'target_valence': 0.5,
                'target_energy': 0.2,
                'target_tempo': 70
            },
            'angry': {
                'seed_genres': ['metal', 'hard-rock', 'punk'],
                'target_valence': 0.3,
                'target_energy': 0.9,
                'target_tempo': 130
            },
            'romantic': {
                'seed_genres': ['romance', 'r-n-b', 'soul'],
                'target_valence': 0.7,
                'target_energy': 0.4,
                'target_tempo': 90
            },
            'anxious': {
                'seed_genres': ['alternative', 'indie', 'emo'],
                'target_valence': 0.4,
                'target_energy': 0.5,
                'target_tempo': 100
            },
            'melancholic': {
                'seed_genres': ['indie', 'folk', 'singer-songwriter'],
                'target_valence': 0.3,
                'target_energy': 0.4,
                'target_tempo': 85
            }
        }

        params = base_params.get(mood, base_params['calm'])

        # Adjust energy based on intensity
        intensity_factor = intensity / 100
        params['target_energy'] = min(
            1.0, params['target_energy'] * (0.8 + intensity_factor * 0.4))

        return params

    def get_recommendations(self, mood: str, intensity: float, count: int = 5) -> List[Song]:
        """Get personalized recommendations with audio features"""
        if not self.available:
            return []

        try:
            params = self._get_audio_params(mood, intensity)

            results = self.spotify.recommendations(
                seed_genres=params['seed_genres'],
                limit=count,
                target_valence=params['target_valence'],
                target_energy=params['target_energy'],
                target_tempo=params['target_tempo']
            )

            songs = []
            track_ids = [track['id'] for track in results['tracks']]

            # Get audio features for all tracks
            audio_features = self.spotify.audio_features(track_ids)

            for track, features in zip(results['tracks'], audio_features):
                songs.append(Song(
                    title=track['name'],
                    artist=', '.join([a['name'] for a in track['artists']]),
                    album=track['album']['name'],
                    url=track['external_urls']['spotify'],
                    preview_url=track.get('preview_url'),
                    popularity=track.get('popularity'),
                    audio_features={
                        'energy': features.get('energy'),
                        'valence': features.get('valence'),
                        'tempo': features.get('tempo')
                    } if features else None,
                    source='Spotify'
                ))

            return songs

        except Exception as e:
            print(f"⚠️  Spotify error: {e}")
            return []


class LastFMAsyncRecommender:
    """Async Last.fm recommender for faster requests"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
        self.available = bool(api_key)

        if self.available:
            print("✅ Last.fm API ready")

    def _get_mood_tag(self, mood: str) -> str:
        """Map mood to Last.fm tag"""
        tags = {
            'happy': 'happy',
            'sad': 'sad',
            'energetic': 'energetic',
            'calm': 'chill',
            'angry': 'aggressive',
            'romantic': 'love',
            'melancholic': 'melancholy',
            'anxious': 'dark'
        }
        return tags.get(mood, 'rock')

    async def get_recommendations_async(self, mood: str, count: int = 5) -> List[Song]:
        """Async method to fetch recommendations"""
        if not self.available:
            return []

        try:
            tag = self._get_mood_tag(mood)
            params = {
                'method': 'tag.gettoptracks',
                'tag': tag,
                'api_key': self.api_key,
                'format': 'json',
                'limit': count
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=5) as response:
                    data = await response.json()

            songs = []
            for track in data.get('tracks', {}).get('track', [])[:count]:
                songs.append(Song(
                    title=track['name'],
                    artist=track['artist']['name'],
                    url=track['url'],
                    source='Last.fm'
                ))

            return songs

        except Exception as e:
            print(f"⚠️  Last.fm error: {e}")
            return []


class MusicRecommenderSystem:
    """Advanced music recommender with caching and multi-source support"""

    def __init__(self, spotify_id: str = None, spotify_secret: str = None,
                 lastfm_key: str = None):
        self.analyzer = AdvancedMoodAnalyzer(use_vader=VADER_AVAILABLE)
        self.cache = CacheManager(max_size=200, ttl_minutes=120)

        # Initialize recommenders
        self.spotify = None
        self.lastfm = None

        if spotify_id and spotify_secret:
            self.spotify = SpotifyAdvancedRecommender(
                spotify_id, spotify_secret)

        if lastfm_key:
            self.lastfm = LastFMAsyncRecommender(lastfm_key)

        # Fallback local database
        self.local_db = self._init_local_db()

    def _init_local_db(self) -> Dict:
        """Initialize compact local database"""
        return {
            'happy': [('Happy', 'Pharrell Williams'), ('Walking on Sunshine', 'Katrina')],
            'sad': [('Someone Like You', 'Adele'), ('The Scientist', 'Coldplay')],
            'energetic': [('Eye of the Tiger', 'Survivor'), ('Thunderstruck', 'AC/DC')],
            'calm': [('Weightless', 'Marconi Union'), ('Clair de Lune', 'Debussy')],
            'angry': [('Break Stuff', 'Limp Bizkit'), ('Bodies', 'Drowning Pool')],
            'romantic': [('Perfect', 'Ed Sheeran'), ('All of Me', 'John Legend')],
            'melancholic': [('Fix You', 'Coldplay'), ('Skinny Love', 'Bon Iver')],
            'anxious': [('Breathe', 'Pink Floyd'), ('Stressed Out', 'Twenty One Pilots')]
        }

    async def get_recommendations_async(self, analysis: MoodAnalysis,
                                        count: int = 5) -> Tuple[List[Song], str]:
        """Get recommendations asynchronously from multiple sources"""
        cache_key = f"{analysis.mood}_{int(analysis.intensity)}_{count}"

        # Check cache first
        cached = self.cache.get(cache_key)
        if cached:
            return cached, 'Cache'

        # Try Spotify first
        if self.spotify and self.spotify.available:
            songs = self.spotify.get_recommendations(
                analysis.mood, analysis.intensity, count)
            if songs:
                self.cache.set(cache_key, songs)
                return songs, 'Spotify'

        # Try Last.fm asynchronously
        if self.lastfm and self.lastfm.available:
            songs = await self.lastfm.get_recommendations_async(analysis.mood, count)
            if songs:
                self.cache.set(cache_key, songs)
                return songs, 'Last.fm'

        # Fallback to local
        local_songs = self.local_db.get(analysis.mood, self.local_db['calm'])
        songs = [Song(title=t, artist=a, source='Local')
                 for t, a in random.sample(local_songs, min(count, len(local_songs)))]

        return songs, 'Local Database'

    def analyze_mood(self, text: str) -> MoodAnalysis:
        """Analyze mood with advanced NLP"""
        return self.analyzer.analyze(text)

    def display_analysis(self, analysis: MoodAnalysis):
        """Display detailed mood analysis"""
        print("\n" + "="*70)
        print("📊 ADVANCED MOOD ANALYSIS")
        print("="*70)
        print(f"🎭 Mood: {analysis.mood.upper()}")
        print(f"📈 Confidence: {analysis.confidence}%")
        print(f"😊 Sentiment: {analysis.sentiment_score}")
        print(f"🎯 Subjectivity: {analysis.subjectivity}")
        print(f"⚡ Intensity: {analysis.intensity}%")
        print(f"🕐 Timestamp: {analysis.timestamp}")

        if analysis.keyword_matches:
            print(f"\n🔍 Keyword Matches:")
            for mood, count in analysis.keyword_matches.items():
                if count > 0:
                    print(f"   • {mood}: {count} matches")

        print("="*70)

    def display_recommendations(self, songs: List[Song], source: str):
        """Display song recommendations with details"""
        print(f"\n🎵 RECOMMENDATIONS FROM {source.upper()}")
        print("-"*70)

        for i, song in enumerate(songs, 1):
            print(f"\n{i}. 🎵 {song.title}")
            print(f"   👤 {song.artist}")

            if song.album:
                print(f"   💿 Album: {song.album}")

            if song.popularity:
                print(f"   📊 Popularity: {song.popularity}/100")

            if song.audio_features:
                features = song.audio_features
                print(f"   🎚️  Audio: Energy={features.get('energy', 'N/A'):.2f}, "
                      f"Valence={features.get('valence', 'N/A'):.2f}, "
                      f"Tempo={features.get('tempo', 'N/A'):.0f}")

            if song.url:
                print(f"   🔗 {song.url}")

        print("\n" + "-"*70)

    async def run_async(self):
        """Main async application loop"""
        print("\n" + "="*70)
        print("🎵  ADVANCED AI MOOD-BASED MUSIC RECOMMENDER  🎵")
        print("="*70)
        print("\nFeatures: Multi-API, Caching, Advanced NLP, Audio Analysis")
        print("Type 'exit' or 'quit' to stop\n")

        while True:
            print("💭 Describe your current mood in detail:")
            text = input("> ").strip()

            if not text:
                print("⚠️  Please enter some text!")
                continue

            if text.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using the recommender!")
                print("🎵 Keep listening, keep feeling! 🎵\n")
                break

            # Analyze mood
            print("\n🔄 Analyzing mood with advanced NLP...")
            start_time = time.time()

            analysis = self.analyze_mood(text)

            # Get recommendations
            songs, source = await self.get_recommendations_async(analysis, count=5)

            elapsed = time.time() - start_time

            # Display results
            self.display_analysis(analysis)
            self.display_recommendations(songs, source)

            print(f"\n⏱️  Processing time: {elapsed:.2f}s")

            # Continue?
            cont = input("\n🔄 Analyze another mood? (y/n): ").strip().lower()
            if cont != 'y':
                print("\n👋 Thanks for using the recommender!")
                print("🎵 Keep listening, keep feeling! 🎵\n")
                break


def load_credentials() -> Dict:
    """Load API credentials from environment"""
    return {
        'spotify_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'spotify_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
        'lastfm_key': os.getenv('LASTFM_API_KEY')
    }


async def main():
    """Main entry point"""
    creds = load_credentials()

    if not any(creds.values()):
        print("\n⚠️  No API credentials found in environment")
        print("Set: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, LASTFM_API_KEY")
        print("Continuing with local database...\n")

    system = MusicRecommenderSystem(
        spotify_id=creds['spotify_id'],
        spotify_secret=creds['spotify_secret'],
        lastfm_key=creds['lastfm_key']
    )

    await system.run_async()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted. Goodbye! 👋\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
