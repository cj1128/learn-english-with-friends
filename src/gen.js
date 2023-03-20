import fs from "node:fs"
import path from "node:path"
import { globSync } from "glob"
import { execSync } from "node:child_process"
import { Command } from "commander"

const HTML_DIR = new URL("../tmp", import.meta.url).pathname
const RESULT_ROOT_DIR = new URL("../result", import.meta.url).pathname
const CSS_PATH = new URL("./pdf.css", import.meta.url).pathname

const program = new Command()

program.option("-o, --overwrite")

start()

function start() {
  program.parse()

  const opts = program.opts()

  // create necessary dirs
  if (!fs.existsSync(HTML_DIR)) {
    fs.mkdirSync(HTML_DIR)
  }

  if (program.args.length === 0) {
    console.error("usage: pnpm run gen file_or_dir")
    return
  }

  const path = program.args[0]

  if (isDir(path)) {
    globSync(`${path}/**/*.txt`).forEach((f) => handle(f, opts))
  } else {
    handle(path, opts)
  }
}

function isDir(path) {
  const stats = fs.statSync(path)
  return stats.isDirectory()
}

function handle(file, opts) {
  try {
    const name = path.parse(file).name
    if (!/^S\d\dE\d\d$/.test(name)) {
      console.error(`Invalid name format ${name}, should be SxxExx.txt`)
      return
    }

    const htmlPath = path.join(HTML_DIR, name + ".html")

    const resultDir = path.join(RESULT_ROOT_DIR, name.slice(0, 3))
    fs.mkdirSync(resultDir, { recursive: true })

    const resultPath = path.join(resultDir, name + ".pdf")

    if (fs.existsSync(resultPath) && !opts.overwrite) {
      console.log(`Target found for ${file}, skipped`)
      return
    }

    const content = fs
      .readFileSync(file, "utf8")
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line !== "")
      .map(formatLine)
      .join("\n")

    const html = genHTML(content)

    fs.writeFileSync(htmlPath, html)

    execSync(`prince ${htmlPath} -s ${CSS_PATH} -o ${resultPath}`)

    console.log(`Process ${file}, done`)
  } catch (err) {
    console.error(`Failed to process ${file}`, err)
  }
}

function formatLine(line, idx) {
  // comment
  line = line.replace(/\[.+?\]/g, `<span class='comment'>$&</span>`)

  // person
  line = line.replace(/^\w.+?:/g, `<span class='person'>$&</span>`)

  // highlight
  line = line.replace(/\*(.+?)\*/g, `<span class='highlight'>$1</span>`)

  return idx === 0
    ? `<p><a class="title" href="https://github.com/cj1128/learn-english-with-friends">${line}</a></p>`
    : `<p>${line}</p>`
}

function genHTML(content) {
  return `<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    ${content}
  </body>
</html>
`
}
