import os
import argparse

class GameResult(object):
  def __init__(self, str):
#GAME	RES_B	RES_W	RES_R	ALT	DUP	LEN	TIME_B	TIME_W	CPU_B	CPU_W	ERR	ERR_MSG
#0	B+R	B+R	B+R	0	-	31	17	8.9	0	0	0	
    terms = str.split("\t")
    self.ID = terms[0]
    self.RES_B = terms[1]
    self.RES_W = terms[2]
    self.RES_R = terms[3]
    self.ALT = terms[4]
    self.DUP = terms[5]
    self.LEN = terms[6]
    self.TIME_B = terms[7]
    self.TIME_W = terms[8]
    self.CPU_B = terms[9]
    self.CPU_W = terms[10]
    self.ERR = terms[11]
    self.ERR_MSG = terms[12]


def result_info(list):
  l = len(list)
  if l == 0:
    return "0\taverage len: -"
  else:
    return "{}\taverage len: {:.2f}".format(l, sum(list)/l)

def win_rate(win_count, loss_count, draw_count):
  return (win_count + draw_count * 0.5) / (win_count + loss_count + draw_count)

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-file", required = True)
  args = parser.parse_args()

  gamelist = []
  file_name = args.file.split("/")[-1]
  with open(args.file + "/" + file_name + ".dat") as file:
    for line in file:
      line = line.split("\n")[0]
      if line[0] == "#":
        continue
      else:
        game = GameResult(line)
        gamelist.append(game)
 
  black_win = []
  black_loss = []
  black_draw = []
  white_win = []
  white_loss = []
  white_draw = []
  for game in gamelist:
    if game.ALT == "0":
      if game.RES_R[0] == "B":
        black_win.append(int(game.LEN))
      elif game.RES_R[0] == "W":
        black_loss.append(int(game.LEN))
      else:
        black_draw.append(int(game.LEN))
    else:
      if game.RES_R[0] == "B":
        white_win.append(int(game.LEN))
      elif game.RES_R[0] == "W":
        white_loss.append(int(game.LEN))
      else:
        white_draw.append(int(game.LEN))

  print("========= Played as black =========") 
  print("Win:\t" + result_info(black_win))
  print("Loss:\t" + result_info(black_loss))
  print("Draw:\t" + result_info(black_draw))
  print("Win rate: {}%".format(100 * win_rate(len(black_win), len(black_loss), len(black_draw))))
  print("========= Played as white =========") 
  print("Win:\t" + result_info(white_win))
  print("Loss:\t" + result_info(white_loss))
  print("Draw:\t" + result_info(white_draw))
  print("Win rate: {}%".format(100 * win_rate(len(white_win), len(white_loss), len(white_draw))))
  print("============= Overall =============") 
  print("Win:\t" + result_info(black_win + white_win))
  print("Loss:\t" + result_info(black_loss + white_loss))
  print("Draw:\t" + result_info(black_draw + white_draw))
  print("Win rate: {}%".format(100 * win_rate(len(black_win + white_win), len(black_loss + white_loss), len(black_draw + white_draw))))
