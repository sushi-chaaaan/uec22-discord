import subprocess
import json


def md2html_md_to_pdf(filename: str):
    pure_name = filename.removesuffix(".md")
    pdf_opt = '{\"format\": \"A4\", \"margin\": \"20mm\", \"printBackground\": true}'
    pdt_json = json.dumps(pdf_opt)
    subprocess.run(
        f"npx md-to-pdf --stylesheet styles/github-markdown.css --highlight-style github --pdf-options {pdt_json} {filename}",
        shell=True,
    )
    return


def main():
    md2html_md_to_pdf("tmp/report_2.md")


if __name__ == "__main__":
    main()
