from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random


# =========================================================
# INITIALIZATION
# =========================================================

app = Ursina()

window.title = "Mountain Climbing Adventure"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

window.color = color.rgb(135, 200, 235)

sky = Sky(
    color=color.azure
)

# =========================================================
# MAIN MENU BACKGROUND IMAGE
# =========================================================

menu_background = Entity(
    parent=camera.ui,
    model="quad",
    texture="main.png",
    scale=(window.aspect_ratio, 1),
    position=(0, 0),
    z=0
)


# =========================================================
# GAME VARIABLES
# =========================================================

current_level = 1
unlocked_level = 1

game_started = False
level_won = False
game_over = False

lives = 3

player = None

platforms = []
objects = []

summit_position = Vec3(0, 10, 20)
checkpoint_position = Vec3(0, 3, -5)

# =========================================================
# LEVEL INFORMATION
# =========================================================

LEVELS = {

    1: {
        "name": "Beginner Mountain",
        "difficulty": "EASY",
        "platform_count": 10,
        "platform_size": 7,
        "distance": 45
    },

    2: {
        "name": "Rocky Mountain",
        "difficulty": "MEDIUM",
        "platform_count": 14,
        "platform_size": 5,
        "distance": 65
    },

    3: {
        "name": "Extreme Summit",
        "difficulty": "HARD",
        "platform_count": 20,
        "platform_size": 4.5,
        "distance": 125
    }
}




# =========================================================
# MAIN MENU BUTTONS
# =========================================================

start_button = Button(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    position=(0, 0.065),
    scale=(0.32, 0.075),
    color=color.rgba(0, 0, 0, 0),
    z=-5
)

level_select_button = Button(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    position=(0, -0.045),
    scale=(0.32, 0.075),
    color=color.rgba(0, 0, 0, 0),
    z=-5
)

exit_button = Button(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    position=(0, -0.155),
    scale=(0.32, 0.075),
    color=color.rgba(0, 0, 0, 0),
    z=-5
)


# =========================================================
# MAIN MENU INFORMATION
# =========================================================

menu_status = Text(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    position=(0, -0.27),
    scale=0.45,
    color=color.white,
    z=-10
)

menu_help = Text(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    position=(0, -0.335),
    scale=0.32,
    color=color.light_gray,
    z=-10
)


# =========================================================
# LEVEL SELECT SCREEN
# =========================================================

level_select_title = Text(
    parent=camera.ui,
    text="SELECT MOUNTAIN",
    origin=(0, 0),
    position=(0, 0.32),
    scale=1.45,
    color=color.white,
    z=-10
)

level_select_subtitle = Text(
    parent=camera.ui,
    text="Choose your climbing challenge",
    origin=(0, 0),
    position=(0, 0.245),
    scale=0.52,
    color=color.light_gray,
    z=-10
)


# =========================================================
# LEVEL BUTTONS
# =========================================================

level_buttons = []


def make_level_button(level, y):

    data = LEVELS[level]

    button = Button(
        parent=camera.ui,
        text=f"LEVEL {level}\n{data['difficulty']}",
        origin=(0, 0),
        position=(0, y),
        scale=(0.32, 0.085),
        color=color.azure,
        z=-5
    )

    button.on_click = lambda l=level: start_level(l)

    level_buttons.append(button)


make_level_button(1, 0.125)
make_level_button(2, 0.015)
make_level_button(3, -0.095)


# =========================================================
# BACK BUTTON
# =========================================================

back_button = Button(
    parent=camera.ui,
    text="BACK",
    origin=(0, 0),
    position=(0, -0.215),
    scale=(0.22, 0.065),
    color=color.gray,
    z=-5
)


# =========================================================
# GAME UI
# =========================================================

level_text = Text(
    parent=camera.ui,
    text="",
    x=-0.85,
    y=0.45,
    scale=1.1,
    color=color.black
)

altitude_text = Text(
    parent=camera.ui,
    text="",
    x=-0.85,
    y=0.40,
    scale=1.0,
    color=color.black
)

