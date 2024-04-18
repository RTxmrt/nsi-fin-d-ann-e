import pygame
pygame.init()
pygame.display.set_caption("Projet final")
surface = pygame.display.set_mode((720, 480))
background = pygame.image.load("plage.webp")

running = True

while running:
    
    surface.blit(background, (0, 0))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fenetre fermée")
