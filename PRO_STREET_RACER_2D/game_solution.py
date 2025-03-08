import random
import tkinter as tk
from tkinter import Canvas, BOTH, Button, messagebox
from functools import partial
import json
import os

SAVE = "save.json"

key_bindings = {
    "move_left": "<Left>",
    "move_right": "<Right>",
    "pause_game": "<Escape>",
    "boss_key": "<b>",
}

default_game_state = {
    "score": 0,
    "speed": 10,
    "player_car_x": 350,
    "player_car_y": 600,
    "enemy_car_x": 650,
    "enemy_car_y": 100,
    "paused": False,
    "game_over": False,
    "invincibility_mode": False,
    "mirrored_controls": False,
    "car_colour_1": "RoyalBlue3",
    "car_colour_2": "RoyalBlue4",
}

game_state = default_game_state.copy()


def save_game():
    """"
    Saves current game state and key bindings
    """
    data = {
        "game_state": game_state,
        "key_bindings": key_bindings
    }
    file = open(SAVE, "w")
    file.write(json.dumps(data))
    file.close()
    print("Save has been done")


def load_game():
    """"
    Loads current game state and key bindings
    """
    global game_state, key_bindings
    if os.path.exists(SAVE):
        file = open(SAVE, "r")
        data = json.loads(file.read())
        file.close()
        if "game_state" in data:
            game_state.update(data["game_state"])
        if "key_bindings" in data:
            key_bindings.update(data["key_bindings"])
    else:
        print("Save file is not found")


def open_settings():
    """
    Opens the settings menu.
    """
    create_settings_frame()  # Creates settings frame with key bindings
    hide_frame(main_menu_frame)
    show_frame(settings_frame)


REBIND_LABEL = None


def rebind_action(action, key_label_var):
    """
    Rebinds a key to a specified game action.
    """
    global REBIND_LABEL
    if REBIND_LABEL:
        REBIND_LABEL.destroy()
    REBIND_LABEL = tk.Label(settings_frame, text=f"Press a new key for {action}")
    REBIND_LABEL.pack()

    def on_key_press(event):
        global REBIND_LABEL
        key_bindings[action] = event.keysym  # Update the key binding
        temp = event.keysym
        if temp == "Left":
            key_bindings[action] = "<Left>"
        if temp == "Right":
            key_bindings[action] = "<Right>"
        if temp == "Up":
            key_bindings[action] = "<Up>"
        if temp == "Down":
            key_bindings[action] = "<Down>"
        key_label_var.set(event.keysym)
        root.unbind("<KeyPress>")
        if REBIND_LABEL:
            REBIND_LABEL.destroy()
            REBIND_LABEL = None

    root.bind("<KeyPress>", on_key_press)


def create_settings_frame():
    """
    Creates the settings frame, generates key-binding settings
    """
    for widget in settings_frame.winfo_children():
        widget.destroy()

    tk.Label(settings_frame, text="Settings", font=("PIXY", 40)).pack(pady=20)

    for action, key in key_bindings.items():
        frame = tk.Frame(settings_frame)
        frame.pack(pady=5, padx=10, fill="x")

        action_label = tk.Label(frame, text=action, font=("PIXY", 22), anchor="w", width=20)
        action_label.pack(side="left", padx=10)

        key_label_var = tk.StringVar(value=key)
        key_label = tk.Label(frame, textvariable=key_label_var, font=("PIXY", 22), anchor="center", width=15)
        key_label.pack(side="left", padx=10)

        rebind_button = tk.Button(frame, text="Rebind", font=("PIXY", 22),
                                  height=2, width=5, bg="#ff422b", fg="#1f100e",
                                  command=lambda action=action, var=key_label_var: rebind_action(action, var))
        rebind_button.pack(side="left", padx=10)

    tk.Button(settings_frame, text="Menu", height=2, width=9, font=("PIXY", 22), fg="#1f100e", bg="#ff422b",
              command=lambda: show_frame(main_menu_frame)).place(x=500, y=660, anchor="center")


