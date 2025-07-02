import streamlit as st
import os
from utils.general import load_text_file, flatten_cv_data
from job_matching.matcher import cosine_score
from cv_parser.extractor import extract_cv_data
from langchain_openai import OpenAIEmbeddings

CVS_DIR   = "data/cvs"
OFFERS_DIR= "data/jobs"

def show_cv_matcher():
    st.header("🔍 CV ↔️ Offer Matching")

    # build lists
    cv_files    = [f for f in os.listdir(CVS_DIR) if f.endswith((".pdf", ".txt"))]
    offer_files = [f.replace(".txt","") for f in os.listdir(OFFERS_DIR) if f.endswith(".txt")]

    if not cv_files or not offer_files:
        st.info("Please upload at least one CV and create at least one job offer first.")
        return

    # selectors
    cv_sel    = st.selectbox("Select CV", cv_files, key="match_cv")
    offer_sel = st.selectbox("Select Offer", offer_files, key="match_offer")

    if st.button("Compute Compatibility", key="match_compute"):
        # load & parse CV text
        if cv_sel.endswith(".txt"):
            raw = load_text_file(os.path.join(CVS_DIR, cv_sel))
        else:
            docs = __import__('cv_parser.loader', fromlist=['load_cv']).load_cv(os.path.join(CVS_DIR, cv_sel))
            raw = __import__('cv_parser.validation', fromlist=['get_cv_text_from_docs'])\
                    .get_cv_text_from_docs(docs, cv_sel)
        cv_data = extract_cv_data(raw)

        # flatten for embedding
        flat = flatten_cv_data(cv_data)

        # compute embeddings
        emb = OpenAIEmbeddings()
        cv_vec  = emb.embed_documents([flat])[0]
        job_txt = load_text_file(os.path.join(OFFERS_DIR, f"{offer_sel}.txt"))
        job_vec = emb.embed_documents([job_txt])[0]
        score = cosine_score(cv_vec, job_vec)

        st.metric(label="Compatibility Score", value=f"{score:.2f}")
        # optionally show structured match summary
        st.json(cv_data)  # or pretty-print any fields you like
