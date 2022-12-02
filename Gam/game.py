import math as Math
import pygame, random, pathfinding
from pygame import *
from pathfinding import *
pygame.init()

# CONSTANTS
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 768)


screen = pygame.display.set_mode(SIZE)
highlight_item = pygame.Surface((48, 48), pygame.SRCALPHA)
highlight_item.fill((255, 255, 255, 128))
collisionMap = pygame.image.load('assets/map/test.png').convert_alpha()
bg = pygame.image.load('assets/map/maintest.png').convert_alpha()

pygame.mouse.set_visible(False)

# Player sprite
player_actions = ['idle', 'left', 'right', 'up', 'down']
player_img = {}
for img in player_actions:
    filename = 'assets/player/player_' + img + '.png'
    player_img[img] = pygame.image.load(filename).convert_alpha()

# Weapon sprite
sprite_list = ['0', '1', '2', '3']
axe_img = {}
for img in sprite_list:
    filename = 'assets/weapon/axe_' + img + '.png'
    axe_img[img] = pygame.image.load(filename).convert_alpha()
sword_img = {}
for img in sprite_list:
    filename = 'assets/weapon/sword_' + img + '.png'
    sword_img[img] = pygame.image.load(filename).convert_alpha()
knife_img = {}
for img in sprite_list:
    filename = 'assets/weapon/knife_' + img + '.png'
    knife_img[img] = pygame.image.load(filename).convert_alpha()

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()

    def update(self):
        pass

    def exist(self):
        return True

cursor = Sprite()
cursor.surf = pygame.image.load('assets/player/cursor.png').convert_alpha()
cursor.rect = cursor.surf.get_rect()


class Item (Sprite):
    def __init__(self, type, subclass, x = 0, y = 0):
        super(Item, self).__init__()
        filename = 'assets/' + subclass + '/'  + str(type) + '_0.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.subclass = subclass
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type
        self.onGround = True
        self.inChest = False
        self.inInventory = False
        self.active = False
        self.existing = False
        self.tick = 0
        self.frame = 0

    def setGround(self, on):
        self.onGround = on

    def setChest(self, chest):
        self.inChest = chest

    def setInventory(self, holding):
        self.inInventory = holding

    def setActive(self, active):
        self.active = active

    def holding(self):
        return self.inInventory
    
    def pickUp(self):
        if len(player.inventory) < 15:
            player.pickUpItem(self)
            self.onGround = False
            self.existing = False
            self.inInventory = True
        else:
            print("Inventory full!")
            # have image in text on screen with fading letters
    
    def exist(self):
        return self.existing

    def update(self, mouse_pos, mouse_click):
        
        if (self.onGround == True):
            self.existing = True
            self.tick += 1
            if self.tick > 15:
                self.frame += 1
                if 0 < self.frame <= 20:
                    self.rect.move_ip(0,1)
                elif 21 <= self.frame <=40:
                    self.rect.move_ip(0,-1)
                else:
                    self.frame = 0
                self.tick = 0

            if (self.rect.collidepoint(mouse_pos)) & (player.openInventory == False):
                highlight_type = self.type + "_highlight"
                filename = 'assets/' + self.subclass + '/' + str(highlight_type) + '.png'
                self.surf = pygame.image.load(filename).convert_alpha()

                if mouse_click:
                    dist = Math.sqrt(((player.rect.x + 32) - (self.rect.x + 32))**2 + ((player.rect.y + 32) - (self.rect.y + 32))**2)
                    if (-128 <= dist <= 128):
                        self.pickUp()
                        
            else:
                self.surf = self.def_img
        elif ((self.inInventory) & (player.openInventory) & (player.control == False)):
            self.surf = self.def_img
            if self.rect.collidepoint(mouse_pos):
                self.highlight = highlight_item.copy()
                screen.blit(self.highlight, (self.rect.x, self.rect.y))
                if mouse_click:
                    self.selected = True
            
                
        # if condition for in inventory, hover img, moving in inventorry, drop from inventory

    
class Weapon (Item):
    def __init__(self, type, dmg, range, element, x=0, y=0):
        super(Weapon, self).__init__(type, 'weapon', x, y)
        self.type = type
        self.dmg = dmg
        self.range = range
        self.element = element

    def getDmg(self):
        return self.dmg

    def getElement(self):
        return self.element

    def getRange(self):
        return self.range

class Armor (Item):
    def __init__(self, type, health, durability):
        super(Item, self).__init__(type, 'armor')
        self.health = health
        self.durability = durability

    def setElement(self, element):
        self.element = element

class Money (Item):
    def __init__(self, quantity, x=0, y=0):
        super(Money, self).__init__('coin', 'misc', x, y)
        self.quantity = quantity

class Usable (Item):
    def __init__(self, type):
        super(Usable, self).__init__(type, 'usable')

class Artifact (Item):
    def __init__(self, type):
        super(Artifact, self).__init__(type, 'artifact')
        
