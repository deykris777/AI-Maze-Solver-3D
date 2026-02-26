import pygame
import sys
from core.maze import Maze
from core.search import bfs, dfs, astar
from core.agent import Agent
from gui.renderer import draw

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("AI Maze Solver")
font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()

ROWS = 20
COLS = 20
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

def new_game():
    maze = Maze(ROWS, COLS)
    agent = Agent(start, 3)
    return maze, agent, [], []

maze, agent, explored, path = new_game()
algorithm = "BFS"

game_state = "PLAYING"  
# PLAYING | WON | LOST | NO_PATH

while True:
    clock.tick(60)

    draw(screen, font, maze, set(explored), set(path),
         agent, goal, algorithm, game_state)

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:

            if e.key in (pygame.K_1, pygame.K_KP1):
                algorithm = "BFS"

            elif e.key in (pygame.K_2, pygame.K_KP2):
                algorithm = "DFS"

            elif e.key in (pygame.K_3, pygame.K_KP3):
                algorithm = "A*"

            elif e.key == pygame.K_r:
                maze, agent, explored, path = new_game()
                game_state = "PLAYING"

            elif e.key == pygame.K_SPACE and game_state == "PLAYING":

                if algorithm == "BFS":
                    path, explored = bfs(maze, start, goal)
                elif algorithm == "DFS":
                    path, explored = dfs(maze, start, goal)
                else:
                    path, explored = astar(maze, start, goal)

                if not path:
                    game_state = "NO_PATH"
                    continue

                # Animate exploration
                for node in explored:
                    draw(screen, font, maze,
                         set(explored[:explored.index(node)+1]),
                         set(), agent, goal, algorithm, game_state)
                    pygame.time.delay(15)

                # Animate path
                for step in path:
                    agent.move(step, maze.traps)

                    draw(screen, font, maze,
                         set(explored), set(path),
                         agent, goal, algorithm, game_state)

                    pygame.time.delay(70)

                    if agent.lives <= 0:
                        game_state = "LOST"
                        break

                    if step == goal:
                        game_state = "WON"
                        break