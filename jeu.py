import pygame

#oui bonjour
pygame.init()
from monster import Monster
#creer une classe qui va representer notre jeu

class Game:

    def __init__(self):
        #générer notre joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}
        self.spawn_monster()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)



#creer une premiere classe qui va representer le joueur

class Player (pygame.sprite.Sprite) :    
    def __init__ (self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("Asset/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

        self.velocity = 1
        self.attack = 10
        self.attack_speed = 1
        self.hp = 10
        self.shooting_mode = "normal"
        self.all_projectiles = pygame.sprite.Group()

    def launch_projectile(self):
        # créer une nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectile(self))

    def moove_down(self):
        self.rect.y += self.velocity

    def moove_up (self) :
        self.rect.y -= self.velocity
    
    def moove_left (self) :
        self.rect.x = self.rect.x - self.velocity

    def moove_right (self) :
        #si le joueur n'est pas en collision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity 

    



# définir la classe qui va gérer le projectile de notre joueur 
class Projectile(pygame.sprite.Sprite):

    #définir le constructeur de cette classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 1
        self.player = player
        self.image = pygame.image.load('Asset/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x+180
        self.rect.y = player.rect.y +100



    def remove(self):
        self.player.all_projectiles.remove(self)


    def move(self):
        self.rect.x += self.velocity

        #vérifier si le projectile touche un ennemni
        if self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()

        #vérifier si le projectile n'est plus dans l'écran
        if self.rect.x > 1080:
            #supprimer le projectile
            self.remove()
            



# générer la fenetre de notre jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080, 720))

#importer l'arriere plan de notre jeu
background = pygame.image.load('Asset/bg.jpg')




#charger notre jeu
game = Game()
running = True

# boucle tant que cette condition est vrai
while running == True :

    #appliquer l'arriere plan de notre jeu
    screen.blit(background, (0, -200))

    #appliquer l'image de mon joueur
    screen.blit(game.player.image, game.player.rect)

    #récupérer les projectiles du joueur
    for projectile in game.player.all_projectiles:
        projectile.move()

    #recupérer les monstres de notre jeu
    for monster in game.all_monsters:
        monster.forward()

    #appliquer les images de mon groupe de projectiles
    game.player.all_projectiles.draw(screen)

    #appliquer l'ensemble des images de mon groupe de monstres
    game.all_monsters.draw(screen)

    #verifier si le joueur souhaite aller à gauche ou à droite
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width< screen.get_width():
        game.player.moove_right()

    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.moove_left()

    if game.pressed.get(pygame.K_UP) and game.player.rect.y > 0:
        game.player.moove_up()

    if game.pressed.get(pygame.K_DOWN) and game.player.rect.y + game.player.rect.width< 720:
        game.player.moove_down()

    

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

            #détecter si la touche espace est enclenchée pour lancer notre projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:

            game.pressed[event.key] = False

            

