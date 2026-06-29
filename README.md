<div align="center">

# 🧠 IntelliSearch — AI-Powered Research Engine

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green?style=for-the-badge&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-blueviolet?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=for-the-badge&logo=streamlit&logoColor=white)

**A fully autonomous AI research engine that searches the web, scrapes sources, writes structured research reports, and critiques them — all in one seamless pipeline.**

🔗 **Live Demo:** [multiagentresearchsystem-4k4lzlhioy43pvc9awelbr.streamlit.app](https://multiagentresearchsystem-4k4lzlhioy43pvc9awelbr.streamlit.app/)

</div>

---

## 📌 Problem Statement

Conducting in-depth research on any topic is time-consuming and fragmented — you have to search multiple sources, read through pages, synthesize information, and then write a structured report. **IntelliSearch automates this entire workflow** using a 4-step AI pipeline that delivers a polished, cited research report in minutes.

---

## 🎥 Demo

<div align="center">
  <img width="800" alt="IntelliSearch Demo" src="https://github.com/user-attachments/assets/3cfdd460-6ea5-4fd8-af10-dd36b4c28a4c" />
</div>

---

## 🏗️ Architecture

```
User Input (Topic)
       │
       ▼
┌─────────────────┐
│  Search Agent   │  ── Calls Tavily API directly to find top 5 relevant web sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reader Agent   │  ── Scrapes the most relevant URL directly using BeautifulSoup
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Chain   │  ── Groq LLM synthesizes research into a structured report (LCEL)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic Chain   │  ── Groq LLM reviews and scores the report with feedback (LCEL)
└─────────────────┘
         │
         ▼
  Final Report + Score + Feedback + Download (.md)
```

---

## ✨ Features

- 🔍 **Search Agent** — Calls Tavily API directly to retrieve top 5 sources with titles, URLs, and snippets
- 📄 **Reader Agent** — Picks the most relevant URL and scrapes clean readable content using BeautifulSoup
- ✍️ **Writer Chain** — Uses LCEL pipeline (`prompt | llm | StrOutputParser`) to write a structured report with Introduction, Key Findings, Conclusion, and Sources
- 🧐 **Critic Chain** — Reviews the report and gives a score out of 10 with Strengths and Areas to Improve
- ⬇️ **Download Report** — Export the final report as a `.md` file
- 🎨 **Beautiful Dark UI** — Custom purple-themed Streamlit UI with real-time pipeline status indicators
- ⚡ **100% Free** — Powered by Groq (free tier) and Tavily (free tier), no OpenAI credits needed

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq API (Free) |
| Pipeline | LCEL (LangChain Expression Language) with Runnables |
| Web Search | Tavily API (direct call) |
| Web Scraping | BeautifulSoup4 + Requests (direct call) |
| Frontend | Streamlit |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
multi_agent_research_system/
│
├── agents.py          # Search Agent, Reader Agent, Writer Chain, Critic Chain
├── tools.py           # web_search (Tavily) and scrape_url (BeautifulSoup) tools
├── pipeline.py        # 4-step research pipeline orchestrator (CLI version)
├── app.py             # Streamlit web UI
├── requirements.txt   # All dependencies
├── .env               # API keys (not committed to GitHub)
└── .gitignore         # Ignores .env and __pycache__
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A free [Groq API key](https://console.groq.com) — no credit card needed
- A free [Tavily API key](https://app.tavily.com) — 1000 free searches/month

### 1. Clone the Repository

```bash
git clone https://github.com/Ayushyadav14/multi_agent_research_system.git
cd multi_agent_research_system
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **Get your free keys:**
> - Groq: [console.groq.com](https://console.groq.com) → API Keys → Create API Key
> - Tavily: [app.tavily.com](https://app.tavily.com) → Dashboard → Copy API Key

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🖥️ Usage

1. Enter any research topic in the input box (e.g. *"Impact of AI on healthcare 2025"*)
2. Click **🧠 Run IntelliSearch**
3. Watch all 4 pipeline steps run in real-time
4. Read the full structured report with key findings and sources
5. Download the report as a `.md` file

---

## 🤖 How the Pipeline Works

### Step 1 — Search Agent
Calls the Tavily API directly to find the most recent and reliable information. Returns titles, URLs, and snippets from the top 5 results. No LLM involved — fast and always reliable.

### Step 2 — Reader Agent
Extracts the most relevant URL from search results and scrapes it directly using BeautifulSoup. Returns clean readable text for deeper analysis. No LLM involved — zero tool-calling errors.

### Step 3 — Writer Chain (LCEL)
Takes the combined search results and scraped content, and uses Groq LLM via a structured LCEL pipeline to write a detailed report:
- Introduction
- Key Findings (minimum 3 points)
- Conclusion
- Sources

### Step 4 — Critic Chain (LCEL)
Groq LLM reviews the final report and provides:
- A score out of 10
- Strengths
- Areas to Improve
- One-line verdict

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GROQ_API_KEY` | API key for Groq LLM (Llama 3.3 70B) | [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | API key for Tavily web search | [app.tavily.com](https://app.tavily.com) |

---

## 📦 Dependencies

```
langchain>=0.2.0
langchain-core>=0.2.0
langchain-community>=0.2.0
langchain-groq>=0.1.0
tavily-python>=0.3.0
beautifulsoup4>=4.12.0
requests>=2.31.0
lxml>=5.0.0
python-dotenv>=1.0.0
streamlit>=1.35.0
rich>=13.7.0
pydantic>=2.5.0
aiohttp>=3.9.0
tenacity>=8.2.0
```

---

## ⚠️ Important Notes

- The `.env` file is **not committed** to GitHub. Never share your API keys publicly.
- Groq's free tier has a daily token limit of 100,000 tokens. If you hit it, wait until midnight UTC for it to reset.
- Tavily's free tier allows 1000 searches/month which is more than enough for personal use.

---

## 🙋 Author

**Ayush Yadav**
- GitHub: [@Ayushyadav14](https://github.com/Ayushyadav14)
- Email: ayushy.in@gmail.com

---

<div align="center">
  <b>If you found this useful, please ⭐ star the repository!</b>
</div>