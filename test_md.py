import subprocess


def md2html(filename: str):
    pure_name = filename.removesuffix(".md")
    subprocess.run(
        f"pandoc -s -o {pure_name}.html --mathjax -c styles/github-markdown.css {filename}",
        shell=True,
    )
    return f"{pure_name}.html"


def html2pdf(filename: str):
    pure_name = filename.removesuffix(".html")
    subprocess.run(
        f"wkhtmltopdf --disable-smart-shrinking --margin-top 20 --margin-left 20 --margin-right 20 --margin-bottom 20 --footer-center '[page]/[topage]' {filename} {pure_name}.pdf",
        shell=True,
    )
    return f"{pure_name}.pdf"


def main():
    html = md2html("tmp/report_2.md")
    pdf = html2pdf(html)
    print(pdf)


if __name__ == "__main__":
    main()
