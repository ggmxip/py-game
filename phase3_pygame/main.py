import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 22)
big_font = pygame.font.SysFont("monospace", 36)

WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.w = 40
        self.h = 30
        self.speed = 5
        self.hp = 3
        self.last_shot = 0
        self.shoot_delay = 250

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.w:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.h:
            self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.w, self.h))
        pygame.draw.polygon(screen, GREEN, [
            (self.x + self.w // 2, self.y - 10),
            (self.x + 5, self.y),
            (self.x + self.w - 5, self.y),
        ])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 12
        self.speed = 8

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.w, self.h))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Enemy:
    def __init__(self):
        self.w = 30
        self.h = 30
        self.x = random.randint(0, WIDTH - self.w)
        self.y = -self.h
        self.speed = random.randint(2, 5)
        self.hp = 1

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Game:
    def __init__(self):
        self.state = "menu"
        self.reset()

    def reset(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_delay = 30
        self.enemy_speed = 2

    def spawn_enemy(self):
        e = Enemy()
        e.speed = random.randint(self.enemy_speed, self.enemy_speed + 3)
        self.enemies.append(e)

    def run(self):
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.state == "menu" and event.key == pygame.K_SPACE:
                        self.state = "playing"
                        self.reset()
                    elif self.state == "gameover" and event.key == pygame.K_SPACE:
                        self.state = "menu"

            if self.state == "playing":
                self.update()

            self.draw()
            pygame.display.flip()
        pygame.quit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.player.last_shot > self.player.shoot_delay:
            self.bullets.append(Bullet(self.player.x + self.player.w // 2 - 2, self.player.y - 10))
            self.player.last_shot = now

        for b in self.bullets[:]:
            b.update()
            if b.y + b.h < 0:
                self.bullets.remove(b)

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0
            self.spawn_delay = max(10, self.spawn_delay - 0.5)

        for e in self.enemies[:]:
            e.update()
            if e.y > HEIGHT:
                self.enemies.remove(e)
                continue
            for b in self.bullets[:]:
                if e.rect().colliderect(b.rect()):
                    self.enemies.remove(e)
                    self.bullets.remove(b)
                    self.score += 10
                    break
            if e in self.enemies and e.rect().colliderect(self.player.rect()):
                self.enemies.remove(e)
                self.player.hp -= 1
                if self.player.hp <= 0:
                    self.state = "gameover"

    def draw(self):
        screen.fill(BLACK)
        if self.state == "menu":
            t = big_font.render("SPACE SHOOTER", True, WHITE)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 3))
            t2 = font.render("Press SPACE to play", True, WHITE)
            screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2))
        elif self.state == "playing":
            self.player.draw()
            for b in self.bullets:
                b.draw()
            for e in self.enemies:
                e.draw()
            score_text = font.render(f"Score: {self.score}  HP: {self.player.hp}", True, WHITE)
            screen.blit(score_text, (10, 10))
        elif self.state == "gameover":
            t = big_font.render("GAME OVER", True, RED)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 3))
            s = big_font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2))
            t2 = font.render("Press SPACE to continue", True, WHITE)
            screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 50))


if __name__ == "__main__":
    Game().run()