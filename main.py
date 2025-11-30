import pygame

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

y1 = height // 2  # Initial position of the square
y2 = height // 2  # Initial position of the square
run = True
while run:
    pygame.time.delay(20)  # Delay to control frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

    if keys[pygame.K_w]:
        if y2 > 0:
            y2 -= 5
    if keys[pygame.K_s]:
        if y2 < height - 130:
            y2 += 5 
    if keys[pygame.K_UP]:
        if y1 > 0:
            y1 -= 5
    if keys[pygame.K_DOWN]:
        if y1 < height - 130:
            y1 += 5

    screen.fill((0, 0, 0))  # Fill the screen with black

    pygame.draw.rect(screen, (255, 255, 255), (20, y1, 30, 130))  # Draw a red square
    pygame.draw.rect(screen, (255, 255, 255), (750, y2, 30, 130))  # Draw a blue square
    pygame.display.flip()  # Update the display

pygame.quit()