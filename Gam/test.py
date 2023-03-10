import pygame
pygame.init()
# As a module set outside of the current file, we need to import pygame
# and initialize in order to be able to access it

# Player now inherits the sprite class from pygame, can use sprite
# methods and variables now
class Player (pygame.sprite.Sprite):
    def __init__ (self, x, y, hp):

# super() is required when inheriting another class
# super(*class that is being created*, self).__init__()
        super(Player, self).__init__()

        self.playerX = x
        self.playerY = y
        self.playerHP = hp

# Now we can create an image to represent the player
# surf is a placeholder variable to hold the image
        self.surf = pygame.image.load('testdirectory/playerimg.png')
# Sprites have a variable called 'rect' which is a rectangle object that
# holds the sprite in its location
# This line sets the boundaries of this 'rect' as the size of the image
        self.rect = self.surf.get_rect()

    def getHit(self, dmg):
        self.playerHP = self.playerHP - dmg

# This method uses the Sprite method 'move()'
    def movePlayer(self, newX, newY):
        self.move(newX, newY)

# uses Sprite method 'move_ip'
    def moveUp(self):
        self.move_ip(0, -5)

