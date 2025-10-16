import json
from typing import Dict, Any

class StoryManager:
    def __init__(self, story_file: str = 'story.json') -> None:
        with open(story_file, 'r', encoding='utf-8') as f:
            self.story = json.load(f)

    def get_node(self, node_id: str) -> Dict[str, Any]:
        return self.story.get(node_id)

    def list_choices(self, node: Dict) -> Dict[str, Dict]:
        # return mapping from key to choice
        return {c['key']: c for c in node.get('choices', [])}