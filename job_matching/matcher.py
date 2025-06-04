from langchain_openai import OpenAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from job_matching.filters import passes_hard_filters, soft_filter_score
from utils.general import flatten_cv_data
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings()

def cosine_score(text1: str, text2: str) -> float:
    try:
        vec1 = embeddings.embed_query(text1)
        vec2 = embeddings.embed_query(text2)
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return float(cosine_similarity([vec1], [vec2])[0][0])
    except Exception:
        return 0.0

def match_cv_to_offers(cv_dict: dict, offer_dict: dict, offer_criteria: dict, top_k=3) -> dict:
    results = {}
    for cv_id, cv_data in cv_dict.items():
        offer_scores = []
        for offer_id, offer_text in offer_dict.items():
            criteria = offer_criteria.get(offer_id, {})
            # Hard filter
            if not passes_hard_filters(cv_data, criteria):
                continue
            text_str = flatten_cv_data(cv_data)
            embed_score = cosine_score(text_str, offer_text)
            soft_score = soft_filter_score(cv_data, criteria)
            # Combined score: 70% embed + 30% soft filter
            combined = 0.7 * embed_score + 0.3 * soft_score
            offer_scores.append((offer_id, combined))
        offer_scores.sort(key=lambda x: x[1], reverse=True)
        results[cv_id] = offer_scores[:top_k]
    return results

def match_offer_to_cvs(cv_dict: dict, offer_dict: dict, offer_criteria: dict, top_k=3) -> dict:
    results = {}
    for offer_id, offer_text in offer_dict.items():
        criteria = offer_criteria.get(offer_id, {})
        cv_scores = []
        for cv_id, cv_data in cv_dict.items():
            if not passes_hard_filters(cv_data, criteria):
                continue
            embed_score = cosine_score(flatten_cv_data(cv_data), offer_text)
            soft_score = soft_filter_score(cv_data, criteria)
            combined = 0.7 * embed_score + 0.3 * soft_score
            cv_scores.append((cv_id, combined))
        cv_scores.sort(key=lambda x: x[1], reverse=True)
        results[offer_id] = cv_scores[:top_k]
    return results
