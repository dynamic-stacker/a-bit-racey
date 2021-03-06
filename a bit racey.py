import pygame
import time
import math, sys
import random

from db import Database

# Database setup
db = Database()

# Prefer to put into a main() function
# But it works for now
db.setup()

pygame.init()

crash_sound = pygame.mixer.Sound("msc_snds/Crash.wav")
coins_drop = pygame.mixer.Sound("msc_snds/coins_drop.wav")
button_sound = pygame.mixer.Sound("msc_snds/button_snd.wav")
helicopter_sound = pygame.mixer.Sound("msc_snds/helicopter_snd.wav")
engine_sound = pygame.mixer.Sound("msc_snds/engine_rev.wav")
pygame.mixer.music.load("msc_snds/Drag_Race.wav")

is_muted = False
snd_muted = False

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

coins = db.get_coins(1);
gems = db.get_gems(1);
score = 0
h_score = db.get_highscore(1);
lives = 1

speed = 5
s_buff = 0
s_nerf = 1
bought_s_nerf = False
nerf = False

unlock = db.is_vehicle_unlocked(1, 4)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('images/racecar.png')
gameIcon = pygame.image.load('images/racecaricon.png')
intro_img = pygame.image.load('images/intro_img.png')
intro_img2 = pygame.image.load('images/intro_img2.png')
bg_img = pygame.image.load('images/bg.png')
bg_img = pygame.transform.scale(bg_img, (800, 600))

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
    gameDisplay.blit(text_c, (700,3))
    
    pygame.draw.circle(gameDisplay, gold, (685,12), 9)
    
    ltr_S = font_c.render("S", True, dark_gold)
    gameDisplay.blit(ltr_S, (680,4))

    font_l = pygame.font.SysFont(None, 29)
    ltr_l = font_l.render("l", True, dark_gold)
    gameDisplay.blit(ltr_l, (683,3))

def gems_collected(count):
    font_g = pygame.font.SysFont(None, 25)
    text_g = font_g.render("Gems: " + str(count), True, gem_color)
    gameDisplay.blit(text_g, (598,3))
    
    pygame.draw.circle(gameDisplay, gem_color, (585,12), 9)

    ltr_G = font_g.render("G", True, dark_green)
    gameDisplay.blit(ltr_G, (578,3))

def lives_left(count):
    font_l = pygame.font.SysFont(None, 25)
    text_l = font_l.render("Lives: " + str(count), True, black)
    gameDisplay.blit(text_l, (210,0))

#things and car
def things(thingx, thingy, thingw, thingh, block_color):
    pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def things2(thingx, thingy, thingw, thingh, block_color):
    pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def gems_falling(gemx, gemy, gemw, gem_color):
    pygame.draw.circle(gameDisplay, gem_color, [gemx, gemy], gemw)

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def car2(x,y):
    gameDisplay.blit(carImg,(x,y))

