from ursina import *
from ursina.shaders import lit_with_shadows_shader
from core.maze import Maze
from core.search import bfs, dfs, astar

# ──────────────────────────────────────────
# APP INIT
# ──────────────────────────────────────────
app = Ursina(title='AI Maze Solver 3D', borderless=False, fullscreen=False, development_mode=False)
window.color = color.rgb32(15, 20, 30)
window.size = (1280, 720)

scene.fog_density = 0.04
scene.fog_color = color.rgb32(15, 20, 30)
AmbientLight(color=color.rgba32(50, 50, 60, 255))

# ──────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────
ROWS, COLS = 21, 21
WALL_HEIGHT = 4
CELL_SIZE = 1

# ──────────────────────────────────────────
# GAME STATE
# ──────────────────────────────────────────
play_mode = 'USER'       # 'AI' or 'USER'
algorithm = 'BFS'
game_state = 'IDLE'      # IDLE, EXPLORING, ANIMATING, WON, LOST
current_level = 1
lives = 3
nodes_explored = 0
path_length_val = 0
move_count = 0

# ──────────────────────────────────────────
# 3D WORLD CONTAINERS
# ──────────────────────────────────────────
wall_entities = []
floor_entities = []
trap_entities = []
path_markers = []
explored_markers = []
goal_entity = None

# ──────────────────────────────────────────
# MAZE GENERATION
# ──────────────────────────────────────────
maze = Maze(ROWS, COLS)
start_pos = (0, 0)
goal_pos = (ROWS - 1, COLS - 1)

# ──────────────────────────────────────────
# MINIMAP
# ──────────────────────────────────────────
minimap_bg = Entity(parent=camera.ui, model='quad', color=color.rgba32(0, 0, 0, 180), scale=(0.3, 0.3), position=(0.65, 0.3))
minimap_border = Entity(parent=minimap_bg, model='quad', color=color.rgba32(120, 120, 120, 150), scale=(1.04, 1.04), z=0.01)
minimap_entities = []
minimap_player = Entity(parent=minimap_bg, model=Circle(3), color=color.cyan, scale=(2.0/COLS, 0.8/ROWS), z=-0.1)

def clear_minimap():
    global minimap_entities
    for e in minimap_entities:
        destroy(e)
    minimap_entities = []

def build_minimap():
    global minimap_entities
    minimap_player.scale = (2.0/COLS, 0.8/ROWS)
    for r in range(ROWS):
        for c in range(COLS):
            cell_w = 1 / COLS
            cell_h = 1 / ROWS
            x = -0.5 + c * cell_w + cell_w / 2
            y = 0.5 - r * cell_h - cell_h / 2
            
            if maze.grid[r][c] == 1:
                wall = Entity(parent=minimap_bg, model='quad', color=color.rgb32(180, 180, 180), scale=(cell_w, cell_h), position=(x, y), z=-0.05)
                minimap_entities.append(wall)
            elif (r, c) in maze.traps:
                trap = Entity(parent=minimap_bg, model='quad', color=color.red, scale=(cell_w, cell_h), position=(x, y), z=-0.05)
                minimap_entities.append(trap)
    
    gx = -0.5 + goal_pos[1] * (1/COLS) + (1/COLS) / 2
    gy = 0.5 - goal_pos[0] * (1/ROWS) - (1/ROWS) / 2
    goal_mark = Entity(parent=minimap_bg, model='quad', color=color.magenta, scale=(1/COLS, 1/ROWS), position=(gx, gy), z=-0.05)
    minimap_entities.append(goal_mark)


def clear_world():
    """Destroy all 3D entities."""
    global wall_entities, floor_entities, trap_entities, path_markers, explored_markers, goal_entity
    for e in wall_entities + floor_entities + trap_entities + path_markers + explored_markers:
        destroy(e)
    if goal_entity:
        destroy(goal_entity)
    wall_entities = []
    floor_entities = []
    trap_entities = []
    path_markers = []
    explored_markers = []
    goal_entity = None
    clear_minimap()


