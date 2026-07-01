from typing import List, Optional, Any, Dict
from app.search_engine import search_entities

# Extensible catalog mapping
CATALOG_MAPPING = {
    "medication": ["medicine"],
    "investigationAdvised": ["investigation"],
    "procedureAdvised": ["procedure"]
}

def map_json(ep_json: dict) -> dict:
    """
    Maps free-text clinical entities from an EP JSON payload to structured database records.
    This function is framework-agnostic and returns a plain Python dictionary.
    
    Example input:
    {
      "medication": [{"drugDesc": "Ibuprofen"}],
      "investigationAdvised": [{"investigationAdvised": "CBC"}],
      "procedureAdvised": [{"procedureAdvised": "Appendectomy"}]
    }
    """
    def process_items(items: Optional[List[Any]], category: str, keys: List[str]) -> Optional[List[Dict[str, Any]]]:
        if not items:
            return None
            
        mapped_items = []
        allowed_types = CATALOG_MAPPING.get(category, ["medicine", "investigation", "procedure"])
        
        for item in items:
            input_text = ""
            
            # Extract the string input depending on whether item is a dict or string
            if isinstance(item, dict):
                for key in keys:
                    if key in item and isinstance(item[key], str):
                        input_text = item[key]
                        break
            elif isinstance(item, str):
                input_text = item
                
            if not input_text:
                continue
                
            results = search_entities(input_text, allowed_types)
            if results:
                best = results[0]
                mapped_item = {
                    "input": input_text,
                    "matched_id": best.id,
                    "matched_name": best.name,
                    "score": round(best.score, 2),
                    "match_type": best.type
                }
            else:
                mapped_item = {
                    "input": input_text,
                    "matched_id": None,
                    "matched_name": None,
                    "score": None,
                    "match_type": None
                }
            mapped_items.append(mapped_item)
                
        return mapped_items

    meds = process_items(ep_json.get("medication"), "medication", ["drugDesc"])
    invs = process_items(ep_json.get("investigationAdvised"), "investigationAdvised", ["investigationAdvised"])
    procs = process_items(ep_json.get("procedureAdvised"), "procedureAdvised", ["procedureAdvised", "procedure"])
    
    return {
        "medication": meds,
        "investigationAdvised": invs,
        "procedureAdvised": procs
    }