def show_frame(frame):
    """
    Displays the specified frame in the application.
    """
    for f in (main_menu_frame, settings_frame, tutorial_frame, leaderboard_frame, customisation_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)
    frame.update_idletasks()
    root.update()


def hide_frame(frame):
    """
    Displays the specified frame in the application.
    """
    frame.pack_forget()


def exit_game():
    """
    Exits the game after prompting the user for confirmation, saves game state before closing.
    """
    if messagebox.askokcancel("Exit Game", "Are you sure you want to exit?"):
        save_game()
        root.destroy()


root = tk.Tk()
root.title("PRO STREET RACER 2D")
root.geometry("1000x700+100+100")
load_game()
root.protocol("WM_DELETE_WINDOW", lambda: [save_game(), root.destroy()])

"""
This module handles main menu.
"""
main_menu_bg = tk.PhotoImage(file="main_menu.png")
main_menu_frame = tk.Frame(root)

main_menu_bg_label = tk.Label(main_menu_frame, image=main_menu_bg)
main_menu_bg_label.place(x=0, y=0)

tk.Button(main_menu_frame, text="START GAME", bg="#ff422b", fg="#1f100e", height=1, width=14, font=("PIXY", 28),
          command=lambda: start_game(root)).place(x=220,
                                                  y=120,
                                                  anchor="center")

tk.Button(main_menu_frame, text="CUSTOMISE CAR", bg="#ff422b", fg="#1f100e", height=1, width=14,
          font=("PIXY", 28), command=lambda: show_frame(customisation_frame)).place(x=220,
                                                                                    y=190,
                                                                                    anchor="center")

tk.Button(main_menu_frame, text="LEADERBOARD", bg="#ff422b", fg="#1f100e", height=1, width=14, font=("PIXY", 28),
          command=lambda: [update_leaderboard_display(), show_frame(leaderboard_frame)]).place(x=220,
                                                                                               y=260,
                                                                                               anchor="center")

tk.Button(main_menu_frame, text="SETTINGS", bg="#ff422b", fg="#1f100e", height=1, width=14, font=("PIXY", 28),
          command=lambda: open_settings()).place(x=220,
                                                 y=330,
                                                 anchor="center")

tk.Button(main_menu_frame, text="TUTORIAL", bg="#ff422b", fg="#1f100e", height=1, width=14, font=("PIXY", 28),
          command=lambda: show_frame(tutorial_frame)).place(x=220,
                                                            y=400,
                                                            anchor="center")

tk.Button(main_menu_frame, text="EXIT", bg="#ff422b", fg="#1f100e", height=1, width=14,
          font=("PIXY", 28), command=exit_game).place(x=220,
                                                      y=470,
                                                      anchor="center")

settings_frame = tk.Frame(root)

"""
Module for customisation frame
"""
customisation_frame = tk.Frame(root)
preview_frame = tk.Frame(customisation_frame, width=500, height=500, bg="white")
preview_frame.pack(side="left", fill="both", expand=True)

controls_frame = tk.Frame(customisation_frame, width=500, height=500, bg="lightgray")
controls_frame.pack(side="right", fill="both", expand=True)

car_primary_colour = game_state["car_colour_1"]
car_secondary_colour = game_state["car_colour_2"]

preview_canvas = tk.Canvas(preview_frame, width=400, height=400, bg="white")
preview_canvas.place(x=50, y=50)


