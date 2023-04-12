import pygame

pygame.init()

# générer la fenetre de notre jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080, 720))


background = pygame.image.load('Asset/bg.jpg')

running = True

# boucle tant que cette condition est vrai
while running == True :

    
    screen.blit(background, (0, -200))

    pygame.display.flip()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

