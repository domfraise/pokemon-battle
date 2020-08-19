

import pygame, sys, random
from pygame.locals import *


pygame.init()
screen_width = 640*2
screen_height = 360*2
screen=pygame.display.set_mode((screen_width,screen_height))   #set window size
pygame.display.set_caption("Pokemon")#set caption

clock = pygame.time.Clock()
font = pygame.font.Font(None,25)

class Pokemon():
    def __init__(self,poke_num,friendly=True):
        self.size = [400,400]
        self.x_speed = 0
        self.y_speed = 0
        self.friendly_pos = [-self.size[0],160] #position of your pokeon @ start #100,200 is fighting pos
        self.friendly_fight_pos =[100,160]
        self.enemy_pos = [screen_width,0]
        self.enemy_fight_pos =  [780,0]
        self.base_health = 100
        self.health = self.base_health
        self.image_friendly = pygame.image.load("bpkm"+str(poke_num)+".png")
        self.image_friendly = pygame.transform.scale(self.image_friendly,self.size)
        self.image_enemy = pygame.image.load("pkm"+str(poke_num)+".png")
        self.image_enemy = pygame.transform.scale(self.image_enemy,self.size)
        
    def appear_left(self): #speeds for appearance on screen
        if self.friendly_pos[0] <100: #move in from left at
            self.x_speed = 10
        elif self.friendly_pos[0] == 100:
            self.x_speed = 0
            return True
            
    def appear_right(self):
        if self.enemy_pos[0] > 800:
            self.x_speed = -10
        elif self.enemy_pos[0] <= 800:
            self.x_speed == 0
            return True
                                  
    def attack_enemy(self):
    #sets animation speeds for attack
        if self.enemy_pos == self.enemy_fight_pos and self.x_speed != 10:
            self.x_speed = -10
            self.y_speed = 10
        elif self.enemy_pos[0] <=730: # 730 being the x coordinate where pokemone directiron switches
            self.x_speed = 10
            self.y_speed = -10
        elif self.enemy_pos == self.enemy_fight_pos and self.x_speed == 10:  #checks to see if back to origonal pos [680,0]
            self.x_speed = 0                                    #sets speeds to zero
            self.y_speed = 0            
            return True
            
    def attack_friendly(self):
        """sets animation speeds for attack"""
        if self.friendly_pos == self.friendly_fight_pos and self.x_speed != -10:
            self.x_speed = 10
            self.y_speed = -10
        elif self.friendly_pos[0] >=150: #150 being when diriction switches
            self.x_speed = -10
            self.y_speed = 10
        elif self.friendly_pos == self.friendly_fight_pos and self.x_speed == -10:
            self.x_speed = 0
            self.y_speed = 0
            return True
            
    def move_friendly(self):
        """animation speeds for appearance"""
        self.friendly_pos[0]+=self.x_speed
        self.friendly_pos[1]+=self.y_speed
        
    def move_enemy(self):
        self.enemy_pos[0]+=self.x_speed
        self.enemy_pos[1]+=self.y_speed
        

def blit_background():
    background = pygame.image.load("battlebackground.jpeg")
    background = pygame.transform.smoothscale(background,(screen_width,screen_height))
    screen.blit(background,(0,0))
    background_color = background.get_at((50,550)) #colour of background to text for seethrough Rects
    return background,background_color
    
def blit_image(File,size,pos):
    image = pygame.image.load(File)
    image = pygame.transform.smoothscale(image,size)
    screen.blit(image,pos)  
    
def blit_friendly(friendly):
    screen.blit(friendly.image_friendly,friendly.friendly_pos)
    
def blit_enemy(enemy):
    screen.blit(enemy.image_enemy,enemy.enemy_pos)
    
def blit_text(text,pos,color = (250,250,250),font_size = 40):
    font = pygame.font.Font("Minecraft.ttf",font_size) 
    text = font.render(text,1,(color)) 
    screen.blit(text,pos)
    return
    
def blit_health(friendly,enemy):
    red = (250,0,0)
    yellow = (250,250,0)
    green = (0,250,0)
    blit_text("HP "+str(enemy.health)+"/"+str(enemy.base_health),(400,177),red,20) # shows  text of total health vs max health
    blit_text("HP "+str(friendly.health)+"/"+str(friendly.base_health),(782,452),red,20)
    
    if friendly.health >=50:
        pygame.draw.rect(screen,green,(909,453,380*friendly.health/100,15))  #380 = no of pixels for full health bar
    elif friendly.health >= 20:     #and friendly.health <50                       # /100 to normilise the health #can be replaced with base_health
        pygame.draw.rect(screen,yellow,(909,453,380*friendly.health/100,15))  #(x pos, y pos, width, height)
    elif friendly.health <20 :
        pygame.draw.rect(screen,red,(909,453,380*friendly.health/100,15))
    if enemy.health >=50:
        pygame.draw.rect(screen,green,(0,177,380*enemy.health/100,15))      #enemy health calculation for correct colour
    elif enemy.health >= 20 :
        pygame.draw.rect(screen,yellow,(0,177,380*enemy.health/100,15))   
    elif enemy.health <20 :
        pygame.draw.rect(screen,red,(0,177,380*enemy.health/100,15))
           
