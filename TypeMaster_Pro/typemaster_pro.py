"""
TypeMaster Pro - Advanced Terminal Typing Speed Test
A comprehensive typing practice tool with multiple difficulty levels,
performance tracking, and detailed statistics.
"""

import time
import random
import json
import os
from datetime import datetime

class TypeMasterPro:
    def __init__(self):
        self.quotes = {
            'easy': [
                "The quick brown fox jumps over the lazy dog.",
                "A journey of a thousand miles begins with a single step.",
                "Time flies when you are having fun.",
                "Practice makes perfect every single day.",
                "Never give up on your dreams and goals."
            ],
            'medium': [
                "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "The only way to do great work is to love what you do and embrace challenges.",
                "In the middle of difficulty lies opportunity waiting to be discovered.",
                "Life is what happens when you're busy making other plans for tomorrow.",
                "The future belongs to those who believe in the beauty of their dreams."
            ],
            'hard': [
                "It is during our darkest moments that we must focus to see the light ahead of us.",
                "The greatest glory in living lies not in never falling, but in rising every time we fall.",
                "Believe you can and you're halfway there; doubt will only hold you back from success.",
                "The only impossible journey is the one you never start, so take that first step today.",
                "Do not go where the path may lead, go instead where there is no path and leave a trail."
            ]
        }
        self.history_file = 'typemaster_history.json'
        self.history = self.load_history()

    def load_history(self):
        """Load typing test history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self, result):
        """Save test result to history"""
        self.history.append(result)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def calculate_wpm(self, text, time_taken):
        """Calculate words per minute"""
        words = len(text.split())
        minutes = time_taken / 60
        return round(words / minutes, 2) if minutes > 0 else 0

    def calculate_accuracy(self, original, typed):
        """Calculate typing accuracy"""
        if len(original) == 0:
            return 0
        
        correct_chars = sum(1 for i, char in enumerate(typed) if i < len(original) and char == original[i])
        total_chars = len(original)
        return round((correct_chars / total_chars) * 100, 2)

    def display_header(self):
        """Display welcome header"""
        print("\n" + "="*60)
        print("⌨️  TYPEMASTER PRO ⌨️".center(60))
        print("Master Your Typing Skills".center(60))
        print("="*60)
        print()

    def select_difficulty(self):
        """Let user select difficulty level"""
        print("Select Difficulty Level:")
        print("1. Easy (Short sentences)")
        print("2. Medium (Moderate complexity)")
        print("3. Hard (Longer sentences)")
        print()
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                return 'easy'
            elif choice == '2':
                return 'medium'
            elif choice == '3':
                return 'hard'
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def run_test(self):
        """Run a single typing test"""
        difficulty = self.select_difficulty()
        quote = random.choice(self.quotes[difficulty])
        
        print("\n" + "-"*60)
        print("Type the following text:")
        print("-"*60)
        print(f"\n{quote}\n")
        print("-"*60)
        
        input("Press ENTER when you're ready to start...")
        print("\nStart typing NOW!\n")
        
        start_time = time.time()
        typed_text = input("> ")
        end_time = time.time()
        
        time_taken = end_time - start_time
        wpm = self.calculate_wpm(quote, time_taken)
        accuracy = self.calculate_accuracy(quote, typed_text)
        
        # Display results
        print("\n" + "="*60)
        print("📊 TEST RESULTS".center(60))
        print("="*60)
        print(f"Time Taken: {time_taken:.2f} seconds")
        print(f"Words Per Minute (WPM): {wpm}")
        print(f"Accuracy: {accuracy}%")
        print(f"Difficulty Level: {difficulty.capitalize()}")
        
        # Performance rating
        if accuracy >= 95 and wpm >= 60:
            rating = "🏆 Excellent!"
        elif accuracy >= 90 and wpm >= 40:
            rating = "👍 Great job!"
        elif accuracy >= 80 and wpm >= 30:
            rating = "👌 Good effort!"
        else:
            rating = "💪 Keep practicing!"
        
        print(f"Rating: {rating}")
        print("="*60)
        
        # Save to history
        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'difficulty': difficulty,
            'wpm': wpm,
            'accuracy': accuracy,
            'time': round(time_taken, 2)
        }
        self.save_history(result)

    def show_history(self):
        """Display typing test history"""
        if not self.history:
            print("\n📋 No history available yet. Take some tests first!\n")
            return
        
        print("\n" + "="*60)
        print("📈 YOUR TYPING HISTORY".center(60))
        print("="*60)
        print()
        
        # Show last 10 tests
        recent_tests = self.history[-10:]
        for i, test in enumerate(recent_tests, 1):
            print(f"Test {i} - {test['date']}")
            print(f"  Difficulty: {test['difficulty'].capitalize()} | WPM: {test['wpm']} | Accuracy: {test['accuracy']}%")
            print()
        
        # Statistics
        if len(self.history) > 0:
            avg_wpm = sum(t['wpm'] for t in self.history) / len(self.history)
            avg_accuracy = sum(t['accuracy'] for t in self.history) / len(self.history)
            best_wpm = max(t['wpm'] for t in self.history)
            
            print("-"*60)
            print("📊 STATISTICS")
            print("-"*60)
            print(f"Total Tests: {len(self.history)}")
            print(f"Average WPM: {avg_wpm:.2f}")
            print(f"Average Accuracy: {avg_accuracy:.2f}%")
            print(f"Best WPM: {best_wpm}")
            print("="*60)

    def run(self):
        """Main program loop"""
        self.display_header()
        
        while True:
            print("\n🎯 MAIN MENU")
            print("1. Start Typing Test")
            print("2. View History & Statistics")
            print("3. Exit")
            print()
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.run_test()
            elif choice == '2':
                self.show_history()
            elif choice == '3':
                print("\n👋 Thanks for practicing! Keep improving your typing skills!\n")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    typemaster = TypeMasterPro()
    typemaster.run()
