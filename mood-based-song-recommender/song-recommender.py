"""
AI Mood-Based Music Recommender - Mini Project
Analyzes text sentiment and recommends music based on detected mood
"""

from textblob import TextBlob
import random

class MoodMusicRecommender:
    def __init__(self):
        # Mood keywords for detection
        self.moods = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'love', 'cheerful'],
            'sad': ['sad', 'depressed', 'down', 'unhappy', 'crying', 'hurt', 'lonely'],
            'energetic': ['energetic', 'pumped', 'motivated', 'workout', 'active', 'hyped'],
            'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'quiet', 'tranquil'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'furious', 'upset'],
            'romantic': ['love', 'romantic', 'date', 'crush', 'valentine', 'affection']
        }
        
        # Music database
        self.music = {
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
    
    def analyze_mood(self, text):
        """Analyze text and detect mood"""
        text = text.lower()
        
        # Count mood keywords
        mood_scores = {mood: sum(1 for word in keywords if word in text) 
                      for mood, keywords in self.moods.items()}
        
        # Get sentiment polarity
        sentiment = TextBlob(text).sentiment.polarity
        
        # Determine mood
        max_score = max(mood_scores.values())
        if max_score > 0:
            mood = max(mood_scores, key=mood_scores.get)
        elif sentiment > 0.3:
            mood = 'happy'
        elif sentiment < -0.3:
            mood = 'sad'
        else:
            mood = 'calm'
        
        confidence = min(100, max_score * 25 + abs(sentiment) * 50)
        
        return {
            'mood': mood,
            'sentiment': sentiment,
            'confidence': round(confidence, 1)
        }
    
    def recommend_songs(self, mood, count=4):
        """Get song recommendations for mood"""
        songs = self.music.get(mood, self.music['calm'])
        return random.sample(songs, min(count, len(songs)))
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*50)
        print("🎵  AI MOOD-BASED MUSIC RECOMMENDER  🎵")
        print("="*50)
        
        while True:
            print("\n💭 How are you feeling? Describe your mood:")
            text = input("> ").strip()
            
            if not text:
                print("⚠️  Please enter some text!")
                continue
            
            if text.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using the recommender! Keep vibing! 🎵\n")
                break
            
            # Analyze mood
            result = self.analyze_mood(text)
            
            # Display results
            print("\n" + "-"*50)
            print(f"🎭 Detected Mood: {result['mood'].upper()}")
            print(f"📊 Confidence: {result['confidence']}%")
            print(f"😊 Sentiment: {result['sentiment']:.2f}")
            print("-"*50)
            
            # Recommend songs
            songs = self.recommend_songs(result['mood'])
            print(f"\n🎵 RECOMMENDED SONGS:")
            for i, (title, artist) in enumerate(songs, 1):
                print(f"{i}. {title} - {artist}")
            
            print("\n" + "="*50)


if __name__ == "__main__":
    recommender = MoodMusicRecommender()
    recommender.run()