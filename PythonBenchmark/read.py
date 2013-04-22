import data_io

def comma_remove(line):
  ret = ""
  quote = 0
  for c in line:
    if c == ',' and quote > 0:
      ret += " "
    elif c == '"' and quote > 0:
      quote -= 1
    elif c == '"' and quote == 0:
      quote += 1
    else:
      ret += str(c)
  return ret

def parse(file, outfile):
  f = open(file, "r")
  out = open(outfile, "a") 
  for line in f.readlines():
    ret = comma_remove(line)
    out.write(ret)

def parse_author(file):
  parse(file, data_io.get_paths()["author_processed_path"])

def parse_paper(file):
  parse(file, data_io.get_paths()["paper_processed_path"])

def parse_paperauthor(file):
  parse(file, data_io.get_paths()["paperauthor_processed_path"])

def same_line(file):
  f = open(file, "r")
  out = open("../int.csv", "a") 
  curr_line = f.readline().strip()
  while True:
    next_line = f.readline()
    if not next_line:
      break
    next_line = next_line.strip()
    s = next_line.split(",")
    if s[0].isdigit():
      out.write(curr_line + "\n")
      curr_line = next_line
    else:
      print next_line.strip(), "->", curr_line
      curr_line += " " + next_line
