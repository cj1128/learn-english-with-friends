#!/usr/bin/env python
import re
import sys
from string import Template
from os.path import isdir, join, basename, splitext, abspath, dirname
from pathlib import Path
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
  print(f"Process: { path }")

  basename = path.name[:-4]
  target_path = Path("result") / basename[:3] / f"{ basename }.pdf"

  if target_path.exists():
    print(f"{ target_path } Found")
    return

  lines = [line.strip() for line in path.read_text().split("\n") if line.strip() != ""]
  content = "\n".join([format(l) for l in lines])

  with tempfile.NamedTemporaryFile(mode="w+t", encoding="utf8") as tmp:
    tmp.write(template.substitute(content=content))
    tmp.flush()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    run(f"prince { tmp.name } -s pdf.css -o { target_path }", shell=True, check=True)

  print(f"Generate { target_path } successfully.")

if len(sys.argv) < 2:
  print("usage: ./generate.py [file_or_dir]")
  exit(0)

p = Path(sys.argv[1])

if p.is_dir():
  for file in p.rglob("*.txt"):
    process(file)
else:
  process(p)
