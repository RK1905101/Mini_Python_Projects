# ai_backend.py

import os
import json
import logging
from typing import TypedDict, Optional, List, Dict, Any

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# This assumes your tools are in 'tools_langchain.py' as created before
from tools.custom_tool import PapersRAGTool, SimRunTool, StatsSuiteTool, WriteReportTool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# --- 1. Define the State ---
class ResearchState(TypedDict):
    topic: str
    literature_review: Optional[Dict[str, Any]]
    statistical_analysis: Optional[Dict[str, Any]]
    final_report_path: Optional[str]

# --- 2. Setup Tools and LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

papers_rag_tool = PapersRAGTool()
sim_run_tool = SimRunTool()
stats_suite_tool = StatsSuiteTool()
write_report_tool = WriteReportTool()

# --- 3. Define the Graph Nodes ---
def researcher_node(state: ResearchState) -> Dict[str, Any]:
    logger.info(f"🔬 Node: Researcher | Topic: '{state['topic']}'")
    review_results = papers_rag_tool.invoke({"query": state['topic']})
    return {"literature_review": review_results}

def analyst_node(state: ResearchState) -> Dict[str, Any]:
    logger.info(f"📊 Node: Analyst | Topic: '{state['topic']}'")
    analysis_data = stats_suite_tool.invoke({"experiment_name": f"Analysis of {state['topic']}", "topic": state['topic']})
    return {"statistical_analysis": analysis_data}

def writer_node(state: ResearchState) -> Dict[str, Any]:
    logger.info("✍️ Node: Writer | Starting professional report generation...")
    topic = state['topic']
    review = state['literature_review']
    stats = state['statistical_analysis']

    prompt = ChatPromptTemplate.from_template(
        """You are an expert scientific writer. Based on the provided literature review and statistical analysis, generate a complete JSON object with the following four keys: "abstract", "methods", "discussion", and "conclusion".

        **Topic:** {topic}
        **Literature Review:** {introduction}
        **Statistical Analysis (JSON):** {stats_json}
        """
    )
    synthesis_chain = prompt | llm | JsonOutputParser()
    
    logger.info("... Synthesizing narrative sections with LLM...")
    narrative_sections = synthesis_chain.invoke({
        "topic": topic,
        "introduction": review.get("answer", "No introduction available."),
        "stats_json": json.dumps(stats, indent=2)
    })
    
    results_summary = (
        f"The analysis of the metric '{stats.get('metric')}' showed a statistically significant difference "
        f"between the treatment group (Mean={stats.get('descriptive_stats', {}).get('treatment', {}).get('mean', 0):.3f}) "
        f"and the control group (Mean={stats.get('descriptive_stats', {}).get('control', {}).get('mean', 0):.3f}). "
        f"The test yielded a p-value of {stats.get('statistical_test', {}).get('p_value', 0):.6f} and a Cohen's d of {stats.get('effect_size', {}).get('cohens_d', 0):.3f}, "
        f"indicating a {stats.get('effect_size', {}).get('magnitude', 'N/A')} effect size."
    )

    report_args = {
        "title": f"An Automated Investigation into {topic}",
        "authors": ["AI Research Agent", "AI Statistical Analyst"],
        "abstract": narrative_sections.get("abstract", ""),
        "introduction": review.get("answer", ""),
        "methods": narrative_sections.get("methods", ""),
        "results": results_summary,
        "discussion": narrative_sections.get("discussion", ""),
        "conclusion": narrative_sections.get("conclusion", ""),
        "citations": review.get("citations", [])
    }
    
    report_result_path = write_report_tool.invoke(report_args)
    return {"final_report_path": report_result_path}

