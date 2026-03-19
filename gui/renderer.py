import pygame

WALL_IMG_PATH = r"C:\Users\KIIT0001\.gemini\antigravity\brain\e4e3097a-8e8e-4f98-83de-70cd2ea1add4\wall_tile_1773858742739.png"
FLOOR_IMG_PATH = r"C:\Users\KIIT0001\.gemini\antigravity\brain\e4e3097a-8e8e-4f98-83de-70cd2ea1add4\floor_tile_1773858758624.png"
TRAP_IMG_PATH = r"C:\Users\KIIT0001\.gemini\antigravity\brain\e4e3097a-8e8e-4f98-83de-70cd2ea1add4\trap_tile_1773858772562.png"

_CACHE = {}

def get_texture(path, size):
    if path not in _CACHE:
        try:
            img = pygame.image.load(path).convert_alpha()
            _CACHE[path] = pygame.transform.scale(img, (size, size))
        except Exception as e:
            surf = pygame.Surface((size, size))
            surf.fill((255, 0, 255))
            _CACHE[path] = surf
    return _CACHE[path]

def get_overlay(color, alpha, size):
    key = (color, alpha, size)
    if key not in _CACHE:
        s = pygame.Surface((size, size))
        s.set_alpha(alpha)
        s.fill(color)
        _CACHE[key] = s
    return _CACHE[key]

BG_COLOR = (13, 17, 23)
HEADER_COLOR = (22, 27, 34)
GRID_COLOR = (33, 38, 45)
WALL_COLOR = (48, 54, 61)
EXPLORED_COLOR = (31, 111, 235)
PATH_COLOR = (255, 210, 50)  # Bright gold for path on fantasy ground
TRAP_COLOR = (248, 81, 73)
GOAL_COLOR = (163, 113, 247)
TEXT_COLOR = (201, 209, 217)
WARNING_COLOR = (210, 153, 34)
AGENT_COLOR = (88, 166, 255)

CELL = 30
TOP = 100
LEFT = 35


