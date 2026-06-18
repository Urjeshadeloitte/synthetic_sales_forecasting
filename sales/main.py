"""Main entry point for the sales forecasting pipeline."""
from sales.graph import build_sales_pipeline
from sales.state import SalesState


def main():
    """Execute the complete sales forecasting pipeline."""
    print("Starting Sales Forecasting Pipeline...")
    print("-" * 80)
    
    # Build the pipeline
    pipeline = build_sales_pipeline()
    
    # Initialize state
    initial_state = SalesState()
    
    # Execute the pipeline
    final_state = pipeline.invoke(initial_state)
    
    print("-" * 80)
    print("Pipeline completed successfully!")
    print(f"Output directory: sales/output/")
    
    return final_state


if __name__ == "__main__":
    main()