def build_world():
    """Build the 3D maze from the maze grid."""
    global goal_entity

    for r in range(ROWS):
        for c in range(COLS):
            x, z = c * CELL_SIZE, r * CELL_SIZE

            # Floor tile for every cell
            floor = Entity(
                model='cube',
                scale=(CELL_SIZE, 0.1, CELL_SIZE),
                position=(x, -0.05, z),
                color=color.white,  # Set to white so the texture isn't tinted
                texture='assets/textures/brick_pavement_03_diff_4k.jpg',
                shader=lit_with_shadows_shader,
                collider=None
            )
            floor_entities.append(floor)

            if maze.grid[r][c] == 1:
                # Wall block
                wall = Entity(
                    model='cube',
                    scale=(CELL_SIZE, WALL_HEIGHT, CELL_SIZE),
                    position=(x, WALL_HEIGHT / 2, z),
                    color=color.white,  # Set to white so the texture isn't tinted
                    texture='assets/textures/red_brick_diff_4k.jpg',
                    shader=lit_with_shadows_shader,
                    collider='box'
                )
                wall_entities.append(wall)
            else:
                # Trap marker
                if (r, c) in maze.traps:
                    trap = Entity(
                        model='cube',
                        scale=(0.6, 0.15, 0.6),
                        position=(x, 0.08, z),
                        color=color.rgb32(220, 50, 50),
                        collider=None
                    )
                    trap_entities.append(trap)

    # Giant background floor extending outwards so camera never sees absolute void
    bg_floor = Entity(
        model='cube',
        scale=(COLS * CELL_SIZE + 20, 0.05, ROWS * CELL_SIZE + 20),
        position=(COLS * CELL_SIZE / 2, -0.1, ROWS * CELL_SIZE / 2),
        color=color.rgb32(30, 35, 45),
        texture='assets/textures/brick_pavement_03_diff_4k.jpg',
        texture_scale=(COLS + 20, ROWS + 20), # Repeat texture so it doesn't stretch
        shader=lit_with_shadows_shader,
        collider=None
    )
    floor_entities.append(bg_floor)

    # Goal beacon
    gx, gz = goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE
    goal_entity = Entity(
        model='cube',
        scale=(0.7, 1.5, 0.7),
        position=(gx, 0.75, gz),
        color=color.rgb32(140, 80, 230),
        shader=lit_with_shadows_shader,
        collider=None
    )
    build_minimap()


# ──────────────────────────────────────────
# PLAYER
# ──────────────────────────────────────────
player = Entity(
    model='assets/textures/iron-man/source/Octane/Octane.obj',
    scale=(0.0008, 0.0008, 0.0008),
    position=(start_pos[1] * CELL_SIZE, 0, start_pos[0] * CELL_SIZE),
    color=color.white,
    texture='assets/textures/iron-man/textures/Octane_default_BaseColor.1001.png',
    shader=lit_with_shadows_shader,
    collider=None
)

# Attach a real-time point light that follows the player
player_light = PointLight(parent=player, y=2, z=0.5, shadows=True, color=color.rgb32(255, 240, 220))

# Player grid position tracking
player_grid_r = start_pos[0]
player_grid_c = start_pos[1]
is_moving = False  # Lock movement during animation


# ──────────────────────────────────────────
# THIRD PERSON CAMERA
# ──────────────────────────────────────────
camera.fov = 70
camera.position = player.position + player.back * 4.5 + Vec3(0, 1.5, 0)
camera.look_at(player.position + Vec3(0, 1.5, 0))
camera_smooth_speed = 10
camera_mode = 'FIRST_PERSON'


# ──────────────────────────────────────────
# HUD
# ──────────────────────────────────────────
hud_mode = Text(
    text=f'[{play_mode}]  Algo: {algorithm}',
    position=(-0.85, 0.48),
    scale=1.4,
    color=color.rgb32(80, 200, 255),
    background=True
)

hud_state = Text(
    text=f'Lvl {current_level} | State: {game_state}',
    position=(-0.85, 0.43),
    scale=1.2,
    color=color.white,
    background=True,
)

hud_stats = Text(
    text='Exp: 0  Path: 0  Moves: 0',
    position=(-0.85, 0.38),
    scale=1.1,
    color=color.rgb32(200, 200, 200),
    background=True,
)

hud_lives = Text(
    text=f'Lives: {lives}',
    position=(0.65, 0.48),
    scale=1.4,
    color=color.rgb32(248, 81, 73),
    background=True
)

