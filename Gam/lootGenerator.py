import random
import json
items = open('itemTables.json',)
item_table = json.load(items)
loot = open('loot_tables.json',)
loot_table = json.load(loot)
class lootGenerator ():
    
    def chestLoot(stage, type):
        lootList = []
        match stage:
            case 1:
                coins = 10 + (random.randint(10 * type, 10 + 10 * type))
                lootList.append(Money(coins))
                # chance for weapon
                weaponChance = random.randint(1,10)
                if weaponChance <= 3 + type:
                    lootList.append(random.choice(sword, axe, spear, knife)) 
                # armor chance
                armorChance = random.randint(1,10)
                if armorChance <= 3:
                    lootList.append(random.choice(leather_helm, leather_breast, leather_greaves, leather_boots))
                elif armorChance >= 10 - type * 2:
                    lootList.append(random.choice(mail_helm, mail_breast, mail_greaves, mail_boots))
                # pot chance
                potChance = random.randInt(1,3)
                if potChance <= 1 + type:
                    lootList.append(random.choice(hp_lvl1, speed_lvl1, shield_lvl1))


    def entityLoot(stage, type):
        drop_list=[]
        for mob in loot_table["entity"]:
            if mob["type"] == type:
                # randomizing drops
                numberDrops = random.randint(1,2)
                weights = [i["weight"] for i in loot_table["entity"][0]["drops"]]
                drops = random.choices(mob["drops"], weights, k=numberDrops)
                for drop in drops:
                    dropName = drop["name"]
                    if dropName == "null":
                        pass
                    elif dropName == "entity_coins":
                        numberCoins = random.randint(item_table["entity_coins"][stage][0], item_table["entity_coins"][stage][1])
                        drop_list.append(Money(numberCoins))
                    else:
                        # change to randomly select item from dictionary using random
                        itemKey = random.choice(item_table[dropName].keys())
                        # can access item data, figure out how to append item with data to drop list and
                        # drop items on ground (dispersal as well), reconfigure entire item system

        return drop_list
                        
