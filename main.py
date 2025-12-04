import pygame, random

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600

score = [0, 0]
ball_size = 30
player1_hight = 130
player2_hight = 130
player_thickness = 30
border_left_right = 20
game_speed_delay = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

player1_pos = (HEIGHT - player1_hight) // 2  # Initial position of the square
player2_pos = (HEIGHT - player2_hight) // 2  # Initial position of the square

ball_pos_x = (WIDTH - ball_size) // 2 # Initial position of the ball
ball_pos_y = (HEIGHT - ball_size) // 2

ball_direction_x = random.choice([-4, 4])
ball_direction_y = random.choice([-4, 4])

font = pygame.font.SysFont('Courier New', 50, bold=True)

sound_ping = pygame.mixer.Sound("sound/Ping.mp3")
sound_pong = pygame.mixer.Sound("sound/Pong.mp3")
sound_rand = pygame.mixer.Sound("sound/Rand.mp3")
sound_tor = pygame.mixer.Sound("sound/Tor.mp3")

def reset_ball():
    global ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y
    ball_pos_x = (WIDTH - ball_size) // 2
    ball_pos_y = (HEIGHT - ball_size) // 2
    ball_direction_x = random.choice([-4, 4])
    ball_direction_y = random.choice([-4, 4])
    pygame.time.delay(1000)  # Pause for a moment before resuming

run = True
while run:
    pygame.time.delay(game_speed_delay)  # Delay to control frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ball_pos_x += ball_direction_x
    ball_pos_y += ball_direction_y
    
    if ball_pos_x < -ball_size:
        score[1] += 1
        pygame.mixer.Sound.play(sound_tor)
        reset_ball()

    if ball_pos_x > WIDTH:
        score[0] += 1
        pygame.mixer.Sound.play(sound_tor)
        reset_ball()

    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    if keys[pygame.K_w]:
        if player1_pos > 0:
            player1_pos -= 5
    if keys[pygame.K_s]:
        if player1_pos < HEIGHT - player1_hight:
            player1_pos += 5 
    if keys[pygame.K_UP]:
        if player2_pos > 0:
            player2_pos -= 5
    if keys[pygame.K_DOWN]:
        if player2_pos < HEIGHT - player2_hight:
            player2_pos += 5
    if keys[pygame.K_r]:
        score = [0, 0]
        reset_ball()
    if keys[pygame.K_ESCAPE]:
        run = False

    screen.fill((0, 0, 0))  # Fill the screen with black
    score_screen = font.render(f"{score[0]}   {score[1]}", True, (255, 255, 255))
    screen.blit(score_screen, ((WIDTH - score_screen.get_width()) // 2, 20))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 3)  # Draw the center line
    player1 = pygame.draw.rect(screen, (255, 255, 255), (border_left_right, player1_pos, player_thickness, player1_hight))
    player2 = pygame.draw.rect(screen, (255, 255, 255), (WIDTH - border_left_right - player_thickness, player2_pos, player_thickness, player2_hight))
    ball = pygame.draw.rect(screen, (255, 255, 255), (ball_pos_x, ball_pos_y, ball_size, ball_size))  # Draw the ball

    if ball_pos_y <= 0 or ball_pos_y >= HEIGHT - ball_size:
        ball_direction_y = -ball_direction_y
        pygame.mixer.Sound.play(sound_rand)
    
    if ball.colliderect(player1):
        if ball_pos_x < border_left_right + player_thickness - 1:  # Prevent multiple collisions
            pass
        else:
            ball_direction_x = -ball_direction_x
            pygame.mixer.Sound.play(sound_ping)
    if ball.colliderect(player2):
        if ball_pos_x > WIDTH - border_left_right - player_thickness - ball_size + 1:  # Prevent multiple collisions
            pass
        else:
            ball_direction_x = -ball_direction_x
            pygame.mixer.Sound.play(sound_pong)

    pygame.display.flip()  # Update the display

pygame.quit()