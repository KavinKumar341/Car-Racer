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
red=(255,0,0)

enemyCar = pygame.image.load("Enemy1.png")
enemyCar = pygame.transform.scale(enemyCar, (100, 160))

enemyCar2 = pygame.image.load("Enemy2.png")
enemyCar2 = pygame.transform.scale(enemyCar2, (100, 160))

carimage = pygame.image.load("User.png")
carimage = pygame.transform.scale(carimage, (90, 150))

road = pygame.image.load("road.png")

highest_score = 0

def things_dodged(count):
    font=pygame.font.SysFont(None,25)
    text=font.render("Score:"+str(count),True,white)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, enemy):
    gameDisplay.blit(enemy, (thingx, thingy))

def text_objects(text,font):
    textSurface=font.render(text,True,white)
    return textSurface,textSurface.get_rect()

def display_message(text):
    largeText=pygame.font.Font('freesansbold.ttf',70)
    TextSurf,TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)

    
    pygame.display.update()
    
    

def crash(score):
    global highest_score

    if score > highest_score:
        highest_score = score

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 350 <= mouse_x <= 650 and 400 <= mouse_y <= 470:
                    return True

        gameDisplay.fill(black)

        large_font = pygame.font.Font('freesansbold.ttf', 70)

        game_over = large_font.render(
            "GAME OVER", True, red
        )

        gameDisplay.blit(
            game_over,
            (display_width / 2 - 180, 120)
        )

        score_font = pygame.font.SysFont(None, 40)

        score_text = score_font.render(
            "Score: " + str(score),
            True,
            white
        )

        gameDisplay.blit(
            score_text,
            (400, 230)
        )

        high_text = score_font.render(
            "Highest Score: " + str(highest_score),
            True,
            white
        )

        gameDisplay.blit(
            high_text,
            (350, 280)
        )

        # PLAY AGAIN BUTTON

        button_rect = pygame.Rect(350, 400, 300, 70)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Change button when mouse is over it
        if button_rect.collidepoint(mouse_x, mouse_y):
            button_color = (0, 255, 0)
        else:
            button_color = (0, 150, 0)

        # Draw button
        pygame.draw.rect(
            gameDisplay,
            button_color,
            button_rect,
            border_radius=15
        )

        # Button border
        pygame.draw.rect(
            gameDisplay,
            white,
            button_rect,
            3,
            border_radius=15
        )

        # Button text
        button_font = pygame.font.SysFont(None, 40)

        button_text = button_font.render(
            "PLAY AGAIN",
            True,
            white
        )

        button_text_rect = button_text.get_rect(
            center=button_rect.center
        )

        gameDisplay.blit(
            button_text,
            button_text_rect
        )

        pygame.display.update()
        clock.tick(60)

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

    thing2_startx = random.randrange(road_left, road_right - enemy_width)
    thing2_starty = -400
    thing2_speed = 4

    background_y = 0
    road_speed = 5
    
    dodged=0

    while abs(thing2_startx - thing_startx) < enemy_width + 50:
        thing2_startx = random.randrange(road_left, road_right - enemy_width)
    
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
        things(thing_startx, thing_starty, enemyCar)
        things(thing2_startx, thing2_starty, enemyCar2)
        thing_starty += thing_speed
        thing2_starty += thing2_speed


        
        if thing_starty > display_height:
            thing_starty = -150
            thing_startx = random.randrange(road_left, road_right - enemy_width)

            while abs(thing_startx - thing2_startx) < enemy_width + 50:
                thing_startx = random.randrange(road_left, road_right - enemy_width)
            
            dodged+=1
            thing_speed = 7 + dodged //10
            road_speed = 5 + dodged // 10

        if thing2_starty > display_height:
            thing2_starty = -400
            thing2_startx = random.randrange(road_left, road_right - enemy_width)

            while abs(thing2_startx - thing_startx) < enemy_width + 50:
                thing2_startx = random.randrange(road_left, road_right - enemy_width)

            dodged+=1
        
            

        if x>display_width-car_width or x<0:
            crash(dodged)
            return

        if y<thing_starty+enemy_height:

           

            if x>thing_startx and x< thing_startx+enemy_width or x+car_width>thing_startx and x+car_width<thing_startx+enemy_width:
                print("x crossover")
                print("Player Top:", y)
                print("Player Bottom:", y + 150)

                print("Enemy Top:", thing_starty)
                print("Enemy Bottom:", thing_starty + enemy_height)
                print("Speed of Car:",thing_speed)
                crash(dodged)
                return

            if y < thing2_starty + enemy_height:

                if x > thing2_startx and x < thing2_startx + enemy_width or x + car_width > thing2_startx and x + car_width < thing2_startx + enemy_width:
                    print("x crossover - Enemy 2")
                    print("Player Top:", y)
                    print("Player Bottom:", y + 150)

                    print("Enemy 2 Top:", thing2_starty)
                    print("Enemy 2 Bottom:", thing2_starty + enemy_height)

                    print("Speed of Car:", thing2_speed)

                    crash(dodged)
                    return

                
        pygame.display.update()
        clock.tick(60)
        
while True:
    game_loop()


pygame.quit()
quit()