def draw(screen, font, maze, explored, path,
         agent, goal, algorithm,
         game_state, nodes_explored, path_length,
         comparison_results, play_mode="AI"):

    screen.fill(BG_COLOR)

    # Modern rounded header
    header_rect = pygame.Rect(15, 15, 670, 70)
    pygame.draw.rect(screen, HEADER_COLOR, header_rect, border_radius=12)
    pygame.draw.rect(screen, (60, 60, 75), header_rect, width=2, border_radius=12)

    title_font = pygame.font.SysFont("segoeui", 26, bold=True)
    control_font = pygame.font.SysFont("segoeui", 16)
    stats_font = pygame.font.SysFont("segoeui", 16, bold=True)

    title = title_font.render("AI Maze Solver", True, (0, 255, 200))
    screen.blit(title, (30, 20))

    if play_mode == "AI":
        mode_str = f"[AI] {algorithm}   State: {game_state}"
        metrics_str = f"Exp: {nodes_explored}   Path: {path_length}"
        controls_str = "M:Mode   1:BFS   2:DFS   3:A*   SPACE:Run   R:Reset"
        mode_color = (88, 166, 255)
    else:
        mode_str = f"[USER]   State: {game_state}"
        metrics_str = f"Moves: {path_length}"
        controls_str = "M:Mode   Arrows:Move   R:Reset"
        mode_color = (46, 160, 67)

    algo_text = stats_font.render(mode_str, True, mode_color)
    screen.blit(algo_text, (230, 28))

    metrics_text = stats_font.render(metrics_str, True, (230, 230, 230))
    screen.blit(metrics_text, (480, 28))

    controls = control_font.render(controls_str, True, (160, 170, 180))
    screen.blit(controls, (30, 55))

    for i in range(agent.lives):
        pygame.draw.circle(screen, (248, 81, 73), (660 - i * 20, 35), 8)

    # Draw a background panel for the maze
    maze_bg = pygame.Rect(LEFT - 5, TOP - 5, maze.cols * CELL + 10, maze.rows * CELL + 10)
    pygame.draw.rect(screen, (30, 25, 20), maze_bg, border_radius=10)
    pygame.draw.rect(screen, (80, 70, 55), maze_bg, width=2, border_radius=10)

    wall_tex = get_texture(WALL_IMG_PATH, CELL)
    floor_tex = get_texture(FLOOR_IMG_PATH, CELL)
    trap_tex = get_texture(TRAP_IMG_PATH, CELL)

    DEPTH = 15
    for r in range(maze.rows):
        for c in range(maze.cols):

            x = c * CELL + LEFT
            y = r * CELL + TOP
            rect = pygame.Rect(x, y, CELL, CELL)

            # Always draw floor first for realistic layering
            screen.blit(floor_tex, (x, y))
            
            # Draw Path/Explored over floor
            if maze.grid[r][c] != 1:
                if (r, c) in path:
                    screen.blit(get_overlay(PATH_COLOR, 130, CELL), (x, y))
                elif (r, c) in explored:
                    screen.blit(get_overlay(EXPLORED_COLOR, 90, CELL), (x, y))

                # Draw traps
                if (r, c) in maze.traps:
                    screen.blit(trap_tex, (x, y))
                elif maze.has_warning(r, c) and (r, c) not in maze.traps:
                    pygame.draw.circle(screen, WARNING_COLOR, rect.center, 3)
                    
                # Draw Goal on the floor
                if (r, c) == goal:
                    # 3D Goal Crystal
                    gy_float = y - 5
                    pygame.draw.rect(screen, GOAL_COLOR, (x + 6, gy_float + 6, CELL - 12, CELL - 12), border_radius=4)
                    pygame.draw.rect(screen, (200, 150, 255), (x + 8, gy_float + 8, CELL - 16, CELL - 16), border_radius=2)

            # Subtle grid line on the floor
            pygame.draw.rect(screen, (25, 20, 15), rect, 1)

            # 3D Wall rendering (drawn over floors from rows above if necessary)
            if maze.grid[r][c] == 1:
                # Front depth face
                front_rect = pygame.Rect(x, y + CELL - DEPTH, CELL, DEPTH)
                pygame.draw.rect(screen, (30, 35, 42), front_rect)
                pygame.draw.rect(screen, (15, 18, 22), front_rect, 1) # inner shadow
                
                # Top face extruded
                screen.blit(wall_tex, (x, y - DEPTH))
                # Top highlight edge
                pygame.draw.line(screen, (80, 90, 100), (x, y - DEPTH), (x + CELL, y - DEPTH))

        # Check if we should draw the Agent on this row for realistic Z-sorting
        agent_r = max(0, min(maze.rows - 1, int((agent.pixel_y - TOP) / CELL)))
        if r == agent_r:
            ax, ay = agent.pixel_x, agent.pixel_y
            ALTITUDE = 16  # Hover height
            
            # Floor shadow directly beneath
            pygame.draw.ellipse(screen, (15, 15, 22), (ax - 10, ay - 5, 20, 10))
            
            sz = 12
            base_points = [
                pygame.math.Vector2(0, -sz),           
                pygame.math.Vector2(sz, sz - 2),       
                pygame.math.Vector2(0, sz//3),         
                pygame.math.Vector2(-sz, sz - 2)       
            ]

            angle = getattr(agent, 'angle', 90)
            agent_points = []
            for p in base_points:
                rotated = p.rotate(angle)
                agent_points.append((ax + rotated.x, ay - ALTITUDE + rotated.y))

            # Draw drone body thickness
            shadow_points = [(p[0], p[1] + 4) for p in agent_points]
            pygame.draw.polygon(screen, (60, 120, 180), shadow_points) 
            pygame.draw.polygon(screen, AGENT_COLOR, agent_points)


    # -------- GAME STATUS OVERLAY --------
    if game_state in ["WON", "LOST", "NO_PATH"]:

        overlay = pygame.Surface((700, 750))
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