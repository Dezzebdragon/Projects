import tkinter
from tkinter import *
from random import *
import time as t
import winsound
import pygame
from PIL import ImageTk,Image

root = Tk()
cwidth = 500
cheight = 650
delitel_platformy = 4
platform_lenght = cheight / delitel_platformy
back = "white"

c = tkinter.Canvas(root, width=cwidth, height=cheight, bg=back)
c.pack()

seconds = t.time()
pygame.init()

boss_music = pygame.mixer.Sound("boss_music.wav")
death = pygame.mixer.Sound("death.wav")
hit = pygame.mixer.Sound("hit.wav")
laser_charge = pygame.mixer.Sound("laser_charge.wav")
shield_down = pygame.mixer.Sound("shield_down.wav")
shield_up = pygame.mixer.Sound("shield_up.wav")
pick_up = pygame.mixer.Sound("pick_up.wav")
takes_damage = pygame.mixer.Sound("takes_damage.wav")



jx = randrange (0,2)
if jx == 0:
    pygame.mixer.music.load("Hotline_Miami_2_(Run).wav")
if jx == 1:
    pygame.mixer.music.load("Hotline_Miami_2_(She_Swallowed_Burning_Coals).wav")
pygame.mixer.music.set_volume(0.15)
vuv = 1
vyv = 1


if vuv + vyv == 2:
    pygame.mixer.music.play(-1)


base_speed = 40
speed = base_speed
time_to_ten = 0
pocet_bodov = 0
enemy_x = randrange(300)
enemy_y = 0
mys_x = 150
mys_y = 250
e_width = 20
e_height = 20
background_movespeed = (0.5)

#enemy hp
e_hp_base = 100
e_hp = e_hp_base
e_hp_y = 10
#player hp
critical_condition = 20
s_hp_base = 100
s_hp = 100
s_hp_y =  -30
sh_lifetime = 0
#dmg
crash_dmg = 50
ep_dmg = 20
ep_x = enemy_x + (e_width / 2)
ep_y = enemy_y + (e_height / 2)
#shield
shield_hp_y = - 60
shield_hp_base = 200
shield_hp = shield_hp_base
shield_load_per = 0
cumcum = 0
num_of_kills_to_acctivate = 10
num_kill = num_of_kills_to_acctivate * 10
#hp heling
hp_heal = 30
hp_pickup_count = 0
sh_pickup_count = 0
#player:
ship_speed = 5

#enemy_projectile
def ep(x,y):
    global projectile_distance_x,projectile_distance_y
    ep_x = enemy_x + (e_width / 2)
    ep_y = enemy_y + (e_height / 2)

    # calculating distance between projectile and ship
    if ep_x >= mys_x:
        projectile_distance_x = ep_x - mys_x
        #print (projectile_distance_x)
    elif ep_x <= mys_x:
        projectile_distance_x = mys_x - ep_x
        #print (projectile_distance_x)

    if ep_y >= mys_y:
        projectile_distance_y = ep_y - mys_y
        #print (projectile_distance_y)
    elif ep_y <= mys_y:
        projectile_distance_y = mys_y - ep_y
        #print (projectile_distance_y)

spawnable_sp_x = 0
spawnable_sp_y = 0
ep(ep_x, ep_y)
one_sec = 0
ep_lifetime = 125  #(time in seonds * 1000 / speed) (3,5s)
shield_lifetime = 250 #(time in seonds * 1000 / speed) (10 s)
damage = True
score = 0
paused = False
five_sec = False
timer_countdown = False
shield_timer_countdown = False
ep_existance = False
crash_possibility = True
shield_existance = False
player_existance = True
hp_sp = False
btn = False
speed_multiplier = 10    
move_speed_x = 0
move_speed_y = 0

enemy_small_img = ImageTk.PhotoImage(Image.open("enemy_small.png"))

def enemy (x,y):
    global e_hp
    c.create_rectangle(x,y,x+e_width,y+e_height,fill="white", tags="deletable")
    c.create_text(x,y - e_hp_y,text="HP:", tags="deletable",fill="white")
    c.create_text(x+20,y - e_hp_y,text=e_hp, tags="deletable",fill="white")

