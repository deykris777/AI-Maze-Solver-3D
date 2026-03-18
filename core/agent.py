class Agent:
    def __init__(self, start, lives=3):
        self.pos = start
        self.lives = lives

        # pixel position for animation
        self.pixel_x = 0
        self.pixel_y = 0

    def set_pixel_position(self, x, y):
        self.pixel_x = x
        self.pixel_y = y

    def move_to(self, new_pos, traps):
        self.pos = new_pos

        # lose life if trap
        if new_pos in traps:
            self.lives -= 1