#messages, buttons
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text,msg_x,msg_y):
    medText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects(text, medText)
    TextRect.center = (msg_x,msg_y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
    global snd_muted
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1: #left click
            if snd_muted == False:
                pygame.mixer.Sound.play(button_sound)
            pygame.time.wait(150)
            action()      
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def large_button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1: #left click
            pygame.mixer.Sound.play(button_sound)
            pygame.time.wait(150)
            action()      
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf", 50)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)
    
#screens
def game_intro():
    pygame.mixer.music.pause()
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
        button("Modes",150,500,100,50,green,bright_green,modes)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Shop",350,500,100,50,blue,bright_blue,shop)
        button("Garage",350,150,100,50,purple,bright_purple,vehicles)
        button("Description",10,10,150,50,bright_grey,dark_grey,description)
        large_button("#",740,10,50,50,bright_grey,dark_grey,settings)

        pygame.display.update()
        clock.tick(15)

def modes():
    gameDisplay.fill(white)
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    mediumText = pygame.font.Font('freesansbold.ttf',80)
    TextSurf, TextRect = text_objects("Game modes", mediumText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        #button(msg,x,y,w,h,ic,ac,action=None)
        button("Normal",150,450,100,50,green,bright_green,game_loop)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Shop",350,380,100,50,blue,bright_blue,shop)
        button("Music",350,450,100,50,yellow,bright_yellow,music)
        button("Garage",350,520,100,50,purple,bright_purple,vehicles)
        
        button("Multiplayer",150,200,125,50,green,bright_green,multiplayer)
        button("Racecourse",350,200,125,50,green,bright_green,racecourse)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("Description", largeText)
        TextRect.center = ((display_width/2),100)
        gameDisplay.blit(TextSurf, TextRect)

        message_display("Objective: Make your highscore as high as possible",400,250)
        message_display("In-Game Controls:",400,280)
        message_display("Left: left arrow, Right: right arrow (A & D for multiplayer)",400,320)
        message_display("Press 'p' to pause and 'escape' to go home",400,360)

        button("Back",150,450,100,50,green,bright_green,game_intro)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def settings():
    global is_muted
    global snd_muted
    
    settings = True
    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        gameDisplay.fill(white)

        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("Settings", largeText)
        TextRect.center = ((display_width/2),125)
        gameDisplay.blit(TextSurf, TextRect)

        if is_muted == False:
            button("Mute",150,250,100,50,bright_grey,dark_grey,mute)
        if is_muted == True:
            button("Unmute",550,250,100,50,bright_grey,dark_grey,unmute)
        if snd_muted == False:
            button("Off",150,350,100,50,bright_grey,dark_grey,sound_off)
        if snd_muted == True:
            button("On",550,350,100,50,bright_grey,dark_grey,sound_on)

        button("Back",150,450,100,50,green,bright_green,game_intro)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)

        message_display("Music settings",400,275)
        message_display("Sound settings",400,375)

        pygame.display.update()
        clock.tick(15)

def unmute():
    global is_muted
    pygame.mixer.music.load("msc_snds/Drag_race.wav")
    is_muted = False
    
def mute():
    global is_muted
    pygame.mixer.music.load("msc_snds/silence.wav")
    is_muted = True

def sound_on():
    global snd_muted
    snd_muted = False

def sound_off():
    global snd_muted
    snd_muted = True
        
def crash(car_id, play_mode):
    global snd_muted
    
    pygame.mixer.music.stop()
    if snd_muted == False:
        pygame.mixer.Sound.play(crash_sound)

    if play_mode == 'single_player':
        # Update database highscore, similar hard coding this part
        db.update_highscore(1, h_score)

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Crashed", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

    if play_mode == 'multiplayer':
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Player " + str(car_id) + "wins!", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        #gameDisplay.fill(white)
        button("Normal",150,450,105,50,green,bright_green,game_loop)
        button("Modes",150,500,105,50,green,bright_green,modes)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Shop",350,500,100,50,blue,bright_blue,shop)
        button("Garage",350,150,100,50,purple,bright_purple,vehicles)

        pygame.display.update()
        clock.tick(15)
        
def survived():
    global lives
    global snd_muted
    
    survived = True
    pygame.mixer.music.stop()
    if snd_muted == False:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()
        
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        #gameDisplay.fill(white)

        #button(msg,x,y,w,h,ic,ac,action=None)
        button("Normal",150,450,100,50,green,bright_green,game_loop)
        button("Modes",150,500,100,50,green,bright_green,modes)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Shop",350,400,100,50,blue,bright_blue,shop)
        button("Garage",350,500,100,50,purple,bright_purple,vehicles)
        
        button("Drag Race",550,200,100,50,yellow,bright_yellow,play_Drag)
        button("Jazz",150,200,100,50,yellow,bright_yellow,play_Jazz)
        button("Country",350,200,100,50,yellow,bright_yellow,play_Country)

        pygame.display.update()
        clock.tick(15)
    
def play_Drag():
    global is_muted
    if is_muted == False:
        pygame.mixer.music.load("msc_snds/Drag_Race.wav")
        print("Drag is chosen")
    else:
        print("You disabled music in settings(#)")
    
def play_Jazz():
    global is_muted
    if is_muted == False:
        pygame.mixer.music.load("msc_snds/Jazz_in_Paris.wav")
        print("Jazz is chosen")
    else:
        print("You disabled music in settings(#)")

def play_Country():
    global is_muted
    if is_muted == False:
        pygame.mixer.music.load("msc_snds/Cherokee_Shuffle.wav")
        print("Country is chosen")
    else:
        print("You disabled music in settings(#)")
        

def shop():
    shop = True
    
    while shop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Shop", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Normal",150,450,100,50,green,bright_green,game_loop)
        button("Modes",150,500,100,50,green,bright_green,modes)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Music",350,400,100,50,yellow,bright_yellow,music)
        button("Garage",350,500,100,50,purple,bright_purple,vehicles)
        
        button("Buy lives",150,150,120,50,blue,bright_blue,add_lives)
        button("Speed buff",350,150,120,50,blue,bright_blue,speed_buff)
        button("Slow blocks",550,150,120,50,blue,bright_blue,speed_nerf)
        button("Buy coins",350,60,120,50,blue,bright_blue,buy_coins)

        font = pygame.font.SysFont(None, 25)
        text = font.render("30 coins ", True, black)
        text2 = font.render("20 coins ", True, black)
        text3 = font.render("25 coins ", True, black)
        text4 = font.render("5 gems ", True, black)
        gameDisplay.blit(text, (175,125))
        gameDisplay.blit(text2, (375,125))
        gameDisplay.blit(text3, (575,125))
        gameDisplay.blit(text4, (375,35))

        coins_earned(coins)
        gems_collected(gems)
        
        pygame.display.update()
        clock.tick(15)

