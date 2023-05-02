import pyautogui
import keyboard

# Set the speed of the mouse movement
SPEED = 10

# Define a function to move the mouse
def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=0)

# Start an infinite loop to listen for arrow key presses
while True:
    if keyboard.is_pressed('up'):
        current_position = pyautogui.position()
        move_mouse(current_position.x, current_position.y - SPEED)
    elif keyboard.is_pressed('down'):
        current_position = pyautogui.position()
        move_mouse(current_position.x, current_position.y + SPEED)
    elif keyboard.is_pressed('left'):
        current_position = pyautogui.position()
        move_mouse(current_position.x - SPEED, current_position.y)
    elif keyboard.is_pressed('right'):
        current_position = pyautogui.position()
        move_mouse(current_position.x + SPEED, current_position.y)