def shield_info(shield_load_per):
    c.create_text(50,10,text="shield_info:", tags="deletable",fill="white")
    c.create_text(cwidth / 4,10,text=shield_load_per, tags="deletable",fill="white")
    c.create_text(cwidth / 4 + 15,10,text='%', tags="deletable",fill="white")

def shield(x,y):
    global ship_shield_width, ship_shield_width, shield_hp
    ship_shield_width = 30
    c.create_oval(x - ship_shield_width, y - ship_shield_width, x + ship_shield_width, y + ship_shield_width, tags="deletable_shield", fill="cyan")
    c.create_text(x,y - shield_hp_y,text="Shield:", tags="deletable_shield",fill="white")
    c.create_text(x+30,y - shield_hp_y,text=shield_hp, tags="deletable_shield",fill="white")

projectile_trajectory_img = ImageTk.PhotoImage(Image.open("bullets.png"))

def projectile_trajectory(x,y):
    c.create_image(x, y - cheight, anchor=NW, image=projectile_trajectory_img, tags='deletable_ship')



ship_img = ImageTk.PhotoImage(Image.open("ship.png"))

def ship(x,y):
    global ship_width, ship_height, s_hp
    ship_width = 18
    ship_height = 20
    c.create_image(x - ship_width, y - ship_height, anchor=NW, image=ship_img, tags='deletable_ship')
    c.create_text(x,y - s_hp_y,text="HP:", tags="deletable_ship",fill="white" )
    c.create_text(x+20,y - s_hp_y,text=s_hp, tags="deletable_ship",fill="white")
    
def pravo_dole():
    global ep_x,ep_y
    c.create_oval(ep_x,ep_y,ep_x + 10,ep_y+10,fill="white", tags="deletable_ep")
    move_speed_x = projectile_distance_x / speed_multiplier
    ep_x = ep_x + move_speed_x
    move_speed_y = projectile_distance_y / speed_multiplier
    ep_y = ep_y + move_speed_y

def pravo_hore():
    global ep_x,ep_y
    c.create_oval(ep_x,ep_y,ep_x + 10,ep_y+10,fill="white", tags="deletable_ep")
    move_speed_x = projectile_distance_x / speed_multiplier
    ep_x = ep_x + move_speed_x
    move_speed_y = projectile_distance_y / speed_multiplier
    ep_y = ep_y - move_speed_y

def lavo_hore():
    global ep_x,ep_y
    c.create_oval(ep_x,ep_y,ep_x + 10,ep_y+10,fill="white", tags="deletable_ep")
    move_speed_x = projectile_distance_x / speed_multiplier
    ep_x = ep_x - move_speed_x
    move_speed_y = projectile_distance_y / speed_multiplier
    ep_y = ep_y - move_speed_y
    
def lavo_dole():
    global ep_x,ep_y
    c.create_oval(ep_x,ep_y,ep_x + 10,ep_y+10,fill="white", tags="deletable_ep")
    move_speed_x = projectile_distance_x / speed_multiplier
    ep_x = ep_x - move_speed_x
    move_speed_y = projectile_distance_y / speed_multiplier
    ep_y = ep_y + move_speed_y
    
def delete_ep():
    ep_x = randrange(0, cwidth) 
    ep_y = 20


#health spawn 

def spawnable_sp(x,y):
    global spawnable_spawn, spawnable_sp_x, spawnable_sp_y,hp_sp
    spawnable_spawn = randrange(0,20)
    if spawnable_spawn == 1:
        hp_sp = True
        spawnable_sp_x = enemy_x
        spawnable_sp_y = enemy_y

        
########################################################################################################################################
########################################################################################################################################

background_img_x = 0
background_img_y = -5850

background_img = ImageTk.PhotoImage(Image.open("test.jpg"))