def event_check(just_quit=True,friendly = None,enemy = None):
    if just_quit == True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()              
    if just_quit == False:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        friendly_turn(friendly,enemy)
                
def get_click():
    click_states = pygame.mouse.get_pressed()
    if click_states[0]:
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos
    else:
        return(0,0)
        
def choose_option(friendly,enemy,opt1="Fight",opt2="Bag",opt3="Pokemon",opt4 = "Run"):
    """boxs and clicking detection for menus"""
    background_color = blit_background()[1]
    blit_friendly(friendly)
    blit_enemy(enemy)
    blit_health(friendly,enemy)
    pygame.display.update()
    pause(friendly,enemy,3) #to stop the click from 1st menu selecting option in second
    mouse_pos = 0,0
    while True:
        event_check(False, friendly,enemy)
        blit_background()
        opt_1 = pygame.draw.rect(screen,((background_color)),(60,540,300,70))
        blit_text(opt1,(70,545))
        opt_3 = pygame.draw.rect(screen,(background_color),(60,615,300,70))
        blit_text(opt2,(70,620))
        opt_2 = pygame.draw.rect(screen,(background_color),(360,540,300,70))
        blit_text(opt3,(370,545))
        opt_4 = pygame.draw.rect(screen,(background_color),(360,615,300,70))
        blit_text(opt4,(370,620))
        mouse_pos = get_click()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_text("What will you do?",(800,580))
        pygame.display.update()
        if opt_1.collidepoint(mouse_pos):
            option =  1
            break
        elif opt_2.collidepoint(mouse_pos):
            option = 2
            break
        elif opt_3.collidepoint(mouse_pos):
            option =  3
            break
        elif opt_4.collidepoint(mouse_pos):
            option =  4
            break
    pygame.display.update()
    return option

def appear(friendly,enemy):
    while True:
        event_check()
        #movement
        enemy.move_enemy()
        friendly.move_friendly()
        arrived1 = enemy.appear_right()
        arrived2 = friendly.appear_left()
        blit_background() 
        blit_enemy(enemy)
        blit_friendly(friendly)
        blit_health(friendly,enemy)
        blit_text("A Wild pokemon has appeared!",(screen_width/20,screen_height*3/4))
        pygame.display.update()
        if arrived1 == True and arrived2 == True:
            return friendly, enemy

def friendly_quick_attack(friendly,enemy):      #animation for basic friendly attack
    while True:
        event_check()
        done = friendly.attack_friendly()
        friendly.move_friendly()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        pygame.display.update()
        if done == True:
            return

def enemy_quick_attack(friendly,enemy): #animation for basic enemy attack
    while True:
        event_check()
        done = enemy.attack_enemy()
        enemy.move_enemy()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        pygame.display.update()
        if done == True:
            return

def friendly_slam(friendly,enemy):
    n=0
    while n<7:
        event_check()
        friendly.x_speed = 55
        friendly.y_speed = -15
        friendly.move_friendly()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        pygame.display.update()
        n+=1
    while True:
        event_check()

        friendly.x_speed = -55
        friendly.y_speed = 15
        friendly.move_friendly()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_image("slam.png",(100,100),(enemy.enemy_pos[0]+enemy.size[0]*1/3,enemy.enemy_pos[1]+enemy.size[1]*1/3)) #2/5ths to allign top corner of animation with center of poke
        pygame.display.update()
        if friendly.friendly_pos[0]<=friendly.friendly_fight_pos[0]:
            return

def friendly_scratch(friendly,enemy):
    n = 0
    while n<10:
        event_check()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_image("scratch.png",(150,150),(enemy.enemy_pos[0]+enemy.size[0]*1/3,enemy.enemy_pos[1]+enemy.size[1]*1/3))
        pygame.display.update()
        n+=1
        
def friendly_surf(friendly,enemy):
    n =0
    m=0
    while True:
        event_check()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_image("surf.png",(300,300),((friendly.friendly_pos[0])+n,(friendly.friendly_pos[1])+m))
        n+=55
        m-=15
        pygame.display.update()
        if friendly.friendly_pos[0]+n >= enemy.enemy_fight_pos[0]:
            return
        
        
        

