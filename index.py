import subprocess
import cv2
import numpy as np
import os
import time
import sys
import msvcrt

button_delay = 0.29
selected_device = None

# Left: 450, 500 | Right: 230, 550 | Up: 350, 450 | Down: 350, 650
# Triangle: 2200, 750 | X: 2200, 950 | Square: 2100, 850 | Circle: 2300, 850

images = [
    "images/base.png",
    "images/battle.png",
    "images/chest.png",
    "images/status.png",
    "images/loading.png",
    "images/world.png",
    "move/-1.png",
    "move/-2.png",
    "move/-3.png",
    "move/-4.png",
    "move/-5.png",
    "move/-6.png",
    "move/0.png",
    "move/1.png",
    "move/2.png",
    "move/3.png",
    "move/back-1.png",
    "move/back-2.png",
    "move/back-3.png",
    "move/back-4.png",
    "move/back-5.png",
    "move/back-6.png",
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

def get_key():
    """Captura uma tecla pressionada no Windows"""
    if sys.platform == 'win32':
        try:
            ch = msvcrt.getch()
            if ch == b'\xe0':  # Prefixo para teclas especiais (setas)
                ch = msvcrt.getch()
                if ch == b'H':  # Seta para cima
                    return 'UP'
                elif ch == b'P':  # Seta para baixo
                    return 'DOWN'
            return ch.decode('utf-8', errors='ignore')
        except:
            return ''
    else:
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def connect():
    """Lista dispositivos conectados e permite seleção interativa"""
    global selected_device
    
    # Lista todos os dispositivos conectados
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]  # Pula a primeira linha "List of devices attached"
    
    devices = []
    for line in lines:
        if line.strip() and '\t' in line:
            device_id, status = line.strip().split('\t')
            if status == 'device':  # Apenas dispositivos autorizados
                devices.append(device_id)
    
    if not devices:
        print("Nenhum dispositivo conectado!")
        return None
    
    if len(devices) == 1:
        selected_device = devices[0]
        print(f"Dispositivo selecionado: {selected_device}")
        return selected_device
    
    # Seleção interativa
    selected_index = 0
    
    while True:
        # Limpa a tela (simula)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Dispositivos Conectados ===\n")
        
        for i, device in enumerate(devices):
            marker = ">>> " if i == selected_index else "    "
            print(f"{marker}[{i+1}] {device}")
        
        print("\nUse W/S ou ↑/↓ para navegar, Enter para selecionar")
        
        key = get_key()
        
        # Detecta setas e teclas de navegação
        if key == 'UP' or key.lower() == 'w':
            selected_index = (selected_index - 1) % len(devices)
        elif key == 'DOWN' or key.lower() == 's':
            selected_index = (selected_index + 1) % len(devices)
        elif key == '\r' or key == '\n':  # Enter
            selected_device = devices[selected_index]
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Dispositivo selecionado: {selected_device}\n")
            return selected_device

def tap(button):
    print(f"Taponando {button}")
    cmd = ["adb"]
    if selected_device:
        cmd.extend(["-s", selected_device])
    cmd.extend(["shell", "input", "swipe", str(button[0]), str(button[1]), str(button[0]), str(button[1]), "100"])
    subprocess.run(cmd)

def printScreen():
    cmd = ["adb"]
    if selected_device:
        cmd.extend(["-s", selected_device])
    cmd.extend(["exec-out", "screencap", "-p"])
    with open("screenshot.png", "wb") as f:
        subprocess.run(cmd, stdout=f)

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

        if similarity > best_score:
            best_score = similarity
            best_match = path
    print(f"Semelhança com {best_match}: {best_score:.4f}")
    return best_match

def move():
    move = diff("screenshot.png", images)
    match move:
        case "move/-1.png":
            tap(buttons["right"])
        case "move/-2.png":
            tap(buttons["right"])
        case "move/-3.png":
            tap(buttons["right"])
        case "move/-4.png":
            tap(buttons["right"])
        case "move/-5.png":
            tap(buttons["right"])
        case "move/-6.png":
            tap(buttons["right"])
        case "move/0.png":
            tap(buttons["x"])
        case "move/1.png":
            tap(buttons["left"])
        case "move/2.png":
            tap(buttons["left"])
        case "move/3.png":
            tap(buttons["left"])
        case i if "back" in i:
            tap(buttons["circle"])

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

# Conecta ao dispositivo antes de iniciar o loop
connect()

if not selected_device:
    print("Nenhum dispositivo selecionado. Encerrando...")
    sys.exit(1)


while True:
    printScreen()
    
    phase = diff("screenshot.png", images)

    match phase:
        case "images/chest.png":
            chest()
        case "images/status.png":
            status()
        case v if "move" in v:
            move()
        case "images/loading.png":
            tap(buttons["x"])
        case "images/battle.png":
            battle()
        case "images/world.png":
            tap(buttons["x"])
            time.sleep(1)
            tap(buttons["up"])
            time.sleep(1)
            tap(buttons["x"])
            time.sleep(1)
            tap(buttons["up"])
            time.sleep(1)
            tap(buttons["x"])
            time.sleep(1)
            tap(buttons["up"])
            time.sleep(1)
            tap(buttons["x"])
    time.sleep(1)