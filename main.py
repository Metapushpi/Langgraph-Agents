from agent import IntelligentRouter
from memory_manager import EnhancedMemory
import json
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    router = None
    memory = None
    
    try:
        # Initialize the memory manager and agent
        memory = EnhancedMemory()
        router = IntelligentRouter(memory_manager=memory)
        
        print("\n=== AI Agent Router initialized successfully! ===")
        print("Type 'exit' to quit the program")
        print("Type 'help' for available commands\n")

        while True:
            try:
                # Get user input
                query = input("\nEnter your query (or 'exit' to quit): ").strip()
                
                if not query:
                    print("Please enter a valid query")
                    continue
                    
                if query.lower() == 'exit':
                    print("\nGoodbye!")
                    break
                    
                if query.lower() == 'help':
                    print_help()
                    continue
                
                if query.lower() == 'history':
                    show_history(memory)
                    continue
                    
                if query.lower() == 'clear':
                    memory.clear_history()
                    print("Conversation history cleared")
                    continue
                    
                if query.lower().startswith('search'):
                    handle_search(memory, query)
                    continue
                    
                if query.lower() == 'context':
                    show_context(memory)
                    continue
                
                # Process query through the agent
                logger.info(f"Processing query: {query}")
                response = router.route_query(query)
                
                # Display response
                print(f"\nResponse: {response}\n")
                
            except KeyboardInterrupt:
                print("\nExiting program...")
                break
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                print(f"\nError processing query: {str(e)}")
                print("Please try again with a different query")
                traceback.print_exc()

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed all requirements (pip install -r requirements.txt)")
        print("2. Set up your Azure OpenAI credentials in .env file:")
        print("   - AZURE_OPENAI_API_KEY")
        print("   - AZURE_OPENAI_ENDPOINT")
        print("   - AZURE_OPENAI_MODEL_DEPLOYMENT")
        print("   - AZURE_OPENAI_MODEL_NAME")
        print("   - AZURE_OPENAI_API_VERSION")
        print("3. Have an active internet connection")
        sys.exit(1)
    finally:
        if router and memory:
            print("\nSaving conversation history...")
            memory._save_to_disk()

def show_history(memory: EnhancedMemory):
    """Display recent conversation history."""
    print("\nRecent conversations:")
    recent = memory.get_recent_interactions(5)
    for interaction in recent:
        print(f"\nTime: {interaction['timestamp']}")
        print(f"Query: {interaction['query']}")
        print(f"Intent: {interaction['intent']}")
        print(f"Response: {interaction['response']}")
    print()

def show_context(memory: EnhancedMemory):
    """Display current conversation context."""
    context = memory.get_current_context()
    if context:
        print("\nCurrent conversation context:")
        print(json.dumps(context, indent=2))
    else:
        print("\nNo active conversation context")
    print()

def handle_search(memory: EnhancedMemory, query: str):
    """Handle search command."""
    search_term = query.replace('search', '').strip()
    if not search_term:
        print("Please specify what to search for")
        return
    
    results = memory.search_by_intent(search_term)
    if not results:
        print(f"No conversations found with intent: {search_term}")
        return
    
    print(f"\nFound {len(results)} conversations:")
    for result in results:
        print(f"\nTime: {result['timestamp']}")
        print(f"Query: {result['query']}")
        print(f"Response: {result['response']}")

def print_help():
    print("\nAvailable commands:")
    print("- 'exit': Quit the program")
    print("- 'help': Show this help message")
    print("- 'history': Show recent conversations")
    print("- 'clear': Clear conversation history")
    print("- 'search <intent>': Search conversations by intent")
    print("- 'context': Show current conversation context")
    print("\nExample queries:")
    print("- What is the stock price of Tesla?")
    print("- What's the weather like in Tokyo?")
    print("- Tell me the latest news about AI")
    print("- Analyze the sentiment of 'The product is amazing'")
    print("- Translate 'Hello' to French\n")

if __name__ == "__main__":
    main() 