import pygame
import time
import random

pygame.init()
crash_sound = pygame.mixer.Sound("Crash.wav")
coins_drop = pygame.mixer.Sound("coins_drop.wav")
pygame.mixer.music.load("Drag_Race.wav")

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)
yellow = (200,200,0)
gold = (255,215,0)
blue = (0,0,150)
purple = (128,0,255)

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_yellow = (255,255,0)
bright_blue = (0,0,255)
bright_purple = (160,30,255)
bright_grey = (128,128,128)

dark_gold = (218,165,32)
dark_green = (0,130,0)
dark_grey = (192,192,192)

block_color = (53,115,255)
gem_color = (18,188,48)

car_width = 73

coins = 0
gems = 0
score = 0
h_score = 0
lives = 1

speed = 5
s_buff = 0
s_nerf = 1
bought_s_nerf = False
nerf = False

unlock = False

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
gameIcon = pygame.image.load('racecaricon.png')
intro_img = pygame.image.load('intro_img.png')
intro_img2 = pygame.image.load('intro_img2.png')

pygame.display.set_icon(gameIcon)

pause = False

#stats
def total_score(count):
    font_s = pygame.font.SysFont(None, 25)
    text_s = font_s.render("Score: " + str(count), True, black)
    gameDisplay.blit(text_s, (0,0))

def total_score2(count):
    font_s = pygame.font.SysFont(None, 25)
    text_s = font_s.render("Score: " + str(count), True, black)
    gameDisplay.blit(text_s, (405,0))

def high_score(count):
    font_h = pygame.font.SysFont(None, 25)
    text_h = font_h.render("High_Score: " + str(count), True, black)
    gameDisplay.blit(text_h, (81,0))

def coins_earned(count):
    font_c = pygame.font.SysFont(None, 25)
    text_c = font_c.render("Coins: " + str(count), True, gold)
    gameDisplay.blit(text_c, (700,5))
    
    pygame.draw.circle(gameDisplay, gold, (685,14), 9)
    
    ltr_S = font_c.render("S", True, dark_gold)
    gameDisplay.blit(ltr_S, (680,6))

    font_l = pygame.font.SysFont(None, 29)
    ltr_l = font_l.render("l", True, dark_gold)
    gameDisplay.blit(ltr_l, (683,5))

def gems_collected(count):
    font_g = pygame.font.SysFont(None, 25)
    text_g = font_g.render("Gems: " + str(count), True, gem_color)
    gameDisplay.blit(text_g, (598,5))
    
    pygame.draw.circle(gameDisplay, gem_color, (585,14), 9)

    ltr_G = font_g.render("G", True, dark_green)
    gameDisplay.blit(ltr_G, (578,5))

def lives_left(count):
    font_l = pygame.font.SysFont(None, 25)
    text_l = font_l.render("Lives: " + str(count), True, black)
    gameDisplay.blit(text_l, (210,0))

#things and car
def things(thingx, thingy, thingw, thingh, block_color):
    pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def gems_falling(gemx, gemy, gemw, gem_color):
    pygame.draw.circle(gameDisplay, gem_color, [gemx, gemy], gemw)

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

#messages, buttons
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text,msg_x,msg_y):
    medText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, medText)
    TextRect.center = (msg_x,msg_y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    
    #time.sleep(2)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1:
            pygame.time.wait(150)
            action()
    else:     
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)
    
#screens
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        gameDisplay.blit(intro_img,(540,50))
        gameDisplay.blit(intro_img2,(50,100))

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("multi",150,550,100,50,green,bright_green,multiplayer)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Shop",350,500,100,50,blue,bright_blue,shop)
        button("Garage",350,150,100,50,purple,bright_purple,vehicles)
        button("Description",10,10,150,50,bright_grey,dark_grey,description)

        pygame.display.update()
        clock.tick(15)

