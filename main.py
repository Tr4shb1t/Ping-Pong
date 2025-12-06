import pygame, random

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
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
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ping Pong")
        self.ball = Ball(self.WIDTH // 2 - self.ball_size // 2, self.HEIGHT // 2 - self.ball_size // 2, self.ball_size, self.game_speed)
        self.player1 = Player(self.border_left_right, self.HEIGHT // 2 - self.player1_hight // 2, self.player_thickness, self.player1_hight, self.HEIGHT, self.player_speed)
        self.player2 = Player(self.WIDTH - self.border_left_right - self.player_thickness, self.HEIGHT // 2 - self.player2_hight // 2, self.player_thickness, self.player2_hight, self.HEIGHT, self.player_speed)
        self.font = pygame.font.SysFont('Courier New', 50, bold=True)
        self.sound_ping = pygame.mixer.Sound("sound/Ping.mp3")
        self.sound_pong = pygame.mixer.Sound("sound/Pong.mp3")
        self.sound_rand = pygame.mixer.Sound("sound/Rand.mp3")
        self.sound_tor = pygame.mixer.Sound("sound/Tor.mp3")

    def eingaben_ausführen(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.move_up()
        if keys[pygame.K_s]:
            self.player1.move_down()
        if keys[pygame.K_UP]:
            self.player2.move_up()
        if keys[pygame.K_DOWN]:
            self.player2.move_down()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if keys[pygame.K_r]:
            self.score = [0, 0]
            self.reset_ball()
        if keys[pygame.K_SPACE]:
            self.reset_ball()

    def zeichnen(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.player1.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.player2.rect)
        pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball.rect)
        for line in range(0, self.HEIGHT, self.HEIGHT // 20):
            pygame.draw.line(self.screen, (255, 255, 255), (self.WIDTH // 2, line), (self.WIDTH // 2, line + self.HEIGHT // 41), 4)
        score_text = self.font.render(f"{self.score[0]}   {self.score[1]}", True, (255, 255, 255))
        self.screen.blit(score_text, ((self.WIDTH - score_text.get_width()) // 2, 20))
        pygame.display.flip()

    def move_ball(self):
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.HEIGHT:
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
            self.reset_ball()
        if self.ball.rect.right >= self.WIDTH:
            self.score[0] += 1
            pygame.mixer.Sound.play(self.sound_tor)
            self.reset_speed()
            self.reset_ball()

    def reset_ball(self):
        self.ball.rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.ball.velocity = pygame.math.Vector2(random.choice([-1, 1]), 0).rotate(random.uniform(-45, 45)) * self.game_speed
        pygame.time.delay(1000)

    def reset_speed(self):
        self.game_speed = 5
        self.player1.speed = 5
        self.player2.speed = 5
    
    def increase_game_speed(self):
        if self.game_speed <= self.max_speed:
            self.game_speed += 0.002
            self.player1.speed += 0.002
            self.player2.speed += 0.002

class Player:
    def __init__(self, x, y, width, height, max_y, speed = 5):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.max_y = max_y

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < self.max_y:
            self.rect.y += self.speed

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
        spiel.eingaben_ausführen()
        spiel.move_ball()
        spiel.zeichnen()
        spiel.increase_game_speed()
        spiel.clock.tick(60)