def enemy_faint(friendly,enemy):
    while True:
        event_check()
        print ("fainteing")
        enemy.enemy_pos[0] +=10
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_text("Enemy has fainted.",(screen_width/20,screen_height*3/4))
        pygame.display.update()
        if enemy.enemy_pos[0] >= screen_width:
            break
        
def friendly_faint(friendly,enemy):
    while True:
        event_check()
        friendly.friendly_pos[0] -=10
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_text("Your Pokemon has fainted.",(screen_width/20,screen_height*3/4))
        pygame.display.update()
        if enemy.enemy_pos[0] <= 0-friendly.size[0]:
            break   
            
def pause(friendly, enemy,delay,text = None):
    counter = 0
    while True:
        event_check()
        blit_background()
        blit_friendly(friendly)
        blit_enemy(enemy)
        blit_health(friendly,enemy)
        blit_text(text,(screen_width/20,screen_height*3/4))
        pygame.display.update()
        if counter >= delay:
            break
        counter+=1


def friendly_turn(friendly,enemy):
    choice = choose_option(friendly,enemy) #returns selection from 'fight bag pokemon run' options
    if choice == 1: #if fight is selected
        move = choose_option(friendly,enemy,"Quick Attack","Scratch","    Slam","    Surf")
        if move == 1: # 1st move
            friendly_quick_attack(friendly,enemy)
            enemy.health -= random.randrange(15,20) # damage range 15 to 20
            pause(friendly,enemy,35,"You Used Quick Attack")
        elif move == 2: # 2nd move
            friendly_slam(friendly,enemy) #slam
            if random.randrange(1,10) != 1: # 1 in 10 chance of missing
                enemy.health -= random.randrange(20,40)#damage range 20-40
                pause(friendly,enemy,35,"You Used Slam")
            else:
                pause(friendly,enemy,35,"You Used Slam")
                pause(friendly,enemy,35,"Your attack missed!")
        elif move == 3: 
            friendly_scratch(friendly,enemy) #scratch
            if random.randrange(1,100) != 1: # 1 in 100 chance of missing
                enemy.health -= 10           #always 10 damage
                pause(friendly,enemy,35,"You Used Scratch")
            else:
                pause(friendly,enemy,35,"You Used Scratch")
                pause(friendly,enemy,35,"Your attack missed!")
        elif move == 4: 
            friendly_surf(friendly,enemy)
            enemy.health -= random.randrange(30,40)
            pause(friendly,enemy,35,"You Used Surf")
            
    elif choice == 2: #Opens available pokemone
        pause(friendly,enemy,35,"Pokemon List Unavailable!")
        friendly_turn(friendly,enemy)
        
    elif choice == 3:
        item = choose_option(friendly,enemy,"Poke-Ball","Potion","-","-")
        if item == 1:
            pause(friendly,enemy, 35, "Pokeball not available!")
            friendly_turn(friendly,enemy)
            
        if item == 3:
            friendly.health +=30
            pause(friendly,enemy,50,"You used a potion.")
            if friendly.health > friendly.base_health:
                friendly.health = friendly.base_health 
                
    elif choice == 4:
        while True:
            event_check()
            blit_background()
            blit_friendly(friendly)
            blit_enemy(enemy)
            blit_health(friendly,enemy)
            blit_text("You got away safely.",(screen_width/20,screen_height*3/4))
            pygame.display.update()


def enemy_turn(friendly,enemy):
    moves = ["Quick Attack"]#enemy moves
    choice = moves[random.randrange(len(moves))] # chooses a random number => picks move of that index from list
    counter = 0    
    while True:
            event_check()
            blit_background()
            blit_friendly(friendly)
            blit_enemy(enemy)
            blit_health(friendly,enemy)
            blit_text("Enemy used "+choice+".",(screen_width/20,screen_height*3/4))
            pygame.display.update()
            counter +=1
            if counter>= 40:     #delay whilst displaying name of move
                break
    enemy_quick_attack(friendly,enemy)
    friendly.health-=random.randrange(10,40)
    pygame.display.update()
    
def fight(friendly,enemy):
    while True:
        if friendly.health > 0 and enemy.health > 0:
            friendly_turn(friendly,enemy)
        else:
            break
        if friendly.health > 0 and enemy.health > 0:        
            enemy_turn(friendly,enemy)
        else:
            break
    if enemy.health < friendly.health:
        enemy_faint(friendly,enemy)
    else:
        friendly_faint(friendly,enemy)
    
    
def battle():
    friendly = Pokemon(random.randrange(1,200)) #random number between 1 and 199
    enemy = Pokemon(random.randrange(1,200))
    appear(friendly,enemy)
    fight(friendly,enemy)
    
battle()
pygame.quit()
sys.exit()



