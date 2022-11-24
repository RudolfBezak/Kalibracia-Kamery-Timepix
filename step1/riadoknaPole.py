#vezme string clustra riadku a rozdeli ho na pole dat
# neico taketo "[25, 60, 17, 1] [24, 61, 17, 1] [25, 61, 54, 1]" na array viacerych stringov ['25, 60, 17, 1', '24, 61, 17, 1', '25, 61, 54, 1']

def riadokNaPole(line: str):
  line = line.strip()
  line = line.split("] [")
  line[0] = line[0].replace("[", "")
  line[-1] = line[0].replace("]", "")
  return line
