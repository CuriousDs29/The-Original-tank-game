import pgzrun
from random import randint
from pygame import Rect

# ============================
#   HD SETTINGS (1280x720)
# ============================
WIDTH = 1280
HEIGHT = 720

# ============================
#   GAME STATE
# ============================
shake_x = 0
shake_y = 0
shake_timer = 0
shake_power = 0  # required for shake

def screen_shake(power=12, duration=20):
    global shake_timer, shake_power
    shake_timer = duration
    shake_power = power

# ============================
#   MUSIC
# ============================
music.play_once("music1")
music.queue("music2")
music.queue("music3")

# ============================
#   PLAYER
# ============================
tank1 = Actor("tank3")
tank1.x = WIDTH // 2
tank1.bottom = HEIGHT - 40
tank1.ammo = 20
tank1.nuke = 1
tank1.points = 0
tank1.health = 50
tank1.max_health = 50
tank1.level = 1
tank1.gameover = False

# ============================
#   PICKUPS
# ============================
health_pickup = Actor("health")
health_pickup.x = randint(50, WIDTH - 50)
health_pickup.y = -200

ammo_box = Actor("box")
ammo_box.x = randint(50, WIDTH - 50)
ammo_box.y = -400

nuke_pickup = Actor("nuke")
nuke_pickup.x = randint(50, WIDTH - 50)
nuke_pickup.y = -600

# ============================
#   PROJECTILES
# ============================
missile1 = Actor("missile")
missile1.y = -200

nuke_proj = Actor("nuke")
nuke_proj.y = -200

missile2 = Actor("m2")
missile3 = Actor("m2")
missile4 = Actor("m2")
boss_missile = Actor("m2")

for m in [missile2, missile3, missile4, boss_missile]:
    m.y = -200

# ============================
#   ENEMIES
# ============================
tank2 = Actor("tank2")
tank2.x = randint(50, WIDTH - 50)
tank2.y = -200

tank3 = Actor("tank4")
tank3.x = randint(50, WIDTH - 50)
tank3.y = -400

tank4 = Actor("tank5")
tank4.x = randint(50, WIDTH - 50)
tank4.y = -600

# ============================
#   BOSS
# ============================
boss = Actor("boss")
boss.x = WIDTH // 2
boss.y = 140
boss.health = 100
boss_max_health = 100
boss_active = False
boss_dead = False
boss_direction = 1

# ============================
#   BACKGROUND & UI
# ============================
bg = Actor("level1")
gameover_screen = Actor("gameover")
youwin_screen = Actor("youwin")

# ============================
#   EXPLOSIONS
# ============================
explosions = []

def spawn_explosion(x, y, size=1.0):
    exp = Actor("explosion")  # file must be explosion.png
    exp.pos = (x, y)
    exp._scale = size
    explosions.append({"actor": exp, "timer": 20})
    screen_shake(18, 25)

# ============================
#   HELPER FUNCTIONS
# ============================
def aim_at_player(missile, shooter, speed):
    dx = tank1.x - shooter.x
    dy = tank1.y - shooter.y
    dist = max(1, (dx*dx + dy*dy)**0.5)
    missile.x += dx / dist * speed
    missile.y += dy / dist * speed

def reset_enemy(enemy):
    enemy.y = -200
    enemy.x = randint(50, WIDTH - 50)

def out_of_bounds(actor):
    return (
        actor.x < -100 or actor.x > WIDTH + 100 or
        actor.y < -100 or actor.y > HEIGHT + 100
    )

