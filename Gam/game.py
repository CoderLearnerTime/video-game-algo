import math as Math
import pygame
import random
import pathfinding
import lootGenerator
from pygame import *
from pathfinding import *

pygame.init()

# CONSTANTS
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 768)
FONT = pygame.font.Font('assets/font/8bit.ttf', 24)


# initialize surfaces/images
screen = pygame.display.set_mode(SIZE)
highlight_item = pygame.Surface((48, 48), pygame.SRCALPHA)
highlight_item.fill((255, 255, 255, 128))
hit_flash = pygame.Surface((1278, 766), pygame.SRCALPHA)
hit_flash.fill((255, 64, 64, 96))
collisionMap = pygame.image.load('assets/map/test.png').convert_alpha()
bg = pygame.image.load('assets/map/maintest.png').convert_alpha()


# pygame clock
clock = pygame.time.Clock()

# caption
pygame.display.set_caption("rpg game")

# loading player sprite
player_actions = ['idle', 'left', 'right', 'up', 'down']
player_img = {}
for img in player_actions:
    filename = 'assets/player/player_' + img + '.png'
    player_img[img] = pygame.image.load(filename).convert_alpha()

# loading weapon sprites
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

element_list = [
    #prot   normal fire  ice  ground air  light  dark
            [1.1 , 0.75, 0.5 , 1.0 , 2.0 , 0.8 , 1.0 ],
            [1.2 , 2.4 , 0.5 , 0.5 , 1.0 , 0.8 , 1.0 ],
            [1.2 , 1.0 , 2.0 , 0.5 , 1.0 , 0.8 , 1.0 ],
            [1.1 , 0.5 , 1.0 , 2.0 , 0.75, 0.8 , 1.0 ],
            [1.2 , 1.0 , 1.0 , 1.0 , 1.0 , 0.75, 2.0 ],
            [1.4 , 1.25, 1.25, 1.25, 1.25, 2.0 , 0.75],
            [1.0 , 0.9 , 0.9 , 0.9 , 0.9 , 0.7 , 0.9 ]
]

# initializing base sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()

    def update(self):
        pass

    def exist(self):
        return True

# custom cursor
pygame.mouse.set_visible(False)
cursor = Sprite()
cursor.surf = pygame.image.load('assets/player/cursor.png').convert_alpha()
cursor.rect = cursor.surf.get_rect()


class Item (Sprite):
    def __init__(self, name, subclass, quantity, x = 0, y = 0):
        super(Item, self).__init__()
        filename = 'assets/' + subclass + '/'  + str(name) + '_0.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = name
        self.subclass = subclass
        self.quantity = quantity

        self.onGround = True
        # onGround = False means item is in inventory
        self.tick = 0
        self.frame = 0

    def setGround(self, on):
        self.onGround = on

    def holding(self):
        return self.inInventory
    
    # pick up item method: tests if inventory isn't full, then appends item to inventory list
    def pickUp(self):
        if len(player.inventory) < 15:
            player.pickUpItem(self)
            self.onGround = False
        else:
            print("Inventory full!")
            # have image in text on screen with fading letters

    # update function runs constantly in main loop
    def update(self, mouse_pos, mouse_click):
        
        # onGround items
        if (self.onGround == True):
            # floating animation
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
            # highlight on hover
            if (self.rect.collidepoint(mouse_pos)) & (player.openInventory == False):
                highlight_type = self.type + "_highlight"
                filename = 'assets/' + self.subclass + '/' + str(highlight_type) + '.png'
                self.surf = pygame.image.load(filename).convert_alpha()
                # pick up item if clicked
                if mouse_click:
                    dist = Math.sqrt(((player.rect.x + 32) - (self.rect.x + 32))**2 + ((player.rect.y + 32) - (self.rect.y + 32))**2)
                    if (-128 <= dist <= 128):
                        self.pickUp()
                        
            else:
                # unhighlights the img if the pointer is off the item
                self.surf = self.def_img
        elif ((self.inInventory) & (player.openInventory) & (player.control == False)):
            # highlights item in inventory on hover
            self.surf = self.def_img
            if self.rect.collidepoint(mouse_pos):
                self.highlight = highlight_item.copy()
                screen.blit(self.highlight, (self.rect.x, self.rect.y))
                if mouse_click:
                    self.selected = True
            
                
        # if condition for in inventory, hover img, moving in inventorry, drop from inventory
