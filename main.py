import pygame
from random import randint
from monster import Monster

pygame.init()
######################################################################## Class ##################################################################################################################################
#création de l'objet Obstacle
class Obstacle (pygame.sprite.Sprite):

    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        # mise en place des informations 
        self.game = game
        self.obstacle_number = randint (1,1)
        self.text = "img/image_obstacle_" + str(self.obstacle_number)  # initialisation 
        print(self.text)
        self.image = pygame.image.load(self.text +".png") # l'image de l'obstacle dépend du background
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect() #on définit la taille de l'obstacle (rectangle de longueur x et largeur y)
        self.rect.x = 1080
        self.rect.y = randint(0,712)

        self.velocity = self.game.player.velocity # augemente avec celle du joueur / distance
        self.elemental = randint(0,1) # choisit aléatoirement si l'obstacle est infusé par une élément ou non
        self.element = "neutral" #dans tous les cas l'élément de base est neutre / "neutral"
        if self.elemental == 1: # si l'obstacle est infusé par un élément
            self.elementalForm() # alors on le modifie pour mettre en place l'infusion
    
    def elementalForm(self):
        element = randint(2,2) #l'élément infusé est choisi aléatoirement entre les 4 éléments
        if element == 1 :
            self.element = "air"
             
        elif element == 2 :
            self.element = "fire"
        
        elif element == 3 :
            self.element = "earth"
        
        elif element == 4 :
            self.element = "water"

        self.text += "_" + self.element
        print(self.text) 
        self.image = pygame.image.load(self.text + ".png") # chargement de l'image de tel obstacle infusé par tel élément
        self.image = pygame.transform.scale(self.image, (32, 32))

    def forward(self):
        #le déplacement se fait que si il n'y a pas de collision
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
    


class Game (object):

    def __init__(self):

        #définir si note jeu a commencé ou non
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
       
        self.all_players.add(self.player)
        self.all_monsters = pygame.sprite.Group()
        self.spawn_monster()
        self.spawn_monster()
        self.all_players.add(self.player)
        self.all_obstacles = pygame.sprite.Group()
        self.spawn_obstacle()
        self.distance = 0
        self.distanceScore = 0
        self.totalScore = 0
        
        #stocker les touches activées par le joueur 
        self.pressed = {}


    

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)

    def spawn_obstacle(self):
        obstacle = Obstacle(self)
        self.all_obstacles.add(obstacle)


#Classe du joueur principal
class Player (pygame.sprite.Sprite):    
    
    def __init__ (self, game):
        super().__init__()
        self.game = game
        '''Methode d'initialisation'''
        self.image = pygame.image.load("img/wazo.png")
        self.rect = self.image.get_rect()
        self.rect.x = 8
        self.rect.y = 8
        self.health = 5

        self.velocity = 6 #vitesse du joueur
        self.attack = 10 #points d'attaque du joueur
        self.attack_speed = 1
        self.hp = 10
        self.shootingMode = "normal"
        self.all_projectiles = pygame.sprite.Group()





    def damage(self, amount):
 
        self.health -= amount
        if self.health <=0 :
            print("yo")

    def launch_projectile(self):
        # créer une nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectile(self))


    def moveDown(self):
        self.rect.y = self.rect.y + self.velocity

    def moveUp (self) :
        self.rect.y = self.rect.y - self.velocity 
    
    def moveLeft (self) :
        self.rect.x = self.rect.x - self.velocity

    def moveRight (self) :
        #si le joueur n'est pas en collision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity 



