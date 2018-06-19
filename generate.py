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

# remove `Commercial Break`, `Closing Credits`
# find overlapped line
def sanitize(text):
  lines = [(idx, line) for idx, line in enumerate(text.split("\n")) if line.strip() != ""]
  result = []
  pattern = re.compile(r"[A-Z][a-z]+: ")
  err_count = 0
  for idx, line in lines:
    if line == "Commercial Break" or line == "Closing Credits":
      continue

    if len(pattern.findall(line)) > 1:
      err_count += 1
      print(f"[error, line {idx + 1}] {line}")

    result.append(line)

  if err_count > 0:
    exit(1)

  return result

# title: first line
# end: last line
# scene: in []
# comment: in ()
# conversation: normal line
def parse(lines):
  result = []

  # title
  result.append(("title", lines[0]))

  for line in lines[1:-1]:
    # secne
    if line.startswith("["):
      result.append(("scene", line))
      continue

    # comment
    if line.startswith("("):
      result.append(("comment", line))
      continue

    # conversation
    result.append(("conv", line))

  # end
  result.append(("end", lines[-1]))

  return result

def format(item):
  if item[0] == "conv":
    index = item[1].index(":")
    person = item[1][:index]
    content = item[1][index+1:]
    return f"<p><span class='person'>{person}:</span> {content}"
  else:
    return f"<p class='{item[0]}'>{item[1]}</p>"

def process(path):
  print(f"Process: {path}")
  with open(path) as f:
    lines = sanitize(f.read())
    content = "\n".join([format(l) for l in parse(lines)])
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
