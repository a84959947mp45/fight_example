import copy
import sys

# stone-based Gomoku

class Gomoku():
  def __init__(self, size):
    self.board_size = size
    self.color = ['B', 'W', '.']
    self.board = ['.'] * (self.board_size * self.board_size)
    self.piece_count = 0
    self.GTP_alphabet = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    self.coordinate_to_id_map = {self.id_to_coordinate(i) : i for i in range(size * size)}
    self.status = 'playing'
    self.result = 'in process'

  def id_to_coordinate(self, id: int):
    return self.GTP_alphabet[id % self.board_size] + str(1 + id // self.board_size)
  
  def action_to_index(self, action):
    return self.coordinate_to_id_map[action]

  def is_legal_action(self, action):
    return self.board[self.action_to_index(action)] == '.'

  def play(self, color, action):
    if self.is_legal_action(action):
      self.board[self.action_to_index(action)] = color
      self.piece_count += 1
      if self.has_line(color, self.action_to_index(action)):
        self.status = 'terminal'
        self.result = color
      elif self.piece_count == self.board_size * self.board_size:
        self.status = 'terminal'
        self.result = 'Draw'
    else:
      self.status = 'terminal'
      if color == 'B':
        self.result = 'W'
      elif color == 'W':
        self.result = 'B'
      else:
        self.result = 'unknown player'

  # taken from Shao's version
  # judge if there's a completed line.
  def has_line(self,player, action:int):
    ai = int(action / self.board_size)
    aj = int(action %  self.board_size)

    # right, down-right, down, down-left
    vi = [0, 1, 1, 1]
    vj = [1, 1, 0, -1]

    count = 0

    for d in range(4):
      count = 0
      ci = ai
      cj = aj
      while(1):
        if( ci >= 0 and ci <  self.board_size and cj >= 0 and cj < self.board_size and self.board[ci * self.board_size + cj] == player ):
          count+=1
          ci = ci- vi[d]
          cj = cj- vj[d]
        else:
          break
      ci = ai
      cj = aj
      while(1):
        if (ci >= 0 and ci <  self.board_size and cj >= 0 and cj < self.board_size and self.board[ci * self.board_size + cj] == player ):
          count+=1
          ci = ci+ vi[d]
          cj = cj+ vj[d]
        else:
          break
   
      # +1 since board_[action] will be counted twice
      if (count >= 6):
        return True
      
    return False

  # taken from Shao's version
  # judge if there's a threat line.
  def has_threat(self,player, action:int):

    if player == 'B':
      opponent = 'W'
    elif player == 'W':
      opponent = 'B'
    #print("action:",action)
    ai = int(action / self.board_size)
    aj = int(action %  self.board_size)
    # print(self.board[ai * self.board_size + aj])
    # right, down-right, down, down-left
    vi = [0, 1, 1, 1]
    vj = [1, 1, 0, -1]

    count = 0

    for d in range(4):

      endColor1 = '-1'
      endColor2 = '-1'
      count = 0
      ci = ai
      cj = aj
      
      while(1):
        if( ci >= 0 and ci <  self.board_size and cj >= 0 and cj < self.board_size and self.board[ci * self.board_size + cj] == player ):
          count+=1
          ci = ci- vi[d]
          cj = cj- vj[d]
        else:
          if(ci < 0 or ci >=  self.board_size or cj < 0 or cj >= self.board_size or self.board[ci * self.board_size + cj] == opponent):
            endColor1 = opponent
          elif(self.board[ci * self.board_size + cj] == '.'):
            endColor1 = '.'
          break
      ci = ai
      cj = aj
      while(1):
        if (ci >= 0 and ci <  self.board_size and cj >= 0 and cj < self.board_size and self.board[ci * self.board_size + cj] == player ):
          count+=1
          ci = ci+ vi[d]
          cj = cj+ vj[d]
        else:
          if(ci < 0 or ci >=  self.board_size or cj < 0 or cj >= self.board_size or self.board[ci * self.board_size + cj] == opponent):
            endColor2 = opponent
          elif(self.board[ci * self.board_size + cj] == '.'):
            endColor2 = '.'
          break
   
      # +1 since board_[action] will be counted twice
      #print(count ,endColor1 , endColor2)
      if ((count == 4 and endColor1 == '.' and endColor2 == '.') 
            or (count == 5 and endColor1 == opponent and endColor2 == '.')
            or (count == 5 and endColor1 == '.' and endColor2 == opponent)):
        return True
      
    return False

  def showboard(self, file=sys.stdout):
    #print("   " + " ".join(["A", "B", "C", "D", "E", "F","G","H","I","J","K","L","M","N","O","P","Q","R","S"]), file=file)
    size = self.board_size
    print("   " + " ".join(self.GTP_alphabet[:size]), file=file)
    for i in range(size, 0, -1):
      if(i < 10):
        print(i, end='  ', file=file)
      else:
        print(i, end=' ', file=file)
      for j in range(size):
        coordinate = self.GTP_alphabet[j] + str(i)
        index = self.coordinate_to_id_map[coordinate]
        print(self.board[index], end=' ', file=file)
      print(file=file) 
    print("status: {}".format(self.status), file=file)
    print("result: {}".format(self.result), file=file)