def update_car_preview():
    """
    Updates the car preview in the customization menu.
    Draws the player's car on the preview canvas based on the selected colors.
    """
    preview_canvas.delete("preview")
    x, y = 200, 200

    preview_canvas.create_rectangle(x - 50, y - 75, x + 50, y + 75, outline=car_primary_colour,
                                    fill=car_primary_colour, tags="preview")

    preview_canvas.create_rectangle(x - 40, y - 30, x + 40, y + 60, outline=car_secondary_colour,
                                    fill=car_secondary_colour, tags="preview")

    preview_canvas.create_rectangle(x - 65, y - 65, x - 50, y - 20, fill="black", tags="preview")
    preview_canvas.create_rectangle(x + 65, y - 65, x + 50, y - 20, fill="black", tags="preview")
    preview_canvas.create_rectangle(x - 65, y + 65, x - 50, y + 20, fill="black", tags="preview")
    preview_canvas.create_rectangle(x + 65, y + 65, x + 50, y + 20, fill="black", tags="preview")
    preview_canvas.create_rectangle(x - 20, y - 85, x - 40, y - 75, fill="gold", outline="gold", tags="preview")
    preview_canvas.create_rectangle(x + 20, y - 85, x + 40, y - 75, fill="gold", outline="gold", tags="preview")


update_car_preview()

tk.Label(controls_frame, text="Customise Your Car", font=("PIXY", 32), bg="lightgray").pack(pady=20)


def set_primary_colour(colour):
    """
    Sets primary colour for player's car, updates car preview in customise menu.
    """
    global car_primary_colour
    car_primary_colour = colour
    update_car_preview()


def set_secondary_colour(colour):
    """
    Sets secondary colour for player's car, updates car preview in customise menu.
    """
    global car_secondary_colour
    car_secondary_colour = colour
    update_car_preview()


# Primary colour buttons
tk.Label(controls_frame, text="Primary Colour", font=("PIXY", 22), bg="lightgray").pack(pady=5)

primary_colours = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple"]
for colour in primary_colours:
    tk.Button(controls_frame, text=colour, bg=colour, width=10, command=lambda c=colour: set_primary_colour(c)).pack(
        pady=2)

# Secondary colour buttons
tk.Label(controls_frame, text="Secondary Colour", font=("PIXY", 22), bg="lightgray").pack(pady=5)

secondary_colours = ["Cyan", "Magenta", "Brown", "Pink", "Gray", "Black"]
for colour in secondary_colours:
    tk.Button(controls_frame, text=colour, bg=colour, width=10, command=lambda c=colour: set_secondary_colour(c)).pack(
        pady=2)


# Save customization and return to main menu
def save_customisation():
    """
    Saves colours set in customisation menu.
    """
    global car_primary_colour, car_secondary_colour
    game_state["car_colour_1"] = car_primary_colour
    game_state["car_colour_2"] = car_secondary_colour
    save_game()
    show_frame(main_menu_frame)


tk.Button(controls_frame, text="Save and Back", command=save_customisation, font=("PIXY", 22),
          bg="#ff422b", fg="#1f100e").pack(pady=5)

"""
Module for tutorial frame
"""
tutorial_frame = tk.Frame(root)
tutorial_text = """
Welcome to Pro Street Racer 2D!

Objective:
The goal is simple - drive your car without colliding with the red cars on the road. 
Avoid collisions to achieve the highest score possible!

---

Default Controls:
    • Move Left:     Press <Arrow Left> ️
    • Move Right:    Press <Arrow Right> ️
    • Pause the Game: Press <Escape> ️
    • Boss Key:      Press <B> (Quickly hide the game)

---

Cheat Codes:
    • Activate Invincibility: Type G O D
    • Mirror Controls: Type D R K
    • Set Custom Score: Type S C R

"""
tk.Label(tutorial_frame, text="Tutorial", font=("PIXY", 40)).pack(pady=20)
tk.Label(tutorial_frame, text=tutorial_text, fg="Black", font=("PIXY", 16), justify="left", padx=10, pady=10).pack()
tk.Button(tutorial_frame, text="Menu", height=2, width=9, font=("PIXY", 22), fg="#1f100e", bg="#ff422b",
          command=lambda: show_frame(main_menu_frame)).place(x=500, y=660, anchor="center")

