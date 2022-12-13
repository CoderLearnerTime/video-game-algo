import random
class R():
    def __init__(self):
        pass
    @classmethod
    def calcChance(percent):
        index = random.randint(1,1000)
        if (index <= (percent * 10)):
            return True
        return False

class ChestLoot():
    def __init__(self, chest):
        self.type = chest.type
        self.content = []
        index = self.type + 1
        # Money
        if self.type == 0:
            self.content.append(Money(random.randint(1,10)))
        else:
            self.content.append(Money(random.randint(index * 10, 10 + (index * 10))))
            # Second Item
        if R.calcChance(70):
            # 70% for potion in gray chest
            pot = random.randint(1,4)
                if pot == 1:
                    self.content.append(Usable('health', 1))
                if pot == 2:
                    self.content.append(Usable('speed', 1))
                if pot == 3:
                    self.content.append(Usable('damage', 1))
                if pot == 4:
                    self.content.append(Usable('shield', 1))
            if R.calcChance(33.4):
                pass
            else:
