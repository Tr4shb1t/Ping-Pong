import pygame, random

pygame.init()

# Set up display
width, height = 800, 600
score = [0, 0]
ball_size = 30
player1_barsize = 130
player2_barsize = 130
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

player1_pos = (height - player1_barsize) // 2  # Initial position of the square
player2_pos = (height - player2_barsize) // 2  # Initial position of the square

ball_pos_x = (width - ball_size) // 2 # Initial position of the ball
ball_pos_y = (height - ball_size) // 2

ball_direction_x = random.choice([-4, 4])
ball_direction_y = random.choice([-4, 4])

pygame.font.init()
font = pygame.font.SysFont('Courier New', 30)

run = True
while run:
    pygame.time.delay(15)  # Delay to control frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ball_pos_x += ball_direction_x
    ball_pos_y += ball_direction_y
    if ball_pos_y <= 0 or ball_pos_y >= height - ball_size:
        ball_direction_y = -ball_direction_y
    if ball_pos_x <= 50:
        if ball_pos_x <= 40:
            pass
        elif player1_pos < ball_pos_y + ball_size and player1_pos + player1_barsize > ball_pos_y:
            ball_direction_x = -ball_direction_x
    if ball_pos_x >= width - 50 - ball_size:
        if ball_pos_x >= width - 40 - ball_size:
            pass
        elif player2_pos < ball_pos_y + ball_size and player2_pos + player2_barsize > ball_pos_y:
            ball_direction_x = -ball_direction_x
    
    if ball_pos_x < -ball_size - 10 or ball_pos_x > width + 10:
        ball_pos_x = (width - ball_size) // 2
        ball_pos_y = (height - ball_size) // 2
        ball_direction_x = random.choice([-4, 4])
        ball_direction_y = random.choice([-4, 4])

    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    if keys[pygame.K_w]:
        if player1_pos > 0:
            player1_pos -= 5
    if keys[pygame.K_s]:
        if player1_pos < height - player1_barsize:
            player1_pos += 5 
    if keys[pygame.K_UP]:
        if player2_pos > 0:
            player2_pos -= 5
    if keys[pygame.K_DOWN]:
        if player2_pos < height - player2_barsize:
            player2_pos += 5

    screen.fill((0, 0, 0))  # Fill the screen with black

    pygame.draw.line(screen, (255, 255, 255), (width // 2, 0), (width // 2, height), 5)  # Draw the center line
    pygame.draw.rect(screen, (255, 255, 255), (20, player1_pos, 30, 130))
    pygame.draw.rect(screen, (255, 255, 255), (750, player2_pos, 30, 130))
    
    pygame.draw.rect(screen, (255, 255, 255), (ball_pos_x, ball_pos_y, ball_size, ball_size))  # Draw the ball
    
    pygame.display.flip()  # Update the display

pygame.quit()