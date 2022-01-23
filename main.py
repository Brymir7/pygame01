import pygame
import os
import random
from threading import Timer
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game01")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

FPS = 60
delta_time = 1 / FPS
VELOCITY = 5
MAX_BULLETS_YELLOW = 3
MAX_BULLETS_RED = 3
BULLET_VEL = 7

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_POWERUP = pygame.USEREVENT + 3
RED_POWERUP = pygame.USEREVENT + 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT =  55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(yellow, red, yellow_bullets, red_bullets, powerup):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y) )
    WIN.blit(RED_SPACESHIP, (red.x, red.y) )
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for powerup1 in powerup:
        pygame.draw.rect(WIN, YELLOW, powerup1)
    pygame.display.update()
    
def yellow_handle_movement(keys_pressed, yellow, powerup):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: 
            yellow.x -= VELOCITY   
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY  + SPACESHIP_WIDTH < BORDER.x : 
            yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY  > 15: 
            yellow.y -= VELOCITY 
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + SPACESHIP_HEIGHT < HEIGHT - 15:
            yellow.y += VELOCITY
    if yellow.colliderect(powerup):
            pygame.event.post(pygame.event.Event(YELLOW_POWERUP))
              
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY - SPACESHIP_WIDTH // 2 > BORDER.x - 5: 
            red.x -= VELOCITY  
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + SPACESHIP_WIDTH // 2 < WIDTH - 15: 
            red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 15: 
            red.y -= VELOCITY 
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + SPACESHIP_HEIGHT < HEIGHT - 15: 
            red.y += VELOCITY
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)     
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:  
            red_bullets.remove(bullet)
def handle_powerups(powerup, powerup1):
    powerup.append(powerup1)
         
def main():
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    max_bullets_upgrade_red = 0
    max_bullets_upgrade_yellow = 0
    random_value_yellow = random.uniform(50, 430)
    random_value_red = random.uniform(430, 850)
    random_value_height = random.uniform(50, 500)
    powerup = []
    power = 0
    yellow_health = 10
    red_health = 10
    powerup1 = pygame.Rect(random_value_yellow, random_value_height, 30, 30)
    yellow_bullets = []
    red_bullets = []
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS_YELLOW + max_bullets_upgrade_yellow:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS_RED + max_bullets_upgrade_red:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            if event.type == YELLOW_POWERUP:
                max_bullets_upgrade_yellow =  max_bullets_upgrade_yellow + delta_time*0.25 *1
                powerup.clear()
                
            if event.type == RED_POWERUP:
                max_bullets_upgrade_red = max_bullets_upgrade_red + delta_time*1
                powerup.clear()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                print("Yellow Health: ", yellow_health)
            if event.type == RED_HIT:
                red_health -= 1
                print("Red Health:", red_health)
        if yellow_health == 0 or red_health == 0:
            print("Game over")
            run = False             
        if power == 0:
            handle_powerups(powerup, powerup1)
            power = power+1 
        keys_pressed = pygame.key.get_pressed()    
        yellow_handle_movement(keys_pressed, yellow, powerup1)
        red_handle_movement(keys_pressed, red)  
        handle_bullets(yellow_bullets, red_bullets, yellow, red)               
        draw_window(yellow, red, yellow_bullets, red_bullets, powerup)
        
    pygame.quit()

if __name__ == "__main__":
    main()