lives_text = Text(
    parent=camera.ui,
    text="Lives: ♥ ♥ ♥",
    x=0.55,
    y=0.45,
    scale=1.1,
    color=color.black
)

control_text = Text(
    parent=camera.ui,
    text="WASD = Move    SPACE = Jump    R = Restart    M = Menu",
    origin=(0, 0),
    y=-0.46,
    scale=0.75,
    color=color.black
)

win_text = Text(
    parent=camera.ui,
    text="",
    origin=(0, 0),
    y=0.15,
    scale=1.5,
    color=color.black
)


# =========================================================
# COMPLETION SCREEN
# =========================================================

next_level_button = Button(
    parent=camera.ui,
    text="NEXT LEVEL",
    origin=(0, 0),
    position=(0, -0.02),
    scale=(0.30, 0.075),
    color=color.azure,
    z=-5
)

completion_menu_button = Button(
    parent=camera.ui,
    text="MAIN MENU",
    origin=(0, 0),
    position=(0, -0.13),
    scale=(0.30, 0.075),
    color=color.gray,
    z=-5
)


# =========================================================
# GAME OVER UI
# =========================================================

game_over_text = Text(
    parent=camera.ui,
    text="GAME OVER",
    origin=(0, 0),
    position=(0, 0.18),
    scale=2.0,
    color=color.red
)

restart_level_button = Button(
    parent=camera.ui,
    text="RESTART LEVEL",
    origin=(0, 0),
    position=(0, -0.02),
    scale=(0.30, 0.075),
    color=color.azure
)

game_over_menu_button = Button(
    parent=camera.ui,
    text="MAIN MENU",
    origin=(0, 0),
    position=(0, -0.13),
    scale=(0.30, 0.075),
    color=color.gray
)


# =========================================================
# INITIAL UI STATE
# =========================================================

level_select_title.enabled = False
level_select_subtitle.enabled = False

for button in level_buttons:
    button.enabled = False

back_button.enabled = False

level_text.enabled = False
altitude_text.enabled = False
control_text.enabled = False
win_text.enabled = False
lives_text.enabled = False

next_level_button.enabled = False
completion_menu_button.enabled = False

game_over_text.enabled = False
restart_level_button.enabled = False
game_over_menu_button.enabled = False


# =========================================================
# UPDATE LEVEL BUTTONS
# =========================================================

def update_buttons():

    for index, button in enumerate(level_buttons):

        level = index + 1

        if level <= unlocked_level:

            button.color = color.azure

            button.text = (
                f"LEVEL {level}\n"
                f"{LEVELS[level]['difficulty']}"
            )

        else:

            button.color = color.gray

            button.text = (
                f"LEVEL {level}\n"
                f"LOCKED"
            )

    menu_status.text = (
        f"Levels Unlocked: {unlocked_level} / 3"
    )


# =========================================================
# UPDATE LIVES
# =========================================================

def update_lives():

    if lives == 3:
        lives_text.text = "Lives: ♥ ♥ ♥"

    elif lives == 2:
        lives_text.text = "Lives: ♥ ♥"

    elif lives == 1:
        lives_text.text = "Lives: ♥"

    else:
        lives_text.text = "Lives: 0"


# =========================================================
# CLEAR OLD LEVEL
# =========================================================

def clear_level():

    global platforms
    global objects

    for entity in platforms:

        if entity:
            destroy(entity)

    for entity in objects:

        if entity:
            destroy(entity)

    platforms = []
    objects = []


# =========================================================
# CREATE TREE
# =========================================================
def create_tree(tx, tz):
    tree = Entity(position=(tx, 0, tz))

    # Trunk
    Entity(
        parent=tree,
        model="cube",
        color=color.brown,
        scale=(0.5, 3, 0.5),
        y=1.5
    )

    # Leaves
    for y, size in [(3, 2.8), (4.2, 2.3), (5.3, 1.7)]:
        Entity(
            parent=tree,
            model="sphere",
            color=color.green,
            scale=size,
            y=y
        )

    tree.scale = random.uniform(1.2, 1.8)
    tree.rotation_y = random.randint(0, 360)

    return tree

