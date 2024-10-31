import random
import tkinter as tk
import os
import sys

cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)
love_frames = [16, 17, 18, 19, 20]

# Constants for physics
GRAVITY = 0.4  # Gravity force
FRICTION = 0.95  # Friction factor
TASKBAR_HEIGHT = 140  # Height of the taskbar in pixels

# Global variables
is_dragging = False
start_drag_x = 0
is_love_animation_running = False  # Define is_love_animation_running
is_drag_animation_running = False
drag_animation_complete = False
is_falling = False
# Pet position dictionary
pet_position = {
    'x': 1400,  # Initial x position
    'y': 1080-140,     # Initial y position
    'y_velocity': 0  # Initial y velocity
}

dir_path = os.path.dirname(os.path.realpath(__file__))

# Get the script directory
script_directory = getattr(
    sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# Load gif paths
gif_paths = {
    'idle': 'doggo-idle.gif',
    'idle_to_sleep': 'doggo-idle-to-sleep.gif',
    'sleep': 'doggo-sleep.gif',
    'sleep_to_idle': 'doggo-sleep-to-idle.gif',
    'walk_positive': 'doggo-walking-left.gif',
    'walk_negative': 'doggo-walking-right.gif',
    'love': 'doggo-love.gif',
    'dragging': 'doggo-dragging.gif',
    'falling': 'doggo-falling.gif'
}


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def event():
    global cycle, check, event_number
    if event_number in idle_num:
        check = 0
        window.after(50, update)
    elif event_number == 5:
        check = 1
        window.after(100, update)
    elif event_number in walk_left:
        check = 4
        window.after(100, update)
    elif event_number in walk_right:
        check = 5
        window.after(100, update)
    elif event_number in sleep_num:
        check = 2
        window.after(250, update)
    elif event_number == 14:
        check = 3
        window.after(100, update)


def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


last_x = None  # Variable to store the last x-position of the mouse when dragging
last_y = None  # Variable to store the last y-position of the mouse when dragging


def apply_physics():
    global pet_position, last_x, last_y, is_falling

    # If not dragging or mouse is moved (but right-click is held), update last_x and last_y
    if not is_dragging or (is_dragging and (last_x != pet_position['x'] or last_y != pet_position['y'])):
        last_x = pet_position['x']
        last_y = pet_position['y']

    # Apply gravity if falling
    if is_falling:
        pet_position['y_velocity'] += GRAVITY       

        # Update pet's y position based on velocity
        pet_position['y'] += pet_position['y_velocity']

    # Stop the fall at the desired position
    if pet_position['y'] >= (1080 - TASKBAR_HEIGHT) or not(is_falling):
        pet_position['y'] = 1080 - TASKBAR_HEIGHT
        pet_position['y_velocity'] = 0
        is_falling = False  # Stop falling
    else:
    # Apply friction
        pet_position['y_velocity'] *= FRICTION

        # If dragging but mouse is not moving, maintain y-coordinate based on last_y
        if is_dragging and last_x == pet_position['x']:
            pet_position['y'] = last_y
        else:
            pet_position['y'] += pet_position['y_velocity']
    
    # Update the pet's position
    window.geometry(f'100x100+{int(last_x)}+{int(pet_position["y"])}')

    # Keep calling apply_physics if falling
    if is_falling:
        window.after(10, apply_physics)


def play_falling_animation():
    global cycle, event_number, is_falling

    if is_falling:
        frame = falling[cycle % len(falling)]  # Ensure cycle is within bounds
        cycle += 1
        label.configure(image=frame)
        window.after(100, play_falling_animation)

        if pet_position['y'] > (1080 - TASKBAR_HEIGHT) - 50:
            is_falling = False
            cycle = 0
    else:
        update()


def update():
    global cycle, check, event_number
    global direction

    x = pet_position['x']  # Get the x-coordinate from pet_position
    y = pet_position['y']  # Get the y-coordinate from pet_position
    if is_love_animation_running:
        frame = love_frames[cycle]
        cycle, event_number = gif_work(
            cycle, love_frames, event_number, 0, len(love_frames) - 1)
    elif is_dragging:
        frame = dragging[cycle]
        cycle, event_number = gif_work(
            cycle, dragging, event_number, 0, len(dragging) - 1)
    else:
        if check == 4:  # Walking left
            direction = -1
        elif check == 5:  # Walking right
            direction = 1
        else:
            direction = 0

        # Update the pet's position based on the direction and movement
        pet_position['x'] += direction * 3

        if check == 0:
            frame = idle[cycle]
            cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
        elif check == 1:
            frame = idle_to_sleep[cycle]
            cycle, event_number = gif_work(
                cycle, idle_to_sleep, event_number, 10, 10)
        elif check == 2:
            frame = sleep[cycle]
            cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
        elif check == 3:
            frame = sleep_to_idle[cycle]
            cycle, event_number = gif_work(
                cycle, sleep_to_idle, event_number, 1, 1)
        elif check == 4:
            frame = walk_positive[cycle]
            cycle, event_number = gif_work(
                cycle, walk_positive, event_number, 1, 9)
            x -= 3
        elif check == 5:
            frame = walk_negative[cycle]
            cycle, event_number = gif_work(
                cycle, walk_negative, event_number, 1, 9)
            x -= -3

        window.geometry(
            f'100x100+{int(pet_position["x"])}+{int(pet_position["y"])}')
        label.configure(image=frame)
        window.after(1, event)

    # Update the x coordinate in the pet_position dictionary
    pet_position['x'] = x
    pet_position['y'] = y


def apply_drag(event):
    global is_dragging, last_x, last_y, is_drag_animation_running

    if is_dragging:
        last_x = event.x_root
        last_y = event.y_root

        # Adjust the y-coordinate based on the taskbar height only if it's below the taskbar
        if last_y - 50 > (1000):
            pet_position['y'] = last_y - TASKBAR_HEIGHT
            window.geometry(
                f'100x100+{int(pet_position["x"])}+{int(pet_position["y"])}')
        else:
            pet_position['y'] = last_y - 50

        # Update the pet's position
        # Adjust the x-coordinate based on pet's width
        pet_position['x'] = last_x - 50

        if not is_drag_animation_running:
            is_drag_animation_running = True
            show_drag_animation()

        # Change cursor to a holding hand icon
        window.config(cursor='hand2')
        # Update the window's position
        window.geometry(
            f'100x100+{int(pet_position["x"])}+{int(pet_position["y"])}')
    else:
        # Change cursor back to the default arrow
        window.config(cursor='heart')


def on_right_click(event):
    global is_dragging
    if event.num == 3:
        is_dragging = True
        show_drag_animation()


def on_right_release(event):
    global is_dragging, is_falling

    if event.num == 3:
        is_dragging = False
        is_falling = True
        # Update the window's position
        window.geometry(
            f'100x100+{int(pet_position["x"])}+{int(pet_position["y"])}')

        # Start applying physics after releasing right-click
        window.after(10, apply_physics)

        # Play falling animation
        play_falling_animation()
        # Reset the y_velocity to prevent increasing fall speed
        pet_position['y_velocity'] = 0
    else:
        update()


def on_left_click(event):
    global is_love_animation_running, check

    # Check if the pet is sleeping (check == 2) and prevent actions if sleeping
    if check != 2:
        if event.num == 1:  # Left mouse button
            is_love_animation_running = True
            pet_position['x'] = pet_position['x']
            show_love_animation()
    else:
        pass  # Pet is sleeping, so don't perform any action on left click


def on_left_release(event):
    global is_love_animation_running
    if event.num == 1:
        is_love_animation_running = False


def show_love_animation():
    global cycle, event_number

    if is_love_animation_running:
        cycle = (cycle + 1) % len(love_frames)  # Loop the animation
        frame = love_frames[cycle]
        label.configure(image=frame)
        window.after(100, show_love_animation)
    else:
        cycle = 0  # Reset the animation cycle
        update()  # Call update to continue the loop


def show_drag_animation():
    global cycle, event_number, is_drag_animation_running

    if is_drag_animation_running:
        cycle %= len(dragging)

        frame = dragging[cycle]
        label.configure(image=frame)

        if cycle < len(dragging) - 1:
            cycle += 1
        else:
            is_drag_animation_running = False
            update()
    else:
        cycle = 0


window = tk.Tk()

# Call buddy's action gif
idle = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['idle'])), format=f'gif -index {i}') for i in range(6)]
idle_to_sleep = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['idle_to_sleep'])), format=f'gif -index {i}') for i in range(13)]
sleep = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['sleep'])), format=f'gif -index {i}') for i in range(6)]
sleep_to_idle = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['sleep_to_idle'])), format=f'gif -index {i}') for i in range(14)]
walk_positive = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['walk_positive'])), format=f'gif -index {i}') for i in range(5)]
walk_negative = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['walk_negative'])), format=f'gif -index {i}') for i in range(5)]
love_frames = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['love'])), format=f'gif -index {i}') for i in range(5)]
dragging = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['dragging'])), format=f'gif -index {i}') for i in range(3)]
falling = [tk.PhotoImage(file=resource_path(os.path.join(
    script_directory, gif_paths['falling'])), format=f'gif -index {i}') for i in range(1)]
# Window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')

label.pack()

# Bind the events for dragging
label.bind('<B3-Motion>', apply_drag)
label.bind('<ButtonPress-3>', on_right_click)
label.bind('<ButtonRelease-3>', on_right_release)
window.bind('<Motion>', apply_drag)
window.bind('<ButtonPress-1>', on_left_click)
window.bind('<ButtonRelease-1>', on_left_release)
window.wm_attributes("-topmost", True)  # Make the window stay on top
# Set cursor to hand when hovering over the window
window.config(cursor='heart')

# Loop the program
window.after(1, update)

window.mainloop()
