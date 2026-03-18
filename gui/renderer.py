import pygame

BG_COLOR = (20, 22, 35)
HEADER_COLOR = (30, 32, 50)
GRID_COLOR = (45, 48, 70)
WALL_COLOR = (25, 25, 30)
EXPLORED_COLOR = (0, 160, 255)
PATH_COLOR = (0, 255, 170)
TRAP_COLOR = (255, 70, 70)
GOAL_COLOR = (170, 0, 255)
TEXT_COLOR = (220, 220, 220)
WARNING_COLOR = (255, 140, 0)
AGENT_COLOR = (0, 255, 140)

CELL = 30
TOP = 90
LEFT = 30


def draw(screen, font, maze, explored, path,
         agent, goal, algorithm,
         game_state, nodes_explored, path_length,
         comparison_results):

    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, HEADER_COLOR, (0, 0, 700, 120))

    title_font = pygame.font.SysFont("arial", 28, bold=True)
    title = title_font.render("AI Maze Solver", True, (0, 255, 200))
    screen.blit(title, (20, 15))

    controls = font.render(
        "1:BFS  2:DFS  3:A*  SPACE:Run  C:Compare  R:Reset",
        True, TEXT_COLOR)
    screen.blit(controls, (20, 55))

    algo_text = font.render(f"Algorithm: {algorithm}", True, (0, 200, 255))
    screen.blit(algo_text, (450, 20))

    metrics1 = font.render(f"Explored Nodes: {nodes_explored}", True, TEXT_COLOR)
    metrics2 = font.render(f"Path Length: {path_length}", True, TEXT_COLOR)

    screen.blit(metrics1, (20, 85))
    screen.blit(metrics2, (250, 85))

    for i in range(agent.lives):
        pygame.draw.circle(screen, (255, 60, 60), (600 + i * 25, 40), 10)

    for r in range(maze.rows):
        for c in range(maze.cols):

            x = c * CELL + LEFT
            y = r * CELL + TOP
            rect = pygame.Rect(x, y, CELL, CELL)

            pygame.draw.rect(screen, GRID_COLOR, rect)

            if (r, c) in explored:
                pygame.draw.rect(screen, EXPLORED_COLOR, rect)

            if (r, c) in path:
                pygame.draw.rect(screen, PATH_COLOR, rect)

            if maze.grid[r][c] == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)

            if (r, c) in maze.traps:
                pygame.draw.circle(screen, TRAP_COLOR, rect.center, 8)

            if maze.has_warning(r, c) and (r, c) not in maze.traps:
                pygame.draw.circle(screen, WARNING_COLOR, rect.center, 4)

            pygame.draw.rect(screen, (60, 60, 80), rect, 1)

    gx = goal[1] * CELL + LEFT
    gy = goal[0] * CELL + TOP
    pygame.draw.rect(screen, GOAL_COLOR, (gx, gy, CELL, CELL))

    pygame.draw.circle(screen, (0, 80, 60),
                       (int(agent.pixel_x), int(agent.pixel_y)), 14)
    pygame.draw.circle(screen, AGENT_COLOR,
                       (int(agent.pixel_x), int(agent.pixel_y)), 10)

    # -------- GAME STATUS OVERLAY --------
    if game_state in ["WON", "LOST", "NO_PATH"]:

        overlay = pygame.Surface((700, 700))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        big_font = pygame.font.SysFont("arial", 48, bold=True)

        if game_state == "WON":
            message = "MISSION COMPLETE 🎉"

        elif game_state == "LOST":
            message = "AGENT FAILED 💀"

        else:
            message = "NO PATH FOUND"

        text = big_font.render(message, True, (0, 255, 200))
        screen.blit(text, (120, 300))

        small_font = pygame.font.SysFont("arial", 24)
        reset_text = small_font.render("Press R to Reset", True, (255,255,255))
        screen.blit(reset_text, (260, 360))
    pygame.display.update()