# =========================================================
# BUILD LEVEL
# =========================================================

def build_level(level):

    global summit_position
    global checkpoint_position

    clear_level()

    data = LEVELS[level]

    # =====================================================
    # GROUND
    # =====================================================

    ground = Entity(
        model="plane",
        texture="grass",
        scale=100
    )

    # NO COLLIDER ON GROUND
    platforms.append(ground)


    # =====================================================
    # BACKGROUND MOUNTAIN
    # =====================================================

    mountain = Entity(
        model="cone",
        color=color.dark_gray,
        scale=(50, 35, 50),
        position=(0, 17, data["distance"] / 2)
    )

    objects.append(mountain)


    # =====================================================
    # PLATFORM PATH
    # =====================================================

    x = 0
    y = 1

    last_platform_z = 0

    for i in range(data["platform_count"]):

        z = i * (
            data["distance"] /
            data["platform_count"]
        )

        last_platform_z = z

        # =================================================
        # DIFFICULTY
        # =================================================

        if i == 0:
            movement = 0

        elif level == 1:
            movement = random.choice([-2, 0, 2])

        elif level == 2:
            movement = random.choice([-3, 0, 3])

        else:
            movement = random.choice([-4, 0, 4])

        x += movement

        x = max(-10, min(10, x))

        # =================================================
        # HEIGHT INCREASE
        # =================================================

        if i > 0:

            if level == 1:

                y += random.choice([
                    0.5,
                    1.0,
                    1.2
                ])

            elif level == 2:

                y += random.choice([
                    0.9,
                    1.2,
                    1.5
                ])

            else:

                y += random.choice([
                    0.4,
                    0.5,
                    0.6
                ])

        # =================================================
        # CREATE PLATFORM
        # =================================================

        platform_size = data["platform_size"]

        # Larger starting platform for safe spawn and respawn
        if i == 0:
            platform_size = 10

        platform = Entity(
            model="cube",
            texture="white_cube",
            color=color.brown,
            scale=(
                platform_size,
                1,
                platform_size
            ),
            position=(x, y, z),
            collider="box"
        )

        platforms.append(platform)


    # =====================================================
    # CHECKPOINT
    # =====================================================

    checkpoint_position = Vec3(
        0,
        3,
        0
    )

    checkpoint = Entity(
        model="cube",
        color=color.azure,
        scale=(
            data["platform_size"],
            0.2,
            data["platform_size"]
        ),
        position=checkpoint_position
    )

    platforms.append(checkpoint)


    # =====================================================
    # SUMMIT
    # =====================================================

    summit_position = Vec3(
        x,
        y + 1.5,
        last_platform_z + 7
    )

    summit = Entity(
        model="cube",
        color=color.yellow,
        scale=(8, 1, 8),
        position=summit_position,
        collider="box"
    )

    platforms.append(summit)



    # =====================================================
    # FLAG
    # =====================================================

    flag_pole = Entity(
        model="cube",
        color=color.black,
        scale=(0.12, 4, 0.12),
        position=(
            summit_position.x - 2.5,
            summit_position.y + 2,
            summit_position.z
        )
    )

    flag_mesh = Mesh(
        vertices=[
            (0, 0, 0),
            (0, 1.5, 0),
            (1.8, 0.75, 0)
        ],
        triangles=[
            (0, 1, 2)
        ],
        mode="triangle"
    )

    flag = Entity(
        model=flag_mesh,
        color=color.red,
        position=(
            summit_position.x - 2.44,
            summit_position.y + 2.8,
            summit_position.z - 0.01
        ),
        double_sided=True
    )

    objects.append(flag_pole)
    objects.append(flag)


    # =====================================================
    # TREES
    # =====================================================

    tree_count = 8 + level * 5

    for i in range(tree_count):

        tx = random.uniform(-25, 25)
        tz = random.uniform(5, data["distance"] - 5)

        tree = create_tree(tx, tz)

        objects.append(tree)