hud_controls = Text(
    text='M:Mode  1/2/3:Algo  SPACE:Solve  R:Reset  Arrows:Move',
    position=(-0.85, -0.46),
    scale=0.9,
    color=color.white,
    background=True,
)

for hud in (hud_mode, hud_state, hud_stats, hud_lives, hud_controls):
    if hasattr(hud, 'background') and hud.background:
        hud.background.color = color.rgba32(0, 0, 0, 150)
        hud.background.scale_x *= 1.1
        hud.background.scale_y *= 1.2

def update_hud():
    hud_mode.text = f'[{play_mode}]  Algo: {algorithm}'
    hud_state.text = f'Lvl {current_level} | State: {game_state}'
    hud_stats.text = f'Exp: {nodes_explored}  Path: {path_length_val}  Moves: {move_count}'
    hud_lives.text = f'Lives: {lives}'
    hud_controls.text = f'M:Mode  1/2/3:Algo  SPACE:Solve  R:Reset  C:Cam({camera_mode[:3]})  Arrows:Move'
    if play_mode == 'AI':
        hud_mode.color = color.rgb32(80, 200, 255)
    else:
        hud_mode.color = color.rgb32(80, 230, 120)


# ──────────────────────────────────────────
# PATH / EXPLORED VISUALIZATION
# ──────────────────────────────────────────
def clear_markers():
    global path_markers, explored_markers
    for e in path_markers + explored_markers:
        destroy(e)
    path_markers = []
    explored_markers = []


def show_explored(explored_list):
    """Place translucent blue markers on explored cells."""
    global explored_markers
    for (r, c) in explored_list:
        if maze.grid[r][c] == 0:
            m = Entity(
                model='cube',
                scale=(CELL_SIZE * 0.9, 0.05, CELL_SIZE * 0.9),
                position=(c * CELL_SIZE, 0.03, r * CELL_SIZE),
                color=color.rgba32(30, 120, 240, 120),
                collider=None
            )
            explored_markers.append(m)


def show_path(path_list):
    """Place bright markers on path cells."""
    global path_markers
    for (r, c) in path_list:
        m = Entity(
            model='cube',
            scale=(CELL_SIZE * 0.7, 0.08, CELL_SIZE * 0.7),
            position=(c * CELL_SIZE, 0.05, r * CELL_SIZE),
            color=color.rgba32(50, 200, 80, 180),
            collider=None
        )
        path_markers.append(m)


# ──────────────────────────────────────────
# MOVEMENT ANIMATION (shared by AI & USER)
# ──────────────────────────────────────────
move_queue = []       # List of (r, c) steps to animate
current_target = None
move_speed = 6        # units per second


def queue_move(step_list):
    """Queue a list of grid (r, c) positions to animate through."""
    global move_queue
    move_queue = list(step_list)


def handle_trap_hit():
    """Handle trap collision effects."""
    global lives, game_state
    lives -= 1
    update_hud()

    # Flash screen red
    flash = Entity(
        model='quad',
        scale=100,
        color=color.rgba32(255, 50, 50, 100),
        parent=camera.ui
    )
    destroy(flash, delay=0.3)

    # Remove the trap entity visually
    for trap_e in trap_entities[:]:
        tr = int(round(trap_e.z / CELL_SIZE))
        tc = int(round(trap_e.x / CELL_SIZE))
        if (tr, tc) == (player_grid_r, player_grid_c):
            destroy(trap_e)
            trap_entities.remove(trap_e)
            break

    # Sound
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_ICONHAND)
    except ImportError:
        pass

    if lives <= 0:
        game_state = 'LOST'
        update_hud()


win_overlay = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2),
    color=color.rgba32(0, 0, 0, 150),
    z=1,
    enabled=False
)

win_text_shadow = Text(
    text='YAYYY! YOU DID IT!',
    position=(0.005, 0.195),
    origin=(0, 0),
    scale=0,
    color=color.black,
    z=-1
)

win_text = Text(
    text='YAYYY! YOU DID IT!',
    position=(0, 0.2),
    origin=(0, 0),
    scale=0,
    color=color.rgb32(255, 215, 0),
    z=-2
)

def _play_win_sound():
    try:
        import winsound
        # Triumphal fanfare (C, E, G, C)
        winsound.Beep(523, 150)   # C5
        winsound.Beep(659, 150)   # E5
        winsound.Beep(784, 150)   # G5
        winsound.Beep(1046, 400)  # C6 (held)
    except:
        pass

