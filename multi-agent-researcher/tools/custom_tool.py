import logging
import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import numpy as np
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from scipy import stats
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# THIS IS THE KEY CHANGE: We now import the BaseTool from LangChain's core library.
from langchain_core.tools import BaseTool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# =======================================================
# All your tool classes from before, now inheriting from the correct BaseTool.
# The code inside your tools is excellent and requires no logical changes.
# =======================================================

# =======================================================
# LITERATURE REVIEW TOOLS
# =======================================================

class PaperSearchInput(BaseModel):
    query: str = Field(..., description="Search query for research papers", min_length=3)
    max_results: int = Field(10, description="Maximum number of papers to return", ge=1, le=50)

class PaperSearchTool(BaseTool):
    name: str = "paper_search"
    description: str = "Searches arXiv for relevant research papers."
    args_schema: Type[BaseModel] = PaperSearchInput

    def _run(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        try:
            url = f"http://export.arxiv.org/api/query?search_query=all:{query.replace(' ', '+')}&start=0&max_results={max_results}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            namespace = {"atom": "http://www.w3.org/2005/Atom"}
            papers = []
            for entry in root.findall("atom:entry", namespace):
                papers.append({
                    "title": entry.find("atom:title", namespace).text.strip(),
                    "abstract": entry.find("atom:summary", namespace).text.strip(),
                    "link": entry.find("atom:id", namespace).text.strip(),
                    "authors": [author.find("atom:name", namespace).text.strip() for author in entry.findall("atom:author", namespace)]
                })
            return {"papers": papers}
        except Exception as e:
            logger.error(f"Paper search failed: {e}")
            return {"error": str(e), "papers": []}

class PapersRAGInput(BaseModel):
    query: str = Field(..., description="Query to retrieve and analyze papers", min_length=3)

class PapersRAGTool(BaseTool):
    name: str = "papers_rag"
    description: str = "Retrieves papers and generates intelligent summaries using semantic similarity analysis."
    args_schema: Type[BaseModel] = PapersRAGInput

    def _run(self, query: str) -> Dict[str, Any]:
        search_tool = PaperSearchTool()
        search_results = search_tool._run(query=query, max_results=10)
        
        if search_results.get("error"):
            return {"answer": f"Failed to search papers: {search_results['error']}", "citations": [], "error": search_results["error"]}
        
        papers = search_results.get("papers", [])
        if not papers:
            return {"answer": "No relevant papers found for the given query.", "citations": []}
            
        documents = [f"{p['title']} {p['abstract']}" for p in papers if p.get("abstract")]
        if not documents:
            return {"answer": "No papers with sufficient content found.", "citations": []}
            
        vectorizer = TfidfVectorizer(stop_words='english')
        doc_vectors = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, doc_vectors).flatten()
        
        top_indices = similarities.argsort()[-3:][::-1]
        
        answer_parts = []
        for i, idx in enumerate(top_indices, 1):
            paper = papers[idx]
            answer_parts.append(f"{i}. **{paper['title']}**\n   Summary: {paper['abstract'][:400]}...")

        final_answer = "\n\n".join(answer_parts)
        citations = [papers[i]['link'] for i in top_indices]
        
        return {"answer": final_answer, "citations": citations}

# =======================================================
# DYNAMIC SIMULATION & ANALYSIS TOOLS
# =======================================================

class SimRunInput(BaseModel):
    experiment_name: str = Field(..., description="Descriptive name for the experiment")
    topic: str = Field(..., description="Research topic for context-aware simulation")

class SimRunTool(BaseTool):
    name: str = "sim_run"
    description: str = "Generates realistic, topic-relevant experimental data."
    args_schema: Type[BaseModel] = SimRunInput

    def _get_simulation_config(self, topic: str) -> Dict[str, Any]:
        topic_lower = topic.lower()
        if any(k in topic_lower for k in ["machine learning", "ai", "model"]): return {"metric_name": "Model Accuracy", "control_params": {"mean": 0.78, "std": 0.08}, "treatment_params": {"mean": 0.87, "std": 0.06}}
        if any(k in topic_lower for k in ["drug", "molecular", "compound"]): return {"metric_name": "Binding Affinity (IC50)", "control_params": {"mean": 125, "std": 35}, "treatment_params": {"mean": 78, "std": 25}}
        return {"metric_name": "Performance Score", "control_params": {"mean": 65, "std": 12}, "treatment_params": {"mean": 78, "std": 10}}

    def _run(self, experiment_name: str, topic: str) -> Dict[str, Any]:
        np.random.seed(42)
        config = self._get_simulation_config(topic)
        control_data = np.random.normal(config["control_params"]["mean"], config["control_params"]["std"], 50)
        treatment_data = np.random.normal(config["treatment_params"]["mean"], config["treatment_params"]["std"], 50)
        return {"experiment_name": experiment_name, "topic": topic, "metric_name": config["metric_name"], "control_results": control_data.tolist(), "treatment_results": treatment_data.tolist()}

class StatsSuiteInput(BaseModel):
    experiment_name: str = Field(..., description="Name of the experiment to analyze")
    topic: str = Field(..., description="Research topic for context")

