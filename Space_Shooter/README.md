# 2D Platformer Game

A simple 2D platformer game built with Pygame featuring player movement, collectibles, enemies, and physics-based gameplay.

## Features

- **Player Movement**: Left/right movement with acceleration and friction
- **Advanced Jumping**: Variable jump height, double-jump, coyote time, and jump buffering
- **Physics System**: Gravity-based movement with realistic collision detection
- **Game Elements**:
  - Collectible coins that increase your score
  - Patrolling enemies that reset the level on contact
  - Goal area to complete the level
- **Camera System**: Smooth camera that follows the player
- **Level Design**: Tile-based level system that's easy to modify

## Controls

- **Movement**: A/D keys or Arrow keys (←/→)
- **Jump**: Spacebar, W key, or Up arrow (↑)
- **Restart**: R key

## Game Mechanics

### Movement System
- Smooth acceleration and deceleration
- Different friction values for ground and air movement
- Maximum speed limits for balanced gameplay

### Jump System
- **Variable Jump Height**: Hold jump longer for higher jumps
- **Double Jump**: Second jump available while in air
- **Coyote Time**: Brief window to jump after leaving a platform
- **Jump Buffering**: Jump input registers slightly before landing

### Level Elements
- `G`/`B`: Ground and brick platforms
- `C`: Collectible coins
- `E`: Patrolling enemies
- `P`: Player starting position
- `F`: Level finish goal

## Installation

1. Install Python 3.6 or higher
2. Install Pygame:
   ```bash
   pip install pygame
   ```

## Running the Game

```bash
python space.py
```

## Customization

### Modifying the Level

Edit the `LEVEL_MAP` list to create custom levels:

```python
LEVEL_MAP = [
    "                            ",
    "      C             C       ",
    "            BBB             ",
    "        BBB         C     F ",
    "   P                        ",
    "BBBBBBBB     BBBBBBB    BBBB",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBB",
]
```

### Adjusting Game Physics

Modify the constants at the top of the file:

- `GRAVITY`: Controls fall speed
- `JUMP_SPEED`: Initial jump velocity
- `MAX_MOVE_SPEED`: Maximum horizontal speed
- `COYOTE_TIME`: Grace period for jumping after leaving ground
- `JUMP_BUFFER_TIME`: Input buffer for jump timing

### Visual Customization

Change colors by modifying the color constants:
- `SKY`: Background color
- `GREEN`: Player color
- `BROWN`: Platform color
- `GOLD`: Coin color
- `RED`: Enemy color

## Code Structure

- **Camera**: Handles viewport and follows player movement
- **Platform**: Static ground and brick tiles
- **Coin**: Collectible items that increase score
- **Enemy**: Moving obstacles with patrol behavior
- **Player**: Main character with physics and input handling
- **Game Loop**: Handles events, updates, collisions, and rendering

## Requirements

- Python 3.6+
- Pygame 2.0+

## License

This project is open source and available under the MIT License.