def next_level():
    global current_level, ROWS, COLS, goal_pos
    current_level += 1
    # Expand the maze size natively (must stay odd to generate perfect walls/paths)
    ROWS += 2
    COLS += 2
    goal_pos = (ROWS - 1, COLS - 1)
    reset_game()

def show_win_screen():
    win_overlay.enabled = True
    win_text.animate_scale(4, duration=1.0, curve=curve.out_bounce)
    win_text_shadow.animate_scale(4, duration=1.0, curve=curve.out_bounce)
    import threading
    threading.Thread(target=_play_win_sound, daemon=True).start()
    
    # Automatically progress to the next level after the 3-second win graphic
    invoke(next_level, delay=3)

def check_win():
    global game_state
    if (player_grid_r, player_grid_c) == goal_pos:
        game_state = 'WON'
        update_hud()
        show_win_screen()
        return True
    return False


# ──────────────────────────────────────────
# RESET
# ──────────────────────────────────────────
def reset_game():
    global maze, lives, game_state, nodes_explored, path_length_val, move_count
    global player_grid_r, player_grid_c, is_moving, move_queue, current_target

    win_overlay.enabled = False
    win_text.scale = 0
    win_text_shadow.scale = 0

    maze = Maze(ROWS, COLS)
    lives = 3
    game_state = 'IDLE'
    nodes_explored = 0
    path_length_val = 0
    move_count = 0
    player_grid_r = start_pos[0]
    player_grid_c = start_pos[1]
    is_moving = False
    move_queue = []
    current_target = None

    player.position = Vec3(start_pos[1] * CELL_SIZE, 0, start_pos[0] * CELL_SIZE)
    player.rotation_y = 0

    clear_world()
    clear_markers()
    build_world()
    update_hud()


# ──────────────────────────────────────────
# AI SOLVE
# ──────────────────────────────────────────
def run_ai():
    global game_state, nodes_explored, path_length_val

    if game_state not in ('IDLE',):
        return

    if algorithm == 'BFS':
        path_result, explored_result = bfs(maze, start_pos, goal_pos)
    elif algorithm == 'DFS':
        path_result, explored_result = dfs(maze, start_pos, goal_pos)
    else:
        path_result, explored_result = astar(maze, start_pos, goal_pos)

    nodes_explored = len(explored_result)
    path_length_val = len(path_result)

    if not path_result:
        game_state = 'IDLE'
        update_hud()
        return

    clear_markers()
    show_explored(explored_result)
    show_path(path_result)

    game_state = 'ANIMATING'
    queue_move(path_result)
    update_hud()


# ──────────────────────────────────────────
# USER MOVE (single step)
# ──────────────────────────────────────────
def try_user_move(dr, dc):
    global move_count

    if is_moving or game_state in ('WON', 'LOST', 'ANIMATING', 'EXPLORING'):
        return

    nr, nc = player_grid_r + dr, player_grid_c + dc

    if 0 <= nr < ROWS and 0 <= nc < COLS and maze.grid[nr][nc] == 0:
        move_count += 1
        path_length_val_update = move_count
        queue_move([(nr, nc)])


# ──────────────────────────────────────────
# INPUT HANDLER
# ──────────────────────────────────────────
def input(key):
    global play_mode, algorithm, camera_mode

    if key == 'c':
        modes = ['FIRST_PERSON', 'TOP_DOWN', 'ISOMETRIC']
        idx = modes.index(camera_mode)
        camera_mode = modes[(idx + 1) % len(modes)]
        update_hud()

    if key == 'm':
        play_mode = 'USER' if play_mode == 'AI' else 'AI'
        reset_game()

    if key == 'r':
        reset_game()

    if play_mode == 'AI':
        if key == '1':
            algorithm = 'BFS'
            update_hud()
        elif key == '2':
            algorithm = 'DFS'
            update_hud()
        elif key == '3':
            algorithm = 'A*'
            update_hud()
        elif key == 'space':
            run_ai()

    if play_mode == 'USER':
        y_rot = int(round(player.rotation_y / 90.0)) * 90 % 360
        
        dir_map = {
            0:   {'up arrow': (1,0),  'down arrow': (-1,0), 'left arrow': (0,-1), 'right arrow': (0,1)},
            90:  {'up arrow': (0,1),  'down arrow': (0,-1), 'left arrow': (1,0),  'right arrow': (-1,0)},
            180: {'up arrow': (-1,0), 'down arrow': (1,0),  'left arrow': (0,1),  'right arrow': (0,-1)},
            270: {'up arrow': (0,-1), 'down arrow': (0,1),  'left arrow': (-1,0), 'right arrow': (1,0)}
        }
        
        if key in dir_map[y_rot]:
            try_user_move(*dir_map[y_rot][key])


