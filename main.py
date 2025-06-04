import os
import logging
from dotenv import load_dotenv

from pipeline import (
    load_and_validate_all_cvs,
    load_offers_and_criteria,
    score_and_generate_cvs,
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    cv_dir = "data/cvs/"
    offer_dir = "data/jobs/"
    criteria_dir = "data/jobs/offer_criteria"
    template_path = "data/templates/cv_template.docx"
    output_dir = "output/"

    all_cvs = load_and_validate_all_cvs(cv_dir)
    if not all_cvs:
        logger.warning("No valid CVs found.")

    all_offers, offer_criteria = load_offers_and_criteria(offer_dir, criteria_dir)
    if not all_offers:
        logger.warning("No job offers found.")

    cv_to_offers, offer_to_cvs = score_and_generate_cvs(
        all_cvs, all_offers, offer_criteria, template_path, output_dir
    )

    logger.info("Ranking of job offers for each CV:")
    for cv_id, scores in cv_to_offers.items():
        logger.info(f"CV {cv_id}:")
        for offer_id, score in scores:
            logger.info(f"  Offer {offer_id} – Score: {score:.3f}")

    logger.info("Ranking of CVs for each job offer:")
    for offer_id, scores in offer_to_cvs.items():
        logger.info(f"Offer {offer_id}:")
        for cv_id, score in scores:
            logger.info(f"  CV {cv_id} – Score: {score:.3f}")


if __name__ == "__main__":
    main()
