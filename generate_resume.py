from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
import subprocess
import os

def render_and_compile(template_file, yaml_file, output_tex, output_pdf):
    # Load YAML
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Jinja2 setup
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape([]),
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{{",
        variable_end_string="}}"
    )

    template = env.get_template(template_file)
    rendered = template.render(data if data else {})

    # Save the output .tex
    with open(output_tex, "w", encoding="utf-8") as f:
        f.write(rendered)

    # Compile with pdflatex
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", output_tex], check=True)
        print(f"✅ PDF generated: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print("❌ LaTeX compilation failed:")
        print(e)

# Define default paths
configs = [

    {
        "template": "simple_boilerplate.tex",
        "yaml": "simple_data.yaml",
        "tex": "simple_output.tex",
        "pdf": "simple_output.pdf"
    }
]

# Use the first valid combination
for cfg in configs:
    if os.path.exists(cfg["template"]) and os.path.exists(cfg["yaml"]):
        print(f"🔍 Using template: {cfg['template']} with data: {cfg['yaml']}")
        render_and_compile(cfg["template"], cfg["yaml"], cfg["tex"], cfg["pdf"])
        break
else:
    print("❌ No valid template/data file combination found.")
