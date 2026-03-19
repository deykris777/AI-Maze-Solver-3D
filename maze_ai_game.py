import pygame
import sys
from core.maze import Maze
from core.search import bfs, dfs, astar
from core.agent import Agent
from gui.renderer import draw

pygame.init()

WIDTH, HEIGHT = 700, 750
CELL = 30
LEFT, TOP = 35, 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze Solver")

font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()

ROWS = 21
COLS = 21

start = (0, 0)
goal = (ROWS - 1, COLS - 1)


def grid_to_pixel(r, c):
    x = c * CELL + LEFT + CELL // 2
    y = r * CELL + TOP + CELL // 2
    return x, y


def new_game():
    maze = Maze(ROWS, COLS)
    agent = Agent(start, 3)

    px, py = grid_to_pixel(*start)
    agent.set_pixel_position(px, py)

    return maze, agent, [], []


maze, agent, explored, path = new_game()

algorithm = "BFS"
nodes_explored = 0
path_length = 0
game_state = "IDLE"
play_mode = "AI"

import math

def take_step(step):
    global game_state, path_length, play_mode
    
    target_x, target_y = grid_to_pixel(*step)
    
    # Update dynamic rotation of the agent
    if step[0] > agent.pos[0]: agent.angle = 180   # DOWN
    elif step[0] < agent.pos[0]: agent.angle = 0   # UP
    elif step[1] > agent.pos[1]: agent.angle = 90  # RIGHT
    elif step[1] < agent.pos[1]: agent.angle = -90 # LEFT

    frames = 15
    dx = (target_x - agent.pixel_x) / frames
    dy = (target_y - agent.pixel_y) / frames

    for _ in range(frames):
        pygame.event.pump()
        agent.pixel_x += dx
        agent.pixel_y += dy
        draw(screen, font, maze, set(explored), set(path), agent, goal, algorithm, game_state, nodes_explored, path_length, None, play_mode)
        pygame.display.update()
        clock.tick(60)

    agent.move_to(step, maze.traps)

    # Play sound and animate burst on collision
    if step in maze.traps:
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONHAND)
        except ImportError:
            pass

        # Remove the trap visually
        maze.traps.remove(step)

        # Burst Animation
        for radius in range(0, 45, 3):
            pygame.event.pump()
            draw(screen, font, maze, set(explored), set(path), agent, goal, algorithm, game_state, nodes_explored, path_length, None, play_mode)
            # Draw expanding blast particles
            for j in range(12):
                angle = j * (math.pi / 6)
                r_offset = radius + (j % 2) * 8
                px = target_x + math.cos(angle) * r_offset
                py = target_y + math.sin(angle) * r_offset
                size = max(1, 10 - radius // 4)
                
                # Outer fire
                pygame.draw.circle(screen, (250, 80, 50), (int(px), int(py)), size)
                # Inner core
                if size > 3:
                    pygame.draw.circle(screen, (255, 220, 100), (int(px), int(py)), size - 2)

            pygame.display.update()
            clock.tick(60)

    if agent.lives <= 0:
        game_state = "LOST"
        return False
        
    if step == goal:
        game_state = "WON"
        return False
        
    return True


# ✅ MAIN GAME LOOP (THIS WAS MISSING)
while True:

    clock.tick(60)

    draw(
        screen, font, maze, set(explored), set(path),
        agent, goal, algorithm,
        game_state, nodes_explored, path_length,
        None, play_mode
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_m:
                if play_mode == "AI":
                    play_mode = "USER"
                else:
                    play_mode = "AI"
                maze, agent, explored, path = new_game()
                nodes_explored = 0
                path_length = 0
                game_state = "IDLE"

            if play_mode == "AI":
                if event.key == pygame.K_1:
                    algorithm = "BFS"
                if event.key == pygame.K_2:
                    algorithm = "DFS"
                if event.key == pygame.K_3:
                    algorithm = "A*"

            if event.key == pygame.K_r:
                maze, agent, explored, path = new_game()
                nodes_explored = 0
                path_length = 0
                game_state = "IDLE"

            # MANUAL USER MOVEMENT
            if play_mode == "USER" and game_state not in ["WON", "LOST", "ANIMATING", "EXPLORING"]:
                dr, dc = 0, 0
                if event.key == pygame.K_UP: dr, dc = -1, 0
                elif event.key == pygame.K_DOWN: dr, dc = 1, 0
                elif event.key == pygame.K_LEFT: dr, dc = 0, -1
                elif event.key == pygame.K_RIGHT: dr, dc = 0, 1
                
                if dr != 0 or dc != 0:
                    r, c = agent.pos
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if maze.grid[nr][nc] == 0:
                            path.append((nr, nc)) # leave trail
                            path_length = len(path)
                            prev_state = game_state
                            game_state = "ANIMATING"
                            
                            is_alive = take_step((nr, nc))
                            
                            if is_alive and game_state == "ANIMATING":
                                game_state = prev_state

            if event.key == pygame.K_SPACE and play_mode == "AI":

                if algorithm == "BFS":
                    path, explored = bfs(maze, start, goal)

                elif algorithm == "DFS":
                    path, explored = dfs(maze, start, goal)

                else:
                    path, explored = astar(maze, start, goal)

                nodes_explored = len(explored)
                path_length = len(path)

                if not path:
                    game_state = "NO_PATH"
                    continue

                game_state = "EXPLORING"
                steps_per_frame = max(1, len(explored) // 90) # Finish roughly around 1.5 seconds max
                
                for i in range(0, len(explored), steps_per_frame):
                    pygame.event.pump()
                    current_explored = explored[:i+steps_per_frame]
                    draw(
                        screen, font, maze,
                        set(current_explored), set(), 
                        agent, goal, algorithm,
                        game_state, len(current_explored),
                        0, None, play_mode
                    )
                    pygame.display.update()
                    clock.tick(60)
                game_state = "ANIMATING"

                for step in path:
                    if not take_step(step):
                        break