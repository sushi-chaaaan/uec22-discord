import json
import subprocess


def md2html_md_to_pdf(filename: str) -> str | None:
    pure_name = filename.removesuffix(".md")
    pdf_opt = '{"format": "A4", "margin": "15mm", "printBackground": true, "preferCSSPageSize": true}'
    pdt_json = json.dumps(pdf_opt)
    launch_opt = (
        '{"args": ["--no-sandbox"],"executablePath": "/usr/bin/google-chrome-stable"}'
    )
    launch_json = json.dumps(launch_opt)
    try:
        subprocess.run(
            f"npx md-to-pdf --stylesheet styles/github-markdown.css --pdf-options {pdt_json} {filename}",
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        print(e)
    else:
        return f"{pure_name}.pdf"


def main():
    md2html_md_to_pdf("tmp/report_2.md")


if __name__ == "__main__":
    main()
