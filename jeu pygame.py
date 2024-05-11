import pygame
import math
import random
pygame.init()

class Game:
    def __init__(self):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = player(self)
        self.all_players.add(self.player)
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False
    def update(self, surface):
        surface.blit(self.player.image, self.player.rect)

        self.player.update_health_bar(surface)

        for projectile in self.player.all_projectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(surface)

        self.player.all_projectiles.draw(surface)

        self.all_monsters.draw(surface)

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < surface.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)
class player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 200
        self.max_health = 200
        self.attack = 10
        self.velocity = 2
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('stickman.png')
        self.image = pygame.transform.scale(self.image, (225, 235))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 470

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            self.game.game_over()
    def update_health_bar(self, surface):
        bar_color = (100, 164, 60)
        back_bar_color = (60, 63, 60)
        bar_position = [self.rect.x + 10, self.rect.y -20, self.health, 5]
        back_bar_position = [self.rect.x + 10, self.rect.y -20, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('glace3.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 4
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    def remove(self):
        self.player.all_projectiles.remove(self)
    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)
        if self.rect.x > 1080:
            self.remove()

class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.5
        self.image = pygame.image.load('traveler.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (220, 220))
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 483
        self.velocity = random.randint(1, 2)

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, 3)
            self.health = self.max_health

    def update_health_bar(self, surface):
        bar_color = (100, 164, 60)
        back_bar_color = (60, 63, 60)
        bar_position = [self.rect.x + 10, self.rect.y -20, self.health, 5]
        back_bar_position = [self.rect.x + 10, self.rect.y -20, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)


pygame.init()
pygame.display.set_caption("Projet final")
surface = pygame.display.set_mode((1080, 720))

background = pygame.image.load("plage.jpg")
background = pygame.transform.scale(background, (1080, 720))

banner = pygame.image.load("plagebanniere.jpg")
banner = pygame.transform.scale(banner, (900, 350))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(surface.get_width() / 10)
banner_rect.y = math.ceil(surface.get_width() / 10)

play_button = pygame.image.load("play.png")
play_button = pygame.transform.scale(play_button, (450, 450))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(surface.get_width() / 3.33)
play_button_rect.y = math.ceil(surface.get_width() / 4)

game = Game()


running = True

while running:

    surface.blit(background, (0, 0))

    print(game.player.rect.x)

    if game.is_playing:
        game.update(surface)
    else:
        surface.blit(banner, banner_rect)
        surface.blit(play_button, play_button_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fenetre fermée")
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()
