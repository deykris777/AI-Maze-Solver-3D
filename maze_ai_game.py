import pygame
import sys
from core.maze import Maze
from core.search import bfs, dfs, astar
from core.agent import Agent
from gui.renderer import draw

pygame.init()

WIDTH, HEIGHT = 700, 700
CELL = 30
LEFT, TOP = 30, 90

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


# ✅ MAIN GAME LOOP (THIS WAS MISSING)
while True:

    clock.tick(60)

    draw(
        screen, font, maze, set(explored), set(path),
        agent, goal, algorithm,
        game_state, nodes_explored, path_length,
        None
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

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

            if event.key == pygame.K_SPACE:

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

                game_state = "ANIMATING"

                for step in path:

                    target_x, target_y = grid_to_pixel(*step)

                    frames = 15
                    dx = (target_x - agent.pixel_x) / frames
                    dy = (target_y - agent.pixel_y) / frames

                    for _ in range(frames):

                        pygame.event.pump()

                        agent.pixel_x += dx
                        agent.pixel_y += dy

                        draw(
                            screen, font, maze,
                            set(explored), set(path),
                            agent, goal, algorithm,
                            game_state, nodes_explored,
                            path_length, None
                        )

                        pygame.display.update()
                        clock.tick(60)

                    agent.move_to(step, maze.traps)

                    if agent.lives <= 0:
                        game_state = "LOST"
                        break

                    if step == goal:
                        game_state = "WON"
                        break