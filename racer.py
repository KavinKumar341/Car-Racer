
import pygame
import time
import random
import cv2
import mediapipe as mp
import threading

pygame.init()

display_width = 1000
display_height = 600
car_width = 90

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("CAR RACER")
clock = pygame.time.Clock()

enemy_width = 100
enemy_height = 160


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

enemyCar = pygame.image.load("Enemy1.png")
enemyCar = pygame.transform.scale(enemyCar, (100, 160))

enemyCar2 = pygame.image.load("Enemy2.png")
enemyCar2 = pygame.transform.scale(enemyCar2, (100, 160))

carimage = pygame.image.load("User.png")
carimage = pygame.transform.scale(carimage, (90, 150))

road = pygame.image.load("road.png")

highest_score = 0

# MEDIAPIPE SETUP
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
BaseOptions = mp.tasks.BaseOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)

# WEBCAM SETUP
cap = cv2.VideoCapture(0)

# Lower camera resolution to reduce CPU usage

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


# Keep only the latest camera frame

cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# CAMERA VARIABLES

# Latest frame received from camera

latest_frame = None


# Controls whether camera thread keeps running

camera_running = True


# -1 = left
#  0 = stop
#  1 = right

hand_direction = 0

# CAMERA THREAD
# Camera runs separately from the Pygame game loop

def camera_loop():

    global latest_frame
    global camera_running

    while camera_running:

        success, frame = cap.read()

        if success:

            # Flip camera

            frame = cv2.flip(frame, 1)

            # Store newest frame

            latest_frame = frame



# Start camera thread

camera_thread = threading.Thread(
    target=camera_loop,
    daemon=True
)

camera_thread.start()


# GAME FUNCTIONS

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score:" + str(count), True, white)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, enemy):
    gameDisplay.blit(enemy, (thingx, thingy))


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def display_message(text):
    largeText = pygame.font.Font('freesansbold.ttf', 70)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def crash(score):
    global highest_score

    if score > highest_score:
        highest_score = score

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                global camera_running

                camera_running = False

                cap.release()

                landmarker.close()

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

        if button_rect.collidepoint(mouse_x, mouse_y):
            button_color = (0, 255, 0)
        else:
            button_color = (0, 150, 0)

        pygame.draw.rect(
            gameDisplay,
            button_color,
            button_rect,
            border_radius=15
        )

        pygame.draw.rect(
            gameDisplay,
            white,
            button_rect,
            3,
            border_radius=15
        )

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


def car(x, y):
    gameDisplay.blit(carimage, (x, y))

