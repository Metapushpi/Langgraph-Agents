from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any
import os
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IntelligentRouter:
    def __init__(self, memory_manager=None):
        try:
            # Load environment variables
            load_dotenv()
            
            # Initialize or use provided memory manager
            self.memory_manager = memory_manager
            
            # Check for Azure OpenAI credentials
            required_vars = [
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_MODEL_DEPLOYMENT",
                "AZURE_OPENAI_MODEL_NAME",
                "AZURE_OPENAI_API_VERSION"
            ]
            
            # Verify all required environment variables
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
            logger.info("Initializing Azure OpenAI connection...")
            
            # Configure Azure OpenAI
            try:
                self.llm = AzureChatOpenAI(
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    azure_deployment=os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT"),
                    model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
                    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                    temperature=0.7
                )
                logger.info("Azure OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
                raise
            
            # Create prompt template for intent detection
            self.intent_prompt = PromptTemplate(
                input_variables=["query"],
                template="""
                Analyze this query and classify it into one of these categories:
                - finance (for stock prices, financial data)
                - weather (for weather information)
                - news (for news updates)
                - sentiment (for sentiment analysis)
                - translation (for language translation)

                Query: {query}

                Return the response in this exact JSON format:
                {{"intent": "category_name", "entities": ["entity1", "entity2"], "function": "function_name"}}
                """
            )
            
            # Create intent detection chain
            self.intent_chain = LLMChain(
                llm=self.llm,
                prompt=self.intent_prompt,
                verbose=True
            )
            
            logger.info("IntelligentRouter initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise

    def detect_intent(self, query: str) -> Dict[str, Any]:
        try:
            logger.info(f"Sending query to Azure OpenAI: {query}")
            response = self.intent_chain.run(query=query)
            logger.info(f"Received response: {response}")
            
            # Clean the response string
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-3]  # Remove ```json and ``` markers
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error in detect_intent: {e}")
            return self._get_default_intent()

    def _get_default_intent(self) -> Dict[str, Any]:
        return {
            "intent": "unknown",
            "entities": [],
            "function": "none"
        }

    def route_query(self, query: str) -> str:
        try:
            # Detect intent
            intent_data = self.detect_intent(query)
            logger.info(f"Detected intent: {intent_data}")
            
            # Route to appropriate function
            response = self._execute_functions(intent_data, query)
            
            # Save to memory if memory manager exists
            if self.memory_manager:
                self.memory_manager.save_interaction(query, response, intent_data)
            
            return response
        except Exception as e:
            logger.error(f"Error in route_query: {e}")
            return "I encountered an error processing your request."

    def _execute_functions(self, intent_data: Dict[str, Any], query: str) -> str:
        try:
            from api_functions import (
                get_financial_data,
                get_weather,
                get_news,
                analyze_sentiment,
                translate_text
            )
            
            function_map = {
                "finance": get_financial_data,
                "weather": get_weather,
                "news": get_news,
                "sentiment": analyze_sentiment,
                "translation": translate_text
            }
            
            intent = intent_data.get("intent", "unknown")
            if intent in function_map:
                result = function_map[intent](query)
                return json.dumps(result, indent=2)
            else:
                return "I couldn't determine how to handle that request."
                
        except Exception as e:
            logger.error(f"Error in _execute_functions: {e}")
            return "An error occurred while processing your request." 