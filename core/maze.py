import random


class Maze:

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        # create empty grid
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # generate walls
        self.generate_walls()

        # traps
        self.traps = self.generate_traps(6)

    # -----------------------------
    # WALL GENERATION
    # -----------------------------
    def generate_walls(self):

        for r in range(self.rows):
            for c in range(self.cols):

                # keep start and goal open
                if (r, c) == (0, 0) or (r, c) == (self.rows - 1, self.cols - 1):
                    continue

                # random walls (lower probability)
                if random.random() < 0.22:
                    self.grid[r][c] = 1

        # ensure goal neighbors are open
        self.grid[self.rows-2][self.cols-1] = 0
        self.grid[self.rows-1][self.cols-2] = 0

    # -----------------------------
    # TRAP GENERATION
    # -----------------------------
    def generate_traps(self, count):

        traps = set()

        while len(traps) < count:

            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (
                self.grid[r][c] == 0
                and (r, c) != (0, 0)
                and (r, c) != (self.rows - 1, self.cols - 1)
            ):
                traps.add((r, c))

        return traps

    # -----------------------------
    # NEIGHBORS
    # -----------------------------
    def neighbors(self, node):

        r, c = node

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        result = []

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:
                    result.append((nr, nc))

        return result

    # -----------------------------
    # WARNING SYSTEM
    # -----------------------------
    def has_warning(self, r, c):

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if (nr, nc) in self.traps:
                return True

        return False