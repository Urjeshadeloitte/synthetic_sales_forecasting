"""Main entry point for the weather forecasting pipeline."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from weather.graph import graph
from weather.utils.reporting import print_pipeline_summary


def main():
    """
    Execute the weather forecasting pipeline.
    
    1. Initialize empty pipeline state
    2. Run graph.invoke() to execute all nodes sequentially
    3. Print summary of results to console
    """
    print("Starting weather forecasting pipeline...")
    print("=" * 60)
    
    # Initialize empty state
    initial_state = {}
    
    # Execute pipeline
    final_state = graph.invoke(initial_state)
    
    # Print summary
    print_pipeline_summary(final_state)
    
    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()
