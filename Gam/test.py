import json
file = open('loot_tables.json',)
loot_table = json.load(file)
loot = [i["weight"] for i in loot_table["entity"][0]["drops"]]
print(loot)