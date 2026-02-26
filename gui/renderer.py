import pygame

BG_COLOR = (25, 25, 35)
GRID_COLOR = (50, 50, 65)
WALL_COLOR = (40, 40, 50)
EXPLORED_COLOR = (0, 180, 255)
PATH_COLOR = (0, 255, 170)
TRAP_COLOR = (255, 70, 70)
START_COLOR = (255, 215, 0)
GOAL_COLOR = (180, 0, 255)
TEXT_COLOR = (220, 220, 220)
WARNING_COLOR = (255, 140, 0)
AGENT_COLOR = (0, 255, 120)

CELL = 30
TOP = 100
LEFT = 100


def draw(screen, font, maze, explored, path,
         agent, goal, algorithm, game_state):

    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, (35, 35, 50), (0, 0, 800, 80))

    title_font = pygame.font.SysFont("arial", 28, bold=True)
    title = title_font.render("AI Maze Solver", True, (0, 255, 200))
    screen.blit(title, (20, 20))

    controls = font.render(
        "1:BFS   2:DFS   3:A*   SPACE:Start   R:Reset",
        True, TEXT_COLOR)
    screen.blit(controls, (20, 55))

    algo_text = font.render(
        f"Algorithm: {algorithm}", True, (0, 200, 255))
    screen.blit(algo_text, (600, 20))

    lives_text = font.render(
        f"Lives: {agent.lives}", True, (255, 100, 100))
    screen.blit(lives_text, (600, 50))

    # ----- Maze -----
    for r in range(maze.rows):
        for c in range(maze.cols):

            x = c * CELL + LEFT
            y = r * CELL + TOP
            rect = pygame.Rect(x, y, CELL, CELL)

            pygame.draw.rect(screen, GRID_COLOR, rect)

            if maze.grid[r][c] == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)

            elif (r, c) in explored:
                pygame.draw.rect(screen, EXPLORED_COLOR, rect)

            elif (r, c) in path:
                pygame.draw.rect(screen, PATH_COLOR, rect)

            if (r, c) in maze.traps:
                pygame.draw.circle(screen, TRAP_COLOR, rect.center, 8)

            if maze.has_warning(r, c) and (r, c) not in maze.traps:
                pygame.draw.circle(screen, WARNING_COLOR,
                                   rect.center, 4)

            pygame.draw.rect(screen, (70, 70, 90), rect, 1)

    pygame.draw.rect(screen, START_COLOR,
                     (LEFT, TOP, CELL, CELL))

    gx = goal[1] * CELL + LEFT
    gy = goal[0] * CELL + TOP
    pygame.draw.rect(screen, GOAL_COLOR,
                     (gx, gy, CELL, CELL))

    ax = agent.pos[1] * CELL + LEFT + CELL // 2
    ay = agent.pos[0] * CELL + TOP + CELL // 2
    pygame.draw.circle(screen, (0, 100, 60), (ax, ay), 14)
    pygame.draw.circle(screen, AGENT_COLOR, (ax, ay), 10)

    # ----- Overlay Messages -----
    if game_state != "PLAYING":

        overlay = pygame.Surface((800, 700))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        big_font = pygame.font.SysFont("arial", 50, bold=True)
        small_font = pygame.font.SysFont("arial", 28)

        if game_state == "WON":
            main = "🎉 MISSION COMPLETE! 🎉"
            sub = "Intelligent Agent Reached Goal 🚀"

        elif game_state == "LOST":
            main = "💀 GAME OVER 💀"
            sub = "Agent Failed to Survive..."

        elif game_state == "NO_PATH":
            main = "🚫 NO PATH FOUND 🚫"
            sub = "Environment Has No Valid Solution"

        win_text = big_font.render(main, True, (0, 255, 170))
        sub_text = small_font.render(sub, True, (255, 255, 255))
        reset_text = small_font.render(
            "Press R to Play Again", True, (200, 200, 200))

        screen.blit(win_text, (140, 260))
        screen.blit(sub_text, (200, 330))
        screen.blit(reset_text, (250, 380))

    pygame.display.update()