from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo")

def generate_linkedin_post(offer_id: str, title: str, description: str, criteria: dict) -> str:
    prompt = f"""
You are an expert recruiter. Generate a LinkedIn job announcement post.
Offer ID: {offer_id}
Title: {title}
Description: {description}
Criteria:
"""
    for k, v in criteria.items():
        prompt += f"- {k}: {v}\n"
    prompt += "\nProvide a concise, engaging LinkedIn post (2–3 short paragraphs)."
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
