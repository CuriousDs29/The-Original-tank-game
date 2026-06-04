import pgzrun
from random import randint

WIDTH = 900
HEIGHT = 700

# --- MUSIC ---
music.play_once("music1")
music.queue("music2")
music.queue("music3")

# --- PLAYER TANK ---
tank1 = Actor("tank3")
tank1.x = WIDTH / 2
tank1.bottom = HEIGHT
tank1.ammo = 20
tank1.nuke = 1
tank1.points = 0
tank1.health = 50
tank1.max_health = 50
tank1.level = 1
tank1.gameover = False

# --- PICKUPS ---
health_pickup = Actor("health")
health_pickup.x = randint(0, WIDTH)
health_pickup.y = 0

ammo_box = Actor("box")
ammo_box.x = randint(0, WIDTH)
ammo_box.y = -200

nuke_pickup = Actor("nuke")   # falling pickup
nuke_pickup.x = randint(0, WIDTH)
nuke_pickup.y = -400

# --- PROJECTILES ---
missile1 = Actor("missile")   # player missile
missile1.y = -200

nuke_proj = Actor("nuke")     # nuke projectile
nuke_proj.y = -200

missile2 = Actor("m2")        # tank2 missile
missile3 = Actor("m2")        # tank3 missile
missile4 = Actor("m2")        # tank4 missile
boss_missile = Actor("m2")    # boss missile
missile2.y = -200
missile3.y = -200
missile4.y = -200
boss_missile.y = -200

# --- ENEMIES ---
tank2 = Actor("tank2")
tank2.x = randint(0, WIDTH)
tank2.y = 0

tank3 = Actor("tank4")
tank3.x = randint(0, WIDTH)
tank3.y = -200

tank4 = Actor("tank5")
tank4.x = randint(0, WIDTH)
tank4.y = -400

# --- BOSS ---
boss = Actor("boss")  # change image name if needed
boss.x = WIDTH / 2
boss.y = 100
boss.health = 100
boss_active = False
boss_dead = False
boss_direction = 1

# --- BACKGROUND & UI ---
bg = Actor("level1")
gameover_screen = Actor("gameover")
win_screen = Actor("gameover")  # reuse image or change if you have a win screen

# --- EXPLOSIONS ---
explosions = []  # list of dicts: {"actor": Actor, "timer": int}


# --- HELPER FUNCTIONS ---

def aim_at_player(missile, shooter, speed=6):
    dx = tank1.x - shooter.x
    dy = tank1.y - shooter.y
    dist = max(1, (dx * dx + dy * dy) ** 0.5)
    missile.x += dx / dist * speed
    missile.y += dy / dist * speed


def reset_enemy(enemy):
    enemy.y = 0
    enemy.x = randint(0, WIDTH)


def reset_pickup(pickup):
    pickup.y = 0
    pickup.x = randint(0, WIDTH)


def spawn_explosion(x, y):
    exp = Actor("explosion")
    exp.pos = (x, y)
    explosions.append({"actor": exp, "timer": 10})  # 10 frames


def clamp_player_to_screen():
    if tank1.left < 0:
        tank1.left = 0
    if tank1.right > WIDTH:
        tank1.right = WIDTH
    if tank1.top < 0:
        tank1.top = 0
    if tank1.bottom > HEIGHT:
        tank1.bottom = HEIGHT


def check_gameover():
    global boss_dead
    if tank1.health <= 0:
        tank1.gameover = True
    if boss_active and boss.health <= 0 and not boss_dead:
        boss_dead = True
        tank1.gameover = True  # treat boss kill as end of game


# --- DRAW ---

