"""v3.6: agentes por proyecto generados desde projects.json + índice de conocimiento local."""
from .manifest import load_manifest, manifest_path, knowledge_dir
from .knowledge import KnowledgeIndex, get_index

__all__ = ["load_manifest", "manifest_path", "knowledge_dir", "KnowledgeIndex", "get_index"]