"""
Module for leaderboard frame
"""
leaderboard_frame = tk.Frame(root)
tk.Label(leaderboard_frame, text="Leaderboard", font=("PIXY", 40)).pack(pady=20)
leaderboard_displayed_data = []
for i in range(1, 11):
    label = tk.Label(leaderboard_frame, text="", font=("PIXY", 22), anchor="w")
    label.pack(pady=2)
    leaderboard_displayed_data.append(label)


def update_leaderboard_display():
    """
    Updates the leaderboard display with the top scores from the leaderboard.
    """
    for i, label in enumerate(leaderboard_displayed_data):
        if i < len(leaderboard.scores):  # If there are enough scores to display
            value = leaderboard.scores[i]
            label.config(text=f"{i + 1}. {value['name']} - {value['score']}")
        else:
            label.config(text="")


tk.Button(leaderboard_frame, text="Menu", height=2, width=9, font=("PIXY", 22), fg="#1f100e", bg="#ff422b",
          command=lambda: show_frame(main_menu_frame)).pack(pady=10)

show_frame(main_menu_frame)


class Leaderboard:
    """
    Manages the leaderboard, including loading, saving, and displaying top scores.
    """

    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = self.load_leaderboard()

    def load_leaderboard(self):
        try:
            file = open(self.filename, "r")
            data = json.load(file)
            file.close()
            return data
        except FileNotFoundError:
            print(f"file {self.filename} not found")
            return []
        except json.JSONDecodeError:
            print(f"file {self.filename} is not valid")
            return []

    def save_leaderboard(self):
        file = open(self.filename, "w")
        json.dump(self.scores, file)
        file.close()

    def add_score(self, name, score):
        saved_name = None
        for value in self.scores:
            if value["name"] == name:
                saved_name = value
                break
        if saved_name:
            if score > saved_name["score"]:
                saved_name["score"] = score
        else:
            self.scores.append({"name": name, "score": score})
        # self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]
        self.save_leaderboard()

    def display_leadeboard(self):
        print("LEADERBOARD")
        for i, value in enumerate(self.scores, 1):
            print(f'{i}. {value["name"]} - {value["score"]}')


leaderboard = Leaderboard()


class Line:
    """
    Road lines in the game.
    """
    x = 0
    y = 0
    rec = 0

    def __init__(self, x1, y1, canvas, speedprovider):
        self.x = x1
        self.y = y1
        self.print_line(canvas)
        self.speedprovider = speedprovider

    def change_coord(self, canvas):
        """
        Cycles lines.
        """
        canvas.delete(self.rec)
        self.y = (self.y + self.speedprovider.speed)
        if self.y >= 700:
            self.y -= 800
        if self.y <= -100:
            self.y += 800
        self.print_line(canvas)

    def print_line(self, canvas):
        """
        Draws lines on road.
        """
        self.rec = canvas.create_rectangle(self.x, self.y, self.x + 20, self.y + 100, fill="white", outline="white",
                                           width=2)

    # def upSpeed(self):
    #     self.speedprovider.speed += 5
    #     if self.speedprovider.speed > 30:
    #         self.speedprovider.speed = 30
    #
    # def downSpeed(self):
    #     self.speedprovider.speed -= 5
    #     if self.speedprovider.speed < 0:
    #         self.speedprovider.speed = -10

    def get_speed(self):
        return self.speedprovider.speed


class SpeedProvider:
    """
    Provides the speed for game objects.
    """
    speed = game_state["speed"]