# GAME LOOP
def game_loop():

    global hand_direction

    x_change=0
    x=(display_width*0.45)
    y=(display_height*0.8)


    road_left = 170
    road_right = 850

    thing_startx = random.randrange(
        road_left,
        road_right - enemy_width
    )

    thing_starty = -150
    thing_speed = 4


    thing2_startx = random.randrange(
        road_left,
        road_right - enemy_width
    )
    thing2_starty = -400
    thing2_speed = 4
    background_y = 0
    road_speed = 5
    dodged=0
    # MEDIAPIPE DETECTION TIMING

    last_detection_time = 0

    # Detect hand approximately 12 times per second

    detection_interval = 1 / 12
    # PREVENT ENEMY OVERLAP
    while abs(
        thing2_startx - thing_startx
    ) < enemy_width + 50:

        thing2_startx = random.randrange(
            road_left,
            road_right - enemy_width
        )
    gameExit=False
    while not gameExit:

        # HAND DETECTION
        current_time = time.time()
        if (
            current_time - last_detection_time
            >= detection_interval
        ):

            last_detection_time = current_time

            frame = latest_frame
            if frame is not None:
                # Convert BGR → RGB

                rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )
                # Convert to MediaPipe image

                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb
                )
                # Detect hand

                result = landmarker.detect(
                    mp_image
                )
                # HAND DETECTED
                if result.hand_landmarks:

                    hand = result.hand_landmarks[0]
                    wrist = hand[0]
                    hand_x = wrist.x
                    # LEFT

                    if hand_x < 0.4:

                        hand_direction = -1
                    # RIGHT

                    elif hand_x > 0.6:

                        hand_direction = 1
                    # CENTER

                    else:

                        hand_direction = 0
                # NO HAND
                else:
                    hand_direction = 0

        # KEYBOARD CONTROL


        # Define keyboard direction

        keyboard_direction = 0
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                camera_running = False

                cap.release()

                landmarker.close()

                pygame.quit()

                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:

                    keyboard_direction = -1

                elif event.key == pygame.K_d:

                    keyboard_direction = 1
            if event.type == pygame.KEYUP:

                if (
                    event.key == pygame.K_a
                    or event.key == pygame.K_d
                ):

                    keyboard_direction = 0
        # MOVEMENT CONTROL

        if keyboard_direction != 0:

            x_change = keyboard_direction * 5
        else:

            x_change = hand_direction * 5
        # CAR MOVEMENT

        x += x_change
        if x < road_left:

            x = road_left
        if x > road_right - car_width:

            x = road_right - car_width
        # ROAD MOVEMENT

        background_y += road_speed
        if background_y >= display_height:

            background_y = 0
        gameDisplay.blit(
            road,
            (0, background_y)
        )
        gameDisplay.blit(
            road,
            (0, background_y - display_height)
        )
        # DRAW CAR

        car(x,y)
        # SCORE

        things_dodged(dodged)
        # ENEMY CARS

        things(
            thing_startx,
            thing_starty,
            enemyCar
        )
        things(
            thing2_startx,
            thing2_starty,
            enemyCar2
        )
        # MOVE ENEMY CARS

        thing_starty += thing_speed

        thing2_starty += thing2_speed
        # ENEMY 1 RESET

        if thing_starty > display_height:

            thing_starty = -150
            thing_startx = random.randrange(
                road_left,
                road_right - enemy_width
            )
            while abs(
                thing_startx - thing2_startx
            ) < enemy_width + 50:

                thing_startx = random.randrange(
                    road_left,
                    road_right - enemy_width
                )
            dodged += 1
            thing_speed = 7 + dodged // 10

            road_speed = 5 + dodged // 10
        # ENEMY 2 RESET

        if thing2_starty > display_height:
            thing2_starty = -400
            thing2_startx = random.randrange(
                road_left,
                road_right - enemy_width
            )
            while abs(
                thing2_startx - thing_startx
            ) < enemy_width + 50:

                thing2_startx = random.randrange(
                    road_left,
                    road_right - enemy_width
                )
            dodged += 1
        # BOUNDARY COLLISION
        if (
            x > display_width-car_width
            or x < 0
        ):
            crash(dodged)

            return
        # ENEMY 1 COLLISION
        if y < thing_starty + enemy_height:
            if (
                x > thing_startx
                and
                x < thing_startx + enemy_width
                or
                x + car_width > thing_startx
                and
                x + car_width <
                thing_startx + enemy_width
            ):
                print("x crossover")
                print(
                    "Player Top:",
                    y
                )
                print(
                    "Player Bottom:",
                    y + 150
                )
                print(
                    "Enemy Top:",
                    thing_starty
                )
                print(
                    "Enemy Bottom:",
                    thing_starty + enemy_height
                )
                print(
                    "Speed of Car:",
                    thing_speed
                )
                crash(dodged)
                return
        # ENEMY 2 COLLISION
        if y < thing2_starty + enemy_height:


            if (
                x > thing2_startx
                and
                x < thing2_startx + enemy_width
                or
                x + car_width > thing2_startx
                and
                x + car_width <
                thing2_startx + enemy_width
            ):
                print(
                    "x crossover - Enemy 2"
                )
                print(
                    "Player Top:",
                    y
                )
                print(
                    "Player Bottom:",
                    y + 150
                )
                print(
                    "Enemy 2 Top:",
                    thing2_starty
                )
                print(
                    "Enemy 2 Bottom:",
                    thing2_starty + enemy_height
                )
                print(
                    "Speed of Car:",
                    thing2_speed
                )
                print("*******************************")


                crash(dodged)
                return

        # DISPLAY
        pygame.display.update()

        clock.tick(60)
# START GAME

while True:

    game_loop()
# CLEANUP

camera_running = False
cap.release()
landmarker.close()
pygame.quit()
quit()
