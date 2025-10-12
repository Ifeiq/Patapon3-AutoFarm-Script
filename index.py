import subprocess
import cv2
import numpy as np
import os
import time

button_delay = 0.29

# Left: 450, 500 | Right: 230, 550 | Up: 350, 450 | Down: 350, 650
# Triangle: 2200, 750 | X: 2200, 950 | Square: 2100, 850 | Circle: 2300, 850

images = [
    "images/base.png",
    "images/battle.png",
    "images/chest.png",
    "images/status.png",
    "images/loading.png",
]

buttons = {
    "right": [450, 500],
    "left": [230, 550],
    "up": [350, 450],
    "down": [350, 650],
    "triangle": [2200, 750],
    "x": [2200, 950],
    "square": [2100, 850],
    "circle": [2300, 850],
    "start": [1470, 940]
}

def tap(button):
    print(f"Taponando {button}")
    subprocess.run(["adb", "shell", "input", "swipe", str(button[0]), str(button[1]), str(button[0]), str(button[1]), "100"])

def printScreen():
    with open("screenshot.png", "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)

def diff(img1_path, images):
    img1 = cv2.imread(img1_path)
    if img1 is None:
        print(f"Erro: não foi possível abrir {img1_path}")
        return

    best_match = None
    best_score = -1

    for name in images:
        path = name if os.path.splitext(name)[1] else f"{name}.png"
        img2 = cv2.imread(path)
        if img2 is None:
            print(f"Erro: não foi possível abrir {path}")
            continue

        img1_resized = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
        result = cv2.matchTemplate(img1_resized, img2, cv2.TM_CCOEFF_NORMED)
        similarity = result.max()

        print(f"Semelhança com {path}: {similarity:.4f}")

        if similarity > best_score:
            best_score = similarity
            best_match = path

    return best_match

def chest():
    tap(buttons["left"])
    time.sleep(1)
    tap(buttons["x"])

def status():
    tap(buttons["x"])
    time.sleep(3)

def base():
    tap(buttons["right"])
    time.sleep(1)
    tap(buttons["right"])
    time.sleep(1)
    tap(buttons["x"])
    time.sleep(1)
    tap(buttons["x"])
    time.sleep(1)
    tap(buttons["up"])
    time.sleep(1)
    tap(buttons["x"])
    time.sleep(1)
    tap(buttons["start"])
    time.sleep(1)
    tap(buttons["up"])
    time.sleep(1)
    tap(buttons["x"])
    time.sleep(1)

def battle():

    tap(buttons["square"])
    time.sleep(button_delay)
    tap(buttons["square"])
    time.sleep(button_delay)
    tap(buttons["square"])
    time.sleep(button_delay)
    tap(buttons["circle"])

    time.sleep(2.3)

    tap(buttons["circle"])
    time.sleep(button_delay)
    tap(buttons["circle"])
    time.sleep(button_delay)
    tap(buttons["square"])
    time.sleep(button_delay)
    tap(buttons["circle"])

    time.sleep(1)

while True:
    printScreen()

    phase = diff("screenshot.png", images)

    match phase:
        case "images/chest.png":
            chest()
        case "images/status.png":
            status()
        case "images/base.png":
            base()
        case "images/loading.png":
            tap(buttons["x"])
        case "images/battle.png":
            battle()