import yaml
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util

# -------------------- Functions --------------------

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

def embed(text):
    return model.encode(text, convert_to_tensor=True)

def score_optional_sections_cosine(full_resume, optional_fields, job_description):
    job_embedding = embed(job_description)
    scored = defaultdict(list)

    for section, option in optional_fields.items():
        content = full_resume.get(section)
        if not content:
            continue

        if option is True:
            entries = content if isinstance(content, list) else [content]
            for item in entries:
                text = str(item)
                similarity = float(util.cos_sim(embed(text), job_embedding))
                scored[section].append((similarity, item))

        elif isinstance(option, set):
            entries = content if isinstance(content, list) else [content]
            for item in entries:
                for field in option:
                    value = item.get(field)
                    if value:
                        text = str(value)
                        similarity = float(util.cos_sim(embed(text), job_embedding))
                        scored[section].append((similarity, item, field))
    return scored

# -------------------- Load Inputs --------------------

with open('config.yaml') as f:
    config = yaml.safe_load(f)

with open('full_resume.yaml') as f:
    full_resume = yaml.safe_load(f)

with open('job_description.txt') as f:
    job_description = f.read()

# -------------------- Main Logic --------------------

optional_fields = extract_optional_fields(config)
model = SentenceTransformer('all-MiniLM-L6-v2')
scored_sections = score_optional_sections_cosine(full_resume, optional_fields, job_description)

# -------------------- Output Top Matches --------------------

for section, items in scored_sections.items():
    print(f"\nSECTION: {section}")
    sorted_items = sorted(items, reverse=True, key=lambda x: x[0])
    for match in sorted_items:
        print(f"SCORE: {match[0]:.4f}")
        print("CONTENT:", match[1] if optional_fields[section] is True else match[1].get(match[2]))
