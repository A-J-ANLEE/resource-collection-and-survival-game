# *🪓🌲 Resource Survival Game (Ursina Engine)*

This is a simple 2D top-down resource collection and survival game built using the [Ursina Game Engine](https://www.ursinaengine.org/). You control an orange square character that can collect wood, stone, and gold, while avoiding red enemy bots that chase you!

## 🚀 *Features*

- ✅ Free-roaming top-down player movement  
- ✅ Collect resources: trees (wood), rocks (stone), and gold  
- ✅ Animated resource interaction with sounds  
- ✅ Enemy bots that chase and damage the player  
- ✅ Game Over system and health bar  
- ✅ Simple UI for resource tracking  
- ✅ 1-second sound effect playback for interactions

## 🕹️ *Controls*

| Key | Action              |
|-----|---------------------|
| W   | Move up             |
| A   | Move left           |
| S   | Move down           |
| D   | Move right          |
| LMB | Interact with objects (chop, mine, collect) |

## 🧠 *AI & Mechanics*

- Bots use **simple chase logic**: they move directly toward the player if within range.
- No advanced pathfinding (like A*), but can be added.
- Game ends when the player’s HP drops to 0.

## 📁 *Assets Folder Structure*


## 🔊 *Sound Behavior*

Sound effects play **only for 1 second**, regardless of the full clip duration. This is ideal for short feedback sounds and avoids overlapping noise.

## 🧱 *How to Run*

1. Install Ursina:
    ```bash
    pip install ursina
    ```

2. Run the game:
    ```bash
    python game.py
    ```

3. Enjoy playing!

**Author**: *A.J.ANLEE*  
**Engine**: [Ursina](https://www.ursinaengine.org/)  
**License**: MIT (MIT License.md)