def timer():
    c.delete("deletable")
    c.delete('deletable_ep')
    c.delete('deletable_ship')
    c.delete('deletable_shield')
    c.delete('deletable_background')
    global background_movespeed, paused, base_speed,five_sec, ship_speed, spawnable_move, background_img_y, sh_pickup_count,hp_pickup_count, sh_lifetime, player_existance, one_sec, cumcum,critical_condition, times_to_ten, shield_timer_countdown, shield_load_per2,shield_load_per,btn, sh_sp, hp_sp,hp_heal,spawnable_spawn, spawnable_sp_x, spawnable_sp_y, timer_countdown,ep_lifetime, time_to_ten, shield_hp_base,shield_existance, ship_shield_width, ship_shield_width, shield_hp, score, crash_possibility, crash_dmg, ep_dmg, damage, s_hp, enemy_x, enemy_y, pocet_bodov, speed,back,delitel_platformy, e_hp, move_speed_y, move_speed_x,ep_x, ep_y, ep_existance,projectile_distance_x,projectile_distance_y, ship_width, ship_height
    
    background_img_y = background_img_y + background_movespeed
    background_img2 = c.create_image(background_img_x, background_img_y, anchor=NW, image=background_img, tags='deletable_background')
    #print(background_img_y)

    
    

    if hp_sp == True:
        c.delete('deletable_hp_spawn')
        spawnable_sp_y = spawnable_sp_y + ship_speed
        c.create_oval(spawnable_sp_x,spawnable_sp_y ,spawnable_sp_x+10,spawnable_sp_y+10,fill="red" ,tags="deletable_hp_spawn")
        #print(spawnable_sp_y)
    
#shield existance
    if shield_existance == True:
        shield(mys_x, mys_y)
        shield_timer_countdown = True

    if shield_existance == False:
        c.delete('deletable_shield')

    enemy_y = enemy_y + ship_speed
    enemy(enemy_x, enemy_y)
    ship(mys_x, mys_y)
    shield_info(shield_load_per)
    sh_lifetime = sh_lifetime + 1


    if ep_existance == True:
        timer_countdown = True

#ship shield lifetime
    if shield_timer_countdown == True:
        times_to_ten = times_to_ten +1
        if times_to_ten >= (shield_lifetime):
            winsound.PlaySound('shield_disabled.wav', winsound.SND_ASYNC)
            shield_existance = False
            c.delete('deletable_shield')
            shield_timer_countdown = False
            cumcum = 0
    elif shield_timer_countdown == False:
        times_to_ten = 0
        

#ep lifetime
    if timer_countdown == True:
        time_to_ten = time_to_ten + 1
        if time_to_ten == (ep_lifetime):
            ep_existance = False
            c.delete('deletable_ep')
            ep_x = randrange(0, cwidth) 
            ep_y = 20
            time_to_ten = 0
            timer_countdown = False
            cumcum = 0
    elif timer_countdown == False:
        time_to_ten = 0



    if ep_existance == False:
        move_speed_x = 0
        move_speed_y = 0

    if ep_existance == True:
        global projectile_distance_x, projectile_distance_y

        if ep_x >= mys_x and ep_y >= mys_y:
            projectile_distance_x = ep_x - mys_x
            projectile_distance_y = ep_y - mys_y
            #print ('lavo-hore')
            lavo_hore()            
        elif ep_x >= mys_x and ep_y <= mys_y:
            projectile_distance_x = ep_x - mys_x
            projectile_distance_y = mys_y - ep_y
            #print ('lavo-dole')
            lavo_dole()                
        elif ep_x <= mys_x and ep_y >= mys_y:
            projectile_distance_x = mys_x - ep_x
            projectile_distance_y = ep_y - mys_y
            #print ('pravo-hore')
            pravo_hore()
        elif ep_x <= mys_x and ep_y <= mys_y:
            projectile_distance_x = mys_x - ep_x
            projectile_distance_y = mys_y - ep_y
            #print ('pravo-dole')
            pravo_dole()


