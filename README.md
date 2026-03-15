# Market Analysis Agent

This project implements a small agent-style system that generates a
market analysis report for a product in a given region.

The user provides:

-   a product name
-   a region
-   a request such as **"Generate a market analysis report"**

The system then performs several steps automatically:

1.  Search the web for relevant information about the product
2.  Extract structured insights from the retrieved sources
3.  Generate a written market analysis report
4.  Produce simple visualizations
5.  Store the report artifacts locally

The goal is to demonstrate how an AI agent can orchestrate external
tools (search, reasoning, and report generation) to produce a structured
analysis.

------------------------------------------------------------------------

# Architecture

![System Architecture](architecture.png)
High level flow:

    User Request
          ↓
    Planner
          ↓
    Web Research Tool
          ↓
    LLM Insight Extraction
          ↓
    Report Generation
          ↓
    Charts & Visualizations
          ↓
    Local Storage

------------------------------------------------------------------------

# Project Structure

    Market_cruncher_demo_ai
    │
    ├── app/
    │   ├── main.py
    │   ├── routes.py
    │   ├── orchestrator.py
    │   ├── planner.py
    │   ├── schemas.py
    │   ├── llm_client.py
    │   ├── report_store.py
    │   ├── report_formatter.py
    │   └── visualizations.py
    │
    ├── tools/
    │   └── web_research.py
    │
    ├── tests/
    │   ├── test_api.py
    │   ├── test_orchestrator.py
    │   └── test_web_research.py
    │
    ├── reports/
    │
    ├── docs/
    │   └── architecture.png
    │
    ├── Dockerfile
    ├── requirements.txt
    └── README.md

Main components:

**Planner**\
Determines which tools should be executed for a request.

**Orchestrator**\
Coordinates the workflow and runs the tools in sequence.

**Tools**\
External capabilities used by the agent (for example web search).

**LLM Client**\
Handles calls to the language model for insight extraction and report
generation.

**Report Generator**\
Formats the final report and produces charts.

**Storage Layer**\
Stores generated artifacts locally.

------------------------------------------------------------------------

# Workflow

Typical execution flow:

    User request
       ↓
    Planner decides which tools to use
       ↓
    Web search retrieves evidence
       ↓
    LLM extracts structured insights
       ↓
    LLM generates market report
       ↓
    Charts are generated
       ↓
    Artifacts are stored locally

The API response returns:

-   the execution plan
-   retrieved search results
-   extracted market insights
-   the generated report
-   the location where artifacts were stored

------------------------------------------------------------------------

# Tech Stack

The project uses a lightweight stack:

-   Python
-   FastAPI
-   Serper API (web search)
-   Groq LLM
-   Matplotlib
-   Pytest
-   Docker

------------------------------------------------------------------------

# Running the Project Locally

### 1. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 2. Create a `.env` file

Example:

    SERPER_API_KEY=your_serper_key
    GROQ_API_KEY=your_groq_key

------------------------------------------------------------------------

### 3. Start the API

``` bash
uvicorn app.main:app --reload
```

Open the interactive API docs:

    http://127.0.0.1:8000/docs

Requests can be sent directly from the Swagger UI.

------------------------------------------------------------------------

# Running with Docker

Build the container:

``` bash
docker build -t market-analysis-agent .
```

Run the container:

``` bash
docker run -p 8000:8000 --env-file .env market-analysis-agent
```

Then open:

    http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# Example Request

POST `/analyze`

``` json
{
  "product_name": "Tesla Model 3",
  "region": "US",
  "user_query": "Generate a market analysis report"
}
```

The response includes:

-   retrieved sources
-   extracted insights
-   the generated report
-   where the artifacts were saved

------------------------------------------------------------------------

# Generated Artifacts

Each run generates files stored in the `reports/` directory.

Example:

    reports/
    tesla_model3_us_20260314.json
    tesla_model3_us_20260314.md
    tesla_model3_us_20260314_sentiment.png
    tesla_model3_us_20260314_competitors.png

The markdown report embeds the generated charts.

------------------------------------------------------------------------

# Tests

Run the test suite with:

``` bash
pytest
```

Tests cover:

-   API endpoint behavior
-   orchestrator workflow
-   web research tool

External APIs are mocked so tests run quickly.

------------------------------------------------------------------------

# Limitations

This project is intentionally lightweight for demonstration purposes.

Some simplifications include:

-   limited search depth
-   simple visualization logic
-   no persistent database
-   reports stored locally

The goal is to show the **agent orchestration workflow**, not to build a
full production analytics platform.
