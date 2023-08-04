from ursina import *
from random import randint
from menu import *
import os


def splash_screen():
    black_bg = Entity(model='quad', texture='brick', scale=10,
                      parent=camera.ui, color=color.black)
    icon = Entity(model='quad', texture='assets/tornado.png',
                  scale=0.5, parent=camera.ui, alpha=0)
    icon.fade_in(duration=3)
    menu = Menu()
    menu.disable()
    s = Sequence(Func(icon.fade_out), Func(black_bg.fade_out),
                 Func(setattr, menu, 'enabled', True), duration=4)
    s.start()


def initialize():
    global running, timer_elapsed, score, box, score_board, timer, create_box
    running = False
    timer_elapsed = 10   # Elapsed time in seconds
    score = 0
    box = []

    def create_box():
        return Button(parent=scene, model='sphere', color=color.brown, position=(3, randint(2, 4), randint(2, 5)), highlight_color=color.brown, pressed_color=color.brown)
    for _ in range(5):
        box.append(create_box())
    score_board = Button(parent=scene, model='quad', position=(
        3, 4, 8), text=f'Score: {score}', rotation=Vec3(0, 90, 0), color=color.clear)
    timer = Button(parent=scene, model='quad', position=(
        3, 3, 8), text=f'Time: {round(timer_elapsed)}', rotation=Vec3(0, 90, 0), color=color.clear)


# Game
app = Ursina()

# Splash screen
# menu = Menu()
splash_screen()

# Initialize the game
initialize()


def save_score():
    file_path = 'data/score.json'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    new_score = {
        f'score': score
    }
    with open(file_path, 'w') as file:
        json.dump(new_score, file)


def update():
    global score, timer_elapsed, running, box, score_board, start, timer, end, last_score
    if running:
        destroy(score_board)
        destroy(timer)
        score_board = Button(parent=scene, model='quad', position=(
            3, 4, 8), text=f'Score: {score}', rotation=Vec3(0, 90, 0), color=color.clear)
        timer = Button(parent=scene, model='quad', position=(
            3, 3, 8), text=f'Time: {round(timer_elapsed)}', rotation=Vec3(0, 90, 0), color=color.clear)
        if len(box) < 5:
            box.append(create_box())
        timer_elapsed -= time.dt
        print(timer_elapsed)
        if timer_elapsed < 0:
            running = False
            for ball in box:
                destroy(ball)
            try:
                with open('data/score.json', 'r') as file:
                    history = json.load(file)
                    last_score = history.get('score', 0)
            except FileNotFoundError:
                last_score = 0
            save_score()
            end = Button(parent=scene, model='quad', position=(
                3, 2, 3), text=f'Time out!!\nYour score: {score}\nYour latest score: {last_score}\nPress "Enter" to restart or "Esc" to quit.', rotation=Vec3(0, 90, 0), color=color.clear)
            # invoke(Func(destroy,end), delay = 5)


def input(key):
    global score, running, box, timer_elapsed, timer, end
    for ball in box:
        if ball.hovered and key == 'left mouse down':
            box.remove(ball)
            destroy(ball)
            if timer_elapsed > 0:
                running = True
                score += 1
        if key == 'escape':
            quit()
    if not running:
        if score != 0 and key == 'enter':
            destroy(score_board)
            destroy(timer)
            destroy(end)
            initialize()


app.run()
