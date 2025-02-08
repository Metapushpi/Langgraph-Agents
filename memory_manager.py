import json
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from langchain.memory import ConversationBufferMemory

logger = logging.getLogger(__name__)

class EnhancedMemory:
    def __init__(self, file_path: str = "conversation_history.json"):
        """Initialize the enhanced memory manager with both short-term and persistent memory."""
        self.file_path = file_path
        self.history: List[Dict[str, Any]] = self._load_from_disk()
        self.buffer_memory = ConversationBufferMemory(return_messages=True)
        
    def _load_from_disk(self) -> List[Dict[str, Any]]:
        """Load conversation history from disk."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading conversation history: {e}")
            return []

    def _save_to_disk(self) -> None:
        """Save conversation history to disk."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.history, f, indent=2)
            logger.info("Conversation history saved successfully")
        except Exception as e:
            logger.error(f"Error saving conversation history: {e}")

    def save_interaction(self, query: str, response: str, intent: dict):
        """Save an interaction to the conversation history."""
        try:
            # Load existing conversations
            with open(self.file_path, 'r') as f:
                history = json.load(f)
            
            # Create new interaction
            new_interaction = {
                "query": query,
                "response": response,
                "intent": intent,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            }
            
            # Append to the conversations list
            history["conversations"].append(new_interaction)
            
            # Write back to file
            with open(self.file_path, 'w') as f:
                json.dump(history, f, indent=2)
            
        except Exception as e:
            logging.error(f"Error saving interaction: {str(e)}")

    def get_current_context(self) -> Dict[str, Any]:
        """Get the current conversation context from buffer memory."""
        try:
            return self.buffer_memory.load_memory_variables({})
        except Exception as e:
            logger.error(f"Error loading context: {e}")
            return {}

    def get_recent_interactions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent interactions."""
        return self.history[-limit:]

    def search_by_intent(self, intent: str) -> List[Dict[str, Any]]:
        """Search interactions by intent."""
        return [
            interaction for interaction in self.history 
            if interaction.get("intent") == intent
        ]

    def search_by_entity(self, entity: str) -> List[Dict[str, Any]]:
        """Search interactions by entity."""
        return [
            interaction for interaction in self.history 
            if entity in interaction.get("entities", [])
        ]

    def get_context_for_intent(self, intent: str, limit: int = 3) -> str:
        """Get relevant context for a specific intent."""
        relevant_history = self.search_by_intent(intent)[-limit:]
        context = []
        for interaction in relevant_history:
            context.append(f"Query: {interaction['query']}")
            context.append(f"Response: {interaction['response']}\n")
        return "\n".join(context)

    def clear_history(self) -> None:
        """Clear all conversation history."""
        try:
            self.history = []
            self.buffer_memory.clear()
            self._save_to_disk()
            logger.info("Conversation history cleared")
        except Exception as e:
            logger.error(f"Error clearing history: {e}") 