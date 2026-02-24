import tkinter as tk
import threading
import time
import math

root = None
canvas = None
circle = None
waves = []
running = False

WIDTH = 260
HEIGHT = 260
CENTER = WIDTH // 2
RADIUS = 45

def create_orb():
    global root, canvas, circle

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "black")
    root.geometry(f"{WIDTH}x{HEIGHT}+900+500")
    root.configure(bg="black")

    canvas = tk.Canvas(
        root, width=WIDTH, height=HEIGHT,
        bg="black", highlightthickness=0
    )
    canvas.pack()

    # Core orb
    circle = canvas.create_oval(
        CENTER-RADIUS, CENTER-RADIUS,
        CENTER+RADIUS, CENTER+RADIUS,
        fill="white", outline=""
    )

    # Waveform lines
    for i in range(7):
        line = canvas.create_line(
            CENTER-30+i*10, CENTER,
            CENTER-30+i*10, CENTER,
            fill="#9fdcff", width=3
        )
        waves.append(line)

    root.withdraw()
    animate()
    root.mainloop()

def animate():
    def loop():
        t = 0
        while True:
            if running:
                # Pulse orb
                r = RADIUS + 3 * math.sin(t)
                canvas.coords(
                    circle,
                    CENTER-r, CENTER-r,
                    CENTER+r, CENTER+r
                )

                # Wave animation
                for i, line in enumerate(waves):
                    h = 10 + abs(math.sin(t + i)) * 25
                    canvas.coords(
                        line,
                        CENTER-30+i*10, CENTER-h,
                        CENTER-30+i*10, CENTER+h
                    )

                t += 0.15
            time.sleep(0.03)

    threading.Thread(target=loop, daemon=True).start()

def show_orb():
    global running
    running = True
    root.deiconify()

def hide_orb():
    global running
    running = False
    root.withdraw()
