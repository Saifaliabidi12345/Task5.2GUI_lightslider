import tkinter as tk
from tkinter import Scale, Label, Button
import tkinter.font
import RPi.GPIO as GPIO
from time import sleep
import threading

led_pins = {"red": 26, "yellow": 13, "green": 19}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)

pwm_leds = {}
for color, pin in led_pins.items():
    pwm_leds[color] = GPIO.PWM(pin, 100)
    pwm_leds[color].start(0)

def update_brightness(color, value):
    duty_cycle = int(value)
    pwm_leds[color].ChangeDutyCycle(duty_cycle)
    if duty_cycle > 0:
        GPIO.output(led_pins[color], GPIO.HIGH)
    else:
        GPIO.output(led_pins[color], GPIO.LOW)

def close_window():
    for pwm in pwm_leds.values():
        pwm.stop()
    GPIO.cleanup()
    win.destroy()

win = tk.Tk()
win.title("Task5.2c Rpi - LED slider")
win.geometry("800x600")
myFont = tkinter.font.Font(family='Helvetica', size=14, weight="bold")

sliders = {}
for color in led_pins.keys():
    label = Label(win, text=f"{color.capitalize()} LED")
    label.pack()
    slider = Scale(win, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda value, color=color: update_brightness(color, value), length=300)
    slider.pack()
    sliders[color] = slider

exitButton = Button(win, text="Exit", font=myFont, command=close_window, bg='light gray', height=1, width=6, borderwidth=2, highlightthickness=1)
exitButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

def change_intensity():
    while True:
        for i in range(101):
            for color in ["yellow", "green"]:
                sliders[color].set(i)
                update_brightness(color, i)
                sleep(0.1)
            if sliders["yellow"].get() != i or sliders["green"].get() != i:
                return

intensity_thread = threading.Thread(target=change_intensity)
intensity_thread.start()

try:
    win.mainloop()
except KeyboardInterrupt:
    close_window()
