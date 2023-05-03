import pyautogui
import keyboard

# Set the speed of the mouse movement
SPEED = 10

# Define a function to move the mouse
def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=0)

# Start an infinite loop to listen for arrow key presses

def click():
    pyautogui.doubleClick()

def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def move_up():
    current_position = pyautogui.position()
    move_mouse(current_position.x, current_position.y - SPEED)

def move_down():
    current_position = pyautogui.position()
    move_mouse(current_position.x, current_position.y + SPEED)

def move_left():
    current_position = pyautogui.position()
    move_mouse(current_position.x - SPEED, current_position.y)

def move_right():
    current_position = pyautogui.position()
    move_mouse(current_position.x + SPEED, current_position.y)