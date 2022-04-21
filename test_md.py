import subprocess

subprocess.run(
    "pandoc -t pdf -s -o tmp/report_2.pdf --pdf-engine=wkhtmltopdf -c styles/github-markdown.css tmp/report_2.md",
    shell=True,
)
