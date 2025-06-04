import os
import pandas as pd

def export_matches_csv(cv_to_offers_scores: dict, output_dir: str):
    rows = []
    for cv_id, offers in cv_to_offers_scores.items():
        for offer_id, score in offers:
            rows.append({'cv_id': cv_id, 'offer_id': offer_id, 'score': score})
    df = pd.DataFrame(rows)
    csv_path = os.path.join(output_dir, 'all_matches.csv')
    df.to_csv(csv_path, index=False)
