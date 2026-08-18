import pygame
import time
import random

pygame.init()

display_width=1000
display_height=600
car_width=90

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("CAR RACER")
clock=pygame.time.Clock()

enemy_width = 100
enemy_height = 160



black=(0,0,0)
white=(255,255,255)

enemyCar = pygame.image.load("enemycar.png")
enemyCar = pygame.transform.scale(enemyCar, (100, 160))

carimage = pygame.image.load("car.png")
carimage = pygame.transform.scale(carimage, (90, 150))

road = pygame.image.load("road.png")

def things_dodged(count):
    font=pygame.font.SysFont(None,25)
    text=font.render("Score:"+str(count),True,white)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy):
    gameDisplay.blit(enemyCar, (thingx, thingy))

def text_objects(text,font):
    textSurface=font.render(text,True,white)
    return textSurface,textSurface.get_rect()

def display_message(text):
    largeText=pygame.font.Font('freesansbold.ttf',70)
    TextSurf,TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)

    
    pygame.display.update()
    
    time.sleep(2)

    game_loop()

def crash():
    display_message('You Have Been Crashed!!!')

def car(x,y):
    gameDisplay.blit(carimage,(x,y))

def game_loop():
    
    x_change=0
    x=(display_width*0.45)
    y=(display_height*0.8)

    road_left = 170
    road_right = 850

    thing_startx = random.randrange(0, display_width - enemy_width)
    thing_starty = -150
    thing_speed = 4

    background_y = 0
    road_speed = 5
    
    dodged=0
    
    gameExit=False
    while not gameExit:
        background_y += road_speed
        if background_y >= display_height:
            background_y = 0
            
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change =-5
                elif event.key == pygame.K_d:
                    x_change =5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0

        x+=x_change
        if x < road_left:
            x = road_left

        if x > road_right - car_width:
            x = road_right - car_width

        gameDisplay.blit(road, (0, background_y))
        gameDisplay.blit(road, (0, background_y - display_height))

        car(x,y)
        
        things_dodged(dodged)
        things(thing_startx, thing_starty)
        thing_starty += thing_speed


        
        if thing_starty > display_height:
            thing_starty = -150
            thing_startx = random.randrange(road_left, road_right - enemy_width)
            dodged+=1
            thing_speed = 7 + dodged //10
            road_speed = 5 + dodged // 10
            

        if x>display_width-car_width or x<0:
            crash()

        if y<thing_starty+enemy_height:

           

            if x>thing_startx and x< thing_startx+enemy_width or x+car_width>thing_startx and x+car_width<thing_startx+enemy_width:
                print("x crossover")
                print("Player Top:", y)
                print("Player Bottom:", y + 150)

                print("Enemy Top:", thing_starty)
                print("Enemy Bottom:", thing_starty + enemy_height)
                print("Speed of Car:",thing_speed)
                crash()

                
        pygame.display.update()
        clock.tick(60)
        


game_loop()
pygame.quit()
quit()
