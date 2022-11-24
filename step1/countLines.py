#vezme adresu suboru a vrati pocet riadkov subora

def countLines(fileAdress):
  return sum(1 for line in open(fileAdress, 'r', encoding='utf-8'))