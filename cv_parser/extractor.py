import logging
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-3.5-turbo")

def extract_cv_data(cv_text: str) -> dict:
    prompt = f"""
    Extract relevant structured information from this CV text:

    {cv_text}

    Provide the result in JSON format with fields:
    - name
    - contact_info
    - skills
    - experience
    - education
    - certifications (optional)
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        import json
        data = json.loads(response.content)
        return data
    except Exception as e:
        logger.error(f"Error extracting CV data: {e}")
        return {
            "name": "",
            "contact_info": "",
            "skills": "",
            "experience": "",
            "education": "",
            "certifications": ""
        }
