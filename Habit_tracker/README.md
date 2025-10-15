# 🎯 Habit Tracker

A comprehensive habit tracking application that helps you build consistency through streak tracking, progress visualization, and daily reminders.

## ✨ Features

- **Streak Tracking**: Monitor current and longest streaks to stay motivated
- **Progress Visualization**: Weekly charts and overview of all habits
- **Smart Reminders**: Get notified about incomplete habits
- **Completion Statistics**: Track completion rates and total achievements
- **Historical Data**: Mark habits complete for past dates
- **Flexible Tracking**: Support for daily and weekly habits
- **Persistent Storage**: All data saved in JSON format

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Setup
1. Download the project files
2. No external dependencies required!

```bash
python main.py
```

## 📖 Usage

### Main Menu Options

1. **Add Habit**: Create a new habit to track
2. **View All Habits**: See all your habits with current status
3. **Mark Habit Complete**: Log completion for today or any past date
4. **Unmark Habit**: Remove a completion entry
5. **View Weekly Chart**: See 7-day progress for a specific habit
6. **View All Habits Overview**: Grid view of all habits for the week
7. **View Statistics**: Overall performance metrics
8. **View Reminders**: See incomplete habits for today
9. **Delete Habit**: Remove a habit permanently
10. **Exit**: Save and quit

### Adding a Habit

```
Habit name: Morning Exercise
Frequency: daily/weekly (default: daily)
Enter frequency: daily
Target days (default: 30): 30
```

### Viewing Progress

The app provides multiple visualization options:

**Individual Weekly Chart:**
```
📊 Weekly Progress: Morning Exercise
=====================================
     Mon    Tue    Wed    Thu    Fri    Sat    Sun
   01/06  01/07  01/08  01/09  01/10  01/11  01/12
     ✓✓     ✓✓     ○○     ✓✓     ✓✓     ○○     ✓✓

This week: 5/7 days completed
```

**All Habits Overview:**
```
📈 ALL HABITS OVERVIEW
==================================================
Habit                   01/06  01/07  01/08  01/09  Streak
--------------------------------------------------
Morning Exercise          ✓      ✓      -      ✓    🔥 2
Read 30 Minutes           ✓      ✓      ✓      ✓    🔥 4
Meditation                -      ✓      -      ✓    🔥 1
```

## 🎯 Understanding Streaks

- **Current Streak**: Consecutive days you've completed the habit (up to yesterday or today)
- **Longest Streak**: Your best streak ever
- **🔥 Fire emoji**: Active streak
- **💤 Sleep emoji**: No active streak

### Streak Rules
- Completing a habit today or yesterday keeps the streak alive
- Missing a day breaks the streak
- Historical entries update streaks retroactively

## 📊 Statistics

The app tracks:
- Total number of habits
- Completion rate (percentage)
- Total completions across all habits
- Best performing habits
- Average completion rates

## 🔔 Reminders

View incomplete habits for the day:
```
⏰ REMINDERS - Incomplete Habits Today
=====================================
○ Morning Exercise
  Current streak: 5 days
  Don't break the chain! ⛓️

○ Read 30 Minutes
  Current streak: 0 days
  Don't break the chain! ⛓️
```

## 💾 Data Storage

All data is stored in `habits.json` in the same directory:

```json
[
  {
    "id": 12345,
    "name": "Morning Exercise",
    "frequency": "daily",
    "target_days": 30,
    "created_at": "2025-01-01",
    "completion_dates": ["2025-01-01", "2025-01-02", "2025-01-03"],
    "current_streak": 3,
    "longest_streak": 5,
    "total_completions": 15
  }
]
```

## 🎓 Tips for Success

1. **Start Small**: Begin with 1-3 habits you want to build
2. **Be Consistent**: Aim for daily completion, even if brief
3. **Track Honestly**: Mark habits only when truly completed
4. **Use Reminders**: Check incomplete habits daily
5. **Celebrate Streaks**: Acknowledge your progress milestones
6. **Don't Break the Chain**: Visual streaks are powerful motivators
7. **Review Statistics**: Weekly reviews help identify patterns
8. **Set Realistic Targets**: 30-day targets work well for habit formation

## 📅 Best Practices

### For Daily Habits
- Morning routines (exercise, meditation)
- Reading or learning sessions
- Health habits (water intake, vitamins)
- Creative practice (writing, drawing)

### For Weekly Habits
- Deep cleaning
- Meal prep
- Financial review
- Relationship check-ins

## 🔧 Advanced Features

### Historical Tracking
You can mark habits complete for past dates:
```
Enter habit ID to mark complete: 12345
Date (YYYY-MM-DD, press Enter for today): 2025-01-10
```

### Unmarking Entries
Made a mistake? Remove a completion:
```
Enter habit ID to unmark: 12345
Date (YYYY-MM-DD): 2025-01-10
```

## 📈 Tracking Metrics

The app calculates:
- **Completion Rate**: (Total completions / Days since creation) × 100
- **Current Streak**: Consecutive days including today/yesterday
- **Longest Streak**: Best consecutive streak ever
- **Total Completions**: Lifetime count

## 🎯 Example Use Cases

### Building a Morning Routine
```
1. Morning Exercise (Target: 30 days)
2. Meditation (Target: 30 days)
3. Healthy Breakfast (Target: 30 days)
```

### Learning Goals
```
1. Read 30 Minutes (Target: 60 days)
2. Code Practice (Target: 100 days)
3. Language Learning (Target: 90 days)
```

### Health & Wellness
```
1. 8 Hours Sleep (Target: 30 days)
2. 10K Steps (Target: 30 days)
3. No Social Media Before Bed (Target: 30 days)
```

## 🐛 Troubleshooting

**Streaks not calculating correctly?**
- The app recalculates streaks each time you mark/unmark
- Ensure dates are in YYYY-MM-DD format

**Can't see my habit?**
- Check if it was deleted accidentally
- Verify the habits.json file exists

**Statistics seem wrong?**
- Completion rate is based on days since creation
- Historical entries affect all calculations

## 🔮 Future Enhancements

Potential additions:
- Daily/weekly/monthly goals with notifications
- Export data to CSV/PDF
- Graphs and charts with matplotlib
- Habit categories/tags
- Notes for each completion
- Mobile app integration
- Social features (share streaks)

## 📝 Technical Details

- **Language**: Python 3.7+
- **Dependencies**: None (standard library only)
- **Storage**: JSON file-based
- **File Size**: ~10KB

## 🤝 Contributing

Feel free to fork and enhance! Some ideas:
- Add color output for terminal
- Implement reminder notifications
- Create data visualization exports
- Add habit templates

## 📄 License

Free to use and modify for personal and commercial projects.

---

**Build better habits, one day at a time! 🎯🔥**