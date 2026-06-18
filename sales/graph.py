"""LangGraph pipeline for sales forecasting."""
from langgraph.graph import StateGraph
from sales.state import SalesState
from sales.nodes.generate import generate_sales_data
from sales.nodes.clean import clean_sales_data
from sales.nodes.features import engineer_features
from sales.nodes.train import train_model
from sales.nodes.forecast import forecast_sales
from sales.nodes.output import write_outputs


def build_sales_pipeline():
    """
    Build the LangGraph state machine for the sales forecasting pipeline.
    
    Flow:
    1. generate_sales_data: Create 180 days of synthetic data
    2. clean_sales_data: Clean and validate
    3. engineer_features: Add time-based and seasonal features
    4. train_model: Train LinearRegression model
    5. forecast_sales: Forecast next 30 days
    6. write_outputs: Save CSV, PNG, and print metrics
    
    Returns:
    --------
    Compiled StateGraph
    """
    graph = StateGraph(SalesState)
    
    # Add nodes
    graph.add_node("generate", generate_sales_data)
    graph.add_node("clean", clean_sales_data)
    graph.add_node("features", engineer_features)
    graph.add_node("train", train_model)
    graph.add_node("forecast", forecast_sales)
    graph.add_node("output", write_outputs)
    
    # Add edges (sequential flow)
    graph.add_edge("generate", "clean")
    graph.add_edge("clean", "features")
    graph.add_edge("features", "train")
    graph.add_edge("train", "forecast")
    graph.add_edge("forecast", "output")
    
    # Set entry point
    graph.set_entry_point("generate")
    
    # Compile
    compiled_graph = graph.compile()
    
    return compiled_graph