# =========================================================
# LOSE LIFE
# =========================================================

def lose_life():

    global lives
    global game_started
    global game_over

    if not game_started:
        return

    if level_won:
        return

    # Remove one life
    lives -= 1

    update_lives()

    print("LIFE LOST! Remaining lives:", lives)


    # =====================================================
    # GAME OVER
    # =====================================================

    if lives <= 0:

        game_over = True
        game_started = False

        if player:
            player.enabled = False

        level_text.enabled = False
        altitude_text.enabled = False
        control_text.enabled = False
        lives_text.enabled = False

        game_over_text.text = (
            "GAME OVER\n\n"
            "You lost all your lives!"
        )

        game_over_text.enabled = True

        restart_level_button.enabled = True
        game_over_menu_button.enabled = True

        return


    # =====================================================
    # RESPAWN
    # =====================================================

    if player:

        player.position = checkpoint_position

        player.velocity = Vec3(0, 0, 0)

# =========================================================
# START LEVEL
# =========================================================

def start_level(level):

    global current_level
    global game_started
    global level_won
    global game_over
    global lives
    global player

    if level > unlocked_level:
        return

    current_level = level

    game_started = True
    level_won = False
    game_over = False
    lives = 3

    # =====================================================
    # HIDE MAIN MENU
    # =====================================================

    menu_background.enabled = False

    start_button.enabled = False
    level_select_button.enabled = False
    exit_button.enabled = False

    menu_status.enabled = False
    menu_help.enabled = False

    # =====================================================
    # HIDE LEVEL SELECT
    # =====================================================

    level_select_title.enabled = False
    level_select_subtitle.enabled = False

    for button in level_buttons:
        button.enabled = False

    back_button.enabled = False

    # =====================================================
    # SHOW GAME UI
    # =====================================================

    level_text.enabled = True
    altitude_text.enabled = True
    control_text.enabled = True
    lives_text.enabled = True

    win_text.enabled = False

    game_over_text.enabled = False
    restart_level_button.enabled = False
    game_over_menu_button.enabled = False

    next_level_button.enabled = False
    completion_menu_button.enabled = False

    update_lives()

    # =====================================================
    # BUILD LEVEL
    # =====================================================

    build_level(level)

    # =====================================================
    # CREATE PLAYER
    # =====================================================

    if player:
        destroy(player)

    player = FirstPersonController()

    player.position = (0, 3, 0)

    player.speed = 6
    player.jump_height = 4
    player.gravity = 1

    # =====================================================
    # LEVEL TEXT
    # =====================================================

    level_text.text = (
        f"LEVEL {level} - "
        f"{LEVELS[level]['difficulty']}"
    )

  







# =========================================================
# SHOW MAIN MENU
# =========================================================

def show_menu():

    global game_started

    game_started = False

    if player:
        player.enabled = False

    clear_level()


    # =====================================================
    # MAIN MENU ON
    # =====================================================

    menu_background.enabled = True

    start_button.enabled = True
    level_select_button.enabled = True
    exit_button.enabled = True

    menu_status.enabled = True
    menu_help.enabled = True


    # =====================================================
    # LEVEL SELECT OFF
    # =====================================================

    level_select_title.enabled = False
    level_select_subtitle.enabled = False

    for button in level_buttons:
        button.enabled = False

    back_button.enabled = False


    # =====================================================
    # GAME UI OFF
    # =====================================================

    level_text.enabled = False
    altitude_text.enabled = False
    control_text.enabled = False
    win_text.enabled = False
    lives_text.enabled = False

    game_over_text.enabled = False
    restart_level_button.enabled = False
    game_over_menu_button.enabled = False

    next_level_button.enabled = False
    completion_menu_button.enabled = False

    update_buttons()


# =========================================================
# SHOW LEVEL SELECT
# =========================================================

