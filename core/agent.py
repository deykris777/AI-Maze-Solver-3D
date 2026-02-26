class Agent:
    def __init__(self,start,lives=3):
        self.pos=start
        self.lives=lives

    def move(self,new_pos,traps):
        self.pos=new_pos
        if new_pos in traps:
            self.lives-=1