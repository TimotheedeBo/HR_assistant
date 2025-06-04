import os
import re
import unicodedata

def ensure_dir_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def flatten_cv_data(cv_data: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in cv_data.items() if isinstance(v, str))

def generate_offer_id(title: str) -> str:
    title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode()
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', title.strip().lower())
    return slug.strip('_')

def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
