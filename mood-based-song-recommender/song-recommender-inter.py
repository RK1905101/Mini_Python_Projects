"""
AI Mood-Based Music Recommender with Spotify Integration
Analyzes text sentiment and recommends music using Spotify API
"""

from textblob import TextBlob
import random
import os

# Spotify imports
try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False
    print("⚠️  Install spotipy: pip install spotipy")


class MoodMusicRecommender:
    def __init__(self, spotify_id=None, spotify_secret=None):
        # Mood keywords for detection
        self.moods = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'love', 'cheerful', 'amazing'],
            'sad': ['sad', 'depressed', 'down', 'unhappy', 'crying', 'hurt', 'lonely', 'heartbroken'],
            'energetic': ['energetic', 'pumped', 'motivated', 'workout', 'active', 'hyped', 'party'],
            'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'quiet', 'tranquil', 'meditate'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'upset', 'rage'],
            'romantic': ['love', 'romantic', 'date', 'crush', 'valentine', 'affection', 'intimate']
        }
        
        # Fallback local music database
        self.local_music = {
            'happy': [
                ('Happy', 'Pharrell Williams'),
                ('Walking on Sunshine', 'Katrina and the Waves'),
                ("Don't Stop Me Now", 'Queen'),
                ('Good Vibrations', 'The Beach Boys')
            ],
            'sad': [
                ('Someone Like You', 'Adele'),
                ('The Scientist', 'Coldplay'),
                ('Tears in Heaven', 'Eric Clapton'),
                ('Mad World', 'Gary Jules')
            ],
            'energetic': [
                ('Eye of the Tiger', 'Survivor'),
                ('Lose Yourself', 'Eminem'),
                ('Thunderstruck', 'AC/DC'),
                ('Till I Collapse', 'Eminem')
            ],
            'calm': [
                ('Weightless', 'Marconi Union'),
                ('Clair de Lune', 'Debussy'),
                ('River Flows in You', 'Yiruma'),
                ('Holocene', 'Bon Iver')
            ],
            'angry': [
                ('Break Stuff', 'Limp Bizkit'),
                ('Killing in the Name', 'Rage Against the Machine'),
                ('Bodies', 'Drowning Pool'),
                ('Chop Suey!', 'System of a Down')
            ],
            'romantic': [
                ('Perfect', 'Ed Sheeran'),
                ('All of Me', 'John Legend'),
                ('Thinking Out Loud', 'Ed Sheeran'),
                ('At Last', 'Etta James')
            ]
        }
        
        # Initialize Spotify
        self.spotify = None
        self.use_spotify = False
        
        if SPOTIFY_AVAILABLE and spotify_id and spotify_secret:
            try:
                auth_manager = SpotifyClientCredentials(
                    client_id=spotify_id,
                    client_secret=spotify_secret
                )
                self.spotify = spotipy.Spotify(auth_manager=auth_manager)
                self.use_spotify = True
                print("✅ Connected to Spotify API")
            except Exception as e:
                print(f"⚠️  Spotify connection failed: {e}")
                print("📂 Using local database instead")
        else:
            print("📂 Using local music database")
    
    def analyze_mood(self, text):
        """Analyze text and detect mood using keyword matching and sentiment"""
        text_lower = text.lower()
        
        # Count mood keywords
        mood_scores = {}
        for mood, keywords in self.moods.items():
            score = sum(1 for word in keywords if word in text_lower)
            mood_scores[mood] = score
        
        # Get sentiment polarity from TextBlob
        sentiment = TextBlob(text).sentiment.polarity
        
        # Determine final mood
        max_score = max(mood_scores.values())
        
        if max_score > 0:
            detected_mood = max(mood_scores, key=mood_scores.get)
        elif sentiment > 0.3:
            detected_mood = 'happy'
        elif sentiment < -0.3:
            detected_mood = 'sad'
        else:
            detected_mood = 'calm'
        
        # Calculate confidence score
        confidence = min(100, max_score * 25 + abs(sentiment) * 50)
        
        return {
            'mood': detected_mood,
            'sentiment': round(sentiment, 3),
            'confidence': round(confidence, 1)
        }
    
    def get_spotify_features(self, mood):
        """Map mood to Spotify audio features"""
        features = {
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
            }
        }
        return features.get(mood, features['calm'])
    
    def get_spotify_recommendations(self, mood, count=5):
        """Get song recommendations from Spotify API"""
        try:
            features = self.get_spotify_features(mood)
            
            # Request recommendations from Spotify
            results = self.spotify.recommendations(
                seed_genres=features['seed_genres'],
                limit=count,
                target_valence=features['target_valence'],
                target_energy=features['target_energy'],
                target_tempo=features['target_tempo']
            )
            
            # Parse results
            recommendations = []
            for track in results['tracks']:
                recommendations.append({
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'url': track['external_urls']['spotify'],
                    'preview': track.get('preview_url')
                })
            
            return recommendations
            
        except Exception as e:
            print(f"⚠️  Spotify error: {e}")
            return None
    
    def get_local_recommendations(self, mood, count=4):
        """Get recommendations from local database"""
        songs = self.local_music.get(mood, self.local_music['calm'])
        selected = random.sample(songs, min(count, len(songs)))
        
        return [
            {'title': title, 'artist': artist, 'url': None, 'preview': None}
            for title, artist in selected
        ]
    
    def recommend_songs(self, mood, count=5):
        """Get song recommendations (Spotify or fallback to local)"""
        if self.use_spotify:
            songs = self.get_spotify_recommendations(mood, count)
            if songs:
                return songs, 'Spotify'
        
        # Fallback to local database
        return self.get_local_recommendations(mood, count), 'Local Database'
    
    def display_results(self, analysis, songs, source):
        """Display mood analysis and song recommendations"""
        print("\n" + "="*60)
        print("📊 MOOD ANALYSIS")
        print("="*60)
        print(f"🎭 Detected Mood: {analysis['mood'].upper()}")
        print(f"📈 Confidence: {analysis['confidence']}%")
        print(f"😊 Sentiment Score: {analysis['sentiment']}")
        print("="*60)
        
        print(f"\n🎵 RECOMMENDED SONGS ({source}):")
        print("-"*60)
        
        for i, song in enumerate(songs, 1):
            print(f"\n{i}. 🎵 {song['title']}")
            print(f"   👤 {song['artist']}")
            if song.get('url'):
                print(f"   🔗 {song['url']}")
        
        print("\n" + "-"*60)
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("🎵  AI MOOD-BASED MUSIC RECOMMENDER  🎵")
        print("="*60)
        print("\nDescribe how you're feeling, and I'll recommend music!")
        print("(Type 'exit' or 'quit' to stop)\n")
        
        while True:
            print("💭 How are you feeling right now?")
            text = input("> ").strip()
            
            if not text:
                print("⚠️  Please enter some text!")
                continue
            
            if text.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using the recommender!")
                print("🎵 Keep listening, keep feeling! 🎵\n")
                break
            
            # Analyze mood
            print("\n🔄 Analyzing your mood...")
            analysis = self.analyze_mood(text)
            
            # Get recommendations
            songs, source = self.recommend_songs(analysis['mood'])
            
            # Display results
            self.display_results(analysis, songs, source)
            
            # Ask to continue
            continue_choice = input("\n🔄 Analyze another mood? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Thanks for using the recommender!")
                print("🎵 Keep listening, keep feeling! 🎵\n")
                break


def load_credentials():
    """Load Spotify credentials from environment or user input"""
    spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
    spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not spotify_id or not spotify_secret:
        print("\n🔑 Spotify API Setup")
        print("-"*60)
        print("Get your credentials at: https://developer.spotify.com/dashboard")
        print("(Press Enter to skip and use local database)")
        print("-"*60)
        
        spotify_id = input("Client ID: ").strip()
        spotify_secret = input("Client Secret: ").strip()
        
        if not spotify_id or not spotify_secret:
            return None, None
    
    return spotify_id, spotify_secret


if __name__ == "__main__":
    # Load credentials
    client_id, client_secret = load_credentials()
    
    # Create and run recommender
    recommender = MoodMusicRecommender(client_id, client_secret)
    
    try:
        recommender.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Goodbye! 👋\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")