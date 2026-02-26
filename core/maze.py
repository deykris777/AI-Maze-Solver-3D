import random

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0]*cols for _ in range(rows)]
        self.traps=set()
        self.generate()

    def generate(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random()<0.25:
                    self.grid[r][c]=1

        self.grid[0][0]=0
        self.grid[self.rows-1][self.cols-1]=0

        for _ in range(20):
            r=random.randint(0,self.rows-1)
            c=random.randint(0,self.cols-1)
            if self.grid[r][c]==0 and (r,c)!=(0,0) and (r,c)!=(self.rows-1,self.cols-1):
                self.traps.add((r,c))

    def neighbors(self,r,c):
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        out=[]
        for dr,dc in dirs:
            nr,nc=r+dr,c+dc
            if 0<=nr<self.rows and 0<=nc<self.cols:
                if self.grid[nr][nc]==0:
                    out.append((nr,nc))
        return out

    def has_warning(self,r,c):
        for n in self.neighbors(r,c):
            if n in self.traps:
                return True
        return False