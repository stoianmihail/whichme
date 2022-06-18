from refextract import extract_references_from_file

import sys
import PyPDF2

def build_regex(number): 
  return f'(?<=[,\[]) ?{number} ?(?=[,\]])'

def build_author(p, n):
  return f'{p} ?{n}|{p[0]} ?{n}|{n}, ?{p}'

def main():
  if len(sys.argv) != 2:
    print(f'...')
    sys.exit(-1)  

  file = sys.argv[1]

  obj = open(file, 'rb')
  reader = PyPDF2.PdfFileReader(obj)
  num_pages = reader.numPages
  obj.close()

  def fetch_page(index):
    import os
    os.system(f'gs -sDEVICE=txtwrite -dFirstPage={index} -dLastPage={index} -o output.txt 3514221.3526121.pdf >/dev/null 2>&1')
    lines = open("output.txt", "r", encoding="latin1").readlines()
    return lines

  references = extract_references_from_file(file)
  myrefs = []
  import re
  myengine = re.compile(build_author('Mihail', 'Stoian'), flags=re.IGNORECASE)
  print(f'engine={myengine}')
  for ref in references:
    if myengine.search(ref['raw_ref'][0]):
      myrefs.append(ref['linemarker'][0])

  print(f'myrefs={myrefs}')
  myengines = [re.compile(build_regex(x)) for x in myrefs]

  for i in range(1, num_pages + 1):
    print(f'Page: {i}')
    lines = fetch_page(i)
    for line in lines:
      for index, engine in enumerate(myengines):
        if engine.search(line):
          if myengine.search(line):
            continue
          print(f'{myrefs[index]} -> line={line}')

if __name__ == '__main__':
  main()
