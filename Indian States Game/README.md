#  Indian States Game

An interactive educational game built with Python that helps you learn and memorize the 28 states of India through an engaging guessing game interface.

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Description

The Indian States Game is a fun and educational application that displays a map of India and challenges players to identify all 28 states by typing their names. As you correctly guess each state, its name appears on the map at the appropriate location. The game tracks your progress and generates a report of any states you missed.

## ✨ Features

- **Interactive Map Interface**: Beautiful visual representation of India with state boundaries
- **Real-time Progress Tracking**: Shows how many states you've correctly identified (e.g., "15/28")
- **Smart Name Recognition**: Uses title case formatting to accept various input formats
- **Exit Anytime**: Type "exit" to quit the game before completing all states
- **Missed States Report**: Automatically generates a CSV file with states you couldn't guess
- **Visual Feedback**: Correctly guessed states appear on the map at their geographic locations

## 🚀 Getting Started

### Prerequisites

Before running the application, ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/).

### Required Dependencies

Install the required Python packages using pip:

```bash
pip install pandas
```

**Note:** The `turtle` module comes pre-installed with Python's standard library.

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd "indian states game"
   ```

2. **Verify required files are present:**
   - `main.py` - Main application file
   - `states.csv` - Database of state names and coordinates
   - `indiamap.gif` - Map image of India
   - `missed_states.csv` - Generated after game ends (contains missed states)

## 🎮 How to Play

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **The game window will open** displaying a map of India

3. **A text input dialog will appear** asking you to guess a state name

4. **Type the name of an Indian state** and press Enter
   - Correct guesses will appear on the map
   - The title bar shows your progress (e.g., "5/28")

5. **Continue guessing** until you've identified all 28 states or type "exit" to quit

6. **After the game ends**, click anywhere on the map to close the window

7. **Check `missed_states.csv`** to see which states you didn't guess

## 📁 Project Structure

```
indian states game/
│
├── main.py                 # Main application file
├── states.csv              # State names with X, Y coordinates
├── indiamap.gif           # Background map image
├── missed_states.csv      # Generated file with missed states
└── README.md              # This file
```

## 📊 File Descriptions

### `main.py`
The main Python script that:
- Loads state data from CSV
- Displays the India map using Turtle graphics
- Handles user input and game logic
- Tracks progress and validates answers
- Generates the missed states report

### `states.csv`
Contains three columns:
- `states`: Names of all 28 Indian states
- `x`: X-coordinate for label placement on map
- `y`: Y-coordinate for label placement on map

### `missed_states.csv`
Auto-generated after each game session, listing all states you didn't guess (useful for learning).

## 🎯 Game Tips

- State names are case-insensitive (the game converts to title case)
- Focus on geographical regions to systematically identify states
- The progress counter helps you track how many states remain
- Use the missed states report to improve your knowledge for next time

## 🔧 Troubleshooting

### File Not Found Errors
Ensure all required files (`states.csv`, `indiamap.gif`) are in the same directory as `main.py`.

### Module Import Errors
Install pandas if you get an import error:
```bash
pip install pandas
```

### Map Not Displaying
Make sure the `indiamap.gif` file is not corrupted and is in the correct directory.

## 🛠️ Technical Details

**Built With:**
- **Python 3.x** - Core programming language
- **Turtle Graphics** - For GUI and map visualization
- **Pandas** - For data management and CSV operations

**Key Concepts Demonstrated:**
- File I/O operations
- Data manipulation with Pandas
- GUI programming with Turtle
- List comprehensions and data structures
- User input handling and validation

## 📝 Code Highlights

```python
# Smart state validation
if answer in state_list:
    entered_states.append(answer)
    # Display state name on map at correct coordinates
    ttl.goto(x=int(df[df["states"] == answer].x), 
             y=int(df[df["states"] == answer].y))
    ttl.write(answer)
```

## 🎓 Educational Value

This game helps with:
- **Geography Education**: Learn locations of Indian states
- **Memory Training**: Improve recall of state names
- **Interactive Learning**: Engage with educational content in a fun way

## 🔮 Future Enhancements

Potential improvements for future versions:
- [ ] Add state capitals quiz mode
- [ ] Include Union Territories
- [ ] Timer-based challenges
- [ ] Difficulty levels (hints, multiple attempts)
- [ ] High score tracking
- [ ] State facts and trivia display
- [ ] Color-coding by region

## 👨‍💻 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 🙏 Acknowledgments

- Map data based on the geography of India
- Built as an educational tool for learning Indian geography
- Inspired by similar geography learning games

## 📧 Contact

For questions, suggestions, or feedback, please open an issue in the repository.

---

**Happy Learning! 🎉**

Remember: Practice makes perfect. Play multiple times to master all 28 states!