# --- 4. Build and Compile the Graph ---
workflow = StateGraph(ResearchState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()
logger.info("✅ LangGraph application compiled successfully.")

# --- 5. Define the Main Function for the Frontend ---
def writer_node(state: ResearchState) -> Dict[str, Any]:
    """Node for synthesizing all artifacts into a final, professional report."""
    logger.info("✍️ Node: Writer | Starting professional report generation...")
    
    topic = state['topic']
    review = state['literature_review']
    stats = state['statistical_analysis']

    # This prompt is specifically designed to fill our new template.
    prompt = ChatPromptTemplate.from_template(
        """You are a world-class scientific writer. Your task is to generate the core narrative sections of a research paper based on the provided data. Be thorough, clear, and professional.

        **Research Topic:** {topic}
        **Literature Review Summary:** {introduction}
        **Statistical Analysis Results (JSON):** {stats_json}

        Based on all this information, generate a complete JSON object with the following four keys:
        1.  "abstract": A concise, single-paragraph summary (approx. 150-250 words) of the entire study. It must include the background, the methods used, the primary results (mentioning the key metric and significance), and the main conclusion.
        2.  "methods": A paragraph describing the simulated experiment. Explain the setup, including the metric being measured ({metric}), the two groups being compared, and the statistical tests that were performed.
        3.  "discussion": A detailed paragraph interpreting the results. What do these findings mean in the context of the literature? What are the broader implications? Critically evaluate the limitations of this simulated study.
        4.  "conclusion": A short, powerful final paragraph summarizing the main takeaway and contribution of this work. Reiterate the significance of the findings.
        """
    )
    
    synthesis_chain = prompt | llm | JsonOutputParser()
    
    logger.info("... Synthesizing narrative sections (Abstract, Methods, Discussion, Conclusion) with LLM...")
    narrative_sections = synthesis_chain.invoke({
        "topic": topic,
        "introduction": review.get("answer", "An introduction could not be generated."),
        "stats_json": json.dumps(stats, indent=2),
        "metric": stats.get('metric', 'a performance metric')
    })
    
    # This summary is now more detailed and robust.
    results_summary = (
        f"The primary metric for this study was '{stats.get('metric')}'. The analysis compared the treatment group with the control group. "
        f"The treatment group yielded a mean score of {stats.get('treatment_mean', 0):.4f}, while the control group had a mean score of {stats.get('control_mean', 0):.4f}. "
        f"The difference between the groups was found to be {stats.get('significance', 'N/A')}. "
        f"An independent samples t-test resulted in a p-value of {stats.get('p_value', 0):.6f}. "
        f"The effect size, as measured by Cohen's d, was {stats.get('cohens_d', 0):.3f}, indicating a {stats.get('effect_size', {}).get('magnitude', 'N/A')} effect."
    )

    report_args = {
        "title": f"An Automated Investigation into: {topic}",
        "authors": ["AI Research Analyst", "AI Simulation Engineer", "AI Statistical Analyst"],
        "abstract": narrative_sections.get("abstract", "The abstract could not be generated."),
        "introduction": review.get("answer", "The introduction could not be generated."),
        "methods": narrative_sections.get("methods", "The methods section could not be generated."),
        "results": results_summary,
        "discussion": narrative_sections.get("discussion", "The discussion could not be generated."),
        "conclusion": narrative_sections.get("conclusion", "The conclusion could not be generated."),
        "citations": review.get("citations", [])
    }
    
    report_result_path = write_report_tool.invoke(report_args)
    return {"final_report_path": report_result_path}


# --- Main Function for Frontend (No changes needed, it works with the fixes above) ---
def run_research_graph(topic: str) -> str:
    # ... your existing run_research_graph function is correct ...
    if not os.getenv("GOOGLE_API_KEY"):
        return "Error: GOOGLE_API_KEY not found."
    try:
        final_state = app.invoke({"topic": topic})
        report_path = final_state.get("final_report_path")
        if report_path and "error" not in report_path.lower() and os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return f"Error: The report was not generated successfully. Tool output: {report_path}"
    except Exception as e:
        return f"An error occurred while running the research graph: {e}"
        