# ============================
#   DRAW
# ============================
def draw():
    global shake_x, shake_y

    if shake_timer > 0:
        shake_x = randint(-shake_power, shake_power)
        shake_y = randint(-shake_power, shake_power)
    else:
        shake_x = shake_y = 0

    screen.blit(bg.image, (shake_x, shake_y))

    screen.draw.text(f"Ammo: {tank1.ammo}", (20, 20), color="white")
    screen.draw.text(f"Points: {tank1.points}", (20, 60), color="white")
    screen.draw.text(f"Nukes: {tank1.nuke}", (20, 100), color="white")

    screen.draw.filled_rect(Rect((20, 150), (300, 25)), "red")
    ratio = tank1.health / tank1.max_health
    screen.draw.filled_rect(Rect((20, 150), (300 * ratio, 25)), "green")

    tank1.draw()
    if not boss_active:
        tank2.draw()
        if tank1.points > 30:
            tank3.draw()
        if tank1.points > 50:
            tank4.draw()

    health_pickup.draw()
    ammo_box.draw()
    nuke_pickup.draw()

    missile1.draw()
    nuke_proj.draw()
    missile2.draw()
    missile3.draw()
    missile4.draw()
    boss_missile.draw()

    if boss_active and not boss_dead:
        boss.draw()
        screen.draw.filled_rect(Rect((WIDTH - 350, 20), (300, 25)), "red")
        boss_ratio = boss.health / boss_max_health
        screen.draw.filled_rect(Rect((WIDTH - 350, 20), (300 * boss_ratio, 25)), "yellow")

    for e in explosions:
        e["actor"].draw()

    if tank1.gameover:
        if boss_dead:
            youwin_screen.draw()
        else:
            gameover_screen.draw()

# ============================
#   UPDATE
# ============================
def update():
    global boss_active, shake_timer

    if tank1.gameover:
        return

    if shake_timer > 0:
        shake_timer -= 1

    update_level()
    update_player()
    update_projectiles()
    update_enemies()
    update_enemy_shooting()
    update_boss()
    update_pickups()
    update_explosions()

    # player death
    if tank1.health <= 0 and not boss_dead:
        tank1.gameover = True

# ============================
#   LEVEL PROGRESSION
# ============================
def update_level():
    global boss_active

    p = tank1.points

    if p > 150:
        boss_active = True
        bg.image = "level5"
    elif p > 110:
        bg.image = "level4"
    elif p > 50:
        bg.image = "level3"
    elif p > 30:
        bg.image = "level2"
    else:
        bg.image = "level1"

# ============================
#   PLAYER MOVEMENT
# ============================
def update_player():
    if keyboard.left: tank1.x -= 6
    if keyboard.right: tank1.x += 6
    if keyboard.up: tank1.y -= 6
    if keyboard.down: tank1.y += 6

    tank1.x = max(40, min(WIDTH - 40, tank1.x))
    tank1.y = max(40, min(HEIGHT - 40, tank1.y))

# ============================
#   PROJECTILES
# ============================
def update_projectiles():
    # Player missile
    missile1.y -= 22
    if missile1.bottom < 0:
        missile1.y = -200

    # Player missile hits enemies
    if missile1.colliderect(tank2) and not boss_active:
        spawn_explosion(tank2.x, tank2.y, 1.5)
        reset_enemy(tank2)
        tank1.points += 1
        missile1.y = -200

    if tank1.points > 30 and missile1.colliderect(tank3) and not boss_active:
        spawn_explosion(tank3.x, tank3.y, 1.5)
        reset_enemy(tank3)
        tank1.points += 5
        missile1.y = -200

    if tank1.points > 50 and missile1.colliderect(tank4) and not boss_active:
        spawn_explosion(tank4.x, tank4.y, 1.5)
        reset_enemy(tank4)
        tank1.points += 10
        missile1.y = -200

    # Player missile hits boss
    if boss_active and missile1.colliderect(boss):
        spawn_explosion(boss.x, boss.y, 1.5)
        boss.health -= 5
        missile1.y = -200

    # Nuke
    nuke_proj.y -= 28
    if nuke_proj.bottom < 0:
        nuke_proj.y = -200

    # Nuke effect (detonate near top)
    if 0 < nuke_proj.y < HEIGHT // 3:
        spawn_explosion(nuke_proj.x, nuke_proj.y, 2.5)
        tank1.points += 20
        if boss_active:
            boss.health -= 25
        nuke_proj.y = -200

