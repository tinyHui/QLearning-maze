class Walker:
    def __init__(self, maze):
        self.maze = maze
        self.current_cell = maze.get(*maze.start)
        self.maze.mark_history(self.current_cell)
        self.last_pos = self.current_cell.get_pos()
    
    def reset(self):
        self.current_cell = self.maze.get(*self.maze.start)
        self.maze.empty_history()
    
    def get_current_cell(self):
        return self.current_cell
    
    def is_end(self):
        return self.maze.is_end(self.current_cell.get_pos())
    
    def get_all_moves(self):
        return ('L', 'R', 'U', 'D')
    
    def move(self, direct):
        self.__move__(direct, record=True)
        
    def assume_move(self, direct):
        self.last_pos = self.current_cell.get_pos()
        self.__move__(direct, record=False)
        
    def undo_move(self):
        self.current_cell = self.maze.get(*self.last_pos)
        
    def __move__(self, direct, record=False):
        tgt_y, tgt_x = self.get_target(direct)
        self.current_cell = self.maze.get(tgt_y, tgt_x)
        if record:
            self.maze.mark_history(self.current_cell)
        
    def can_move(self, direct):
        return self.__can_move__(self.get_target(direct), direct)
        
    def __can_move__(self, tgt_pos, direct):
        tgt_y, tgt_x = tgt_pos
        try:
            self.maze.get(tgt_y, tgt_x)
            return True
        except IndexError:
            return False
     
    def get_target(self, direct):
        return self.__get_target__(self.current_cell.get_pos(), direct)
    
    def __get_target__(self, tgt_pos, direct):
        crt_y, crt_x = tgt_pos
        tgt_y, tgt_x = crt_y, crt_x
        if direct == 'L':
            tgt_x -= 1
        elif direct == 'R':
            tgt_x += 1
        elif direct == 'U':
            tgt_y -= 1
        elif direct == 'D':
            tgt_y += 1
            
        return tgt_y, tgt_x
    
    def target_is_end(self, direct):
        tgt_y, tgt_x = self.get_target(direct)
        return self.maze.is_end((tgt_y, tgt_x))
    
    def get_available_moves(self):
        return list(filter(lambda x: self.can_move(x), self.get_all_moves()))