def speed_buff():
    global s_buff
    global coins
    global snd_muted

    if coins >= 20:
        s_buff += 3
        print("you bought speed buff")
        print("-20 coins")
        coins -= 20
        if snd_muted == False:
            pygame.mixer.Sound.play(coins_drop)
        db.update_coins(1, coins)
    else:
        print("you do not have enough coins!")

def add_lives():
    global lives
    global coins
    global snd_muted

    if coins >= 30:
        lives += 1
        print("you bought 1 live")
        print("-30 coins")
        coins -= 30
        if snd_muted == False:
            pygame.mixer.Sound.play(coins_drop)
        db.update_coins(1, coins)
    else:
        print("you do not have enough coins!")

def speed_nerf():
    global s_nerf
    global nerf
    global bought_s_nerf
    global coins
    global snd_muted

    if coins >= 25:
        if bought_s_nerf == False:
            s_nerf -= 0.15
            coins -= 25
            print("blocks slower by 15%")
            print("-25 coins")
            if snd_muted == False:
                pygame.mixer.Sound.play(coins_drop)
            nerf = True
            bought_s_nerf = True
            db.update_coins(1, coins)
        else:
            print("you bought it already!")
    else:
        print("you do not have enough coins!")

def buy_coins():
    global gems
    global coins
    global snd_muted

    if gems >= 5:
        coins += 20
        print("you bought 20 coins")
        print("-5 gems")
        gems -= 5
        if snd_muted == False:
            pygame.mixer.Sound.play(coins_drop)
        db.update_coins(1, coins)
        db.update_gems(1, gems)
        
    else:
        print("you do not have enough gems!")

