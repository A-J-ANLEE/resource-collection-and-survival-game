from ursina import *
import random

app = Ursina()
camera.orthographic = True
camera.fov = 20
window.color = color.white

# Game over state
game_over_text = None
game_over_triggered = False

# Load textures
grass_texture = load_texture('assets/grass.jpeg')
tree_texture = load_texture('assets/tree_img.jpg')
rock_texture = load_texture('assets/rock.jpeg')
gold_texture = load_texture('assets/gold.png')

# Load sounds
chop_sound = Audio('assets/chopping-tree-root-212654.mp3', autoplay=False)
mine_sound = Audio('assets/Stone_hit6.mp3', autoplay=False)
gold_sound = Audio('assets/Stone_hit6.mp3', autoplay=False)
chop_sound.volume = 1.0
mine_sound.volume = 1.0
gold_sound.volume = 1.0

# Background grass
tile_size = 15
for x in range(-50, 51):
    for y in range(-30, 31):
        Entity(
            model='quad',
            texture=grass_texture,
            scale=(tile_size, tile_size),
            position=(x * tile_size, y * tile_size),
            collider='box',
            z=0
        )

# Player
player = Entity(
    model='quad',
    color=color.orange,
    scale=(2, 2),
    position=(0, 0),
    collider='box',
    health=5
)
player_speed = 10

# HP Bar
hp_bar_bg = Entity(parent=camera.ui, model='quad', color=color.black, scale=(0.4, 0.03), position=(-0.6, 0.45))
hp_bar = Entity(parent=hp_bar_bg, model='quad', color=color.lime, scale=(1, 1), position=(-0.5, 0), origin_x=-0.5)

# Lists to store entities
trees = []
rocks = []
golds = []
bots = []

# Tree class
class Tree(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad', texture=tree_texture, scale=(3, 4.5), collider='box', z=-0.1, **kwargs)
        self.hp = 10

    def shake(self):
        self.animate_position(self.position + Vec3(0.2, 0), duration=0.05)
        self.animate_position(self.position - Vec3(0.2, 0), duration=0.05, delay=0.05)

    def destroy(self):
        self.disable()
        trees.remove(self)

# Rock class
class Rock(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad', texture=rock_texture, scale=(2.5, 2.5), collider='box', z=-0.1, **kwargs)
        self.hp = 10

    def shake(self):
        self.animate_position(self.position + Vec3(0.2, 0), duration=0.05)
        self.animate_position(self.position - Vec3(0.2, 0), duration=0.05, delay=0.05)

    def destroy(self):
        self.disable()
        rocks.remove(self)

# Gold class
class Gold(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad', texture=gold_texture, scale=(2.5, 2.5), collider='box', z=-0.1, **kwargs)
        self.hp = 5

    def shake(self):
        self.animate_position(self.position + Vec3(0.2, 0), duration=0.05)
        self.animate_position(self.position - Vec3(0.2, 0), duration=0.05, delay=0.05)

    def destroy(self):
        self.disable()
        golds.remove(self)

# Spawning functions
def spawn_trees(count=15):
    for _ in range(count):
        pos_x = random.randint(-80, 80) * 2
        pos_y = random.randint(-50, 50) * 2
        tree = Tree(position=(pos_x, pos_y))
        trees.append(tree)

def spawn_rocks(count=10):
    for _ in range(count):
        pos_x = random.randint(-80, 80) * 2
        pos_y = random.randint(-50, 50) * 2
        rock = Rock(position=(pos_x, pos_y))
        rocks.append(rock)

def spawn_golds(count=10):
    for _ in range(count):
        pos_x = random.randint(-80, 80) * 2
        pos_y = random.randint(-50, 50) * 2
        gold = Gold(position=(pos_x, pos_y))
        golds.append(gold)

def spawn_bots(count=10):
    for _ in range(count):
        pos_x = random.randint(-100, 100) * 2
        pos_y = random.randint(-70, 70) * 2
        bot = Entity(
            model='circle',
            color=color.red,
            scale=2,
            position=(pos_x, pos_y),
            collider='box'
        )
        bots.append(bot)

spawn_trees()
spawn_rocks()
spawn_golds()
spawn_bots()

# Resource counters
wood_collected = 0
stone_collected = 0
gold_collected = 0

# UI Text
wood_text = Text(text=f"Wood: {wood_collected}", position=window.top_right + Vec2(-0.25, -0.05), scale=1.5, color=color.black)
stone_text = Text(text=f"Stone: {stone_collected}", position=window.top_right + Vec2(-0.25, -0.1), scale=1.5, color=color.black)
gold_text = Text(text=f"Gold: {gold_collected}", position=window.top_right + Vec2(-0.25, -0.15), scale=1.5, color=color.black)

# Bot movement
def bot_behavior():
    for bot in bots:
        if distance(player.position, bot.position) < 8:
            bot.look_at_2d(player.position, axis='z')
            bot.position += (player.position - bot.position).normalized() * time.dt * 4
            if distance(player.position, bot.position) < 1:
                player.health -= time.dt

# Game loop
def update():
    global game_over_triggered, game_over_text

    if game_over_triggered:
        return

    if held_keys['w']:
        player.y += time.dt * player_speed
    if held_keys['s']:
        player.y -= time.dt * player_speed
    if held_keys['a']:
        player.x -= time.dt * player_speed
    if held_keys['d']:
        player.x += time.dt * player_speed

    camera.position = (player.x, player.y)
    bot_behavior()

    # Update HP bar
    hp_percent = max(player.health / 5, 0)
    hp_bar.scale_x = hp_percent

    if not game_over_triggered and player.health <= 0:
        player.disable()
        game_over_text = Text(
            text="GAME OVER",
            origin=(0, 0),
            scale=3,
            color=color.red,
            position=(0, 0),
            background=True
        )
        game_over_triggered = True

# Input events
def input(key):
    global wood_collected, stone_collected, gold_collected

    if game_over_triggered:
        return

    if key == 'left mouse down':
        for tree in trees:
            if tree.hovered and distance(player.position, tree.position) < 8:
                chop_sound.stop()
                chop_sound.play()
                tree.shake()
                tree.hp -= 1
                if tree.hp <= 0:
                    tree.destroy()
                wood_collected += 1
                wood_text.text = f"Wood: {wood_collected}"
                return

        for rock in rocks:
            if rock.hovered and distance(player.position, rock.position) < 8:
                mine_sound.stop()
                mine_sound.play()
                rock.shake()
                rock.hp -= 1
                if rock.hp <= 0:
                    rock.destroy()
                stone_collected += 1
                stone_text.text = f"Stone: {stone_collected}"
                return

        for gold in golds:
            if gold.hovered and distance(player.position, gold.position) < 8:
                gold_sound.stop()
                gold_sound.play()
                gold.shake()
                gold.hp -= 1
                if gold.hp <= 0:
                    gold.destroy()
                gold_collected += 1
                gold_text.text = f"Gold: {gold_collected}"
                return

app.run()