# ──────────────────────────────────────────
# UPDATE LOOP (runs every frame)
# ──────────────────────────────────────────
def update():
    global current_target, is_moving, player_grid_r, player_grid_c, game_state, move_count

    # ---- Smooth camera follow ----
    if camera_mode == 'FIRST_PERSON':
        player.visible = False
        # True First Person View (from human eyes)
        target_cam_pos = player.position + player.forward * 0.4 + Vec3(0, 1.8, 0)
        camera.position = lerp(camera.position, target_cam_pos, camera_smooth_speed * time.dt)
        # Lock roll and pitch to 0 to prevent the screen from turning sideways (portrait mode glitch)
        camera.rotation = Vec3(0, player.rotation_y, 0)
    elif camera_mode == 'TOP_DOWN':
        player.visible = True
        target_cam_pos = player.position + Vec3(0, 15, -0.1)  # slightly offset Z to avoid gimbal lock
        camera.position = lerp(camera.position, target_cam_pos, camera_smooth_speed * time.dt)
        camera.look_at(player.position)
    elif camera_mode == 'ISOMETRIC':
        player.visible = True
        target_cam_pos = player.position + Vec3(12, 18, -12)
        camera.position = lerp(camera.position, target_cam_pos, camera_smooth_speed * time.dt)
        camera.look_at(player.position)

    # ---- Animate movement queue ----
    if move_queue and not is_moving:
        current_target = move_queue.pop(0)
        is_moving = True

    if is_moving and current_target:
        tr, tc = current_target
        target_pos = Vec3(tc * CELL_SIZE, 0, tr * CELL_SIZE)

        # Rotate player to face movement direction
        direction = target_pos - player.position
        if direction.length() > 0.01:
            import math
            target_angle = math.degrees(math.atan2(direction.x, direction.z))
            
            # Shortest path angle interpolation prevents whirlwind spinning
            diff = (target_angle - player.rotation_y) % 360
            if diff > 180:
                diff -= 360
            player.rotation_y += diff * 15 * time.dt

        # Move towards target
        dist = (target_pos - player.position).length()
        if dist > 0.05:
            player.position = lerp(player.position, target_pos, move_speed * time.dt)
        else:
            # Snap to target
            player.position = target_pos
            player_grid_r = tr
            player_grid_c = tc
            is_moving = False
            current_target = None

            # Check trap
            if (player_grid_r, player_grid_c) in maze.traps:
                maze.traps.remove((player_grid_r, player_grid_c))
                handle_trap_hit()

            # Check win
            if check_win():
                move_queue.clear()

            # Check loss
            if game_state == 'LOST':
                move_queue.clear()

            # If AI queue is finished
            if not move_queue and game_state == 'ANIMATING':
                if game_state not in ('WON', 'LOST'):
                    game_state = 'IDLE'
                update_hud()

    # ---- Rotate goal beacon ----
    if goal_entity:
        goal_entity.rotation_y += 60 * time.dt

    # ---- Game over overlay ----
    # (handled by checking game_state in HUD)

    # ---- Update Minimap Player ----
    if minimap_player:
        cell_w = 1 / COLS
        cell_h = 1 / ROWS
        minimap_player.x = -0.5 + (player.position.x / CELL_SIZE) * cell_w + cell_w / 2
        minimap_player.y = 0.5 - (player.position.z / CELL_SIZE) * cell_h - cell_h / 2
        
        # Triangle points right by default. Subtract 90 to make it point up when rotation_y is 0.
        minimap_player.rotation_z = player.rotation_y - 90


# ──────────────────────────────────────────
# BUILD AND RUN
# ──────────────────────────────────────────
build_world()
update_hud()

# Dark sky background
camera.clip_plane_far = 200
window.color = color.rgb32(20, 25, 35)

app.run()