# hit-reg of the player 
    if enemy_x <= mys_x <= enemy_x + e_width and mys_y > enemy_y:
        global e_hp_base, sh_sp
        if damage == True:
            projectile_trajectory(mys_x, mys_y)
            e_hp = e_hp - 10
            pygame.mixer.Sound.play(hit)          
        if e_hp <= 0:
            spawnable_sp(enemy_x, enemy_y)
            enemy_x = randrange(0, cwidth) 
            enemy_y = 20
            pocet_bodov = pocet_bodov +1
            shield_load_per = shield_load_per + 5
            if e_hp < e_hp_base:
                e_hp_lost = e_hp_base - e_hp 
                e_hp = e_hp + e_hp_lost
                ep_existance = True
                timer_countdown = False
                

    if shield_load_per >= num_kill:
        c.create_text(cwidth / 2,cheight / 2 + 70,text='SHIELD READY!', tags="deletable",fill="white")
        c.create_text(cwidth / 2,cheight / 2 + 85,text='PRESS S TO ACTIVATE!', tags="deletable",fill="white")



# spawnable hp drop
    if player_existance == True:       
        if spawnable_sp_x < mys_x - ship_width < spawnable_sp_x + 10 and spawnable_sp_y < mys_y - ship_height < spawnable_sp_y + 10 or spawnable_sp_x < mys_x + ship_width < spawnable_sp_x + 10 and spawnable_sp_y < mys_y + ship_height < spawnable_sp_y + 10 or spawnable_sp_x < mys_x - ship_width < spawnable_sp_x + 10 and spawnable_sp_y < mys_y + ship_height < spawnable_sp_y + 10 or spawnable_sp_x < mys_x + ship_width < spawnable_sp_x + 10 and spawnable_sp_y < mys_y - ship_height < spawnable_sp_y + 10 or spawnable_sp_x < mys_x < spawnable_sp_x + 10 and spawnable_sp_y < mys_y < spawnable_sp_y + 10 or spawnable_sp_x < mys_x < spawnable_sp_x + 10 and spawnable_sp_y < mys_y < spawnable_sp_y + 10 or spawnable_sp_x < mys_x < spawnable_sp_x + 10 and spawnable_sp_y < mys_y < spawnable_sp_y + 10 or spawnable_sp_x < mys_x < spawnable_sp_x + 10 and spawnable_sp_y < mys_y < spawnable_sp_y + 10:
            pygame.mixer.Sound.play(pick_up)
            c.delete('deletable_hp_spawn')
            hp_sp = False
            s_hp = s_hp + hp_heal
            hp_pickup_count = hp_pickup_count + 1
            if s_hp > s_hp_base:
                s_hp = s_hp_base
                if s_hp == s_hp_base:
                    winsound.PlaySound('health_restored.wav', winsound.SND_ASYNC)
                    #print('healt restored')
            spawnable_sp_x = -100 
            spawnable_sp_y = -100
        

    if enemy_y > cheight:
        enemy_x = randrange(0, cwidth) 
        enemy_y = 20
        if e_hp < e_hp_base:
            e_hp_lost = e_hp_base - e_hp 
            e_hp = e_hp + e_hp_lost
        
#projectile hits the ship
    if mys_x - ship_width <= ep_x <= mys_x + ship_width and mys_y - ship_height <= ep_y <= mys_y + ship_height:
        pygame.mixer.Sound.play(takes_damage)
        if shield_existance == True:
            shield_hp = shield_hp - ep_dmg * (1.5)
            c.delete('deletable_ep')
            ep_x = randrange(0, cwidth) 
            ep_y = 20
            ep_existance = False
            timer_countdown = False
        elif shield_existance == False:
            s_hp = s_hp - ep_dmg
            if 0 < s_hp <= critical_condition:
                px = randrange (0,2)
                if px == 0:
                    winsound.PlaySound('critical_damage.wav', winsound.SND_ASYNC)
                if px == 1:
                    winsound.PlaySound('hull_in_critical_condition.wav', winsound.SND_ASYNC)
            c.delete('deletable_ep')
            ep_x = randrange(0, cwidth) 
            ep_y = 20
            ep_existance = False
            timer_countdown = False
        
