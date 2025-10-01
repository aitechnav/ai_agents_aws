"""Main entry point for the agents orchestrator application."""

import logging
from orchestrator import AgentsOrchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_example_queries():
    """Run example queries to demonstrate the orchestrator functionality."""
    
    # Initialize the orchestrator
    orchestrator = AgentsOrchestrator()
    
    # Display agent info
    info = orchestrator.get_agent_info()
    logger.info(f"Agent Info: {info}")
    
    # Example queries
    queries = [
        "Can you research the following link: https://strandsagents.com/latest/documentation/docs/ and summarize the content in a few sentences.",
        "Can you list all the S3 buckets in my account?",
        "Do I have any SageMaker endpoints running?",
    ]
    
    # Process each query
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*50}")
        print(f"Query {i}: {query}")
        print('='*50)
        
        try:
            result = orchestrator.process_query(query, include_metadata=True)
            print(f"Response: {result['response']}")
            
            if 'metadata' in result:
                print(f"\nMetadata: {result['metadata']}")
                
        except Exception as e:
            logger.error(f"Error processing query {i}: {str(e)}")


def main():
    """Main function to run example queries."""
    
    print("🤖 Agents Orchestrator - Running Example Queries")
    print("="*50)
    
    try:
        run_example_queries()
            
    except KeyboardInterrupt:
        print("\n Goodbye!")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main() 