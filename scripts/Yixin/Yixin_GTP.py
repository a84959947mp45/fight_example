import os
import subprocess
import Gomoku
import argparse

class Yixin():
  def __init__(self, port, time_limit):
    self.game = Gomoku.Gomoku(15)
    self.name_str = "Yixin from gogui-client"
    self.args = ["./gogui-1.4.9/bin/gogui-client", "140.113.167.50", port]
#    self.args = ["gogui-client", "140.113.167.21", port]
    self.time_limit_milliseconds = time_limit
    self.GTP_alphabet = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    self.GTP_to_Yixin_coordinate_map = {self.GTP_alphabet[i] + str(1 + j) : "{},{}".format(i, j) for i in range(15) for j in range(15)}
    self.Yixin_to_GTP_coordinate_map = {"{},{}".format(i, j) : self.GTP_alphabet[i] + str(1 + j) for i in range(15) for j in range(15)}
    self.history = []

  def build_process(self):
    env = os.environ.copy()
    
    self.process = subprocess.Popen(
        args = self.args,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.DEVNULL,
        env = env,
        universal_newlines = True,
        cwd = "./"
    )
    self.process.stdin.write("INFO timeout_turn {}\n".format(self.time_limit_milliseconds))
    self.process.stdin.flush()
    self.process.stdin.write("START 15\n")
    self.process.stdin.flush()
    self.process.stdout.readline()
    self.process.stdout.readline()
  def firstPlay(self, color, action):
    color = color.upper()
    action = action.upper()
    if(action != 'PASS'):
      self.game.play(color, action)
      self.history.append((color, action))
    print(f"= {action}\n")
  def boardsize(self, size):
    size = int(size)
    self.game = Gomoku.Gomoku(size)
    self.GTP_to_Yixin_coordinate_map = {self.GTP_alphabet[i] + str(1 + j) : "{},{}".format(i, j) for i in range(size) for j in range(size)}
    self.Yixin_to_GTP_coordinate_map = {"{},{}".format(i, j) : self.GTP_alphabet[i] + str(1 + j) for i in range(size) for j in range(size)}
    self.process.stdin.write("START {}\n".format(size))
    self.process.stdin.flush()
    _ = self.process.stdout.readline()
    _ = self.process.stdout.readline() 
    self.history = []
    print("= \n")
  
  def play(self, color, action):
    color = color.upper()
    action = action.upper()
    if(action != 'PASS'):
      self.game.play(color, action)
      self.history.append((color, action))
    print("= \n")

  def showboard(self):
    self.game.showboard()
    print("= \n")
 
  def genmove(self, color):
    color = color.upper()
    if self.game.status == 'terminal':
      if self.game.result == color:
        print("= PASS\n")
      elif self.game.result == 'Draw':
        print("= PASS\n")
      else:
        print("= RESIGN\n")
    else:
      self.process.stdin.write("RESTART\n")
      self.process.stdin.write("BOARD\n")
      for h_color, h_action in self.history:
        action = self.GTP_to_Yixin_coordinate_map[h_action]
        if h_color == color:
          self.process.stdin.write("{},1\n".format(action))
        else:
          self.process.stdin.write("{},2\n".format(action))
      self.process.stdin.write("DONE\n")
      self.process.stdin.flush()
      _ = self.process.stdout.readline()
      _ = self.process.stdout.readline()
      if len(self.history) != 0:
        _ = self.process.stdout.readline()
      _ = self.process.stdout.readline()
      reply = self.process.stdout.readline()
      action = self.Yixin_to_GTP_coordinate_map[reply.replace("\n", " ").split()[0]]
      self.game.play(color, action)
      self.history.append((color, action))
      print("= {}\n".format(action))

  def final_score(self):
    if(self.game.status == 'Terminal' and self.game.result != 'Draw'):
      print("= {}+0\n".format(self.game.result))
    else:
      print("= 0\n")

  def clear_board(self):
    self.game = Gomoku.Gomoku(self.game.board_size)
    self.history = []
    print("= \n")

  def name(self):
    print("= {}\n".format(self.name_str))

  def version(self):
    print("= time_limit-{}\n".format(self.time_limit_milliseconds))

  def quit(self):
    self.process.stdin.write("END\n")
    self.process.stdin.flush()
    
    try:
      if self.process.poll() == None:
        self.process.terminate()
      self.process.wait(10)
    except:
      self.process.kill()
      self.process.wait()

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-port", default = '9999')
  parser.add_argument("-time", default = '1000')
  args = parser.parse_args()

  yixin = Yixin(args.port, args.time)
  yixin.build_process() 
 
  command = input()
  while command != "quit":
    if "play" in command:
      tmp = command.split()
      yixin.play(tmp[1], tmp[2])
    elif "genmove" in command:
      if len(yixin.history) != 0:
        tmp = command.split()
        yixin.genmove(tmp[1])
      else:
        yixin.firstPlay('B','O8')

    elif "clear_board" in command:
      yixin.clear_board()
    elif "name" in command:
      yixin.name()
    elif "boardsize" in command:
      tmp = command.split()
      yixin.boardsize(tmp[1])
    elif "version" in command:
      yixin.version()
    elif "showboard" in command:
      yixin.showboard()
    elif "final_score" in command:
      yixin.final_score()
    elif "list_commands" in command:
      print("= \n")
    elif "protocol_version" in command:
      print("= \n")
    else:
      print("= unknown command\n")
    command = input()

  print("= \n")
  yixin.quit()
