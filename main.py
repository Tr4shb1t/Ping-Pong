import pygame, random

class PongGame:
    def __init__(self, color=(255, 255, 255)):
        pygame.init()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 600
        self.color = color
        self.score = [0, 0]
        self.ball_size = 30
        self.player1_hight = 130
        self.player2_hight = 130
        self.player_thickness = 30
        self.border_left_right = 20
        self.game_speed = 5
        self.player_speed = 5
        self.max_speed = 20
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Ping Pong")
        self.ball = Ball(self.WINDOW_WIDTH // 2 - self.ball_size // 2, self.WINDOW_HEIGHT // 2 - self.ball_size // 2, self.ball_size, self.game_speed)
        self.player1 = Player(self.border_left_right, self.WINDOW_HEIGHT // 2 - self.player1_hight // 2, self.player_thickness, self.player1_hight, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.player_speed)
        self.player2 = Player(self.WINDOW_WIDTH - self.border_left_right - self.player_thickness, self.WINDOW_HEIGHT // 2 - self.player2_hight // 2, self.player_thickness, self.player2_hight, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.player_speed)
        self.font = pygame.font.SysFont('Arial', 70, bold=True)
        self.sound_ping = pygame.mixer.Sound("sound/Ping.mp3")
        self.sound_pong = pygame.mixer.Sound("sound/Pong.mp3")
        self.sound_rand = pygame.mixer.Sound("sound/Rand.mp3")
        self.sound_tor = pygame.mixer.Sound("sound/Tor.mp3")
        self.crazy = False

    def randomize_colors(self):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color

    def eingaben_ausführen(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.move_up()
        if keys[pygame.K_s]:
            self.player1.move_down()
        if keys[pygame.K_a] and self.crazy:
            self.player1.move_left()
        if keys[pygame.K_d] and self.crazy:
            self.player1.move_right()
        if keys[pygame.K_UP]:
            self.player2.move_up()
        if keys[pygame.K_DOWN]:
            self.player2.move_down()
        if keys[pygame.K_LEFT] and self.crazy:
            self.player2.move_left()
        if keys[pygame.K_RIGHT] and self.crazy:
            self.player2.move_right()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if keys[pygame.K_r]:
            self.reset_game()
        if keys[pygame.K_SPACE]:
            self.reset_ball_and_player()
        if keys[pygame.K_z] and not self.crazy:
            self.crazy = True

    def zeichnen(self):
        if self.crazy:
            self.color = self.randomize_colors()
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.color, self.player1.rect)
        pygame.draw.rect(self.screen, self.color, self.player2.rect)
        pygame.draw.rect(self.screen, self.color, self.ball.rect)
        for line in range(0, self.WINDOW_HEIGHT, self.WINDOW_HEIGHT // 20):
            pygame.draw.line(self.screen, self.color, (self.WINDOW_WIDTH // 2, line), (self.WINDOW_WIDTH // 2, line + self.WINDOW_HEIGHT // 41), 4)
        score_text = self.font.render(f"{self.score[0]}   {self.score[1]}", True, self.color)
        self.screen.blit(score_text, ((self.WINDOW_WIDTH - score_text.get_width()) // 2, 20))
        pygame.display.flip()

    def check_angle(self, vector):
        if vector.x < 0:
            vector = vector.reflect(pygame.math.Vector2(1, 0))
        angle = vector.angle_to(pygame.math.Vector2())
        return angle

    def move_ball(self):
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.WINDOW_HEIGHT:
            self.ball.velocity = self.ball.velocity.reflect(pygame.math.Vector2(0, 1))
            pygame.mixer.Sound.play(self.sound_rand)
        self.ball.rect.x += self.ball.velocity.x
        self.ball.rect.y += self.ball.velocity.y
        if self.ball.rect.colliderect(self.player1.rect) and self.ball.velocity.x < 0 and self.ball.rect.left >= self.player1.rect.right - 10:
            hit_pos = self.ball.rect.centery - self.player1.rect.centery
            hit_norm = hit_pos / (self.player1.rect.height / 2)
            self.ball.velocity = self.ball.velocity.reflect(pygame.math.Vector2(1, 0))
            angle_change = hit_norm * 45
            self.ball.velocity = self.ball.velocity.rotate(angle_change)
            self.ball.velocity = self.ball.velocity.normalize() * self.game_speed
            pygame.mixer.Sound.play(self.sound_ping)
        if self.ball.rect.colliderect(self.player2.rect) and self.ball.velocity.x > 0 and self.ball.rect.right <= self.player2.rect.left + 10:
            hit_pos = self.ball.rect.centery - self.player2.rect.centery
            hit_norm = hit_pos / (self.player2.rect.height / 2)
            self.ball.velocity = self.ball.velocity.reflect(pygame.math.Vector2(-1, 0))
            angle_change = hit_norm * 45
            self.ball.velocity = self.ball.velocity.rotate(-angle_change)
            self.ball.velocity = self.ball.velocity.normalize() * self.game_speed
            pygame.mixer.Sound.play(self.sound_pong)
        if self.ball.rect.left <= 0:
            self.score[1] += 1
            pygame.mixer.Sound.play(self.sound_tor)
            self.reset_speed()
            self.reset_ball_and_player()
        if self.ball.rect.right >= self.WINDOW_WIDTH:
            self.score[0] += 1
            pygame.mixer.Sound.play(self.sound_tor)
            self.reset_speed()
            self.reset_ball_and_player()

    def reset_ball_and_player(self):
        self.ball.rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        self.ball.velocity = pygame.math.Vector2(random.choice([-1, 1]), 0).rotate(random.uniform(-45, 45)) * self.game_speed
        self.player1.rect.y = self.WINDOW_HEIGHT // 2 - self.player1_hight // 2
        self.player2.rect.y = self.WINDOW_HEIGHT // 2 - self.player2_hight // 2
        self.player1.rect.x = self.border_left_right
        self.player2.rect.x = self.WINDOW_WIDTH - self.border_left_right - self.player_thickness

    def reset_speed(self):
        self.game_speed = 5
        self.player1.speed = 5
        self.player2.speed = 5

    def reset_game(self):
        self.crazy = False
        self.score = [0, 0]
        self.reset_speed()
        self.reset_ball_and_player()
        self.zeichnen()
        pygame.time.delay(1000)
    
    def increase_game_speed(self):
        if self.game_speed <= self.max_speed:
            self.game_speed += 0.002
            self.player1.speed += 0.002
            self.player2.speed += 0.002

    def pause_game(self):
        paused = True
        pause_font = pygame.font.SysFont('Arial', 100, bold=True)
        pause_text = pause_font.render("PAUSED", True, self.color)
        self.screen.blit(pause_text, ((self.WINDOW_WIDTH - pause_text.get_width()) // 2, (self.WINDOW_HEIGHT - pause_text.get_height()) // 2))
        pygame.display.flip()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                self.clock.tick(15)

class Player:
    def __init__(self, x, y, width, height, max_x, max_y, speed = 5):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.max_y = max_y
        self.max_x = max_x

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < self.max_y:
            self.rect.y += self.speed

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed
    
    def move_right(self):
        if self.rect.right < self.max_x:
            self.rect.x += self.speed

class Ball:
    def __init__(self, x, y, size, speed = 5):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.velocity = pygame.math.Vector2(random.choice([-1, 1]), 0).rotate(random.uniform(-45, 45)) * speed

if __name__ == "__main__":
    spiel = PongGame()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    spiel.pause_game()
        spiel.eingaben_ausführen()
        spiel.move_ball()
        spiel.zeichnen()
        spiel.increase_game_speed()
        spiel.clock.tick(60)