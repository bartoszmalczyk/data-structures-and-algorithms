class Ork: 
    def __init__(self, hp, weapon, armor):
        self.hp = hp
        self.weapon = weapon
        self.armor = armor
    def attack(self):
        return f"Orks attacks with {self.weapon}"

class Goblin:
    def __init__(self, hp, weapon):
        self.hp = hp
        self.weapon = weapon 
    def attack(self):
        return f"Goblin attacks with {self.weapon}"

# Bad solution!
# Client must know how to create an enemy
enemy_1 = Ork(hp=100, weapon="Topór")
enemy_2 = Goblin(hp=30, weapon="Sztylet")
# if creators add armor to Orks, we will need to fix  the code 
# each time where we create an Ork.


# Good solution!
class EnemyFactory:
    def __init__(self):
        self._registry = {
            "ork": lambda: Ork(hp=100, weapon="Topór", armor=50),
            "goblin": lambda: Goblin(hp=30, weapon="Sztylet")
        }
    def create_enemy(self, enemy_type):
        creator = self._registry.get(enemy_type)

        if creator is None:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        return creator()
    
factory = EnemyFactory()
enemy1 = factory.create_enemy("ork")
enemy2 = factory.create_enemy("goblin")
# Now client doesn't now how to create an ork, it simply gets one :) 


# PROS:
# + Centralization of creation: if anything changes in ork's 'recipe', 
# we change it only in facotry
# + We hide the complexity under the hood 

# CONS:
# - Problem with naive implementation: few people would create factory purely with
# if statements which again break the SOLID rule
# - Code is more abstract 