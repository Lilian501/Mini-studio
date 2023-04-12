import pygame

pygame.init()

#creer une classe qui va representer notre jeu

class Game:

    def __init__(self):
        #générer notre joueur

        self.player = Player()
        self.pressed = {
            
        }



#creer une premiere classe qui va representer le joueur

class Player (pygame.sprite.Sprite) :    
    def __init__ (self):
        self.image = pygame.image.load("Asset/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

        self.velocity = 1
        self.attack = 10
        self.attack_speed = 1
        self.hp = 10
        self.shooting_mode = "normal"

    def moove_down(self):
        self.rect.y += self.velocity

    def moove_up (self) :
        self.rect.y -= self.velocity
    
    def moove_left (self) :
        self.rect.x = self.rect.x - self.velocity

    def moove_right (self) :
        self.rect.x += self.velocity 

    

# générer la fenetre de notre jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080, 720))

#importer l'arriere plan de notre jeu
background = pygame.image.load('Asset/bg.jpg')

# charger notre joueur
player = Player()

#charger notre jeu
game = Game()
running = True

# boucle tant que cette condition est vrai
while running == True :

    #appliquer l'arriere plan de notre jeu
    screen.blit(background, (0, -200))

    #appliquer l'image de mon joueur
    screen.blit(game.player.image, game.player.rect)

    #verifier si le joueur souhaite aller à gauche ou à droite
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width< screen.get_width():
        game.player.moove_right()

    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.moove_left()

    elif game.pressed.get(pygame.K_UP) and game.player.rect.y > 0:
        game.player.moove_up()

    elif game.pressed.get(pygame.K_DOWN) and game.player.rect.y + game.player.rect.width< 720:
        game.player.moove_down()

    print(game.player.rect.y)

    #mettre à jour l'écran
    pygame.display.flip()
    
    #si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # que l'evenement est fermeture de la fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # detecter si un joueur lache une touche du clavier

        elif event.type == pygame.KEYDOWN:

            game.pressed[event.key] = True

        elif event.type == pygame.KEYUP:

            game.pressed[event.key] = False

            

