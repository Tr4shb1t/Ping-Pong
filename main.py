import pygame, random

Vector2 = pygame.math.Vector2
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600

score = [0, 0]
ball_size = 30
player1_hight = 130
player2_hight = 130
player_thickness = 30
border_left_right = 20
game_speed = 5

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

ball = pygame.Rect((WIDTH - ball_size) // 2, (HEIGHT - ball_size) // 2, ball_size, ball_size)
ball_vel = Vector2(random.choice([-1, 1]), 0).rotate(random.uniform(-45, 45)) * game_speed

player1_pos = (HEIGHT - player1_hight) // 2  # Initial position of the square
player2_pos = (HEIGHT - player2_hight) // 2  # Initial position of the square

player1 = pygame.Rect(border_left_right, player1_pos, player_thickness, player1_hight)
player2 = pygame.Rect(WIDTH - border_left_right - player_thickness, player2_pos, player_thickness, player2_hight)

font = pygame.font.SysFont('Courier New', 50, bold=True)

sound_ping = pygame.mixer.Sound("sound/Ping.mp3")
sound_pong = pygame.mixer.Sound("sound/Pong.mp3")
sound_rand = pygame.mixer.Sound("sound/Rand.mp3")
sound_tor = pygame.mixer.Sound("sound/Tor.mp3")

def reset_ball():
    global ball_vel, ball, game_speed
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_vel = Vector2(random.choice([-1, 1]), 0).rotate(random.uniform(-45, 45)) * game_speed
    pygame.time.delay(1000)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    if keys[pygame.K_w] and player1_pos > 0:
        player1_pos -= game_speed
    if keys[pygame.K_s] and player1_pos < HEIGHT - player1_hight:
        player1_pos += game_speed 
    if keys[pygame.K_UP] and player2_pos > 0:
        player2_pos -= game_speed
    if keys[pygame.K_DOWN] and player2_pos < HEIGHT - player2_hight:
        player2_pos += game_speed
    if keys[pygame.K_r]:
        score = [0, 0]
        reset_ball()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_SPACE]:
        reset_ball()

    # Bewegung
    ball.x += ball_vel.x
    ball.y += ball_vel.y

    # Wandkollision oben/unten
    if ball.top <= 0 or ball.bottom >= 600:
        ball_vel = ball_vel.reflect(Vector2(0, 1))
        pygame.mixer.Sound.play(sound_rand)

    # Schlägerkollision
    if ball.colliderect(player1) and ball_vel.x < 0 and ball.left >= player1.right - 10:
        hit_pos = ball.centery - player1.centery
        hit_norm = hit_pos / (player1.height / 2)
        ball_vel = ball_vel.reflect(Vector2(1, 0))
        angle_change = hit_norm * 45
        ball_vel = ball_vel.rotate(angle_change)
        ball_vel = ball_vel.normalize() * game_speed
        pygame.mixer.Sound.play(sound_ping)

    if ball.colliderect(player2) and ball_vel.x > 0 and ball.right <= player2.left + 10:
        hit_pos = ball.centery - player2.centery
        hit_norm = hit_pos / (player2.height / 2)
        ball_vel = ball_vel.reflect(Vector2(-1, 0))
        angle_change = hit_norm * 45
        ball_vel = ball_vel.rotate(-angle_change)
        ball_vel = ball_vel.normalize() * game_speed
        pygame.mixer.Sound.play(sound_pong)
    
    if ball.x < -ball_size:
        score[1] += 1
        pygame.mixer.Sound.play(sound_tor)
        reset_ball()

    if ball.x > WIDTH:
        score[0] += 1
        pygame.mixer.Sound.play(sound_tor)
        reset_ball()

    if game_speed < 15:
        game_speed += 0.001  # Increase game speed over time

    screen.fill((0, 0, 0))  # Fill the screen with black
    score_screen = font.render(f"{score[0]}   {score[1]}", True, (255, 255, 255))
    screen.blit(score_screen, ((WIDTH - score_screen.get_width()) // 2, 20))
    for line in range(0, HEIGHT, HEIGHT // 20):
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, line), (WIDTH // 2, line + HEIGHT // 41), 4)
    player1 = pygame.draw.rect(screen, (255, 255, 255), (border_left_right, player1_pos, player_thickness, player1_hight))
    player2 = pygame.draw.rect(screen, (255, 255, 255), (WIDTH - border_left_right - player_thickness, player2_pos, player_thickness, player2_hight))
    pygame.draw.rect(screen, (255, 255, 255), ball)

    pygame.display.flip()  # Update the display
    clock.tick(60)

pygame.quit()