import pygame
from pygame.locals import *
import os
import math
DEFAULT_ACTOR_SPRITE_WIDTH = 16
DEFAULT_TILE_SPRITE_WIDTH = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 625

class Actor(pygame.sprite.Sprite):
    totalActorCount = []
    def __init__(self, x, y, width = DEFAULT_ACTOR_SPRITE_WIDTH, height = DEFAULT_ACTOR_SPRITE_WIDTH, color = (255, 255, 255), filename = "default.png"):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.imageS = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def register_subclass(self, name):
        print("Registered " + name +  " as a subclass of Actor") 
        self.totalActorCount.append(name)
    

class Player(Actor):
    def __init__(self, startingx, startingy):
        super().__init__(startingx, startingy, DEFAULT_ACTOR_SPRITE_WIDTH, DEFAULT_ACTOR_SPRITE_WIDTH, (255, 255, 255), "player.png")
        self.dir = 0
        super().register_subclass("player")
        self.deltax = 0
        self.deltay = 0
    def _update_keypressed(self, event):
        
        if event.key == pygame.K_a:
            player.dir = 1
            self.deltax = -10
        if event.key == pygame.K_d:
            player.dir = 2
            self.deltax = 10
        if event.key == pygame.K_w:
            player.dir = 3
            self.deltay = -10
        if event.key == pygame.K_s:
            player.dir = 4
            self.deltay = 10
        if event.key == pygame.K_s and pygame.key == pygame.K_a:
            print("hi")
        
            
    def _update_keyup(self, event):
        
        if event.key == pygame.K_a:
            self.deltax = 0 
        if event.key == pygame.K_d:
            self.deltax = 0
        if event.key == pygame.K_w:
            self.deltay = 0
        if event.key == pygame.K_s:
            self.deltay = 0

    def update(self):
        self.rect.x += self.deltax 
        self.rect.y += self.deltay 
        wall_collide = pygame.sprite.spritecollide(self, self.walls, False)

        for col in wall_collide:
            if self.rect.left <= col.rect.left and self.rect.left <= col.rect.right and col.rect.left and self.dir == 2:
                self.rect.right = col.rect.left
                
                
            if self.rect.right >= col.rect.left and self.rect.right >= col.rect.right and col.rect.left and self.dir == 1:
                self.rect.left = col.rect.right
                
                
            if self.rect.top <= col.rect.top and self.rect.top <= col.rect.bottom and col.rect.top and self.dir == 4:
                self.rect.bottom = col.rect.top

                
            if self.rect.bottom >= col.rect.top and self.rect.bottom >= col.rect.bottom and col.rect.top and self.dir == 3:
                self.rect.top = col.rect.bottom
                                                                                                                                                 
            
class GroupManager:
    all_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    enemy_sprite = pygame.sprite.Group()
    wall_sprite = pygame.sprite.Group()

class Camera:
    CameraX = 0
    CameraY = 0
    VelocityX = 0
    VelocityY = 0
    CameraWidth = SCREEN_WIDTH
    CameraHeight = SCREEN_HEIGHT
    CameraDir = 0
    @staticmethod
    def Update_Keypressed(event):
        if event.key == pygame.K_LEFT:
            Camera.VelocityX = -1
        if event.key == pygame.K_RIGHT:
            Camera.VelocityX = 1
        if event.key == pygame.K_UP:
            Camera.VelocityY = 1
        if event.key == pygame.K_DOWN:
            Camera.VelocityY = -1
    @staticmethod
    def Update_Keyup(event):
        if event.key == pygame.K_LEFT:
            Camera.VelocityX = 0
        if event.key == pygame.K_RIGHT:
            Camera.VelocityX = 0
        if event.key == pygame.K_UP:
            Camera.VelocityY = 0
        if event.key == pygame.K_DOWN:
            Camera.VelocityY = 0

    @staticmethod
    def Update():
        Camera.CameraX += Camera.VelocityX
        Camera.CameraY += Camera.VelocityY

    @staticmethod
    def Check_Boundaries(player):
        if player.rect.y >= SCREEN_HEIGHT / 4 * 3 + 10:
            
            Camera.VelocityY = -10
        elif player.rect.y <= SCREEN_HEIGHT / 4 * 3 - 250:
            Camera.VelocityY = 10

        elif player.rect.x >= SCREEN_WIDTH / 4 * 3 + 10:
            Camera.VelocityX = -10
        elif player.rect.x <= SCREEN_WIDTH / 4 * 3 - 350:
            Camera.VelocityX = 10
        else:
            Camera.VelocityX = 0
            Camera.VelocityY = 0

        

        
        print(Camera.CameraDir)
class Wall(Actor):
    def __init__(self, x, y, width , height, color):
        super().__init__(x, y, width, height, color)
        super().register_subclass("wall")
       


pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player(10, 10)
backgroundimage = pygame.image.load ("background.png")
player.walls = GroupManager.wall_sprite
clock = pygame.time.Clock()
world = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
world.set_colorkey((255, 0, 255))
world.fill((255, 0, 255))
GroupManager.all_sprite.add(player)
wall1 = Wall(10, 10, 16, 160, (0, 255, 0))
GroupManager.all_sprite.add(wall1)
GroupManager.wall_sprite.add(wall1)
isRunning = True
while isRunning:
    Camera.Check_Boundaries(player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        if event.type == pygame.KEYDOWN:            
            player._update_keypressed(event)
            Camera.Update_Keypressed(event)

        if event.type == pygame.KEYUP:
            
            player._update_keyup(event)
            Camera.Update_Keyup(event)
           
    display.fill((255, 0, 0))
    display.blit(backgroundimage, (0, 0))
    Camera.Update()
    GroupManager.all_sprite.update()
    display.blit(world, (Camera.CameraX, Camera.CameraY))
    GroupManager.all_sprite.draw(display)
    for ent in GroupManager.all_sprite:
        ent.rect.x = ent.rect.x + Camera.VelocityX
        ent.rect.y = ent.rect.y + Camera.VelocityY
    pygame.display.update()
    clock.tick(60)
pygame.quit()

