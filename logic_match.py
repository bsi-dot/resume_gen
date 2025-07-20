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
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str):
                            for part in value.split(','):
                                part = part.strip()
                                if part:
                                    similarity = float(util.cos_sim(embed(part), job_embedding))
                                    scored[section].append((similarity, part))
                        elif isinstance(value, list):
                            for val in value:
                                val = str(val).strip()
                                if val:
                                    similarity = float(util.cos_sim(embed(val), job_embedding))
                                    scored[section].append((similarity, val))
                else:
                    text = str(item).strip()
                    similarity = float(util.cos_sim(embed(text), job_embedding))
                    scored[section].append((similarity, text))

        elif isinstance(option, set):
            entries = content if isinstance(content, list) else [content]
            for entry in entries:
                if not isinstance(entry, dict):
                    continue

                identifier = entry.get("company") or entry.get("title") or "unknown"

                for field in option:
                    value = entry.get(field)

                    # Handle list fields like highlights, courses, etc.
                    if isinstance(value, list):
                        for item in value:
                            item = str(item).strip()
                            if item:
                                similarity = float(util.cos_sim(embed(item), job_embedding))
                                scored[section].append((similarity, item, field, identifier))

                    elif isinstance(value, str):
                        for part in value.split(','):
                            part = part.strip()
                            if part:
                                similarity = float(util.cos_sim(embed(part), job_embedding))
                                scored[section].append((similarity, part, field, identifier))

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

    # If subsection grouping is available (4-tuple)
    if sorted_items and len(sorted_items[0]) == 4:
        grouped = defaultdict(list)
        for score, content, field, subgroup in sorted_items:
            grouped[subgroup].append((score, content))

        for subgroup, entries in grouped.items():
            print(f"\n-- {subgroup}")
            for score, content in entries:
                print(f"  SCORE: {score:.4f}")
                print(f"  CONTENT: {content}")

    else:
        # Fallback for regular fields
        for match in sorted_items:
            score = match[0]
            content = match[1] if len(match) == 2 else match[1].get(match[2], "") if isinstance(match[1], dict) else str(match[1])
            print(f"SCORE: {score:.4f}")
            print("CONTENT:", content)


