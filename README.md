# 🧩 AI Maze Solver 3D

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Ursina](https://img.shields.io/badge/Ursina-Engine-purple?style=for-the-badge)
![Pygame](https://img.shields.io/badge/Pygame-2D-green?style=for-the-badge&logo=pygame&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A dual-engine Python maze game where you can challenge yourself manually — or sit back and watch an AI figure it out.**

*Featuring real-time pathfinding visualization, a true 3D environment, procedurally generated mazes, and an Iron Man character model.*

</div>

---

## 📸 Screenshots

> **3D Version — First-Person View**

<!-- Add your first-person screenshot or GIF here -->
```
[ Screenshot / GIF: First-person corridor view — maze_3d.py ]
```

> **3D Version — Isometric View with AI Path Highlighted**

<!-- Add your isometric AI solve screenshot or GIF here -->
```
[ Screenshot / GIF: Isometric view, green BFS path overlaid — maze_3d.py ]
```

> **3D Version — Top-Down View with Minimap**

<!-- Add your top-down screenshot here -->
```
[ Screenshot / GIF: Top-down camera, minimap visible — maze_3d.py ]
```

> **2D Version — AI Exploration in Progress**

<!-- Add your 2D pygame screenshot or GIF here -->
```
[ Screenshot / GIF: 2D pygame version, BFS frontier expanding — maze_ai_game.py ]
```

---

## ✨ Features

### 🎮 Gameplay
- 🧠 **Dual Play Modes** — Play manually with arrow keys or let the AI take the wheel
- 🪜 **Level Progression** — Beat the maze to advance to a larger, harder one (3D version)
- 💣 **Traps & Hazards** — Hidden traps scattered across the grid; step on one and lose a life with a satisfying blast animation
- ❤️ **Lives System** — You start with 3 lives; hit zero and it's game over
- 🔄 **Procedural Generation** — Every reset spawns a brand-new, randomly generated maze

### 🤖 AI & Algorithms
- 🔍 **BFS (Breadth-First Search)** — Guarantees the shortest path; explores level by level
- 🌲 **DFS (Depth-First Search)** — Goes deep fast; path not always optimal, but visually dramatic
- ⭐ **A\* Search** — Heuristic-guided; the smartest and most efficient of the three
- 🎬 **Real-Time Visualization** — Watch the AI's exploration frontier expand across the maze before it locks in the final path

### 🌐 3D Version (`maze_3d.py`)
- 🎥 **Three Camera Modes** — Switch between First-Person, Top-Down, and Isometric perspectives
- 🦸 **Iron Man Character Model** — The agent uses a custom `Octane.obj` 3D model
- 💡 **Dynamic Lighting & Shaders** — Powered by the Ursina engine
- 🗺️ **Live Minimap** — Always know where you are in the maze

### 🕹️ 2D Version (`maze_ai_game.py`)
- 🎆 **Burst Animations** — Animated particle explosion when a trap is triggered
- 🔊 **Sound Effects** — Platform-native audio feedback on trap collision
- ⚡ **Lightweight** — Pure Pygame; runs on any machine without a GPU

### 📊 HUD & Statistics
- Tracks **nodes explored**, **path length**, **move count**, **current level**, **algorithm in use**, and **remaining lives** — all displayed live on screen

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **3D Engine** | [Ursina Engine](https://www.ursinaengine.org/) |
| **2D Engine** | [Pygame](https://www.pygame.org/) |
| **Language** | Python 3.x |
| **3D Model** | Custom `.obj` (Iron Man / Octane) |
| **Pathfinding** | Custom BFS, DFS, A* implementations |
| **Maze Generation** | Recursive procedural generation |

---

## 📁 Project Structure

```
AI-Maze-Solver-3D/
│
├── maze_3d.py              # 🌐 3D version entry point (Ursina engine)
├── maze_ai_game.py         # 🕹️  2D version entry point (Pygame)
│
├── core/
│   ├── maze.py             # Procedural maze & trap generation
│   ├── search.py           # BFS, DFS, and A* algorithms
│   └── agent.py            # Agent state: position, lives, movement
│
├── gui/
│   └── renderer.py         # 2D rendering & HUD drawing (Pygame)
│
├── assets/
│   └── textures/           # Wall/floor textures & 3D model files
│       └── Octane.obj      # Iron Man 3D model
│
└── requirements.txt
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/deykris777/AI-Maze-Solver-3D.git
cd AI-Maze-Solver-3D
```

### 2. (Recommended) Create a Virtual Environment

```bash
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> The key dependencies are `ursina` (for the 3D version) and `pygame` (for the 2D version).

### 4. Run the Game

**▶️ 3D Version (Ursina Engine):**
```bash
python maze_3d.py
```

**▶️ 2D Version (Pygame):**
```bash
python maze_ai_game.py
```

---

## 🎮 Controls

### Global Controls (Both Versions)

| Key | Action |
|-----|--------|
| `M` | Toggle between **USER** mode and **AI** mode |
| `R` | Reset / generate a new maze |

### AI Mode Controls

| Key | Action |
|-----|--------|
| `1` | Select **BFS** (Breadth-First Search) |
| `2` | Select **DFS** (Depth-First Search) |
| `3` | Select **A\*** (A-Star Search) |
| `Space` | 🚀 Run the selected AI algorithm — visualizes exploration, then animates the path |

### USER Mode Controls

| Key | Action |
|-----|--------|
| `↑` `↓` `←` `→` | Move the character |

> In the 3D version, movement direction adapts to the active camera orientation.

### 3D Exclusive Controls (`maze_3d.py`)

| Key | Action |
|-----|--------|
| `C` | Cycle camera: **First-Person → Top-Down → Isometric** |

---

## 🧠 How It Works

### Procedural Maze Generation

Each time a new maze is created, the `Maze` class generates a grid of walls and open paths using a randomized algorithm, ensuring the maze is always solvable. Traps are then scattered randomly across passable cells. In the 3D version, advancing a level increases the grid dimensions, making each successive maze larger and more complex.

### AI Pathfinding Algorithms

All three algorithms operate on the same grid graph. The key difference is their exploration strategy:

| Algorithm | Strategy | Path Quality | Speed |
|-----------|----------|-------------|-------|
| **BFS** | Explores all neighbors level by level (queue) | ✅ Always shortest | Moderate |
| **DFS** | Dives deep along one branch before backtracking (stack) | ❌ Not guaranteed shortest | Fast to find *a* path |
| **A\*** | Uses a heuristic (Manhattan distance) to prioritize promising nodes | ✅ Optimal (with admissible heuristic) | Fastest in practice |

When you press `Space` in AI mode, the game first animates the full exploration frontier (showing every node the algorithm visits), and then smoothly moves the agent along the discovered solution path — making it easy to compare how each algorithm "thinks."

### The Agent

The `Agent` class tracks the player's grid position, pixel position (for smooth interpolation), rotation angle, and remaining lives. Movement is animated over multiple frames, giving the character fluid motion rather than snapping between cells.

---

## 🗺️ Minimap Legend

| Color | Meaning |
|-------|---------|
| ⬜ White / Grey | Open path |
| ⬛ Black | Wall |
| 🔴 Red | Trap location |
| 🔵 Cyan | Agent (current position) |
| 🟣 Magenta | Goal / Exit |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/cool-new-thing`
3. Commit your changes: `git commit -m 'Add cool new thing'`
4. Push to the branch: `git push origin feature/cool-new-thing`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ and Python · *"The maze is not the challenge — the algorithm is."*

</div>
