# AI Maze Solver 3D 🧩🤖

An interactive, dual-engine Python game that allows users to manually navigate through a randomly generated maze or watch an AI solve it in real-time.

## Screenshots

<p align="center">
  <img src="screenshots/s1.png" width="45%" border="1" alt="Screenshot 1"/>
  <img src="screenshots/s2.png" width="45%" border="1" alt="Screenshot 2"/>
  <br>
  <img src="screenshots/s4.png" width="45%" border="1" alt="Screenshot 4"/>
  <img src="screenshots/s5.png" width="45%" border="1" alt="Screenshot 5"/>
</p>

## Project Overview

"AI Maze Solver" contains two distinct versions of the game built on the same core logic:
1. **A 3D Version (`maze_3d.py`)**: Built using the `ursina` engine. Features dynamic lighting, 3D models (the player uses an Iron Man `Octane.obj` model), a minimap, and three different camera views (First-Person, Top-Down, Isometric).
2. **A 2D Version (`maze_ai_game.py`)**: Built using `pygame`. Serves as a classic, lightweight, top-down 2D version of the maze solver with burst animations for traps.

## Core Mechanics & Features

- **Two Play Modes**: 
  - **USER Mode**: The player manually navigates the maze using arrow keys.
  - **AI Mode**: The user sets the agent to autonomously find the goal using pathfinding algorithms.
- **Three Search Algorithms (AI Mode)**:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search (A-Star)
- **Procedural Maze Generation**: The maze walls and traps are randomly generated via a custom `Maze` class every time the game resets or advances.
- **Traps / Obstacles**: The grid contains hidden/visible traps. Stepping on one deducts a life (the player starts with 3 lives), flashes the screen/shows a blast animation, and plays a sound effect. If lives reach 0, you lose.
- **Level Progression (3D Version)**: Upon reaching the goal (purple beacon in 3D), a win screen appears, and the game automatically advances to the next level, increasing the grid dimensions (spawning a larger maze).
- **Statistical HUD**: Both versions display an on-screen overlay tracking: nodes explored by the AI, path length, move count, current level, current algorithm, and remaining lives.

## Controls

### Global Controls
- `M`: Toggle Play Mode between 'USER' and 'AI'.
- `R`: Reset the current game/maze.

### AI Mode Controls
- `1`: Select BFS Algorithm
- `2`: Select DFS Algorithm
- `3`: Select A* Algorithm
- `Spacebar`: Start AI Solver (visualizes the search exploration, then animates the agent moving along the solved path)

### USER Mode Controls
- `Arrow Keys`: Move the character manually (Up, Down, Left, Right). Movement adapts to camera orientation in the 3D version.

### 3D Exclusive Controls (`maze_3d.py`)
- `C`: Toggle Camera Mode between `FIRST_PERSON`, `TOP_DOWN`, and `ISOMETRIC`.

## Tech Stack / Dependencies

- **Python 3.x**
- **Ursina Engine (`ursina`)**: For the 3D game environment, models, and shaders.
- **Pygame (`pygame`)**: For the 2D game environment and font rendering.
- **Structure**: The codebase is neatly separated:
  - `core/maze.py`: Maze generation logic.
  - `core/search.py`: Pathfinding algorithms (BFS, DFS, A*).
  - `core/agent.py`: Agent state tracking.
  - `assets/`: Holds 3D models and textures (e.g., Iron Man model, brick textures).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deykris777/AI-Maze-Solver-3D.git
   cd AI-Maze-Solver-3D
   ```
2. **Install dependencies:**
   Make sure to install `ursina` and `pygame`.
   ```bash
   pip install ursina pygame
   ```
   *(Or standard `pip install -r requirements.txt` if available)*
3. **Run the 3D version:**
   ```bash
   python maze_3d.py
   ```
4. **Run the 2D version:**
   ```bash
   python maze_ai_game.py
   ```

Enjoy navigating the maze or watching the artificial intelligence explore the path for you!
