from typing import List, Dict

class Player:
    def __init__(self, name: str = 'Adventurer') -> None:
        self.name = name
        self.health = 30
        self.max_health = 30
        self.strength = 3
        self.inventory: List[str] = []
        self.node = 'start'
        self.warden_debuff = False

    def apply_effects(self, effects: Dict):
        # effects include health, items, strength and warden debuff
        if not effects:
            return
        if 'health' in effects:
            self.health += effects['health']
            if self.health > self.max_health:
                self.health = self.max_health
        if 'items' in effects:
            for it in effects['items']:
                if it not in self.inventory:
                    self.inventory.append(it)
        if 'strength' in effects:
            self.strength += effects['strength']
        if 'warden_debuff' in effects and effects['warden_debuff']:
            self.warden_debuff = True

    def has_items(self, items: List[str]) -> bool:
        return all(it in self.inventory for it in items)

    def to_dict(self):
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'strength': self.strength,
            'inventory': self.inventory,
            'node': self.node,
            'warden_debuff': self.warden_debuff
        }

    @classmethod
    def from_dict(cls, data: Dict):
        p = cls(data.get('name','Adventurer'))
        p.health = data.get('health',30)
        p.max_health = data.get('max_health',30)
        p.strength = data.get('strength',3)
        p.inventory = data.get('inventory',[])
        p.node = data.get('node','start')
        p.warden_debuff = data.get('warden_debuff',False)
        return p