# ship crashes into the enemy
    if player_existance == True: 
        if enemy_x < mys_x - ship_width < enemy_x + e_width and enemy_y < mys_y - ship_height < enemy_y + e_height or enemy_x < mys_x + ship_width < enemy_x + e_width and enemy_y < mys_y - ship_height < enemy_y + e_height or enemy_x < mys_x + ship_width < enemy_x + e_width and enemy_y < mys_y + ship_height < enemy_y + e_height or enemy_x < mys_x - ship_width < enemy_x + e_width and enemy_y < mys_y + ship_height < enemy_y + e_height:
            pygame.mixer.Sound.play(takes_damage)
            if shield_existance == True:
                shield_hp = shield_hp - crash_dmg * (1.5)
                #print('crash!')
                if crash_possibility == True:
                    enemy_x = randrange(0, cwidth) 
                    enemy_y = 20
                    if e_hp < e_hp_base:
                        e_hp_lost = e_hp_base - e_hp 
                        e_hp = e_hp + e_hp_lost
            elif shield_existance == False:
                s_hp = s_hp - crash_dmg
                p = randrange (0,1)
                if p == 0:
                    winsound.PlaySound('critical_damage.wav', winsound.SND_ASYNC)
                else:
                    print('critical_dmg')
                if 0 < s_hp <= critical_condition:
                    px = randrange (0,2)
                    if px == 0:
                        winsound.PlaySound('critical_damage.wav', winsound.SND_ASYNC)
                    if px == 1:
                        winsound.PlaySound('hull_in_critical_condition.wav', winsound.SND_ASYNC)
                #print('crash!')
                if crash_possibility == True:
                    enemy_x = randrange(0, cwidth) 
                    enemy_y = 20
                    if e_hp < e_hp_base:
                        e_hp_lost = e_hp_base - e_hp 
                        e_hp = e_hp + e_hp_lost

    if shield_hp <= 0:
        pygame.mixer.Sound.play(shield_down)
        shield_existance = False
        c.delete('deletable_shield')
        shield_hp_lost = shield_hp_base - shield_hp 
        shield_hp = shield_hp + shield_hp_lost

    if spawnable_sp_y >= cheight:
        hp_sp = False

# player dies:

    if s_hp <= 0:
        paused = False
        player_existance = False
        hp_sp = False
        one_sec = one_sec + 1
        if one_sec == 5:
            pygame.mixer.Sound.play(death)
        if one_sec == 25:
            winsound.PlaySound('game_over.wav', winsound.SND_ASYNC)
            score = (pocet_bodov * 300) + sh_lifetime + (hp_pickup_count * 200) + (sh_pickup_count * 200)
        if one_sec >= 25:
            c.create_text(cwidth / 2,cheight / 2,text="GAME OVER!", tags="deletable",fill="white")
            c.create_text(cwidth / 2,cheight / 2 + 15,text="Score:", tags="deletable",fill="white")
            c.create_text(cwidth / 2 + 50,cheight / 2 + 15,text=score, tags="deletable",fill="white")
        if one_sec >= 125:
            five_sec = True
            c.create_text(cwidth / 2,cheight / 2 + 50 ,text="PRESS R TO RESTART", tags="deletable",fill="white")
        damage = False
        c.delete('deletable_ship')
        c.delete('deletable_shield')
        pygame.mixer.music.fadeout(5000)
        ep_existance = False
        timer_countdown = False
        crash_possibility = False
        
    if cumcum == 1:
        times_to_ten = times_to_ten +1
        shield_existance = True
        shield_load_per = 0
    
    c.after(speed, timer)

def bruh(cooridinates):
    global pocet_bodov, mys_x, mys_y
    mys_x = cooridinates.x
    mys_y = cooridinates.y
    #print (mys_x)
    #print (mys_y)
    enemy(enemy_x, enemy_y)
    
