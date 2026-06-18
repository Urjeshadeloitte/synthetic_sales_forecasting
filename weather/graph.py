"""LangGraph workflow construction and compilation."""

from langgraph.graph import StateGraph, START, END

from weather.state import PipelineState
from weather.nodes.generate import generate_weather_data
from weather.nodes.clean import clean_weather
from weather.nodes.features import engineer_features
from weather.nodes.train import train_model
from weather.nodes.forecast import forecast_next_30_days
from weather.nodes.metrics import calculate_metrics
from weather.nodes.output import save_outputs


def build_weather_pipeline():
    """
    Build and compile the LangGraph pipeline.
    
    Graph structure (linear execution):
    START → generate → clean → features → train → forecast → metrics → output → END
    
    Returns:
        Compiled StateGraph (Runnable)
    """
    workflow = StateGraph(PipelineState)
    
    # Add nodes
    workflow.add_node("generate", generate_weather_data)
    workflow.add_node("clean", clean_weather)
    workflow.add_node("features", engineer_features)
    workflow.add_node("train", train_model)
    workflow.add_node("forecast", forecast_next_30_days)
    workflow.add_node("metrics", calculate_metrics)
    workflow.add_node("output", save_outputs)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    # Add edges (linear pipeline)
    workflow.add_edge("generate", "clean")
    workflow.add_edge("clean", "features")
    workflow.add_edge("features", "train")
    workflow.add_edge("train", "forecast")
    workflow.add_edge("forecast", "metrics")
    workflow.add_edge("metrics", "output")
    workflow.add_edge("output", END)
    
    # Compile to executable
    return workflow.compile()


# Build and export the compiled graph at module level
graph = build_weather_pipeline()


# Create global graph instance
graph = build_weather_pipeline()
