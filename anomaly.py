import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# SCREEN
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bunker Anomaly Escape")

clock = pygame.time.Clock()


# FONT
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 35)

# COLORS (fallback UI)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# GAME STATES
START, PLAYING, WIN, LOSE = "start", "play", "win", "lose"
state = START

# LOAD IMAGES
bunker_bg = pygame.image.load("assets/bunker.jpeg")
bunker_bg = pygame.transform.scale(bunker_bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (200,210))

crate_img = pygame.image.load("assets/crate.jpeg")
crate_img = pygame.transform.scale(crate_img, (WIDTH, HEIGHT))

anomaly_img = pygame.image.load("assets/light.jpeg")
anomaly_img = pygame.transform.scale(anomaly_img, (WIDTH, HEIGHT))

fog_img = pygame.image.load("assets/fog.jpeg")
fog_img = pygame.transform.scale(fog_img, (WIDTH, HEIGHT))

eye_img = pygame.image.load("assets/eye.jpeg")
eye_img = pygame.transform.scale(eye_img, (WIDTH, HEIGHT))

shadow_img = pygame.image.load("assets/shadow.jpeg")
shadow_img = pygame.transform.scale(shadow_img, (WIDTH, HEIGHT))

start_bg = pygame.image.load("assets/start_screen.jpg")
start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

win_bg = pygame.image.load("assets/win.jpeg")
win_bg = pygame.transform.scale(win_bg, (WIDTH, HEIGHT))

lose_bg = pygame.image.load("assets/lose.jpeg")
lose_bg = pygame.transform.scale(lose_bg, (WIDTH, HEIGHT))

#LOAD MUSIO
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

#LOAD FONT
heading_font = pygame.font.Font("assets/creepster.ttf", 60)
end_font = pygame.font.Font("assets/lylas.ttf", 60)
# PLAYER
player_x, player_y = WIDTH / 6, HEIGHT - 300
speed = 5

# GAME LOGIC
level = 1
score = 0

anomalies = [
    "extra_object",
    "fog",
    "light",
    "slow",
    "eye",
    "shadow"
]

room_has_anomaly = False
current_anomaly = None
last_anomaly = None

def generate_room():
    global room_has_anomaly, current_anomaly, last_anomaly, speed

    speed = 5
    room_has_anomaly = random.choice([True, False])

    if room_has_anomaly:
        available_anomalies = anomalies.copy()
        if last_anomaly in available_anomalies:
            available_anomalies.remove(last_anomaly)
        
        current_anomaly = random.choice(available_anomalies)
        last_anomaly = current_anomaly
    else:
        current_anomaly = None


generate_room()

# BUTTON
start_btn = pygame.Rect(350, 280, 200, 80)
restart_btn = pygame.Rect(320, 340, 250, 60)

# DRAW ROOM
def draw_room():

    # background
    screen.blit(bunker_bg, (0, 0))

    # anomalies
    if current_anomaly == "extra_object":
        screen.blit(crate_img, (0, 0))

    elif current_anomaly == "fog":
        screen.blit(fog_img, (0, 0))

    elif current_anomaly == "light":
        screen.blit(anomaly_img, (0, 0))

    elif current_anomaly == "eye":
        screen.blit(eye_img, (0, 0))

    elif current_anomaly == "shadow":
        screen.blit(shadow_img, (0, 0))

    elif current_anomaly == "slow":
        global speed
        speed = 2

    # player
    screen.blit(player_img, (player_x, player_y))

def check_room_transition():
    global player_x
    global score
    global level
    global state

    #right side = forward
    if player_x >= WIDTH - 120:
        if room_has_anomaly:
            state = LOSE
        else:
            score += 1
            level += 1
            
            if score == 5:
                state = WIN
            else: 
                player_x = 50
                generate_room()
                print(current_anomaly)
    #left side = backward
    elif player_x <= 0:
        if room_has_anomaly:
            score += 1
            level += 1

            if score == 5:
                state = WIN
            else:
                player_x = WIDTH - 150
                generate_room()
                print(current_anomaly)
        else:
            state = LOSE
    
#Restart logic
def restart_game():
    global state 
    global score
    global level
    global player_x
    global player_y 

    score = 0
    level = 1

    player_x = WIDTH // 6
    player_y = HEIGHT - 300

    generate_room()
    state = PLAYING

# LOOP
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == START:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    state = PLAYING
        
        elif state == WIN or state == LOSE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    restart_game()

    # MOVEMENT
    keys = pygame.key.get_pressed()

    if state == PLAYING:
        if keys[pygame.K_LEFT]:
            player_x -= speed
        if keys[pygame.K_RIGHT]:
            player_x += speed
        check_room_transition()

    # DRAW SCREENS
    if state == START:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(start_bg, (0, 0))
        screen.blit(overlay, (0, 0))

        title = heading_font.render("BUNKER ANOMALY ESCAPE", True, WHITE)
        screen.blit(title, (160, 190))

        pygame.draw.rect(screen, BLACK, start_btn)
        screen.blit(font.render("START", True, WHITE), (385, 295))

    elif state == PLAYING:
        draw_room()

        hud = small_font.render(f"Room {level}/5 | Score {score}", True, WHITE)
        screen.blit(hud, (20, 45))
        instruction = small_font.render(
            "LEFT = Anomaly | RIGHT = No Anomaly", True, WHITE
        )
        screen.blit(instruction, (20, 20))


    elif state == WIN:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        screen.blit(win_bg, (0, 0))
        screen.blit(overlay, (0, 0))
        text = end_font.render("YOU ESCAPED!", True, WHITE)
        screen.blit(text, (270, 250))

        pygame.draw.rect(screen, WHITE, restart_btn)
        restart_text = small_font.render("PLAY AGAIN", True, BLACK)
        screen.blit(restart_text, (370, 360))

    elif state == LOSE:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(lose_bg, (0, 0))
        screen.blit(overlay, (0, 0))
        text = end_font.render("YOU LOST", True, WHITE)
        score_text = small_font.render(f"Score: {score}/5", True, WHITE)
        screen.blit(text, (320, 210))
        screen.blit(score_text, (380, 280))

        pygame.draw.rect(screen, BLACK, restart_btn)
        restart_text = small_font.render(
            "PLAY AGAIN", True, WHITE
        )
        screen.blit(restart_text, (370, 360))

    pygame.display.flip()

pygame.quit()
sys.exit()