# player and chest inventory class (needs to show up on screen so needs to be sprite)
class Inventory(Sprite):
    def __init__(self, type):
        super(Inventory, self).__init__()
        if (type == 0):
            self.surf = pygame.image.load('assets/inventory/player_inventory_0.png')
        elif (type == 1):
            self.surf = pygame.image.load('assets/inventory/chest_inventory_0.png')
        self.rect = self.surf.get_rect()
        self.rect.move_ip(390, 110)

hpbar = Sprite()
hpbar.surf = pygame.image.load('assets/player/healthbar.png').convert_alpha()
hpbar.rect = hpbar.surf.get_rect()
HPBROWN = (90, 58, 23)
HPRED = (146,0,0)
HPDARKRED = (115,0,0)
hpbar.rect.move_ip(25, 25)

endGame = Sprite()
endGame.surf = pygame.image.load('assets/map/gameover.png').convert_alpha()
endGame.rect = endGame.surf.get_rect()


class Player (Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = player_img['idle']
        self.rect = self.surf.get_rect()
        self.control = True
        self.openInventory = False
        self.inventory = []
        self.rect.x = x
        self.rect.y = y
        self.pos = (x,y)
        # labeled 0-15, len = 16
        self.invDelay = pygame.time.get_ticks()
        self.hitDelay = pygame.time.get_ticks()
        self.knockbackDelay = pygame.time.get_ticks() - 300
        self.health = 100
        self.maxHealth = 100
        self.dmg = 10
        self.elementDmg =  0
        self.elementProt = 0
        self.money = 0
        self.enemyHit = None
        self.openInterface = False
        # modify these instance variables based on weapon, armor, items, etc

    def update(self, mouse_pos, mouse_click, keys, touching, hitting):
        # Movement
        self.pos = (self.rect.x, self.rect.y)

        # makes sure player has control (so not in inventory) and checks for keys pressed to allow movement
        if (self.control == True):
            if keys[K_UP]:
                self.rect.move_ip(0,-1)
                self.surf = player_img['up']
                for tile in touching:
                    # if player is touching a tile (like a chest), makes sure that it can't go through the tile
                    # tests if player is below the tile and moves them back to not inside of the tile
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
            # delays inventory opening so don't lag game
            if((self.invDelay-pygame.time.get_ticks()) < -200):
                if ((self.openInventory == False) & (self.openInterface == False)):
                    self.invDelay = pygame.time.get_ticks()
                    self.accessInventory()
                elif (self.openInventory) or (self.openInterface == True):
                    self.invDelay = pygame.time.get_ticks()
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

        if ((pygame.time.get_ticks() - self.knockbackDelay) < 300):
            if (pygame.time.get_ticks() % 2 != 1):
                dx = float(self.enemyHit.rect.x) - float(self.rect.x)
                dy = float(self.enemyHit.rect.y) - float(self.rect.y)
                norm = Math.sqrt(dx ** 2.0 + dy ** 2.0)
                x, y = -3 * dx / norm, -3 * dy / norm
                self.rect.move_ip(int(x),int(y))
                self.control = False
        else :
            self.control = True
        if(((self.hitDelay - pygame.time.get_ticks()) > -200 )and (pygame.time.get_ticks() > 200)):
            self.hit = hit_flash.copy()
            screen.blit(self.hit, (0, 0))
            

    def accessInventory(self):
        self.control = False
        self.openInventory = True
        for i in range(4): 
            # adds items that are in inventory onto the screen and moves them to fit with the inventory sprite
            # to give appearance of being in the slots
            try:
                player.inventory[i].rect.x, player.inventory[i].rect.y = ((402 + 68 * i), 122)
                inventoryGroup.add(player.inventory[i])
                continue
            # the try and except statements account for inventory not being full/empty slots so doesn't
            # give an index-out-of-bounds-error
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
        # closes any inventory that are open
        self.control = True
        self.openInventory = False
        self.openInterface = False
        for i in inventories:
            i.kill()

    def pickUpItem(self, item):
        if len(self.inventory) < 16:
            if (item.name != "coins"):
                self.inventory.append(item)
            else:
                player.money += item.quantity
                item.kill()
    
    def drawHealthBar(self):
        pygame.draw.rect(screen, (0,0,0), ((87,33), (self.maxHealth * 4 + 12, 4)))
        pygame.draw.rect(screen, (HPBROWN), ((87,37), (self.maxHealth * 4 + 4, 4)))
        pygame.draw.rect(screen, (0,0,0), ((87,41), (self.maxHealth * 4 + 4, 4)))
        pygame.draw.rect(screen, (HPRED), ((87,45), (self.health * 4, 12)))
        pygame.draw.rect(screen, (HPDARKRED), ((87,57), (self.health * 4, 12)))
        pygame.draw.rect(screen, (0,0,0), ((87,68), (self.maxHealth * 4 + 4, 4)))
        pygame.draw.rect(screen, (HPBROWN), ((87,72), (self.maxHealth * 4 + 4, 4)))
        pygame.draw.rect(screen, (0,0,0), ((87,76), (self.maxHealth * 4 + 12, 4)))

        pygame.draw.rect(screen, (HPBROWN), ((91 + self.maxHealth * 4, 37), (4, 39)))
        pygame.draw.rect(screen, (0,0,0), ((95 + self.maxHealth * 4, 37), (4, 40)))
        pygame.draw.rect(screen, (0,0,0), ((87 + self.maxHealth * 4, 41), (4, 28)))

    def getHit(self, enemy):
        finalDmg = enemy.dmg
        enemyElement = enemy.elementDmg
        dmgMultiplier = element_list[enemyElement][self.elementProt]
        if((self.hitDelay - pygame.time.get_ticks()) < -300):
            self.knockbackDelay = pygame.time.get_ticks()
            self.hitDelay = pygame.time.get_ticks()
            self.enemyHit = enemy
            self.health -= finalDmg * dmgMultiplier

        if (self.health < 0):
            self.control = False
            endGame.set_alpha(0)
            

class Enemy (Sprite):
    def __init__(self, posx, posy, type, dmg, hp):
        super(Enemy, self).__init__()
        filename = 'assets/entity/' + type + '_idle.png'
        self.surf = pygame.image.load(filename).convert_alpha()
        self.def_img = self.surf
        self.rect = self.surf.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.initUpdate = 0
        self.cur_node = 0
        self.elementDmg =  0
        self.elementProt = 0
        self.playerPos = player.pos
        self.speed = 1
        self.dmg = dmg
        self.hp = hp

    def getHit(self, dmg, element):
        pass
    def die(self):
        dropList = lootGenerator.entityLoot(player.stage, self.type)
        for item in dropList:
            pass
        self.kill()
    def pathfind(self):
        self.g = 100000
        if (self.playerPos[0] != player.pos[0]) or (self.playerPos[1] != player.pos[1]) or self.initUpdate == 0:
            hdx, hdy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
            dist = Math.hypot(hdx, hdy)
            if (dist < 1700):
                
                miniPath = pathfinding.aStar.findPath(self, player, collisionMap)
            # take the distance from the player to the enemy

                if miniPath is not None:
                    g = miniPath[1]
                    #print(miniPath[0])
                self.path = []

                
            # if distance is close enough, create full size path of points to follow
                try:
                    if g < 10: 
                        for node in miniPath[0]:
                            self.path.append([node[0] * 32 - 16, node[1] * 32 - 16])
                            #print("append")
                # set initUpdate to 1 to show that has been initialized
                        self.initUpdate = 1
                    dx, dy = self.path[0][0] - self.rect.x, self.path[0][1] - self.rect.y
                    self.cur_node = 0
                    dist = abs(Math.hypot(dx, dy))

                    if -24 <= dist <= 24:
                        dx, dy = self.path[1][0] - self.rect.x, self.path[1][1] - self.rect.y
                        self.cur_node = 1
                        dist = abs(Math.hypot(dx, dy))
                    
                    if dx > 0:
                        dx = int(Math.ceil(dx / dist))
                    elif dx < 0:
                        dx = int(Math.floor(dx / dist))
                    if dy > 0:
                        dy = int(Math.ceil(dy / dist))
                    elif dy < 0:
                        dy = int(Math.floor(dy / dist))
                    self.rect.move_ip(dx, dy)
                                  
                except:
                    pass
                
            #print(self.path)
            self.playerPos = (player.rect.x, player.rect.y)
        # if path exists, follow path
        elif self.path is not None:
            #print(self.cur_node)
            if self.cur_node >= (len(self.path) - 1):
                #print(len(self.path))
                if pygame.sprite.collide_rect(self, player):
                    player.getHit(self)
            elif self.cur_node < (len(self.path) - 1):
                dx, dy = self.path[self.cur_node][0] - self.rect.x, self.path[self.cur_node][1] - self.rect.y
                if -3 <= dx <= 3 and -3 <= dy <= 3:
                    self.cur_node += 1
                    dx, dy = (self.path[self.cur_node][0] - self.rect.x), (self.path[self.cur_node][1] - self.rect.y)
                
                dist = abs(Math.hypot(dx, dy))

                if dx > 0:
                    dx = int(Math.ceil(dx / dist))
                elif dx < 0:
                    dx = int(Math.floor(dx / dist))
                if dy > 0:
                    dy = int(Math.ceil(dy / dist))
                elif dy < 0:
                    dy = int(Math.floor(dy / dist))
                
                self.rect.move_ip(dx, dy)
    def update(self):

        if(pygame.time.get_ticks() % 8 != 1):
            self.pathfind()
        if pygame.sprite.collide_rect(self, player):
            player.getHit(self)
        if (self.hp <= 0):
            self.die()
        



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
        # run method to fill container

    def fill(self, type):
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


class Wall (Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__()
        # initialize sprite, use img, 32*32, and x and y
        # add collision

# load img
#procMap = PIL.Image.open('assets/map/test.png')
#mapArray = procMap.load()

# function for updating each screen
#def updateStage(theStage, theRoom):
#    for i in range(40):
#        for j in range(24):
            # if color in the config map is black, then that area in main
            # map is an edge wall (use different sprite imgs)
#            if (mapArray[i,j] == (0,0,0)):
#                wall = Wall((i * 32), (j * 32), theRoom, theStage, "edgeWall")
            # if color is red, then pillar
#            if (mapArray[i,j] == (255,0,0)):
#                wall = Wall((i * 32), (j * 32), theRoom, theStage, "pillar")
            # if green, then door
#            if (mapArray[i,j] == (0,255,0)):
#                wall = Wall((i * 32), (j * 32), theRoom, theStage, "door")

# init stage and room at 0           
stage = 0
room = 0                
#updateStage(stage, room)

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

player = Player(100, 100)
chest = Chest(600, 300, 0)
zombie = Enemy(200, 500, 'zombie', 10, 10)


all_sprites.add(player)
all_sprites.add(chest)
all_sprites.add(zombie)
all_sprites.add(hpbar)

enemies.add(zombie)
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
    #print(player.health)
    

    screen.fill((100, 100, 100))
    screen.blit(bg, (0,0))
    cursor.rect.center = mouse_pos
    
    for entity in all_sprites:
        if entity.exist() == True:
            screen.blit(entity.surf, entity.rect)
    for inv in inventories:
        screen.blit(inv.surf, inv.rect)
    if player.openInventory == True:        
        for item in inventoryGroup:
            screen.blit(item.surf, item.rect)
    f += 1
    if f> 2:
        enemies.update()
        f =0
    frame += 1
    if frame > speed:
        player.update(mouse_pos, mouse_click, pressed_keys, touching_tiles, hitting_enemies)
        frame = 0
    
    screen.blit(cursor.surf, cursor.rect)
    items.update(mouse_pos, mouse_click)
    tiles.update(mouse_pos, mouse_click)
    player.drawHealthBar()
    pygame.display.flip()

pygame.quit()