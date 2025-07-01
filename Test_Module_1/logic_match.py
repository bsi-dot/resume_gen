import yaml
import re
from collections import defaultdict

def extract_optional_fields(config: dict) -> dict:
    optional_config = config.get("optional_fields", {})
    optional_fields = {}

    for section, fields in optional_config.items():
        if isinstance(fields, list):
            optional_fields[section] = set(fields)
        elif fields is True:
            optional_fields[section] = True
        else:
            optional_fields[section] = set()

    return optional_fields

# Load files
try:
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
except Exception as e:
    print("Error loading config.yaml:", e)

try:
    with open('full_resume.yaml') as f:
        full_resume = yaml.safe_load(f)
except Exception as e:
    print("Error loading full_resume.yaml:", e)

try:
    with open('job_description.txt') as f:
        job_description = f.read()
except Exception as e:
    print("Error loading job_description.txt:", e)
  
#optional fields Extraction

optional_fields = extract_optional_fields(config)
print("Extracted optional fields:", optional_fields)



def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def score_optional_sections(full_resume, optional_fields, job_description):
    job_tokens = tokenize(job_description)
    scored = defaultdict(list)

    for section, option in optional_fields.items():
        content = full_resume.get(section)
        if not content:
            continue

        # Entire section is optional
        if option is True:
            entries = content if isinstance(content, list) else [content]
            for item in entries:
                text = str(item)
                tokens = tokenize(text)
                score = len(tokens & job_tokens)
                scored[section].append((score, item))

        # Subfields are optional
        elif isinstance(option, set):
            entries = content if isinstance(content, list) else [content]
            for item in entries:
                for field in option:
                    value = item.get(field)
                    if value:
                        text = str(value)
                        tokens = tokenize(text)
                        score = len(tokens & job_tokens)
                        scored[section].append((score, item, field))

    return scored


scored_sections = score_optional_sections(full_resume, optional_fields, job_description)

# Show top matches per section
for section, items in scored_sections.items():
    print(f"\nSECTION: {section}")
    sorted_items = sorted(items, reverse=True, key=lambda x: x[0])
    for match in sorted_items:
        print("SCORE:", match[0])
        print("CONTENT:", match[1] if optional_fields[section] is True else match[1].get(match[2]))