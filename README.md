# 🕵️ API Failure Detection & Debugging Agent

**Hackathon Submission** – Problem Statement #4

## Demo Video
[Link to your demo video (upload to YouTube unlisted or Google Drive)]

## Features
- Real-time API log monitoring (simulated with Python generator)
- Detects: error spikes, latency issues, recurring 500s
- AI-powered root cause analysis using **Google Gemini**
- Manual failure injection for easy demo
- Clean Streamlit dashboard with auto-refresh

## Tech Stack
- Python, Streamlit, Pandas
- Google Gemini API (free tier)
- 100% local log simulation

## How to Run
1. Clone repo
2. Create venv: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install: `pip install -r requirements.txt`
5. Add `.env` file with `GEMINI_API_KEY=your_key`
6. Run log generator: `python log_generator.py` (in one terminal)
7. Run dashboard: `streamlit run app.py` (in another terminal)

## Future Improvements
- Slack/Teams alert integration
- Historical anomaly learning
- Direct GitHub auto-fix PR

## Team
- Srushti Nikam
- Renaissance Nath

## Repository Structure
- `log_generator.py` – Simulates API logs
- `anomaly_detector.py` – Detection logic
- `llm_explainer.py` – Gemini integration
- `app.py` – Streamlit UI
- `utils.py` – Demo helper