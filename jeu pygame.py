import pygame
pygame.init()

class Game:
    def __init__(self):
        self.player = player(self)
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}
        self.spawn_monster()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    def spawn_monster(self):
        monster = Monster()
        self.all_monsters.add(monster)
class player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 2
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('stickman.png')
        self.image = pygame.transform.scale(self.image, (225, 235))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 470

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
        self.velocity = 2
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
        if self.rect.x > 1080:
            self.remove()

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.image = pygame.image.load('traveler.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect.x = 1000
        self.rect.y = 500
        self.velocity = 2
    def forward(self):
        self.rect.x -= self.velocity


pygame.init()
pygame.display.set_caption("Projet final")
surface = pygame.display.set_mode((1080, 720))

background = pygame.image.load("plage.jpg")
background = pygame.transform.scale(background, (1080, 720))

game = Game()


running = True

while running:

    surface.blit(background, (0, 0))
    surface.blit(game.player.image, game.player.rect)
    for projectile in game.player.all_projectiles:
        projectile.move()
    for monster in game.all_monsters:
        monster.forward()
    game.player.all_projectiles.draw(surface)

    game.all_monsters.draw(surface)


    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < surface.get_width():
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()
    print(game.player.rect.x)

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