class Car:
    """
    A car in the game.
    """
    x = 0
    y = 0
    direction = 0
    rec1, rec2, rec3, rec4, rec5, rec6, rec7, rec8 = 0, 0, 0, 0, 0, 0, 0, 0

    def __init__(self, x1, y1, colour1, colour2, direct, canvas, speedprovider):
        self.x = x1
        self.y = y1
        self.speedprovider = speedprovider
        self.col1 = colour1
        self.col2 = colour2
        self.direction = direct
        self.print_car(canvas)

    def delete_car(self, canvas):
        if self.rec1 != 0:
            canvas.delete(self.rec1, self.rec2, self.rec3, self.rec4, self.rec5, self.rec6, self.rec7, self.rec8)

    def print_car(self, canvas):
        """
        Draws cars on canvas
        """
        self.delete_car(canvas)
        self.rec1 = canvas.create_rectangle(
            self.x - 50, self.y - 75, self.x + 50, self.y + 75, outline=self.col1, fill=self.col1, width=0)
        roof = self.y - 30
        if self.direction == 1:
            roof = self.y - 60
        self.rec2 = canvas.create_rectangle(
            self.x - 40, roof, self.x + 40, roof + 90, outline=self.col2, fill=self.col2, width=0)

        self.rec3 = canvas.create_rectangle(
            self.x - 65, self.y - 65, self.x - 50, self.y - 20, outline="black", fill="black", width=0)

        self.rec4 = canvas.create_rectangle(
            self.x + 65, self.y - 65, self.x + 50, self.y - 20, outline="black", fill="black", width=0)

        self.rec5 = canvas.create_rectangle(
            self.x - 65, self.y + 65, self.x - 50, self.y + 20, outline="black", fill="black", width=0)

        self.rec6 = canvas.create_rectangle(
            self.x + 65, self.y + 65, self.x + 50, self.y + 20, outline="black", fill="black", width=0)

        light = self.y - 85
        if self.direction == 1:
            light = self.y + 75
        self.rec7 = canvas.create_rectangle(
            self.x - 20, light, self.x - 40, light + 10, outline="gold", fill="gold", width=0)

        self.rec8 = canvas.create_rectangle(
            self.x + 20, light, self.x + 40, light + 10, outline="gold", fill="gold", width=0)

    def change_colour(self, colour1, colour2, canvas):
        self.col1 = colour1
        self.col2 = colour2
        canvas.delete(self.rec1, self.rec2)
        self.rec1 = canvas.create_rectangle(
            self.x - 50, self.y - 75, self.x + 50, self.y + 75, outline=self.col1, fill=self.col1, width=0)
        self.rec2 = canvas.create_rectangle(
            self.x - 40, self.y - 30, self.x + 40, self.y + 60, outline=self.col2, fill=self.col2, width=0)

    def move_left(self, canvas, arg, mirrored=False):  # mirrored is a flag required to prevent infinite recursion.
        """
        Moves car left.
        """
        if game_state["mirrored_controls"] and not mirrored:
            self.move_right(canvas, arg, mirrored=True)
        else:
            if self.x > 70:  # Restricts movement out of screen on the left side
                self.x = (self.x - 20)
                self.print_car(canvas)

    def move_right(self, canvas, arg, mirrored=False):  # mirrored is a flag required to prevent infinite recursion.
        """
        Moves car right.
        """
        if game_state["mirrored_controls"] and not mirrored:
            self.move_left(canvas, arg, mirrored=True)
        else:
            if self.x < 930:  # Restricts movement out of screen on the left side
                self.x = (self.x + 20)
                self.print_car(canvas)

    def change_coord(self, speed, canvas):
        """
        Randomly places enemy car.
        """
        self.y = (self.y + speed)
        if self.y >= 800:
            self.y -= 900
            self.x = random.randint(0 + 100, 1000 - 100)
        self.print_car(canvas)

    def __add__(self, other):
        self_left = self.x - 50
        self_right = self.x + 50
        self_top = self.y - 75
        self_bottom = self.y + 75

        car2_left = other.x - 50
        car2_right = other.x + 50
        car2_top = other.y - 75
        car2_bottom = other.y + 75

        return not (self_right < car2_left or
                    self_left > car2_right or
                    self_bottom < car2_top or
                    self_top > car2_bottom)


def up(line, arg):
    for i in range(5):
        (line[i]).upSpeed()


def down(line, arg):
    for i in range(5):
        (line[i]).downSpeed()


