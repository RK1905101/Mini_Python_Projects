import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

class Habit:
    def __init__(self, name: str, frequency: str = "daily", target_days: int = 30, 
                 habit_id: Optional[int] = None):
        self.id = habit_id if habit_id else id(self)
        self.name = name
        self.frequency = frequency  # daily, weekly
        self.target_days = target_days
        self.created_at = datetime.now().strftime("%Y-%m-%d")
        self.completion_dates = []  # List of dates when habit was completed
        self.current_streak = 0
        self.longest_streak = 0
        self.total_completions = 0

    def mark_complete(self, date: str = None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if date not in self.completion_dates:
            self.completion_dates.append(date)
            self.completion_dates.sort()
            self.total_completions += 1
            self._calculate_streaks()
            return True
        return False

    def unmark_complete(self, date: str):
        if date in self.completion_dates:
            self.completion_dates.remove(date)
            self.total_completions -= 1
            self._calculate_streaks()
            return True
        return False

    def _calculate_streaks(self):
        if not self.completion_dates:
            self.current_streak = 0
            self.longest_streak = 0
            return

        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in self.completion_dates]
        dates.sort(reverse=True)
        
        today = datetime.now().date()
        current_streak = 0
        longest_streak = 0
        temp_streak = 1

        # Calculate current streak
        if dates[0] == today or dates[0] == today - timedelta(days=1):
            current_streak = 1
            for i in range(len(dates) - 1):
                diff = (dates[i] - dates[i + 1]).days
                if diff == 1:
                    current_streak += 1
                else:
                    break

        # Calculate longest streak
        for i in range(len(dates) - 1):
            diff = (dates[i] - dates[i + 1]).days
            if diff == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        longest_streak = max(longest_streak, current_streak)

        self.current_streak = current_streak
        self.longest_streak = longest_streak

    def is_completed_today(self) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        return today in self.completion_dates

    def get_completion_rate(self) -> float:
        if not self.completion_dates:
            return 0.0
        
        start_date = datetime.strptime(self.created_at, "%Y-%m-%d").date()
        days_since_creation = (datetime.now().date() - start_date).days + 1
        
        if days_since_creation == 0:
            return 0.0
        
        return (self.total_completions / days_since_creation) * 100

    def get_weekly_progress(self) -> List[bool]:
        """Returns last 7 days completion status"""
        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        return [date in self.completion_dates for date in last_7_days]

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'frequency': self.frequency,
            'target_days': self.target_days,
            'created_at': self.created_at,
            'completion_dates': self.completion_dates,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'total_completions': self.total_completions
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Habit':
        habit = Habit(
            name=data['name'],
            frequency=data.get('frequency', 'daily'),
            target_days=data.get('target_days', 30),
            habit_id=data['id']
        )
        habit.created_at = data['created_at']
        habit.completion_dates = data.get('completion_dates', [])
        habit.current_streak = data.get('current_streak', 0)
        habit.longest_streak = data.get('longest_streak', 0)
        habit.total_completions = data.get('total_completions', 0)
        habit._calculate_streaks()
        return habit