def click(z):
    
    global background_movespeed, paused, base_speed,five_sec, ship_speed, spawnable_move, background_img_y, sh_pickup_count,hp_pickup_count, sh_lifetime, player_existance, one_sec, cumcum,critical_condition, times_to_ten, shield_timer_countdown, shield_load_per2,shield_load_per,btn, sh_sp, hp_sp,hp_heal,spawnable_spawn, spawnable_sp_x, spawnable_sp_y, timer_countdown,ep_lifetime, time_to_ten, shield_hp_base,shield_existance, ship_shield_width, ship_shield_width, shield_hp, score, crash_possibility, crash_dmg, ep_dmg, damage, s_hp, enemy_x, enemy_y, pocet_bodov, speed,back,delitel_platformy, e_hp, move_speed_y, move_speed_x,ep_x, ep_y, ep_existance,projectile_distance_x,projectile_distance_y, ship_width, ship_height

    cum = z.char
    if cum=='s':      
        if shield_load_per >= num_kill:
            sh_pickup_count = sh_pickup_count + 1
            p = randrange (0,5)
            if p == 0:
                winsound.PlaySound('shield_active.wav', winsound.SND_ASYNC)
            if p == 1:
                winsound.PlaySound('defence_active.wav', winsound.SND_ASYNC)
            if p == 2:
                print('shield')
            if p == 3:
                winsound.PlaySound('active_defence_systems_engaged.wav', winsound.SND_ASYNC)
            if p == 4:
                winsound.PlaySound('defence_online.wav', winsound.SND_ASYNC)
            shield_existance = True
            cumcum = 1

#pause
    if cum=='p' and paused == False and s_hp > 0:
        paused = True
        speed = 0
        damage = False
        background_movespeed = 0
        ship_speed = 0
        times_to_ten = times_to_ten + 0


#unpause
    elif cum=='p' and paused == True and s_hp > 0:
        paused = False
        speed = base_speed
        damage = True
        background_movespeed = (0.5)
        ship_speed = 5
        times_to_ten = times_to_ten +1

        
    if cum=='r' and s_hp <= 0 and five_sec == True:
        
        c.delete("deletable")
        c.delete('deletable_ep')
        c.delete('deletable_ship')
        c.delete('deletable_shield')
        c.delete('deletable_background')
        background_img_y = -5850
        time_to_ten = 0
        pocet_bodov = 0
        background_movespeed = (0.5)
        enemy_x = randrange(300)
        enemy_y = 0
        s_hp = s_hp_base
        mys_x = 150
        mys_y = 250
        sh_lifetime = 0
        shield_load_per = 0
        cumcum = 0
        hp_pickup_count = 0
        sh_pickup_count = 0
        def ep(x,y):
            global projectile_distance_x,projectile_distance_y
            ep_x = enemy_x + (e_width / 2)
            ep_y = enemy_y + (e_height / 2)

            # calculating distance between projectile and ship
            if ep_x >= mys_x:
                projectile_distance_x = ep_x - mys_x
                #print (projectile_distance_x)
            elif ep_x <= mys_x:
                projectile_distance_x = mys_x - ep_x
                #print (projectile_distance_x)

            if ep_y >= mys_y:
                projectile_distance_y = ep_y - mys_y
                #print (projectile_distance_y)
            elif ep_y <= mys_y:
                projectile_distance_y = mys_y - ep_y
                #print (projectile_distance_y)

        one_sec = 0
        damage = True
        score = 0
        five_sec = False
        timer_countdown = False
        shield_timer_countdown = False
        ep_existance = False
        crash_possibility = True
        shield_existance = False
        player_existance = True
        hp_sp = False
        move_speed_x = 0
        move_speed_y = 0
        jx = randrange (0,2)
        if jx == 0:
            pygame.mixer.music.load("Hotline_Miami_2_(Run).wav")
        if jx == 1:
            pygame.mixer.music.load("Hotline_Miami_2_(She_Swallowed_Burning_Coals).wav")
        pygame.mixer.music.set_volume(0.15)
        vuv = 1
        vyv = 1


        if vuv + vyv == 2:
            pygame.mixer.music.play(-1)
        
  

timer()
c.bind("<Motion>", bruh)
c.bind_all('<Key>', click)
root.mainloop()