# ============================
#   ENEMY MOVEMENT
# ============================
def update_enemies():
    if boss_active:
        return

    tank2.y += 5
    if tank2.y > HEIGHT:
        reset_enemy(tank2)

    if tank1.points > 30:
        tank3.y += 6
        if tank3.y > HEIGHT:
            reset_enemy(tank3)

    if tank1.points > 50:
        tank4.y += 7
        if tank4.y > HEIGHT:
            reset_enemy(tank4)

# ============================
#   ENEMY SHOOTING (DAMAGES PLAYER)
# ============================
def update_enemy_shooting():
    if boss_active:
        return

    # tank2 missile
    if tank2.y > 0 and missile2.y < 0 and randint(0, 40) == 0:
        missile2.pos = tank2.pos
    if missile2.y > 0:
        aim_at_player(missile2, tank2, 6)

        if missile2.colliderect(tank1):
            spawn_explosion(tank1.x, tank1.y, 1.5)
            tank1.health -= 5
            missile2.y = -200

        if out_of_bounds(missile2):
            missile2.y = -200

    # tank3 missile
    if tank1.points > 30 and tank3.y > 0 and missile3.y < 0 and randint(0, 35) == 0:
        missile3.pos = tank3.pos
    if missile3.y > 0:
        aim_at_player(missile3, tank3, 7)

        if missile3.colliderect(tank1):
            spawn_explosion(tank1.x, tank1.y, 1.5)
            tank1.health -= 7
            missile3.y = -200

        if out_of_bounds(missile3):
            missile3.y = -200

    # tank4 missile
    if tank1.points > 50 and tank4.y > 0 and missile4.y < 0 and randint(0, 30) == 0:
        missile4.pos = tank4.pos
    if missile4.y > 0:
        aim_at_player(missile4, tank4, 8)

        if missile4.colliderect(tank1):
            spawn_explosion(tank1.x, tank1.y, 1.5)
            tank1.health -= 10
            missile4.y = -200

        if out_of_bounds(missile4):
            missile4.y = -200

# ============================
#   BOSS (DAMAGES PLAYER)
# ============================
def update_boss():
    global boss_direction, boss_dead

    if not boss_active:
        return

    if boss.health <= 0:
        boss_dead = True
        tank1.gameover = True
        spawn_explosion(boss.x, boss.y, 3.0)
        return

    boss.x += boss_direction * 5
    if boss.left < 50 or boss.right > WIDTH - 50:
        boss_direction *= -1

    if boss_missile.y < 0:
        boss_missile.pos = boss.pos

    aim_at_player(boss_missile, boss, 9)

    if boss_missile.colliderect(tank1):
        spawn_explosion(tank1.x, tank1.y, 2.0)
        tank1.health -= 15
        boss_missile.y = -200

    if out_of_bounds(boss_missile):
        boss_missile.y = -200

# ============================
#   PICKUPS
# ============================
def update_pickups():
    for p in [health_pickup, ammo_box, nuke_pickup]:
        p.y += 4
        if p.y > HEIGHT:
            p.y = -200
            p.x = randint(50, WIDTH - 50)

    if health_pickup.colliderect(tank1):
        tank1.health = min(tank1.max_health, tank1.health + 10)
        health_pickup.y = -200

    if ammo_box.colliderect(tank1):
        tank1.ammo += 5
        ammo_box.y = -200

    if nuke_pickup.colliderect(tank1):
        tank1.nuke += 1
        nuke_pickup.y = -200

# ============================
#   EXPLOSIONS
# ============================
def update_explosions():
    for e in explosions[:]:
        e["timer"] -= 1
        if e["timer"] <= 0:
            explosions.remove(e)

# ============================
#   INPUT
# ============================
def on_key_down(key):
    if key == keys.SPACE and missile1.bottom < 0 and tank1.ammo > 0:
        missile1.pos = tank1.pos
        tank1.ammo -= 1

    if key == keys.N and nuke_proj.bottom < 0 and tank1.nuke > 0:
        nuke_proj.pos = tank1.pos
        tank1.nuke -= 1

pgzrun.go()