def show_level_select():

    global game_started

    game_started = False

    if player:
        player.enabled = False

    clear_level()

    menu_background.enabled = False

    start_button.enabled = False
    level_select_button.enabled = False
    exit_button.enabled = False

    menu_status.enabled = False
    menu_help.enabled = False

    level_select_title.enabled = True
    level_select_subtitle.enabled = True

    for button in level_buttons:
        button.enabled = True

    back_button.enabled = True

    level_text.enabled = False
    altitude_text.enabled = False
    control_text.enabled = False
    win_text.enabled = False
    lives_text.enabled = False

    game_over_text.enabled = False
    restart_level_button.enabled = False
    game_over_menu_button.enabled = False

    next_level_button.enabled = False
    completion_menu_button.enabled = False

    update_buttons()


# =========================================================
# LEVEL COMPLETED
# =========================================================

def complete_level():

    global level_won
    global unlocked_level

    if level_won:
        return

    level_won = True


    # =====================================================
    # HIDE GAME UI
    # =====================================================

    level_text.enabled = False
    altitude_text.enabled = False
    control_text.enabled = False
    lives_text.enabled = False


    # =====================================================
    # DISABLE PLAYER
    # =====================================================

    if player:
        player.enabled = False


    # =====================================================
    # LEVEL 1 / LEVEL 2
    # =====================================================

    if current_level < 3:

        if unlocked_level < current_level + 1:
            unlocked_level = current_level + 1
            

        win_text.text = (
            f"LEVEL {current_level} COMPLETE!\n\n"
            f"LEVEL {current_level + 1} UNLOCKED!"
        )

        next_level_button.enabled = True
        completion_menu_button.enabled = True


    # =====================================================
    # LEVEL 3
    # =====================================================

    else:

        win_text.text = (
            "CONGRATULATIONS!\n\n"
            "YOU CONQUERED ALL 3 MOUNTAINS!"
        )

        next_level_button.enabled = False
        completion_menu_button.enabled = True


    win_text.enabled = True


# =========================================================
# NEXT LEVEL
# =========================================================

def next_level():

    global current_level

    if current_level < 3:

        next_level_button.enabled = False
        completion_menu_button.enabled = False
        win_text.enabled = False

        next_level_number = current_level + 1

        start_level(next_level_number)


# =========================================================
# COMPLETION MAIN MENU
# =========================================================

def completion_main_menu():

    next_level_button.enabled = False
    completion_menu_button.enabled = False
    win_text.enabled = False

    show_menu()


# =========================================================
# RESTART LEVEL
# =========================================================

def restart_current_level():

    game_over_text.enabled = False
    restart_level_button.enabled = False
    game_over_menu_button.enabled = False

    start_level(current_level)


# =========================================================
# GAME OVER MAIN MENU
# =========================================================

def game_over_main_menu():

    game_over_text.enabled = False
    restart_level_button.enabled = False
    game_over_menu_button.enabled = False

    show_menu()


# =========================================================
# MENU BUTTON ACTIONS
# =========================================================

start_button.on_click = lambda: start_level(1)

level_select_button.on_click = show_level_select

back_button.on_click = show_menu

exit_button.on_click = application.quit

next_level_button.on_click = next_level

completion_menu_button.on_click = completion_main_menu

restart_level_button.on_click = restart_current_level

game_over_menu_button.on_click = game_over_main_menu


# =========================================================
# INPUT
# =========================================================

def input(key):

    if key == "escape":

        application.quit()

        return


    if not game_started:
        return


    if key == "r":

        start_level(current_level)


    if key == "m":

        show_menu()


# =========================================================
# UPDATE
# =========================================================

def update():

    if not game_started:
        return

    if not player:
        return


    # =====================================================
    # ALTITUDE
    # =====================================================

    altitude = max(0, int(player.y))

    altitude_text.text = (
        f"Altitude: {altitude} m"
    )


    # =====================================================
    # SUMMIT CHECK
    # =====================================================

    if not level_won:

        if distance(
            player.position,
            summit_position
        ) < 6:

            complete_level()

            return


    # =====================================================
    # FALL CHECK
    # =====================================================

    if player.y < -2:

        lose_life()

        return


# =========================================================
# START GAME
# =========================================================
show_menu()
app.run()