def vehicles():
    global unlock
    global coins
    global gems

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        gameDisplay.fill(white)

        largeText = pygame.font.Font('freesansbold.ttf',115)
        mediumText = pygame.font.Font('freesansbold.ttf',80)
        TextSurf, TextRect = text_objects("Garage", mediumText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        #button(msg,x,y,w,h,ic,ac,action=None)
        button("Normal",150,450,100,50,green,bright_green,game_loop)
        button("Modes",150,500,100,50,green,bright_green,modes)
        button("QUIT",550,450,100,50,red,bright_red,quitgame)
        button("Shop",350,400,100,50,blue,bright_blue,shop)
        button("Music",350,500,100,50,yellow,bright_yellow,music)
        
        button("Preview",350,25,100,50,bright_grey,dark_grey,preview)
        button("Racecar 1",150,200,100,50,purple,bright_purple,racecar)
        button("Racecar 2",350,200,100,50,purple,bright_purple,racecar2)
        button("Racecar 3",550,200,100,50,purple,bright_purple,racecar3)
        button("Helicopter",350,100,100,50,purple,bright_purple,helicopter)
        unlock = db.is_vehicle_unlocked(1, 4)
        if unlock == False:
            button("Unlock: 5 gems",325,155,150,35,dark_grey,bright_grey,unlock_skin)
        else:
            button("Unlocked",325,155,150,35,white,white,unlocked)

        coins_earned(coins)
        gems_collected(gems)

        pygame.display.update()
        clock.tick(15)

def preview():
    preview = True
    gameDisplay.fill(white)
    
    while preview:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        largeText = pygame.font.Font('freesansbold.ttf',75)
        TextSurf, TextRect = text_objects("Preview of vehicles", largeText)
        TextRect.center = ((display_width/2),75)
        gameDisplay.blit(TextSurf, TextRect)

        preview1 = pygame.image.load("images/racecar.png")
        preview2 = pygame.image.load("images/racecar2.png")
        preview3 = pygame.image.load("images/racecar3.png")
        preview4 = pygame.image.load("images/helicopter.png")

        image1 = pygame.transform.scale(preview1, (150, 180))
        image2 = pygame.transform.scale(preview2, (150, 180))
        image3 = pygame.transform.scale(preview3, (150, 180))
        image4 = pygame.transform.scale(preview4, (150, 180))

        gameDisplay.blit(image1,(40,200))
        gameDisplay.blit(image2,(230,200))
        gameDisplay.blit(image3,(430,200))
        gameDisplay.blit(image4,(610,200))

        button("Back",150,500,100,50,green,bright_green,vehicles)
        button("QUIT",550,500,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def racecar():
    global carImg
    carImg = pygame.image.load('images/racecar.png')
    if snd_muted == False:
        pygame.mixer.Sound.play(engine_sound)
    print("you chose racecar 1")
    
def racecar2():
    global carImg
    carImg = pygame.image.load('images/racecar2.png')
    if snd_muted == False:
        pygame.mixer.Sound.play(engine_sound)
    print("you chose racecar 2")

def racecar3():
    global carImg
    carImg = pygame.image.load('images/racecar3.png')
    if snd_muted == False:
        pygame.mixer.Sound.play(engine_sound)
    print("you chose racecar 3")

def helicopter():
    global carImg
    global unlock
    unlock = db.is_vehicle_unlocked(1, 4)
    if unlock == True:
        carImg = pygame.image.load('images/helicopter.png')
        if snd_muted == False:
            pygame.mixer.Sound.play(helicopter_sound)
        print("you chose helicopter")
    else:
        print("you need to unlock this vehicle!")
    
def unlock_skin():
    global unlock
    global gems
    unlock = db.is_vehicle_unlocked(1, 4)
    if unlock == False:
        if gems >= 5:
            gems -= 5
            print("you unlocked the helicopter!")
            db.update_gems(1, gems)
            db.unlock_vehicle(1, 4)
        else:
            print("you need 5 gems!")

def unlocked():
    print("you already have this vehicle!")


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    game_intro()

        #gameDisplay.fill(white)
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Modes",150,500,100,50,green,bright_green,modes)
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

    global car_width

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

         #gameDisplay.fill(white)
        gameDisplay.blit(bg_img, (0, 0))

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
            score = 0
            speed = 5
            s_buff = 0
            crash(1, "single_player")

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            score += 1
            coins += 1
            db.update_coins(1, coins)
            
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
                    crash(1, "single_player")
                    
                if lives > 1:
                   survived()

        if y < gem_starty + gem_height:
            if gem_startx > x and gem_startx < x + car_width or gem_startx < x + car_width and x + car_width < gem_startx + gem_width:
                gems += 1
                gem_startx = random.randrange(0, display_width)
                gem_starty = -10000
                db.update_gems(1, gems)
                      
        pygame.display.update()
        clock.tick(60)

def multiplayer():
    global pause
    global speed

    score1 = 0
    score2 = 0

    mid_line = 400
    
    pygame.mixer.music.play(-1)
    
    x1 = (display_width * 0.20)
    x2 = (display_width * 0.65)
    y1 = (display_height * 0.8)
    y2 = (display_height * 0.8)

    x1_change = 0
    x2_change = 0

    thing_speed = 7
    thing_width = 100
    thing_height = 100
    
    thing_startx = random.randrange(0, round(mid_line - thing_width)) # make number integer
    thing2_startx = thing_startx + 400
    thing_starty = -600

    print_max_speed = True

    gameExit = False

    while not gameExit:
        
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
                    x2_change = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x1_change = 0 

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            x2_change = -speed
        if keys_pressed[pygame.K_RIGHT]:
            x2_change = speed
        if keys_pressed[pygame.K_a]:
            x1_change = -speed
        if keys_pressed[pygame.K_d]:
            x1_change = speed
        
        x1 += x1_change   
        x2 += x2_change   
      
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, (mid_line,0,5,600))

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        things2(thing2_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        
        car(x1,y1)
        car2(x2,y2)

        total_score(score1)
        total_score2(score2)

        if x1 > mid_line - car_width or x1 < 0:
            score1 = 0
            score2 = 0
            speed = 5
            crash(2, "multiplayer")

        if x2 > display_width - car_width or x2 < mid_line :
            score1 = 0
            score2 = 0
            speed = 5
            crash(1, "multiplayer")

        if thing_starty > display_height:
            thing_starty = 0 - thing_height

            thing_startx = random.randrange(0, round(mid_line - thing_width))
            thing2_startx = thing_startx + 400
            score1 += 1
            score2 += 1
            
            if thing_speed < 15:
                thing_speed += 1
            if thing_width < 110:
                thing_width += (score1 * 1.2)
                
            if speed < 11:
                speed = (speed * 1.1)
            if speed > 11:
                speed = 11
            if speed == 11:
                if print_max_speed == True:
                    print("MAXIMUM SPEED REACHED")
                    print_max_speed = False
        
        if y1 < thing_starty + thing_height:
            if x1 > thing_startx and x1 < thing_startx + thing_width or x1 + car_width > thing_startx and x1 + car_width < thing_startx + thing_width:
                if lives == 1:
                    speed = 5
                    score1 = 0
                    crash(2, "multiplayer")       
                    
        if y2 < thing_starty + thing_height:
            if x2 > thing2_startx and x2 < thing2_startx + thing_width or x2 + car_width > thing2_startx and x2 + car_width < thing2_startx + thing_width:
                if lives == 1:
                    speed = 5
                    score2 = 0
                    crash(1, "multiplayer")

                      
        pygame.display.update()
        clock.tick(60)

#initialize the screen
from pygame.locals import *

def racecourse():
    global carImg
    global snd_muted
    
    pygame.mixer.music.play(-1)
    
    screen = pygame.display.set_mode((display_width, display_height))
    #GAME CLOCK
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    win_font = pygame.font.Font(None, 50)
    win_condition = None
    win_text = font.render('', True, (0, 255, 0))
    loss_text = font.render('', True, (255, 0, 0))
    t0 = time.time()

    class CarSprite(pygame.sprite.Sprite):
        MAX_FORWARD_SPEED = 9
        MAX_REVERSE_SPEED = 9
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = image
            self.position = position
            self.speed = self.direction = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0
        
        def update(self, deltat):
            #SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            if self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x += -self.speed*math.sin(rad)
            y += -self.speed*math.cos(rad)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

    class PadSprite(pygame.sprite.Sprite):
        normal = pygame.image.load('images/race_pads.png')
        hit = pygame.image.load('images/collision.png')
        def __init__(self, position):
            super(PadSprite, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
        def update(self, hit_list):
            if self in hit_list: self.image = self.hit
            else: self.image = self.normal

    pads = [
        PadSprite((0, 10)),
        PadSprite((600, 10)),
        PadSprite((200, 110)),
        PadSprite((870, 110)),
        PadSprite((340, 210)),
        PadSprite((420, 210)),
        PadSprite((0, 310)),
        PadSprite((630, 310)),
        PadSprite((330, 410)),
        PadSprite((950, 410)),
        PadSprite((30, 510)),
        PadSprite((690, 510)),       
    ]
    pad_group = pygame.sprite.RenderPlain(*pads)

    class Trophy(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('images/trophy.png')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position
        def draw(self, screen):
            screen.blit(self.image, self.rect)

    trophies = [Trophy((285,0))]
    trophy_group = pygame.sprite.RenderPlain(*trophies)

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    image = pygame.transform.scale(carImg, (20, 27))
    car = CarSprite(image, (10, display_height-20))
    car_group = pygame.sprite.RenderPlain(car)

    can_crash_sound = True

    #THE GAME LOOP
    while 1:
        #USER INPUT
        t1 = time.time()
        dt = t1-t0
        
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN 
            if win_condition == None: 
                if event.key == K_RIGHT: car.k_right = down * -6
                if event.key == K_LEFT: car.k_left = down * 6
                if event.key == K_UP: car.k_up = down * 2
                if event.key == K_DOWN: car.k_down = down * -2 
                if event.key == K_ESCAPE: game_intro() # quit the game, go back to main menu
            elif win_condition == True and event.key == K_ESCAPE: game_intro()
            elif win_condition == True and event.key == K_SPACE: racecourse()
            elif win_condition == False:
                if event.key == K_SPACE:
                    can_crash_sound = True
                    racecourse()
                    pygame.mixer.music.unpause()
                    t0 = t1
                if event.key == K_ESCAPE:
                    game_intro()
            elif event.key == K_ESCAPE: sys.exit(0)    
    
        #COUNTDOWN TIMER
        time_allowance = 25
        seconds = round((time_allowance - dt),2)
        record_time = db.get_record(1)
        if win_condition == None:
            timer_text = font.render(str(seconds), True, (0,0,255))
            if seconds <= 0:
                win_condition = False
                timer_text = font.render("Time!", True, (255,0,0))
                loss_text = win_font.render('Press Space to Retry', True, (255,0,0))
            
    
        #RENDERING
        screen.fill((255,255,255))
        car_group.update(deltat)
        collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, collided = None)
        if collisions != {}:
            win_condition = False
            timer_text = font.render("Crash!", True, (255,0,0))
            pygame.mixer.music.pause()
            if can_crash_sound == True and snd_muted == False:
                pygame.mixer.Sound.play(crash_sound)
                can_crash_sound = False
            car.image = pygame.image.load('images/collision.png')
            loss_text = win_font.render('Space to Retry, Escape to home', True, (255,0,0))
            seconds = 0
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            car.k_right = 0
            car.k_left = 0

        trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
        if trophy_collision != {}:
            seconds = seconds
            timer_text = font.render("Finished!", True, (0,255,0))
            win_condition = True
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            time_taken = time_allowance - seconds
            if record_time > time_taken:
                record_time = time_taken
            print(" ")
            print("Record Time:" + str(record_time))
            print("Time taken:" + str(time_taken))
            db.update_record(1, record_time)
            win_text = win_font.render('Escape to home, Space to play', True, (0,255,0))
            if win_condition == True:
                car.k_right = -5
                

        pad_group.update(collisions)
        pad_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (20,40))
        screen.blit(win_text, (180, 550))
        screen.blit(loss_text, (180, 550))
        pygame.display.flip()

game_intro()
pygame.quit()
quit()

    