# définir la classe qui va gérer le projectile de notre joueur 
class Projectile(pygame.sprite.Sprite):

    #définir le constructeur de cette classe
    def __init__(self, player):
        super().__init__()
        self.game = game
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('img/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 100
        self.rect.y = player.rect.y + 25



    def remove(self):
        self.player.all_projectiles.remove(self)


    def move(self):
        self.rect.x += self.velocity

        #vérifier si le projectile touche un ennemni
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(5)

        for _ in self.game.check_collision(self, self.game.all_obstacles) :
            self.remove()

        #vérifier si le projectile n'est plus dans l'écran
        if self.rect.x > 1080:
            #supprimer le projectile
            self.remove()
            

######################################################################## Fonctions ##################################################################################################################################

def blitage () :
    '''fonction qui blit tout ce qu'il faut afficher, il faut mettre dans l'ordre d'affichage du plus au fond au plus devant'''
    screen.blit(background, (0-imageCount, 0))
    screen.blit(background, (1080-imageCount, 0))
    screen.blit(game.player.image, game.player.rect)


def collider (objectA,objectB) :
    '''Fonction qui va renvoyer true si une collision est detectée entre l'objet A et B'''
    if objectA.x < objectB.x + objectB.w and objectA.x + objectA.w > objectB.x and objectA.y < objectB.y + objectB.h and objectA.h + objectA.y > objectB.y :
        return True
    
def settings () :
  '''Fonction qui ouvre les settings'''
  s = pygame.Surface((1080,720)) 
  s.set_alpha(128)                
  s.fill((0,0,0)) 
  pause = pygame.image.load('img/pause.png')
  while True :
    blitage()
    screen.blit(s, (0,0)) 
    screen.blit(pause, (50,200))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:

              return  
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False


# générer la fenetre de notre jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080, 720))

#Génération de toutes les images de fond
background = pygame.image.load('img/fond.png')
background = pygame.transform.scale(background, (1080, 720)) #On redimensionne l'image de fond (pas nécéssaire si l'image est déja dans les bonnes dims)

#importer charger notre bannière
banner = pygame.image.load('Asset/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = screen.get_width() / 4

#charger notre bouton
play_button = pygame.image.load('Asset/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen.get_width() / 3.33
play_button_rect.y = screen.get_height() / 2


game = Game()
running = True



myFont = pygame.font.SysFont('arial', 18) #Pour mettre une font et print une variable
FPS = 100
fpsClock = pygame.time.Clock()
imageCount = 0 #compteur qui va servir à faire défiler les images
speed = 3 #Vitesse globale du jeu

######################################################################## Boucle Principale ################################################################################################################

while running == True :

    

    

    #vérifier si le jeu à commencé
    if game.is_playing:
        blitage()

        distance = myFont.render(str(game.distance), 1, (255,255,255))
        score = myFont.render(str(game.totalScore), 1, (255,255,255))
        fps = myFont.render(str(FPS), 1, (255,255,255))
        screen.blit(distance, (520, 30))
        screen.blit(score, (520, 60))
        screen.blit(fps, (1040, 10))

        for obstacle in game.all_obstacles:
            obstacle.forward()


        #récupérer les projectiles du joueur
        for projectile in game.player.all_projectiles:
            projectile.move()

        #recupérer les monstres de notre jeu
        for monster in game.all_monsters:
            monster.forward()


        #appliquer les images de mon groupe de projectiles
        game.player.all_projectiles.draw(screen)

        game.all_obstacles.draw(screen)

        #appliquer l'ensemble des images de mon groupe de monstres
        game.all_monsters.draw(screen)

        if game.pressed.get(pygame.K_UP) and game.player.rect.y > 0 :
            game.player.moveUp()

        if game.pressed.get(pygame.K_DOWN) and game.player.rect.y + game.player.rect.width < screen.get_height() :
            game.player.moveDown()

        if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
            game.player.moveLeft()

        if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
            game.player.moveRight()
        
        


    #vérifier si le jeu n'a pas commencé
    else :
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
        
        


    

    #print(game.player.rect.y)
    
    

    imageCount = imageCount + speed
    if imageCount >= 1080:
        imageCount = 0

    print(game.player.health)

    #Tentative d'animation sur l'oiseau, marche à moitié
    #if globalCount == 0 :
    #    if game.player.image == tabAnimWazo[0]:
    #        game.player.image.blit(tabAnimWazo[1],(game.player.rect.x,game.player.rect.y))
            #game.player.image = tabAnimWazo[1]
    #    else : 
    #        game.player.image.blit(tabAnimWazo[0],(game.player.rect.x,game.player.rect.y))
            #game.player.image = tabAnimWazo[0]

    #Ca print du texte 
    

    pygame.display.flip()
    
    fpsClock.tick(FPS)

    lastDistance = game.distanceScore 

    game.distance = game.distance + 1 

    game.distanceScore = int(game.distance/10)

    game.totalScore = game.totalScore + (game.distanceScore - lastDistance)

    if game.distance > 100:
        if game.totalScore % 1000 == 0:
            if speed < 50 :
                speed += 1
    
    #print(speed) 
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit() 
    
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True


            #détecter si la touche espace est enclenchée pour lancer notre projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()
            
            if event.key == pygame.K_ESCAPE:
                settings()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN :
            #vérification si la souris touche le bouton
            if play_button_rect.collidepoint(event.pos):
                #lancer le jeu
                game.is_playing = True