def draw():
    bg.draw()

    # HUD text
    screen.draw.text(f"Ammo: {tank1.ammo}", (20, 20), color="black")
    screen.draw.text(f"Points: {tank1.points}", (20, 50), color="black")
    screen.draw.text(f"Health: {tank1.health}", (20, 80), color="black")
    screen.draw.text(f"Level: {tank1.level}", (20, 110), color="black")
    screen.draw.text(f"Nuke: {tank1.nuke}", (20, 140), color="black")

    # Health bar
    bar_width = 200
    bar_height = 20
    x = 20
    y = 170
    screen.draw.filled_rect(Rect((x, y), (bar_width, bar_height)), "red")
    health_ratio = max(0, tank1.health) / tank1.max_health
    screen.draw.filled_rect(Rect((x, y), (bar_width * health_ratio, bar_height)), "green")

    # Actors
    tank1.draw()
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
        screen.draw.text(f"Boss HP: {boss.health}", (WIDTH - 200, 20), color="black")

    # Explosions
    for e in explosions:
        e["actor"].draw()

    # Game over / win
    if tank1.gameover:
        gameover_screen.draw()
        if boss_dead:
            screen.draw.text(
                "YOU WIN!",
                center=(WIDTH / 2, HEIGHT / 2 - 40),
                fontsize=64,
                color="green",
            )
        else:
            screen.draw.text(
                "GAME OVER",
                center=(WIDTH / 2, HEIGHT / 2 - 40),
                fontsize=64,
                color="red",
            )
        screen.draw.text(
            f"Final Score: {tank1.points}",
            center=(WIDTH / 2, HEIGHT / 2 + 20),
            fontsize=40,
            color="white",
        )


# --- UPDATE ---

def update():
    global boss_active

    if tank1.gameover:
        return

    update_level_and_background()
    update_player_movement()
    update_player_projectiles()
    update_enemy_movement()
    update_enemy_shooting()
    update_boss()
    update_pickups()
    update_explosions()
    clamp_player_to_screen()
    check_gameover()


def update_level_and_background():
    global boss_active
    p = tank1.points

    if p > 150:
        tank1.level = "Boss fight"
        bg.image = "level5"
        boss_active = True
    elif p > 130:
        tank1.level = 5
        bg.image = "level5"
    elif p > 110:
        tank1.level = 4
        bg.image = "level4"
    elif p > 50:
        tank1.level = 3
        bg.image = "level3"
    elif p > 30:
        tank1.level = 2
        bg.image = "level2"
    else:
        tank1.level = 1
        bg.image = "level1"


def update_player_movement():
    # Arrow keys
    if keyboard.left:
        tank1.x -= 5
    if keyboard.right:
        tank1.x += 5
    if keyboard.up:
        tank1.y -= 5
    if keyboard.down:
        tank1.y += 5

    # WASD
    if keyboard.a:
        tank1.x -= 5
    if keyboard.d:
        tank1.x += 5
    if keyboard.w:
        tank1.y -= 5
    if keyboard.s:
        tank1.y += 5


def update_player_projectiles():
    # Player missile
    missile1.y -= 20
    if missile1.bottom < 0:
        missile1.y = -200

    # Nuke projectile
    nuke_proj.y -= 25
    if nuke_proj.bottom < 0:
        nuke_proj.y = -200

    # Missile hits enemies
    if tank2.colliderect(missile1):
        spawn_explosion(tank2.x, tank2.y)
        reset_enemy(tank2)
        tank1.points += 1
        missile1.y = -200

    if tank3.colliderect(missile1) and tank1.points > 30:
        spawn_explosion(tank3.x, tank3.y)
        reset_enemy(tank3)
        tank1.points += 5
        missile1.y = -200

    if tank4.colliderect(missile1) and tank1.points > 50:
        spawn_explosion(tank4.x, tank4.y)
        reset_enemy(tank4)
        tank1.points += 10
        missile1.y = -200

    # Missile hits boss
    if boss_active and not boss_dead and boss.colliderect(missile1):
        spawn_explosion(boss.x, boss.y)
        boss.health -= 5
        missile1.y = -200

    # Nuke effect
    if nuke_proj.y > 0:
        # kill enemies
        if tank2.y > 0:
            spawn_explosion(tank2.x, tank2.y)
            reset_enemy(tank2)
        if tank1.points > 30 and tank3.y > 0:
            spawn_explosion(tank3.x, tank3.y)
            reset_enemy(tank3)
        if tank1.points > 50 and tank4.y > 0:
            spawn_explosion(tank4.x, tank4.y)
            reset_enemy(tank4)

        # damage boss
        if boss_active and not boss_dead and boss.y > 0:
            spawn_explosion(boss.x, boss.y)
            boss.health -= 20

        tank1.points += 15
        nuke_proj.y = -200


