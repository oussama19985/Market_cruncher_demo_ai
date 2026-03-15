# Market Analysis Agent

This project implements a small agent-based system that generates a
market analysis report for a product in a given region.

The user provides:

-   a product name\
-   a region\
-   a request such as **"Generate a market analysis report"**

The system then performs several steps automatically:

1.  Search the web for relevant information about the product
2.  Extract structured insights from the retrieved sources
3.  Generate a written market analysis report
4.  Produce simple visualizations
5.  Store the report and artifacts locally

The goal is to demonstrate how an AI agent can orchestrate external
tools (search, LLM reasoning, report generation) to produce a structured
analysis automatically.

------------------------------------------------------------------------

# Project Structure

app/ - main.py - routes.py - orchestrator.py - planner.py - schemas.py -
llm_client.py - report_store.py - report_formatter.py -
visualizations.py

tools/ - web_research.py

tests/ - test_api.py - test_orchestrator.py - test_web_research.py

reports/

Dockerfile requirements.txt

Main components:

**Planner**\
Decides which tools should run for a request.

**Orchestrator**\
Coordinates the workflow and executes tools step by step.

**Tools**\
External capabilities the agent can use (for example web search).

**LLM Client**\
Handles calls to the language model for insight extraction and report
generation.

**Report Generator**\
Formats the final report and generates visualizations.

**Storage Layer**\
Stores generated reports and artifacts locally.

------------------------------------------------------------------------

# Workflow

The typical execution flow is:

User request\
↓\
Planner decides which tools to use\
↓\
Web search retrieves evidence\
↓\
LLM extracts structured insights from the evidence\
↓\
LLM generates a report\
↓\
Charts and visualizations are generated\
↓\
Artifacts are stored locally

The API response contains:

-   the execution plan\
-   retrieved search results\
-   extracted market insights\
-   the generated report\
-   the path where artifacts were stored


![System Architecture](architecture.png)
------------------------------------------------------------------------

# Tech Stack

The implementation uses a lightweight stack:

-   Python
-   FastAPI for the API layer
-   Serper API for web search
-   Groq LLM for reasoning and report generation
-   Matplotlib for simple visualizations
-   Pytest for testing
-   Docker for reproducible execution

------------------------------------------------------------------------

# Running the Project Locally

## 1. Install dependencies

pip install -r requirements.txt

------------------------------------------------------------------------

## 2. Create a `.env` file

Example:

SERPER_API_KEY=your_serper_key\
GROQ_API_KEY=your_groq_key

------------------------------------------------------------------------

## 3. Start the API

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Running with Docker

Build the container:

docker build -t market-analysis-agent .

Run the container:

docker run -p 8000:8000 --env-file .env market-analysis-agent

Then open:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Example Request

POST /analyze

{ "product_name": "Tesla Model 3", "region": "US", "user_query":
"Generate a market analysis report" }

The response includes:

-   retrieved sources\
-   extracted insights\
-   the generated report\
-   the location where artifacts were stored

------------------------------------------------------------------------

# Generated Artifacts

Each analysis produces files stored in the `reports/` directory.

Example:

reports/ tesla_model3_us_20260314.json tesla_model3_us_20260314.md
tesla_model3_us_20260314_sentiment.png
tesla_model3_us_20260314_competitors.png

The Markdown report embeds the generated charts.

------------------------------------------------------------------------

# Tests

Run tests with:

pytest

Tests cover:

-   API endpoint behavior\
-   orchestrator workflow\
-   web research tool

External APIs are mocked so tests stay fast and deterministic.
