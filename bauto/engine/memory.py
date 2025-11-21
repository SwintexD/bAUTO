"""
Memory System for bAUTO (Optional Advanced Feature)
===================================================

Stores and retrieves information from previous automation sessions.
Uses vector embeddings for semantic search.
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Check if optional dependencies are available
try:
    from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage, Settings
    from llama_index.llms.gemini import Gemini
    from llama_index.embeddings.gemini import GeminiEmbedding
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    logger.warning("Memory system dependencies not installed. Memory features disabled.")


class AutomationMemory:
    """
    Stores and retrieves automation history and learned information.
    
    Uses LlamaIndex for vector-based semantic search.
    """
    
    def __init__(self, memory_dir: str = "automation_memory"):
        if not MEMORY_AVAILABLE:
            raise ImportError(
                "Memory system requires llama-index. Install with: "
                "pip install llama-index llama-index-llms-gemini llama-index-embeddings-gemini"
            )
        
        self.memory_dir = memory_dir
        self.index_dir = os.path.join(memory_dir, "index")
        self.sessions_dir = os.path.join(memory_dir, "sessions")
        
        # Create directories
        os.makedirs(self.index_dir, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        # Configure LlamaIndex for Gemini
        if os.environ.get("GOOGLE_API_KEY"):
            Settings.llm = Gemini(model="gemini-pro")
            Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")
        
        # Load or create index
        self.index = self._load_or_create_index()
        
        # Current session
        self.current_session = {
            "id": self._generate_session_id(),
            "start_time": datetime.now().isoformat(),
            "actions": [],
            "results": []
        }
        
        logger.info(f"Memory system initialized at: {memory_dir}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _load_or_create_index(self) -> VectorStoreIndex:
        """Load existing index or create new one."""
        try:
            if os.path.exists(os.path.join(self.index_dir, "index_store.json")):
                storage_context = StorageContext.from_defaults(persist_dir=self.index_dir)
                index = load_index_from_storage(storage_context)
                logger.info("Loaded existing memory index")
            else:
                index = VectorStoreIndex([])
                index.storage_context.persist(persist_dir=self.index_dir)
                logger.info("Created new memory index")
            
            return index
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            # Create new index as fallback
            index = VectorStoreIndex([])
            return index
    
    def add_action(self, instruction: str, code: str, success: bool, 
                   url: Optional[str] = None, error: Optional[str] = None):
        """
        Record an action in memory.
        
        Args:
            instruction: Natural language instruction
            code: Generated code
            success: Whether action succeeded
            url: Current URL
            error: Error message if failed
        """
        
        action_record = {
            "timestamp": datetime.now().isoformat(),
            "instruction": instruction,
            "code": code,
            "success": success,
            "url": url,
            "error": error
        }
        
        self.current_session["actions"].append(action_record)
        
        # Add to vector index for semantic search
        if success:
            doc_text = f"Instruction: {instruction}\nCode: {code}\nURL: {url or 'N/A'}"
            document = Document(text=doc_text, metadata=action_record)
            self.index.insert(document)
            logger.debug(f"Added action to memory: {instruction[:50]}...")
    
    def query(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search memory for relevant past actions.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant actions
        """
        
        try:
            query_engine = self.index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(query)
            
            results = []
            for node in response.source_nodes:
                results.append({
                    "text": node.text,
                    "metadata": node.metadata,
                    "score": node.score
                })
            
            logger.debug(f"Memory query '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Memory query failed: {e}")
            return []
    
    def save_session(self):
        """Save current session to disk."""
        try:
            self.current_session["end_time"] = datetime.now().isoformat()
            
            session_file = os.path.join(
                self.sessions_dir, 
                f"session_{self.current_session['id']}.json"
            )
            
            with open(session_file, 'w') as f:
                json.dump(self.current_session, f, indent=2)
            
            # Persist index
            self.index.storage_context.persist(persist_dir=self.index_dir)
            
            logger.info(f"Session saved: {session_file}")
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a previous session."""
        try:
            session_file = os.path.join(self.sessions_dir, f"session_{session_id}.json")
            
            with open(session_file, 'r') as f:
                session = json.load(f)
            
            logger.info(f"Loaded session: {session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return None
    
    def get_all_sessions(self) -> List[str]:
        """Get list of all session IDs."""
        try:
            sessions = []
            for filename in os.listdir(self.sessions_dir):
                if filename.startswith("session_") and filename.endswith(".json"):
                    session_id = filename.replace("session_", "").replace(".json", "")
                    sessions.append(session_id)
            
            return sorted(sessions, reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        sessions = self.get_all_sessions()
        total_actions = len(self.current_session["actions"])
        
        # Count successes
        successes = sum(1 for a in self.current_session["actions"] if a["success"])
        
        return {
            "total_sessions": len(sessions),
            "current_session_actions": total_actions,
            "current_session_success_rate": successes / total_actions if total_actions > 0 else 0,
            "memory_dir": self.memory_dir
        }


def create_memory(config) -> Optional[AutomationMemory]:
    """
    Create memory system if enabled in config.
    
    Returns:
        AutomationMemory instance or None
    """
    
    if not config.automation.enable_memory:
        return None
    
    if not MEMORY_AVAILABLE:
        logger.warning("Memory system requested but dependencies not installed")
        return None
    
    try:
        memory = AutomationMemory(config.automation.memory_dir)
        return memory
    except Exception as e:
        logger.error(f"Failed to create memory system: {e}")
        return None