class HabitTracker:
    def __init__(self, filename: str = "habits.json"):
        self.filename = filename
        self.habits: List[Habit] = []
        self.load_habits()

    def load_habits(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.habits = [Habit.from_dict(h) for h in data]
            except:
                self.habits = []

    def save_habits(self):
        with open(self.filename, 'w') as f:
            json.dump([h.to_dict() for h in self.habits], f, indent=2)

    def add_habit(self, name: str, frequency: str = "daily", target_days: int = 30):
        habit = Habit(name, frequency, target_days)
        self.habits.append(habit)
        self.save_habits()
        print(f"✓ Habit added: {name}")

    def delete_habit(self, habit_id: int):
        for i, habit in enumerate(self.habits):
            if habit.id == habit_id:
                name = habit.name
                del self.habits[i]
                self.save_habits()
                print(f"✓ Habit deleted: {name}")
                return
        print("✗ Habit not found")

    def mark_habit_complete(self, habit_id: int, date: str = None):
        for habit in self.habits:
            if habit.id == habit_id:
                if habit.mark_complete(date):
                    self.save_habits()
                    print(f"✓ Marked complete: {habit.name}")
                    if habit.current_streak > 0:
                        print(f"  🔥 Current streak: {habit.current_streak} days!")
                else:
                    print(f"✗ Already marked complete for this date")
                return
        print("✗ Habit not found")

    def unmark_habit_complete(self, habit_id: int, date: str):
        for habit in self.habits:
            if habit.id == habit_id:
                if habit.unmark_complete(date):
                    self.save_habits()
                    print(f"✓ Unmarked: {habit.name} for {date}")
                else:
                    print(f"✗ Not marked complete for this date")
                return
        print("✗ Habit not found")

    def get_incomplete_habits_today(self) -> List[Habit]:
        return [h for h in self.habits if not h.is_completed_today()]

    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None


def print_habits_list(habits: List[Habit], title: str = "Habits"):
    if not habits:
        print(f"\n{title}: None")
        return

    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")

    for habit in habits:
        status = "✓" if habit.is_completed_today() else "○"
        streak_emoji = "🔥" if habit.current_streak > 0 else "💤"
        completion_rate = habit.get_completion_rate()
        
        print(f"{status} {habit.name}")
        print(f"   ID: {habit.id} | Streak: {streak_emoji} {habit.current_streak} days " +
              f"| Best: 🏆 {habit.longest_streak} days")
        print(f"   Total: {habit.total_completions} times | " +
              f"Completion Rate: {completion_rate:.1f}%")
        print(f"   Target: {habit.target_days} days | Created: {habit.created_at}")
        print()


def show_weekly_chart(habit: Habit):
    print(f"\n{'='*80}")
    print(f"📊 Weekly Progress: {habit.name}")
    print(f"{'='*80}")
    
    today = datetime.now().date()
    weekly_progress = habit.get_weekly_progress()
    
    # Day labels
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    # Get current day of week
    current_day_index = today.weekday()
    
    # Adjust to show last 7 days
    print("\n  ", end="")
    for i, date in enumerate(dates):
        day_name = days[date.weekday()]
        print(f"{day_name:>6}", end="  ")
    print()
    
    print("  ", end="")
    for date in dates:
        print(f"{date.strftime('%m/%d'):>6}", end="  ")
    print()
    
    print("  ", end="")
    for completed in weekly_progress:
        symbol = "  ✓✓  " if completed else "  ○○  "
        print(symbol, end="")
    print()
    
    completed_this_week = sum(weekly_progress)
    print(f"\n  This week: {completed_this_week}/7 days completed")
    print()


def show_all_habits_overview(habits: List[Habit]):
    if not habits:
        print("\nNo habits to display")
        return
    
    print(f"\n{'='*80}")
    print(f"📈 ALL HABITS OVERVIEW")
    print(f"{'='*80}\n")
    
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    # Header
    print(f"{'Habit':<25}", end="")
    for date in dates:
        print(f"{date.strftime('%m/%d'):>6}", end="  ")
    print(f"{'Streak':>8}")
    
    print("-" * 80)
    
    # Each habit row
    for habit in habits:
        weekly_progress = habit.get_weekly_progress()
        print(f"{habit.name:<25}", end="")
        
        for completed in weekly_progress:
            symbol = "  ✓  " if completed else "  -  "
            print(symbol, end="")
        
        streak_display = f"🔥 {habit.current_streak}" if habit.current_streak > 0 else f"💤 0"
        print(f"{streak_display:>8}")
    
    print()


def show_statistics(tracker: HabitTracker):
    if not tracker.habits:
        print("\nNo habits to analyze")
        return
    
    print(f"\n{'='*80}")
    print(f"📊 STATISTICS")
    print(f"{'='*80}\n")
    
    total_habits = len(tracker.habits)
    completed_today = len([h for h in tracker.habits if h.is_completed_today()])
    total_completions = sum(h.total_completions for h in tracker.habits)
    
    best_streak_habit = max(tracker.habits, key=lambda h: h.longest_streak)
    most_completed_habit = max(tracker.habits, key=lambda h: h.total_completions)
    
    print(f"Total Habits: {total_habits}")
    print(f"Completed Today: {completed_today}/{total_habits}")
    print(f"Total Completions (All Time): {total_completions}")
    print(f"\nBest Streak: {best_streak_habit.name} - {best_streak_habit.longest_streak} days 🏆")
    print(f"Most Completed: {most_completed_habit.name} - {most_completed_habit.total_completions} times")
    
    avg_completion_rate = sum(h.get_completion_rate() for h in tracker.habits) / total_habits
    print(f"Average Completion Rate: {avg_completion_rate:.1f}%")
    print()


def show_reminders(tracker: HabitTracker):
    incomplete = tracker.get_incomplete_habits_today()
    
    if not incomplete:
        print(f"\n{'='*80}")
        print("🎉 All habits completed for today! Great job!")
        print(f"{'='*80}\n")
        return
    
    print(f"\n{'='*80}")
    print(f"⏰ REMINDERS - Incomplete Habits Today")
    print(f"{'='*80}\n")
    
    for habit in incomplete:
        print(f"○ {habit.name}")
        print(f"  Current streak: {habit.current_streak} days")
        print(f"  Don't break the chain! ⛓️")
        print()


def main():
    tracker = HabitTracker()
    
    while True:
        print("\n" + "="*80)
        print("🎯 HABIT TRACKER")
        print("="*80)
        print("1.  Add Habit")
        print("2.  View All Habits")
        print("3.  Mark Habit Complete")
        print("4.  Unmark Habit")
        print("5.  View Weekly Chart (Single Habit)")
        print("6.  View All Habits Overview")
        print("7.  View Statistics")
        print("8.  View Reminders")
        print("9.  Delete Habit")
        print("10. Exit")
        
        choice = input("\nEnter choice (1-10): ").strip()
        
        if choice == "1":
            name = input("Habit name: ").strip()
            if not name:
                print("✗ Name cannot be empty")
                continue
            
            print("Frequency: daily/weekly (default: daily)")
            frequency = input("Enter frequency: ").strip().lower()
            frequency = frequency if frequency in ['daily', 'weekly'] else 'daily'
            
            target = input("Target days (default: 30): ").strip()
            target_days = int(target) if target.isdigit() else 30
            
            tracker.add_habit(name, frequency, target_days)
            
        elif choice == "2":
            print_habits_list(tracker.habits, "All Habits")
            
        elif choice == "3":
            print_habits_list(tracker.habits, "Habits")
            try:
                habit_id = int(input("Enter habit ID to mark complete: "))
                date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
                date = date_input if date_input else None
                tracker.mark_habit_complete(habit_id, date)
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == "4":
            print_habits_list(tracker.habits, "Habits")
            try:
                habit_id = int(input("Enter habit ID to unmark: "))
                date = input("Date (YYYY-MM-DD): ").strip()
                if date:
                    tracker.unmark_habit_complete(habit_id, date)
                else:
                    print("✗ Date required")
            except ValueError:
                print("✗ Invalid input")
                
        elif choice == "5":
            print_habits_list(tracker.habits, "Habits")
            try:
                habit_id = int(input("Enter habit ID to view chart: "))
                habit = tracker.get_habit_by_id(habit_id)
                if habit:
                    show_weekly_chart(habit)
                else:
                    print("✗ Habit not found")
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == "6":
            show_all_habits_overview(tracker.habits)
            
        elif choice == "7":
            show_statistics(tracker)
            
        elif choice == "8":
            show_reminders(tracker)
            
        elif choice == "9":
            print_habits_list(tracker.habits, "Habits")
            try:
                habit_id = int(input("Enter habit ID to delete: "))
                confirm = input(f"Are you sure? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    tracker.delete_habit(habit_id)
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == "10":
            print("Keep building those habits! 🚀")
            break
            
        else:
            print("✗ Invalid choice")


if __name__ == "__main__":
    main()