"""
This module handles cheat codes
"""
key_sequence = []
invincibility_activation_sequence = ["G", "O", "D"]
mirrored_activation_sequence = ["D", "R", "K"]
custom_score_activation_sequence = ["S", "C", "R"]


def check_cheat_codes_sequences(arg, canvas, set_custom_score_callback):
    """
    Checks cheat codes sequences.
    """

    global key_sequence
    key_sequence.append(arg.keysym.upper())
    if key_sequence[-len(invincibility_activation_sequence):] == invincibility_activation_sequence:
        toggle_invincibility(canvas)
        key_sequence.clear()
    elif key_sequence[-len(mirrored_activation_sequence):] == mirrored_activation_sequence:
        toggle_mirrored_controls(canvas)
        key_sequence.clear()
    elif key_sequence[-len(custom_score_activation_sequence):] == custom_score_activation_sequence:
        set_custom_score_callback()
        key_sequence.clear()
    elif len(key_sequence) > max(len(invincibility_activation_sequence), len(mirrored_activation_sequence)):
        key_sequence.pop(0)


def toggle_invincibility(canvas):
    """
    Toggles invincibility mode and shows a flashing message on the canvas.
    """
    game_state["invincibility_mode"] = not game_state["invincibility_mode"]
    if game_state["invincibility_mode"]:
        print("INVINCIBILITY ACTIVATED")
        show_flashing_text("INVINCIBILITY \nACTIVATED", canvas)
    else:
        print("INVINCIBILITY DEACTIVATED")
        show_flashing_text("INVINCIBILITY \nDEACTIVATED", canvas)


def toggle_mirrored_controls(canvas):
    """
    Toggles mirrored controls mode and shows a flashing message on the canvas.
    """
    game_state["mirrored_controls"] = not game_state["mirrored_controls"]
    if game_state["mirrored_controls"]:
        print("mirrored \nCONTROLS \nACTIVATED")
        show_flashing_text("mirrored \nCONTROLS \nACTIVATED", canvas)
    else:
        print("mirrored CONTROLS \n DEACTIVATED")
        show_flashing_text("mirrored \nCONTROLS \nDEACTIVATED", canvas)


def show_flashing_text(message, canvas):
    """"
    Shows flashing message based on the activated cheat code.
    """
    flashing_text = canvas.create_text(895, 150, text=message, fill="black", font=("PIXY", 22),
                                       tags="flashing_text")
    canvas.tag_raise("flashing_text")

    def toggle_visibility(count):
        """"
        Makes text flashing
        """
        if count > 0:
            current_colour = canvas.itemcget(flashing_text, "fill")
            new_colour = "orange" if current_colour == "" else ""
            canvas.itemconfig(flashing_text, fill=new_colour)
            root.after(500, toggle_visibility, count - 1)
        else:
            canvas.delete(flashing_text)

    toggle_visibility(6)


