from jinja2 import Environment, FileSystemLoader
import subprocess
import os
import yaml

TEMPLATE_FILE = "boilerplate.tex"
YAML_FILE = "source.yaml"
OUTPUT_TEX = "output_resume.tex"
OUTPUT_PDF = "output_resume.pdf"

with open(YAML_FILE, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

env = Environment(
    block_start_string="{%",
    block_end_string="%}",
    variable_start_string="{{",
    variable_end_string="}}",
    loader=FileSystemLoader("."),
)

template = env.get_template(TEMPLATE_FILE)
rendered_tex = template.render(data)

with open(OUTPUT_TEX, "w", encoding="utf-8") as f:
    f.write(rendered_tex)

try:
    subprocess.run(["pdflatex", "-interaction=nonstopmode", OUTPUT_TEX], check=True)
    print(f"✅ PDF generated: {OUTPUT_PDF}")
except subprocess.CalledProcessError as e:
    print("❌ LaTeX compilation failed:")
    print(e)
