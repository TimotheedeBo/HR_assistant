import os
import logging

from langchain_openai import OpenAIEmbeddings

from cv_parser.loader import load_cv
from cv_parser.extractor import extract_cv_data
from cv_parser.validation import (
    validate_cv_file,
    get_cv_text_from_docs,
    validate_parsed_cv,
)
from job_matching.matcher import match_cv_to_offers, match_offer_to_cvs
from job_matching.filters import get_offer_criteria
from cv_generation.generator import generate_company_cv
from utils.general import flatten_cv_data, load_text_file, ensure_dir_exists
from utils.export import export_matches_csv

logger = logging.getLogger(__name__)
from dotenv import load_dotenv
load_dotenv()


def load_and_validate_all_cvs(cv_dir: str) -> dict:
    all_cvs = {}
    for f in os.listdir(cv_dir):
        if not (f.endswith(".pdf") or f.endswith(".txt")):
            continue
        cv_id = os.path.splitext(f)[0]
        path = os.path.join(cv_dir, f)
        if not validate_cv_file(path, logger):
            continue
        docs = load_cv(path)
        cv_text = get_cv_text_from_docs(docs, cv_id, logger)
        if not cv_text:
            continue
        parsed = extract_cv_data(cv_text)
        if not validate_parsed_cv(parsed):
            logger.warning(f"CV {cv_id} failed validation. Skipping.")
            continue
        all_cvs[cv_id] = parsed
    return all_cvs


def load_offers_and_criteria(offer_dir: str, criteria_dir: str) -> (dict, dict):
    all_offers = {}
    offer_criteria = {}
    for f in os.listdir(offer_dir):
        if not f.endswith(".txt"):
            continue
        offer_id = os.path.splitext(f)[0]
        text = load_text_file(os.path.join(offer_dir, f))
        all_offers[offer_id] = text
        offer_criteria[offer_id] = get_offer_criteria(offer_id, criteria_dir)
    return all_offers, offer_criteria


def score_and_generate_cvs(
    all_cvs: dict,
    all_offers: dict,
    offer_criteria: dict,
    template_path: str,
    output_dir: str,
) -> (dict, dict):
    ensure_dir_exists(output_dir)
    embeddings = OpenAIEmbeddings()

    cv_to_offers_scores = match_cv_to_offers(all_cvs, all_offers, offer_criteria)
    offer_to_cvs_scores = match_offer_to_cvs(all_cvs, all_offers, offer_criteria)

    for cv_id, scores in cv_to_offers_scores.items():
        if not scores:
            continue
        best_id, best_score = scores[0]
        best_title = all_offers[best_id].splitlines()[0][:80]
        info = {"score": best_score, "offer_id": best_id, "offer_title": best_title}
        out_path = os.path.join(output_dir, f"{cv_id}_{best_id}_final_cv.docx")
        generate_company_cv(all_cvs[cv_id], template_path, out_path, info)

    export_matches_csv(cv_to_offers_scores, output_dir)
    return cv_to_offers_scores, offer_to_cvs_scores