class StatsSuiteTool(BaseTool):
    name: str = "stats_suite"
    description: str = "Performs comprehensive statistical analysis on simulated data."
    args_schema: Type[BaseModel] = StatsSuiteInput

    def _run(self, experiment_name: str, topic: str) -> Dict[str, Any]:
        sim_tool = SimRunTool()
        sim_data = sim_tool._run(experiment_name=experiment_name, topic=topic)
        
        if "error" in sim_data:
            return {"error": sim_data["error"]}
            
        control = np.array(sim_data["control_results"])
        treatment = np.array(sim_data["treatment_results"])
        
        t_stat, p_value = ttest_ind(treatment, control, equal_var=False)
        cohens_d = (np.mean(treatment) - np.mean(control)) / np.sqrt((np.std(control, ddof=1)**2 + np.std(treatment, ddof=1)**2) / 2)
        
        return {
            "metric": sim_data["metric_name"],
            "control_mean": float(np.mean(control)),
            "treatment_mean": float(np.mean(treatment)),
            "p_value": float(p_value),
            "cohens_d": float(cohens_d),
            "significance": "statistically significant" if p_value < 0.05 else "not statistically significant",
            "descriptive_stats": {
                "control": {"mean": np.mean(control), "std": np.std(control, ddof=1)},
                "treatment": {"mean": np.mean(treatment), "std": np.std(treatment, ddof=1)}
            },
            "statistical_test": {"p_value": p_value, "significance": "significant" if p_value < 0.05 else "not significant"},
            "effect_size": {"cohens_d": cohens_d, "magnitude": "large" if abs(cohens_d) > 0.8 else "medium" if abs(cohens_d) > 0.5 else "small"}
        }

# =======================================================
# REPORTING & UTILITY TOOLS
# =======================================================
class WriteReportInput(BaseModel):
    """Input schema for the professional report writing tool."""
    title: str = Field(..., description="The main title for the research report.")
    authors: List[str] = Field(..., description="A list of authors, typically the AI agents.")
    abstract: str = Field(..., description="A concise summary of the entire study.")
    introduction: str = Field(..., description="The introduction section from the literature review.")
    methods: str = Field(..., description="A description of the experimental and analytical methods.")
    results: str = Field(..., description="A summary of the key statistical results and findings.")
    discussion: str = Field(..., description="A discussion of the findings, their implications, and limitations.")
    conclusion: str = Field(..., description="A final concluding paragraph summarizing the work's contribution.")
    citations: List[str] = Field(default_factory=list, description="A list of citation links from the literature review.")

class WriteReportTool(BaseTool):
    name: str = "write_professional_report"
    description: str = "Creates a comprehensive, well-formatted scientific report with a structure similar to an academic paper."
    args_schema: Type[BaseModel] = WriteReportInput

    def _format_citations(self, citations: List[str]) -> str:
        if not citations: return "No citations were provided for this analysis."
        return "\n".join([f"[{i}] {link}" for i, link in enumerate(citations, 1)])

    def _run(self, title: str, authors: List[str], abstract: str, introduction: str, methods: str, results: str, discussion: str, conclusion: str, citations: List[str]) -> str:
        try:
            if not all([title, abstract, introduction, methods, results, discussion, conclusion]):
                return "Error: One or more required report sections were empty. Cannot generate report."

            timestamp = datetime.now().strftime("%Y-%m-%d")
            authors_str = ", ".join(authors)

            # --- THIS IS THE COMPLETE, FIXED TEMPLATE ---
            report_content = f"""
# {title}

**Authors:** {authors_str}  
**Date:** {timestamp}  
**Version:** 1.0  

---

## Abstract
{abstract}

---

### 1. Introduction
{introduction}

---

### 2. Methodology
{methods}

#### 2.1. Experimental Design
A simulated experimental approach was employed to test the central hypothesis. The design involved a comparison between a control group and a treatment group to isolate the effect of the intervention. Data was generated dynamically based on the research topic to ensure contextual relevance.

#### 2.2. Data Analysis
Statistical analysis was conducted using a suite of tests to determine the significance and effect size of the observed differences. All analyses were performed using a significance level (alpha) of 0.05.

---

### 3. Results
{results}

---

### 4. Discussion
{discussion}

#### 4.1. Limitations
It is important to note that this study is based on simulated data. While the simulation parameters are designed to be realistic, they do not capture the full complexity of real-world scenarios. These findings should be interpreted as a preliminary, in-silico investigation intended to generate hypotheses for future empirical research.

---

### 5. Conclusion
{conclusion}

---

### 6. References
{self._format_citations(citations)}

---

*This report was generated by an AI-powered research automation system built with LangChain and LangGraph.*
"""
            # --- END OF TEMPLATE ---

            output_dir = Path("reports")
            output_dir.mkdir(exist_ok=True)
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
            filename = f"{timestamp}_{safe_title.replace(' ', '_')}_report.md"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            with open("report.md", 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"Professional report generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            error_msg = f"Failed to generate report due to a file system error: {e}"
            logger.error(error_msg)
            return error_msg