class Inventory(Sprite):
    def __init__(self, type):
        super(Inventory, self).__init__()
        if (type == 0):
            self.surf = pygame.image.load('assets/inventory/player_inventory_0.png')
        elif (type == 1):
            self.surf = pygame.image.load('assets/inventory/chest_inventory_0.png')
        self.rect = self.surf.get_rect()
        self.rect.move_ip(390, 110)


class Player (Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_img['idle']
        self.rect = self.surf.get_rect()
        self.control = True
        self.openInventory = False
        self.inventory = []
        # labeled 0-15, len = 16
        self.delay = pygame.time.get_ticks()
        self.health = 10
        self.dmg = 10
        self.element = ''
        self.money = 0
        self.openInterface = False
        # modify these instance variables based on weapon, armor, items, etc

    def update(self, mouse_pos, mouse_click, keys, touching, hitting):
        # Movement
        if (self.control == True):
            if keys[K_UP]:
                self.rect.move_ip(0,-1)
                self.surf = player_img['up']
                for tile in touching:
                    if((3 < player.rect.right - tile.rect.left < 125) & (player.rect.y >= tile.rect.y)):
                        player.rect.top = tile.rect.bottom
            elif keys[K_DOWN]:
                self.rect.move_ip(0,1)
                self.surf = player_img['down']
                for tile in touching:
                    if((3 < player.rect.right - tile.rect.left < 125) & (player.rect.y <= tile.rect.y)):
                        player.rect.bottom = tile.rect.top
            elif keys[K_LEFT]:
                self.rect.move_ip(-1,0)
                self.surf = player_img['left']        
                for tile in touching:
                    if((3 < player.rect.bottom - tile.rect.top < 125) & (player.rect.x >= tile.rect.x)):
                        player.rect.left = tile.rect.right
            elif keys[K_RIGHT]:
                self.rect.move_ip(1,0)
                self.surf = player_img['right']
                for tile in touching:
                    if((3 < player.rect.bottom - tile.rect.top < 125) & (player.rect.x <= tile.rect.x)):
                        player.rect.right = tile.rect.left
            else:
                self.surf = player_img['idle']
            for enemy in hitting:
                if mouse_click:
                    dist = Math.sqrt(((player.rect.x + 32) - (enemy.rect.x + 32))**2 + ((player.rect.y + 32) - (enemy.rect.y + 32))**2)
                    if ((-1 * self.range) <= dist <= self.range):
                        enemy.getHit(self.dmg, self.element)
        
        if keys[K_e]:
            if((self.delay-pygame.time.get_ticks()) < -200):
                if ((self.openInventory == False) & (self.openInterface == False)):
                    self.delay = pygame.time.get_ticks()
                    self.accessInventory()
                elif (self.openInventory) or (self.openInterface == True):
                    self.delay = pygame.time.get_ticks()
                    self.closeInterface()
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def accessInventory(self):
        self.control = False
        self.openInventory = True
        for i in range(4): 
            try:
                player.inventory[i].rect.x, player.inventory[i].rect.y = ((402 + 68 * i), 122)
                inventoryGroup.add(player.inventory[i])
                continue
            except IndexError:
                pass
        for i in range(4): 
            try:
                player.inventory[i + 4].rect.x, player.inventory[i+4].rect.y=((402 + 68 * i), 190)
                inventoryGroup.add(player.inventory[i + 4])
                continue
            except IndexError:
                pass
        for i in range(4): 
            try:
                player.inventory[i + 8].rect.x,player.inventory[i + 8].rect.y =((402 + 68 * i), 258)
                inventoryGroup.add(player.inventory[i + 8])
                continue
            except IndexError:
                pass
        for i in range(4): 
            try:
                player.inventory[i + 12].rect.x, player.inventory[i+12].rect.y = ((402 + 68 * i), 326)
                inventoryGroup.add(player.inventory[i + 12])
                continue
            except IndexError:
                pass
        
        self.playerInv = Inventory(0)
        inventories.add(self.playerInv)

    def closeInterface(self):
        self.control = True
        self.openInventory = False
        self.openInterface = False
        for i in inventories:
            i.kill()

    def pickUpItem(self, item):
        if len(self.inventory) < 16:
            if ((isinstance(item, Money)) == False):
                self.inventory.append(item)
            else:
                player.money += item.quantity
                item.kill()

class Enemy (Sprite):
    def __init__(self, posx, posy, type):
        super(Enemy, self).__init__()
        filename = 'assets/entity/' + type + '_idle.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.rect = self.surf.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.initUpdate = 0
        self.cur_node = 0


    def getHit(self, dmg, element):
        pass
    def update(self):
        # if player has updated position (so that new path needs to be found) or init
        # path needs to be found, find path with a*
        g = 100000
        path = []
        if playerPrevPos != (player.rect.x, player.rect.y) or self.initUpdate == 0:
            dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
            dist = Math.hypot(dx, dy)
            if (dist < 100):
                miniPath = pathfinding.aStar.findPath(self, player, collisionMap)
            # take the distance from the player to the enemy

                if miniPath:
                    g = miniPath[-1]
                path = []
            # if distance is close enough, create full size path of points to follow
                if g < 10: 
                    for node in miniPath:
                        path.append((node[0] * 32 - 16), (node[1] * 32 - 16))
                # set initUpdate to 1 to show that has been initialized
                    self.initUpdate = 1
        # if path exists, follow path
        if path:
            dx, dy = self.rect.x - path[self.cur_node][0], self.rect.y - path[self.cur_node][1]
            if dx == 0 and dy == 0:
                self.cur_node += 1
            dist = Math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


class Chest (Sprite):
    def __init__(self, posx, posy, type):
        super(Chest, self).__init__()
        filename = 'assets/tiles/chest_' + str(type) + '.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = posx, posy
        self.type = type
        self.open = False
        self.content = []
        self.fill(type)
        # run Mathod to fill container

    def fill(self, type):
        # Money
        if (type == 0):
            coins = random.randint(1, 10)
            self.content.append(Money(coins))
        elif (type == 1):
            coins = random.randint(15,30)
            self.content.append(Money(coins))
        elif(type == 2):
            coins = random.randint (30, 75)
            self.content.append(Money(coins))
        
        # Slot 2 
        if (type == 0):
            chance = random.randint(1, 20)
            if (chance < 11):
                if (chance < 6):
                    pass
                    #potion

        elif (type == 1):
            pass
        elif (type == 2):
            pass
        
        # Slot 3 
        if (type == 0):
            pass
        elif (type == 1):
            pass
        elif (type == 2):
            pass

        # Slot 4 
        if (type == 0):
            pass
        elif (type == 1):
            pass
        elif (type == 2):
            pass
    def getType(self):
        return self.type
    
    def update(self, mouse_pos, mouse_click):
        if self.open:
            open_type = self.type + 3
            filename = 'assets/tiles/chest_' + str(open_type) +'.png'
            self.surf = pygame.image.load(filename).convert_alpha()
        if self.open == False:
            if self.rect.collidepoint(mouse_pos) & (player.openInventory == False):
                highlight_type = self.type + 6
                filename = 'assets/tiles/chest_' + str(highlight_type) + '.png'
                self.surf = pygame.image.load(filename).convert_alpha()
                if mouse_click:
                    dist = Math.sqrt(((player.rect.x + 32) - (self.rect.x + 32))**2 + ((player.rect.y + 32) - (self.rect.y + 32))**2)
                    # distance formula
                    if (-128 <= dist <= 128):
                        self.open = True
                        self.inv = Inventory(1)
                        inventories.add(self.inv)
                        player.openInterface = True
                        
            else:
                self.surf = self.def_img

# if mouse_pos in rect then randomize loot, open window to show interface of loot, change chest sprite to open

frame = 0
speed = 0
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
tiles = pygame.sprite.Group()
players = pygame.sprite.Group()
cursor_ = pygame.sprite.Group()
items = pygame.sprite.Group()
inventoryGroup = pygame.sprite.Group()
inventories = pygame.sprite.Group()

coin = Money(10, 200, 100)
player = Player()
playerPrevPos = (player.rect.x, player.rect.y)
chest = Chest(600, 300, 0)
item = Weapon('sword', 1, 1, '')
axe = Weapon('axe', 1, 1, '', 400, 100)
zombie = Enemy(1000, 500, 'zombie')


all_sprites.add(player)
all_sprites.add(chest)
all_sprites.add(item)
all_sprites.add(axe)
all_sprites.add(coin)
all_sprites.add(zombie)
enemies.add(zombie)
items.add(item)
items.add(coin)
items.add(axe)
tiles.add(chest)
players.add(player)
cursor_.add(cursor)

running = True
f=0
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONDOWN:
            mouse_click = True
        else:
            mouse_click = False
        if event.type == pygame.QUIT:
            running = False
    mouse_pos = pygame.mouse.get_pos()
    pressed_keys = pygame.key.get_pressed()
    touching_tiles = pygame.sprite.groupcollide(tiles, players, False, False)
    hitting_enemies = pygame.sprite.groupcollide(enemies, cursor_, False, False)
    frame += 1
    if frame > speed:
        player.update(mouse_pos, mouse_click, pressed_keys, touching_tiles, hitting_enemies)
        frame = 0

    screen.fill((100, 100, 100))
    screen.blit(bg, (0,0))
    cursor.rect.center = mouse_pos
    

    print(player.money)
    for entity in all_sprites:
        if entity.exist() == True:
            screen.blit(entity.surf, entity.rect)
    for inv in inventories:
        screen.blit(inv.surf, inv.rect)
    if player.openInventory == True:        
        for item in inventoryGroup:
            screen.blit(item.surf, item.rect)
    f += 1
    if f> 1:
        enemies.update()
        f =0
    
    screen.blit(cursor.surf, cursor.rect)
    items.update(mouse_pos, mouse_click)
    tiles.update(mouse_pos, mouse_click)
 
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()