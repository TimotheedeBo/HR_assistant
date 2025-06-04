import json
import os

def get_offer_criteria(offer_id, criteria_dir):
    path = os.path.join(criteria_dir, f"{offer_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def passes_hard_filters(cv_data, filters):
    required_skills = filters.get("required_skills", [])
    cv_skills = cv_data.get("skills", "").lower()
    for skill in required_skills:
        if skill.lower() not in cv_skills:
            return False
    required_degree = filters.get("required_degree")
    if required_degree:
        cv_edu = cv_data.get("education", "").lower()
        if required_degree.lower() not in cv_edu:
            return False
    min_years = filters.get("min_years_experience")
    if min_years:
        cv_exp = cv_data.get("experience", "")
        years = extract_years_of_experience(cv_exp)
        if years < min_years:
            return False
    return True

def soft_filter_score(cv_data, filters):
    preferred_skills = filters.get("preferred_skills", [])
    if not preferred_skills:
        return 0.0
    cv_skills = cv_data.get("skills", "").lower().split(',')
    match_count = sum(1 for s in preferred_skills if s.lower() in cv_data.get("skills", "").lower())
    return match_count / len(preferred_skills)

def extract_years_of_experience(experience_field):
    import re
    match = re.search(r'(\d+)\s*(years)', experience_field, re.IGNORECASE)
    return int(match.group(1)) if match else 0
