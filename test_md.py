import json
import subprocess

import mistletoe


def make(filename: str):
    pure_name = filename.removesuffix(".md")
    with open(filename, "r") as f:
        result = mistletoe.markdown(f)
    with open(f"{pure_name}.html", "w") as f:
        f.write(result)


def md2html_md_to_pdf(filename: str) -> str | None:
    pure_name = filename.removesuffix(".md")
    marked_opt = '{"gfm": true}'
    marked_json = json.dumps(marked_opt)
    pdf_opt = '{"format": "A4", "margin": "15mm", "printBackground": true}'
    pdt_json = json.dumps(pdf_opt)
    launch_opt = '{"args": ["--no-sandbox","--disable-setuid-sandbox"],"executablePath": "/usr/bin/google-chrome-stable"}'
    launch_json = json.dumps(launch_opt)
    try:
        subprocess.run(
            f"npx md-to-pdf --stylesheet styles/github-markdown.css --highlight-style github --marked-options {marked_json} --launch-options {launch_json} --pdf-options {pdt_json} {filename}",
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        print(e)
    else:
        return f"{pure_name}.pdf"


def read_md(filename: str) -> str:
    with open(filename, "r") as f:
        print(f.read())
        return f.read()


def main():
    # make("tmp/report_2.md")
    md2html_md_to_pdf("tmp/report_2.md")


if __name__ == "__main__":
    main()