def update_enemy_movement():
    # Falling enemies
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

    # Collisions with player
    if tank2.colliderect(tank1):
        spawn_explosion(tank2.x, tank2.y)
        reset_enemy(tank2)
        tank1.health -= 1

    if tank1.points > 30 and tank3.colliderect(tank1):
        spawn_explosion(tank3.x, tank3.y)
        reset_enemy(tank3)
        tank1.health -= 5

    if tank1.points > 50 and tank4.colliderect(tank1):
        spawn_explosion(tank4.x, tank4.y)
        reset_enemy(tank4)
        tank1.health -= 10


def update_enemy_shooting():
    # tank2 missile
    if missile2.y < 0:
        missile2.pos = tank2.pos
    aim_at_player(missile2, tank2, speed=6)
    if out_of_bounds(missile2):
        missile2.y = -200
    if missile2.colliderect(tank1):
        spawn_explosion(tank1.x, tank1.y)
        tank1.health -= 3
        missile2.y = -200

    # tank3 missile
    if tank1.points > 30:
        if missile3.y < 0:
            missile3.pos = tank3.pos
        aim_at_player(missile3, tank3, speed=7)
        if out_of_bounds(missile3):
            missile3.y = -200
        if missile3.colliderect(tank1):
            spawn_explosion(tank1.x, tank1.y)
            tank1.health -= 4
            missile3.y = -200

    # tank4 missile
    if tank1.points > 50:
        if missile4.y < 0:
            missile4.pos = tank4.pos
        aim_at_player(missile4, tank4, speed=8)
        if out_of_bounds(missile4):
            missile4.y = -200
        if missile4.colliderect(tank1):
            spawn_explosion(tank1.x, tank1.y)
            tank1.health -= 5
            missile4.y = -200


def out_of_bounds(actor):
    return actor.x < -50 or actor.x > WIDTH + 50 or actor.y < -50 or actor.y > HEIGHT + 50


def update_boss():
    global boss_direction
    if not boss_active or boss_dead:
        return

    # Move boss horizontally
    boss.x += boss_direction * 4
    if boss.left < 0 or boss.right > WIDTH:
        boss_direction *= -1

    # Boss shooting
    if boss_missile.y < 0:
        boss_missile.pos = boss.pos
    aim_at_player(boss_missile, boss, speed=7)
    if out_of_bounds(boss_missile):
        boss_missile.y = -200
    if boss_missile.colliderect(tank1):
        spawn_explosion(tank1.x, tank1.y)
        tank1.health -= 8
        boss_missile.y = -200


def update_pickups():
    # Health
    health_pickup.y += 5
    if health_pickup.y > HEIGHT:
        reset_pickup(health_pickup)
    if health_pickup.colliderect(tank1):
        tank1.health = min(tank1.max_health, tank1.health + 5)
        reset_pickup(health_pickup)

    # Ammo
    ammo_box.y += 5
    if ammo_box.y > HEIGHT:
        reset_pickup(ammo_box)
    if ammo_box.colliderect(tank1):
        tank1.ammo += 5
        reset_pickup(ammo_box)

    # Nuke pickup
    nuke_pickup.y += 5
    if nuke_pickup.y > HEIGHT:
        reset_pickup(nuke_pickup)
    if nuke_pickup.colliderect(tank1):
        tank1.nuke += 1
        reset_pickup(nuke_pickup)


def update_explosions():
    for e in explosions[:]:
        e["timer"] -= 1
        if e["timer"] <= 0:
            explosions.remove(e)


# --- INPUT ---

def on_key_down(key):
    if key == keys.SPACE and missile1.bottom < 0 and tank1.ammo > 0 and not tank1.gameover:
        missile1.pos = tank1.pos
        tank1.ammo -= 1

    if key == keys.N and nuke_proj.bottom < 0 and tank1.nuke > 0 and not tank1.gameover:
        nuke_proj.pos = tank1.pos
        tank1.nuke -= 1


pgzrun.go()
