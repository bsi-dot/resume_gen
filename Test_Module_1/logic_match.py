from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import yaml

def rank_entries_by_relevance(entries, job_description):
    vectorizer = TfidfVectorizer().fit_transform([job_description] + entries)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    return sorted(zip(entries, similarity[0]), key=lambda x: -x[1])


with open('full_resume.yaml') as f:
    full_resume = yaml.safe_load(f)

with open('config.yaml') as f:
    config = yaml.safe_load(f)

with open('job_description.txt') as f:
    job_description = f.read()