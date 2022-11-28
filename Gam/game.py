import math as meth
import pygame, random, os
from pygame import *
pygame.init()

# CONSTANTS
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)


screen = pygame.display.set_mode(SIZE)
highlight_item = pygame.Surface((64, 64), pygame.SRCALPHA)
highlight_item.fill((255, 255, 255, 128))


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
cursor.surf = pygame.image.load('assets/player/cursor.png')
cursor.rect = cursor.surf.get_rect()


class Item (Sprite):
    def __init__(self, type, subclass):
        super(Item, self).__init__()
        filename = 'assets/' + subclass + '/'  + str(type) + '_0.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.subclass = subclass
        self.rect = self.surf.get_rect()
        self.type = type
        self.onGround = True
        self.inChest = False
        self.inInventory = False
        self.active = False
        self.existing = False

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
        player.pickUpItem(self)
        self.onGround = False
        self.existing = False
    
    def exist(self):
        return self.existing

    def update(self, mouse_pos, mouse_click):
        if (self.onGround):
            self.existing = True
            if self.rect.collidepoint(mouse_pos):
                print('wtf')
                highlight_type = self.type + "_highlight"
                filename = 'assets/' + self.subclass + '/' + str(highlight_type) + '.png'
                self.surf = pygame.image.load(filename).convert_alpha()

                if mouse_click:
                    print('bruh')
                    dist = meth.sqrt(((player.rect.x + 32) - (self.rect.x + 32))**2 + ((player.rect.y + 32) - (self.rect.y + 32))**2)
                    # distance formula
                    if (-128 <= dist <= 128):
                        self.pickUp()
                        
            else:
                # set up img
                self.surf = self.def_img
        # if condition for in inventory, hover img, moving in inventorry, drop from inventory

    
class Weapon (Item):
    def __init__(self, type, dmg, range, element):
        super(Weapon, self).__init__(type, 'weapon')
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


class Usable (Item):
    def __init__(self, type):
        super(Item, self).__init__(type, 'usable')

class Artifact (Item):
    def __init__(self, type):
        super(Item, self).__init__(type, 'artifact')
        
class Inventory(Sprite):
    def __init__(self):
        super(Inventory, self).__init__()
        self.surf = pygame.image.load('assets/inventory/player_inventory_0.png')
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
        # modify these instance variables based on weapon, armor, items, etc

    def update(self, mouse_pos, mouse_click, keys, touching, hitting):
        # Movement
        if (self.control):
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
                    dist = meth.sqrt(((player.rect.x + 32) - (enemy.rect.x + 32))**2 + ((player.rect.y + 32) - (enemy.rect.y + 32))**2)
                    if ((-1 * self.range) <= dist <= self.range):
                        enemy.getHit(self.dmg, self.element)
        
        if keys[K_e]:
            if((self.delay-pygame.time.get_ticks()) < -500):
                if (self.openInventory == False):
                    self.delay = pygame.time.get_ticks()
                    self.accessInventory()
                elif(self.openInventory):
                    self.delay = pygame.time.get_ticks()
                    self.closeInventory()
        #elif (self.control == False):
        #    if (self.openInventory):
        #        for slot in self.inventory:
        #            if slot.rect.collidepoint(mouse_pos):
        #                screen.blit(highlight_item(slot.rect.x, slot.rect.y))
                        # change screen to inventory image once blit
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
        self.playerInv = Inventory()
        all_sprites.add(self.playerInv)

    def closeInventory(self):
        self.control = True
        self.openInventory = False
        self.playerInv.kill()

    def pickUpItem(self, item):
        if len(self.inventory) < 16:
            self.inventory.append(item)

class Enemy (Sprite):
    def __init__(self, posx, posy, type):
        super(Enemy, self).__init__()
        filename = 'assets/tile/' + type + '_0.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.rect = self.surf.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def getHit(self, dmg, element):
        pass


class Chest (Sprite):
    def __init__(self, posx, posy, type):
        super(Chest, self).__init__()
        filename = 'assets/tiles/chest_' + str(type) + '.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = pygame.image.load(filename).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.left = posx
        self.rect.top = posy
        self.type = type
        self.open = False
        self.content = []
        # run method to fill container

    def fill(self, item):
        self.content.append(item)
        # use randomizer to put items in, use type to determine quality/quantity of items
    def getType(self):
        return self.type
    
    def update(self, mouse_pos, mouse_click):
        if self.open:
            open_type = self.type + 3
            filename = 'assets/tiles/chest_' + str(open_type) +'.png'
            self.surf = pygame.image.load(filename).convert_alpha()
        if self.open == False:
            if self.rect.collidepoint(mouse_pos):
                highlight_type = self.type + 6
                filename = 'assets/tiles/chest_' + str(highlight_type) + '.png'
                self.surf = pygame.image.load(filename).convert_alpha()
                if mouse_click:
                    dist = meth.sqrt(((player.rect.x + 32) - (self.rect.x + 32))**2 + ((player.rect.y + 32) - (self.rect.y + 32))**2)
                    # distance formula
                    if (-128 <= dist <= 128):
                        self.open = True
                        
            else:
                self.surf = self.def_img

# if mouse_pos in rect then randomize loot, open window to show interface of loot, change chest sprite to open

frame = 0
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
tiles = pygame.sprite.Group()
players = pygame.sprite.Group()
cursor_ = pygame.sprite.Group()
items = pygame.sprite.Group()

player = Player()
chest = Chest(600, 300, 1)
item = Weapon('test', 1, 1, '')


all_sprites.add(player)
all_sprites.add(chest)
all_sprites.add(item)
items.add(item)
tiles.add(chest)
players.add(player)
cursor_.add(cursor)

running = True
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
    if frame > 3:
        player.update(mouse_pos, mouse_click, pressed_keys, touching_tiles, hitting_enemies)
        frame = 0

    screen.fill((255, 255, 255))
    cursor.rect.center = mouse_pos
    


    for entity in all_sprites:
        if entity.exist() == True:
            screen.blit(entity.surf, entity.rect)

    
    screen.blit(cursor.surf, cursor.rect)
    items.update(mouse_pos, mouse_click)
    tiles.update(mouse_pos, mouse_click)
 
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()