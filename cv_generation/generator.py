from docx import Document
from dotenv import load_dotenv
load_dotenv()

def generate_company_cv(data: dict, template_path: str, output_path: str, match_info: dict = None):
    doc = Document(template_path)
    for para in doc.paragraphs:
        if "{{full_name}}" in para.text:
            para.text = para.text.replace("{{full_name}}", data.get("name", "N/A"))
        if "{{email}}" in para.text:
            para.text = para.text.replace("{{email}}", data.get("contact_info", "N/A"))
        if "{{skills}}" in para.text:
            para.text = para.text.replace("{{skills}}", data.get("skills", "N/A"))
        if "{{experience}}" in para.text:
            para.text = para.text.replace("{{experience}}", data.get("experience", "N/A"))
        if "{{score}}" in para.text:
            score_text = f"{match_info['score']:.2f}" if match_info and "score" in match_info else "N/A"
            para.text = para.text.replace("{{score}}", score_text)
        if "{{best_offer_title}}" in para.text:
            offer_title = match_info.get("offer_title", "N/A") if match_info else "N/A"
            para.text = para.text.replace("{{best_offer_title}}", offer_title)
        if "{{offer_id}}" in para.text:
            offer_id = match_info.get("offer_id", "N/A") if match_info else "N/A"
            para.text = para.text.replace("{{offer_id}}", offer_id)
    doc.save(output_path)
