def validate_cv_file(cv_path, logger=None):
    import os
    if not os.path.isfile(cv_path):
        if logger: logger.warning(f"CV file {cv_path} does not exist.")
        return None
    if os.path.getsize(cv_path) == 0:
        if logger: logger.warning(f"CV file {cv_path} is empty.")
        return None
    return True

def get_cv_text_from_docs(docs, cv_id=None, logger=None):
    if not docs or (isinstance(docs, list) and len(docs) == 0):
        if logger: logger.warning(f"CV {cv_id} could not be loaded or is empty after loading.")
        return None
    if isinstance(docs, list):
        cv_text = docs[0].page_content if hasattr(docs[0], 'page_content') else str(docs[0])
    else:
        cv_text = str(docs)
    if not cv_text.strip():
        if logger: logger.warning(f"CV {cv_id} loaded but contains no readable text.")
        return None
    return cv_text

def validate_parsed_cv(parsed_data):
    if not parsed_data or not isinstance(parsed_data, dict):
        return False
    required_fields = ["name", "skills", "experience", "education"]
    missing_fields = [field for field in required_fields if not parsed_data.get(field)]
    if len(missing_fields) == len(required_fields):
        return False
    return True