def description():
    descript = True

    gameDisplay.fill(white)
    
    while descript:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Description", largeText)
        TextRect.center = ((display_width/2),100)
        gameDisplay.blit(TextSurf, TextRect)

        message_display("Objective: Make your highscore as high as possible",400,250)
        message_display("In-Game Controls:",400,300)
        message_display("Left: left arrow, Right: right arrow",400,340)
        message_display("Press 'p' to pause and 'escape' to go home",400,380)

        button("Back",150,450,100,50,green,bright_green,game_intro)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)
        button("Play Again",150,450,105,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Shop",350,500,100,50,blue,bright_blue,shop)
        button("Garage",350,150,100,50,purple,bright_purple,vehicles)

        pygame.display.update()
        clock.tick(15)

def survived():
    global lives
    
    survived = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects("You lost 1 live!", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    lives -= 1

    while survived:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        button("Continue",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)


def music():
    gameDisplay.fill(white)
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    mediumText = pygame.font.Font('freesansbold.ttf',80)
    TextSurf, TextRect = text_objects("Choose Music", mediumText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)

        #button(msg,x,y,w,h,ic,ac,action=None)
        button("Continue",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Shop",350,400,100,50,blue,bright_blue,shop)
        button("Garage",350,500,100,50,purple,bright_purple,vehicles)
        
        button("Drag Race",550,200,100,50,yellow,bright_yellow,play_Drag)
        button("Jazz",150,200,100,50,yellow,bright_yellow,play_Jazz)
        button("Country",350,200,100,50,yellow,bright_yellow,play_Country)

        pygame.display.update()
        clock.tick(15)
    
def play_Drag():
    pygame.mixer.music.load("Drag_Race.wav")
    print("Drag is chosen")
    
def play_Jazz():
    pygame.mixer.music.load("Jazz_in_Paris.wav")
    print("Jazz is chosen")

def play_Country():
    pygame.mixer.music.load("Cherokee_Shuffle.wav")
    print("Country is chosen")


def shop():
    shop = True

    while shop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Shop", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Garage",350,500,100,50,purple,bright_purple,vehicles)
        
        button("Buy lives",150,150,120,50,blue,bright_blue,add_lives)
        button("Speed buff",350,150,120,50,blue,bright_blue,speed_buff)
        button("Slow blocks",550,150,120,50,blue,bright_blue,speed_nerf)

        font = pygame.font.SysFont(None, 25)
        text = font.render("30 coins ", True, black)
        text2 = font.render("20 coins ", True, black)
        text3 = font.render("25 coins ", True, black)
        gameDisplay.blit(text, (175,125))
        gameDisplay.blit(text2, (375,125))
        gameDisplay.blit(text3, (575,125))

        coins_earned(coins)
        gems_collected(gems)
        
        pygame.display.update()
        clock.tick(15)

def speed_buff():
    global s_buff
    global coins

    if coins >= 20:
        pygame.mixer.Sound.play(coins_drop)
        s_buff += 3
        print("you bought speed buff")
        print("-20 coins")
        coins -= 20        
    else:
        print("you do not have enough coins!")

def add_lives():
    global lives
    global coins

    if coins >= 30:
        pygame.mixer.Sound.play(coins_drop)
        lives += 1
        print("you bought 1 live")
        print("-30 coins")
        coins -= 30
    else:
        print("you do not have enough coins!")

def speed_nerf():
    global s_nerf
    global nerf
    global bought_s_nerf
    global coins

    if coins >= 25:
        if bought_s_nerf == False:
            pygame.mixer.Sound.play(coins_drop)
            s_nerf -= 0.15
            coins -= 25
            print("blocks slower by 15%")
            print("-25 coins")
            nerf = True
            bought_s_nerf = True
        else:
            print("you bought it already!")
    else:
        print("you do not have enough coins!")


def vehicles():
    global unlock
    global coins
    global gems

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        largeText = pygame.font.Font('freesansbold.ttf',115)
        mediumText = pygame.font.Font('freesansbold.ttf',80)
        TextSurf, TextRect = text_objects("Choose skin", mediumText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        #button(msg,x,y,w,h,ic,ac,action=None)
        button("Continue",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Shop",350,400,100,50,blue,bright_blue,shop)
        button("Music",350,500,100,50,yellow,bright_yellow,music)

        button("Racecar 1",150,200,100,50,purple,bright_purple,racecar)
        button("Racecar 2",350,200,100,50,purple,bright_purple,racecar2)
        button("Racecar 3",550,200,100,50,purple,bright_purple,racecar3)
        button("Helicopter",350,100,100,50,purple,bright_purple,helicopter)
        if unlock == False:
            button("Unlock: 5 gems",325,155,150,35,dark_grey,bright_grey,unlock_skin)
        else:
            button("Unlocked",325,155,150,35,white,white,unlocked)

        coins_earned(coins)
        gems_collected(gems)

        pygame.display.update()
        clock.tick(15)

def racecar():
    global carImg
    carImg = pygame.image.load('racecar.png')
    print("you chose racecar 1")
    
def racecar2():
    global carImg
    carImg = pygame.image.load('racecar2.png')
    print("you chose racecar 2")

def racecar3():
    global carImg
    carImg = pygame.image.load('racecar3.png')
    print("you chose racecar 3")

def helicopter():
    global carImg
    global unlock
    
    if unlock == True:
        carImg = pygame.image.load('helicopter.png')
        print("you chose helicopter")
    else:
        print("you need to unlock this skin!")
    
def unlock_skin():
    global unlock
    global gems
    
    if unlock == False:
        if gems >= 5:
            unlock = True
            gems -= 5
            print("you unlocked the helicopter!")
        else:
            print("you need 5 gems!")

def unlocked():
    print("you already have this skin!")


#pause and unpause, quit
def paused():
    pygame.mixer.music.pause()
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Shop",350,500,100,50,blue,bright_blue,shop)
        button("Vehicles",350,150,100,50,purple,bright_purple,vehicles)

        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def quitgame():
    pygame.quit()
    quit()


#gameloop        
def game_loop():
    global pause
    
    global coins
    global gems
    global lives
    global score
    global h_score

    global s_buff
    global s_nerf
    global nerf
    global speed
    
    pygame.mixer.music.play(-1)
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    gem_startx = random.randrange(0, display_width)
    gem_starty = -10000
    gem_speed = 15
    gem_width = 10
    gem_height = 10

    print_max_speed = True

    gameExit = False

    while not gameExit:

        if score > h_score:
            h_score = score
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            x_change = -speed
        if keys_pressed[pygame.K_RIGHT]:
            x_change = speed
        
        x += x_change   
                
        gameDisplay.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        gems_falling(gem_startx, gem_starty, gem_width, gem_color)
        gem_starty += gem_speed
        
        car(x,y)
        coins_earned(coins)
        gems_collected(gems)
        total_score(score)
        lives_left(lives)
        high_score(h_score)

        if x > display_width - car_width or x < 0:
            crash()
            score = 0
            speed = 5
            s_buff = 0

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            score += 1
            coins += 1
            
            if thing_speed < 17:
                thing_speed += 1
                if nerf == True:
                    thing_speed *= s_nerf
                    nerf = False
            if thing_width < 125:
                thing_width += (score * 1.2)
                
            if speed < 11:
                speed = (speed * 1.1) + s_buff
            if speed > 11:
                speed = 11
            if speed == 11:
                if print_max_speed == True:
                    print("MAXIMUM SPEED REACHED")
                    print_max_speed = False
                else:
                    pass

        if gem_starty > display_height:
            gem_starty = -10000
            gem_startx = random.randrange(0, display_width)
        
        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                if lives == 1:
                    s_buff = 0
                    speed = 5
                    score = 0
                    crash()
                    
                if lives > 1:
                   survived()

        if y < gem_starty + gem_height:
            if x > gem_startx and x < gem_startx + gem_width or x + car_width > gem_startx and x + car_width < gem_startx + gem_width:
                gems += 1
                gem_startx = random.randrange(0, display_width)
                gem_starty = -10000
                      
        pygame.display.update()
        clock.tick(60)

def multiplayer():
    global pause
    global speed

    score1 = 0
    score2 = 0
    
    pygame.mixer.music.play(-1)
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    print_max_speed = True

    gameExit = False

    while not gameExit:

##        if score > h_score:
##            h_score = score
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            x_change = -speed
        if keys_pressed[pygame.K_RIGHT]:
            x_change = speed
        
        x += x_change   
                
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, (400,0,5,600))

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        
        car(x,y)
        total_score(score1)
        total_score2(score2)
        high_score(h_score)

        if x > display_width - car_width or x < 0:
            crash()
            score1 = 0
            score2 = 0
            speed = 5

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            score1 += 1
            score2 += 1
            
            if thing_speed < 17:
                thing_speed += 1
            if thing_width < 125:
                thing_width += (score1 * 1.2)
                
            if speed < 11:
                speed = (speed * 1.1)
            if speed > 11:
                speed = 11
            if speed == 11:
                if print_max_speed == True:
                    print("MAXIMUM SPEED REACHED")
                    print_max_speed = False
        
        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                if lives == 1:
                    speed = 5
                    score1 = 0
                    score2 = 0
                    crash()
                      
        pygame.display.update()
        clock.tick(60)
        

game_intro()
#game_loop()
multiplayer()
pygame.quit()
quit()