def start_game(root):
    """
    Starts the game. Initializes game objects, sets up the canvas, and begins the game loop.
    """
    global game_state, leaderboard
    print("Score before starting game:", game_state)  # DEBUG PROCESS
    hide_frame(main_menu_frame)
    canvas = Canvas()
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_rectangle(200, -20, 800, 720, outline="grey", fill="#797c7e", width=20)
    root.bind("<KeyPress>", lambda arg: check_cheat_codes_sequences(arg, canvas, set_custom_score))

    score = game_state["score"]
    speedprovider = SpeedProvider()
    speedprovider.speed = game_state["speed"]

    menu_button = None
    gameover = False
    paused = game_state["paused"]
    pause_title = None
    boss_key_canvas = None
    paused_by_boss_key = False
    pause_return_to_menu_button = None

    score_text = False
    line = [Line(489, i * 200 - 50, canvas, speedprovider) for i in range(5)]

    car = Car(game_state["player_car_x"], game_state["player_car_y"], game_state["car_colour_1"],
              game_state["car_colour_2"], 0, canvas, speedprovider)  # Player's car instance

    car2 = Car(game_state["enemy_car_x"], game_state["enemy_car_y"], "Red", "Dark Red", 1, canvas,
               speedprovider)  # Enemy car instance

    root.bind(key_bindings["move_left"], partial(car.move_left, canvas))
    root.bind(key_bindings["move_right"], partial(car.move_right, canvas))

    def trigger_pause(arg):
        """
        Turns on pause.
        """
        nonlocal paused, pause_title, pause_return_to_menu_button
        if paused_by_boss_key:
            return

        paused = not paused
        if not gameover:
            if paused:
                # print("paused")
                if not pause_title:
                    pause_title = canvas.create_text(500, 300, fill="#1f100e", font=("PIXY", 40), text="PAUSED")
                if not pause_return_to_menu_button:
                    pause_return_to_menu_button = tk.Button(root, text="MENU", font=("PIXY", 32),
                                                            height=1, width=9, command=save_and_return_to_menu,
                                                            bg="#ff422b", fg="#1f100e")
                    pause_return_to_menu_button.place(x=500, y=400, anchor="center")
                root.unbind(key_bindings["move_left"])
                root.unbind(key_bindings["move_right"])
            else:
                print("not paused")
                if pause_title:
                    canvas.delete(pause_title)
                    pause_title = None
                if pause_return_to_menu_button:
                    pause_return_to_menu_button.destroy()
                    pause_return_to_menu_button = None
                root.bind(key_bindings["move_left"], partial(car.move_left, canvas))
                root.bind(key_bindings["move_right"], partial(car.move_right, canvas))
                game_loop()

    root.bind(key_bindings["pause_game"], trigger_pause)

    def trigger_boss_key(arg):
        """
        Turns on boss key pause.
        """
        nonlocal paused, boss_key_canvas, paused_by_boss_key
        if paused:
            return
        paused_by_boss_key = not paused_by_boss_key
        if not gameover:
            if paused_by_boss_key:
                # print("Paused by boss key")
                if not boss_key_canvas:
                    boss_key_canvas = tk.Canvas(root, bg="black")
                    boss_key_canvas.place(x=0, y=0, relwidth=1, relheight=1)
                    boss_key_image = tk.PhotoImage(file="boss_key.png")
                    boss_key_canvas.create_image(500, 350, image=boss_key_image)
                    boss_key_canvas.image = boss_key_image
            else:
                if boss_key_canvas:
                    boss_key_canvas.destroy()
                    boss_key_canvas = None
                game_loop()

    root.bind(key_bindings["boss_key"], trigger_boss_key)

    def save_and_return_to_menu():
        """
        Allows the player to leave to main menu from the pause screen.
        """
        global game_state
        print("Full game state before saving:", game_state)  # DEBUG PROCESS
        game_state["score"] = score
        game_state["speed"] = speedprovider.speed
        game_state["player_car_x"] = car.x
        game_state["player_car_y"] = car.y
        game_state["enemy_car_x"] = car2.x
        game_state["enemy_car_y"] = car2.y
        print(game_state)
        canvas.destroy()
        if pause_return_to_menu_button:
            pause_return_to_menu_button.destroy()
        show_frame(main_menu_frame)
        root.after(10, lambda: show_frame(main_menu_frame))

    def game_over():
        """
        Ends the current game session, displays the Game Over screen,
        and allows the player to submit their score to the leaderboard.
        """
        nonlocal gameover, menu_button
        global game_state
        print("Score at game over:", game_state)  # DEBUG PROCESS
        gameover = True
        car.delete_car(canvas)
        car2.delete_car(canvas)
        speedprovider.speed = 0

        canvas.create_rectangle(200, -20, 800, 720, outline="white", fill="#797c7e", width=20)
        canvas.create_text(500, 300, fill="#ff3217", font=("PIXY", 70), text="GAME OVER")

        name_entry = tk.Entry(root, font=("PIXY", 22), fg="#1f100e", justify="center")
        name_entry.place(x=500, y=360, width=205, anchor="center")

        name_entry.insert(0, "Your name")

        def on_entry_click(arg):
            """
            Removes "Your name" text from name entry when pressed
            """

            if name_entry.get() == "Your name":
                name_entry.delete(0, "end")

        name_entry.bind("<FocusIn>", on_entry_click)

        def submit_name():
            nonlocal menu_button
            global game_state
            # print("Score before submitting name:", game_state)  # DEBUG PROCESS
            name = name_entry.get().strip()
            if name and name != "Your name":
                leaderboard.add_score(name, game_state["score"])
                leaderboard.save_leaderboard()
                # print("Submitted score:", game_state["score"])  # DEBUG PROCESS
            # name_label.destroy()
            name_entry.destroy()
            custom_colours = {
                "car_colour_1": game_state["car_colour_1"],
                "car_colour_2": game_state["car_colour_2"],
            }
            game_state = default_game_state.copy()
            game_state.update(custom_colours)
            return_to_menu()

        menu_button = Button(root, text="MENU", font=("PIXY", 32),
                             command=submit_name, height=1,
                             width=9, bg="#ff422b", fg="#1f100e")
        menu_button.place(x=500, y=410, anchor="center")

        leaderboard.display_leadeboard()
        update_leaderboard_display()

        root.unbind(key_bindings["move_left"])
        root.unbind(key_bindings["move_right"])

    def return_to_menu():
        """
        Called in frames to return to main menu
        """
        nonlocal menu_button
        canvas.destroy()
        if menu_button:
            menu_button.destroy()
        show_frame(main_menu_frame)
        root.after(10, lambda: show_frame(main_menu_frame))

    def increase_speed():
        """
        Increases speed over time.
        """
        nonlocal paused, paused_by_boss_key
        if not paused and not paused_by_boss_key and speedprovider.speed < 50:
            speedprovider.speed += 5
        root.after(5000, increase_speed)

        # print(speedprovider.speed)

    increase_speed()

    def set_custom_score():
        """
        This function is triggered by custom score cheat code, allows player to set custom score.
        """

        nonlocal paused, canvas
        paused = True
        # print("Paused by score cc")

        score_entry = tk.Entry(root, font=("PIXY", 22), fg="#1f100e", justify="center")
        score_entry.place(x=500, y=350, width=200, anchor="center")

        score_entry.insert(0, "Your score")

        def on_entry_click(arg):
            if score_entry.get() == "Your score" or score_entry.get() == "Enter a number":
                score_entry.delete(0, "end")

        score_entry.bind("<FocusIn>", on_entry_click)

        def submit_custom_score():
            nonlocal score, paused
            input_value = score_entry.get()
            if input_value.isdigit():
                custom_score = int(input_value)
                score = custom_score

                score_entry.destroy()
                submit_custom_score_button.destroy()
                paused = False
                game_loop()
            else:
                score_entry.insert(0, "Invalid input. Enter a number")

        submit_custom_score_button = Button(root, text="SUBMIT", font=("PIXY", 32),
                                            command=submit_custom_score, height=2,
                                            width=9, bg="#ff422b", fg="#1f100e")
        submit_custom_score_button.place(x=500, y=410, anchor="center")

    def game_loop():
        """
        Main game loop that continuously updates the game state and graphics.
        """

        nonlocal gameover, score_text, score

        if not paused and not paused_by_boss_key and not gameover:
            if score_text:
                canvas.delete(score_text)

            for i in range(5):
                line[i].change_coord(canvas)
            car.print_car(canvas)
            car2.change_coord(speedprovider.speed, canvas)

            score_text = canvas.create_text(900, 100, fill="black", font=("PIXY", 30),
                                            text="Score: " + str(game_state["score"]))
            score += speedprovider.speed
            game_state["score"] = score
            if (car + car2) and not game_state["invincibility_mode"]:
                game_over()
            else:
                root.after(100, game_loop)

    game_loop()


root.resizable(False, False)
root.mainloop()
