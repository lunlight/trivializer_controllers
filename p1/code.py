import time
import board
import digitalio
import usb_hid
import neopixel
import simpleio
import pwmio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# PLAYER 1
# Button setup
button_pin = digitalio.DigitalInOut(board.A2)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

# NeoPixel setup
num_pixels = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.2, auto_write=False)

# LED setup
led_pin = digitalio.DigitalInOut(board.A1)
led_pin.direction = digitalio.Direction.OUTPUT

# Keyboard setup
keyboard = Keyboard(usb_hid.devices)

# Buzzer setup
buzzer = pwmio.PWMOut(board.AO, variable_frequency=True)

# Color wheel function
def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

# Buzz function
def buzz(duration):
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        buzzer.frequency = 440  # A4 note
        buzzer.duty_cycle = 32768  # 50% duty cycle
        time.sleep(0.001)
        buzzer.frequency = 880  # A5 note
        buzzer.duty_cycle = 32768  # 50% duty cycle
        time.sleep(0.001)
    buzzer.duty_cycle = 0  # Turn off the buzzer

# Main loop
color_index = 0
while True:
    if not button_pin.value:  # Check if button is pressed
        keyboard.press(Keycode.ONE)
        time.sleep(0.1)
        keyboard.release(Keycode.ONE)
        
        # Start the buzz
        buzz(0.6)  # Buzz for 0.6 seconds

        # Flash 3 times while tone is playing
        for _ in range(4):
            pixels.fill(wheel(color_index))
            pixels.show()
            led_pin.value = True
            time.sleep(0.1)
            pixels.fill((0, 0, 0))  # Turn off pixels
            pixels.show()
            led_pin.value = False
            time.sleep(0.1)

        # Wait for button release to avoid repeated triggers
        while not button_pin.value:
            pass
        time.sleep(0.1)  # Debounce delay

    # Color cycling
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + color_index
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    color_index = (color_index + 1) % 256
    time.sleep(0.05)
