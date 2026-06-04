import pgzrun
# Write your code here :-)
from random import randint

WIDTH = 900
HEIGHT = 700
# music
music.play_once("music1")
music.queue("music2")
music.queue("music3")
# Actors
tank1 = Actor("tank3")
tank1.ammo = 20
tank1.nuke = 1
tank1.points = 0
tank1.health = 50
tank1.level = 1
tank1.gameover = False
tank1.x = WIDTH/2
tank1.bottom = HEIGHT
health = Actor("health")
box = Actor("box")
nuke = Actor("nuke")
missile1 = Actor("missile")

tank2 = Actor("tank2")
tank2.x = randint(0, WIDTH)
tank2.y = 0

tank3 = Actor("tank4")
tank3.x = randint(0, WIDTH)
tank3.y = 0

tank4 = Actor("tank5")
tank4.x = randint(0, WIDTH)
tank4.y = 0

missile2 = Actor("m2")

# missile3 = Actor("other nuke")
bg = Actor("level1")
gameover = Actor("gameover")
# draw
def draw():
    bg.draw()
    screen.draw.text(f"Nuke: {tank1.nuke}", (20, 130), color="black")
    screen.draw.text(f"Ammo: {tank1.ammo}", (20, 20), color="black")
    screen.draw.text(f"Points: {tank1.points}", (20, 50), color="black")
    screen.draw.text(f"Health: {tank1.health}", (20, 80), color="black")
    screen.draw.text(f"level: {tank1.level}", (20, 110), color="black")
    tank1.draw()
    health.draw()
    box.draw()
    tank2.draw()
    nuke.draw()
    missile1.draw()
    missile2.draw()
    if tank1.health <= 0:
        tank1.gameover == True
        gameover.draw()
    # missile3.draw()

    if tank1.points > 30:
        tank3.draw()
    if tank1.points > 50:
        tank4.draw()

# def update
def update():
    if tank1.points > 30:
        bg.image = "level2"
        tank3.draw()
        tank1.level = 2
    if tank1.points > 50:
        bg.image = "level3"
        tank1.level = 3
    if tank1.points > 100:
        bg.image = "level3"
        tank1.level = 3
    if tank1.points > 110:
        bg.image = "level4"
        tank1.level = "4"
    if tank1.points > 130:
        bg.image = "level5"
        tank1.level = "5"
    if tank1.points > 150:
        tank1.level = "Boss fight"
    # missile tank1
    missile1.y -= 20
    missile2.x -= 20

    if tank1.ammo < 0:
        print("Can't shoot ammo whomp whomp get some more ammo")
        quit()
    # movement
    if tank2.colliderect(missile1):
        tank2.y = 0
        tank2.x = randint(0, WIDTH)
        tank1.points += 1

    if tank2.colliderect(tank1):
        tank1.gameover == True
        tank2.y = 0
        tank2.x = randint(0, WIDTH)
        tank1.health -= 1

    if tank3.colliderect(missile1):
        tank3.y = 0
        tank3.x = randint(0, WIDTH)
        tank1.points += 5

    if tank3.colliderect(tank1):
        tank1.gameover == True
        tank3.y = 0
        tank3.x = randint(0, WIDTH)
        tank1.health -= 5

    if tank4.colliderect(missile1):
        tank4.y = 0
        tank4.x = randint(0, WIDTH)
        tank1.points += 10

    if tank4.colliderect(tank1):
        tank1.gameover == True
        tank4.y = 0
        tank4.x = randint(0, WIDTH)
        tank1.health -= 10

    tank2.y += 5
    tank3.y += 5
    tank4.y += 5
    if tank2.y > HEIGHT:
        tank2.y = 0
        tank2.x = randint(0, WIDTH)

    if tank3.y > HEIGHT:
        tank3.y = 0
        tank3.x = randint(0, WIDTH)

    if tank4.y > HEIGHT:
        tank4.y = 0
        tank4.x = randint(0, WIDTH)




    if health.colliderect(tank1):
        health.y = 0
        health.x = randint(0, WIDTH)
        tank1.health += 1
    health.y += 5
    if health.y > HEIGHT:
        health.y = 0
        health.x = randint(0, WIDTH)
    if box.colliderect(tank1):
        box.y = 0
        box.x = randint(0, WIDTH)
        tank1.ammo += 1
    box.y += 5
    if box.y > HEIGHT:
        box.y = 0
        box.x = randint(0, WIDTH)
    #nuke
    if nuke.colliderect(tank1):

        nuke.y = 0
        nuke.x = randint(0, WIDTH)
        tank1.nuke += 1
    nuke.y += 5
    if nuke.y > HEIGHT:
        nuke.y = 0
        nuke.x = randint(0, WIDTH)

    # arrow keys
    if keyboard.left:
        tank1.x -= 5
    if keyboard.right:
        tank1.x += 5
    if keyboard.up:
        tank1.y -= 5
    if keyboard.down:
        tank1.y += 5
    # wasd
    if keyboard.w:
        tank1.y -= 5
    if keyboard.a:
        tank1.x -= 5
    if keyboard.d:
        tank1.x += 5
    if keyboard.s:
        tank1.y += 5


def on_key_down(key):
    if key == keys.SPACE and missile1.bottom < 0:
        missile1.pos = tank1.pos
        tank1.ammo -= 1
    if key == keys.N and nuke.bottom < 0 and tank1.nuke > 0 and tank1.ammo > 0:
        nuke.pos = tank1.pos
        tank1.nuke -= 1



if missile2.bottom < 0:
    missile2.pos = tank2.pos

pgzrun.go()