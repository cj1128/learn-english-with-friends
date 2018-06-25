#!/usr/bin/env python
import re
import sys
from string import Template
from os.path import isdir, join, basename, splitext
import glob
import tempfile
from subprocess import run

template = Template("""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    $content
  </body>
</html>
""")

def format(line):
  # comment
  line = re.sub(r"\[.+?\]", "<span class='comment'>\\g<0></span>", line)

  # person
  line = re.sub(r"^\w.+?:", "<span class='person'>\\g<0></span>", line)

  # highlight
  line = re.sub(r"\*(.+?)\*", "<span class='highlight'>\\1</span>", line)

  return f"<p>{line}</p>"

def process(path):
  print(f"Process: {path}")
  with open(path) as f:
    lines = [line.strip() for line in f.read().split("\n") if line.strip() != ""]
    content = "\n".join([format(l) for l in lines])
    with tempfile.NamedTemporaryFile(mode="w+t", encoding="utf8") as tmp:
      tmp.write(template.substitute(content=content))
      tmp.flush()
      name = splitext(basename(path))[0]
      run(f"prince {tmp.name} -s pdf.css -o dist/{name}.pdf", shell=True, check=True)
  print(f"Generate dist/{name}.pdf successfully.")

if len(sys.argv) < 2:
  print("usage: ./generate.py [file_or_dir]")
  exit(0)

target = sys.argv[1]

if isdir(target):
  for path in glob.glob(join(target, "**", "*.txt")):
    process(path)
else:
  process(target)
