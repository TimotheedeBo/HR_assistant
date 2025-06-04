# HRAssistant Final

**AI-powered HR platform** for parsing CVs, managing job offers with dynamic hard & soft filters, matching via embeddings, and generating company-formatted CVs.

## Features

- **CV Parsing**: Extract structured information from PDF/TXT via LangChain & OpenAI.
- **Offer Management**: Create, edit, delete offers; auto-generate IDs; manage criteria (hard & soft) per offer.
- **Matching & Scoring**: Apply hard filters; calculate soft filter score; use embeddings + cosine similarity; combine scores.
- **CV Generation**: Fill a company template with candidate data and match info.
- **Feedback System**: HR can provide feedback per CV per offer.
- **Export**: Download match results as CSV.
- **Template Management**: List and upload new CV templates (.docx).
- **Dashboard UI**: Efficient Streamlit interface with tabs.

## Installation

```bash
git clone <repo_url>
cd HRAssistant_Final
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
streamlit run interface_main.py
```

- **Create/Edit Offers**: Define title, auto-ID, description, and both hard/soft criteria.
- **Configure Offer Criteria**: Adjust required and preferred filters.
- **Manage Templates**: View existing templates and upload new ones.
- **Match & Ranking Dashboard**: View ranked CVs per offer, give feedback, and export to CSV.

Place sample CVs in `data/cvs/` (.pdf or .txt) and job offers in `data/jobs/` (.txt). Templates go in `data/templates/`.
