from usbbutton import USBButton
from blinkytape import BlinkyTape
import threading
from datetime import timedelta, datetime
import glob

TIME_MINUTES = 2.0
LED_COUNT = 60
N_TICK_INTERVAL = TIME_MINUTES * 60 / float(LED_COUNT)
LED_UPDATE_INTERVAL = 0.1
BLINK_INTERVAL = 1
RED = [255, 0, 0]
GREEN = [0, 255, 0]
OFF = [0, 0, 0]

class pitimer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.button = USBButton()
        self.button.subscribe_button(self.button_update)
        self.button.start()
        self.tape = BlinkyTape(port='/dev/ttyACM0')
        self.n = 60
        self.blink_led = True
        self.next_blink = datetime.now()
        self.next_led_update = datetime.now()
        self.next_n_update = datetime.now()

    def run(self):
        while True:
            if datetime.now() >= self.next_blink:
                self.toggle_blink()
                self.next_blink = datetime.now() + timedelta(
                    seconds=BLINK_INTERVAL)
            if datetime.now() >= self.next_led_update:
                self.update_leds()
                self.next_led_update = datetime.now() + timedelta(
                    seconds=LED_UPDATE_INTERVAL)
            if datetime.now() >= self.next_n_update:
                self.n_tick()
                self.next_n_update = datetime.now() + timedelta(
                    seconds=N_TICK_INTERVAL)

    def button_update(self, button_pressed):
        if button_pressed:
            self.n = 0

    def toggle_blink(self):
        if self.blink_led:
            self.blink_led = False
        else:
            self.blink_led = True

    def update_leds(self):
        if self.n >= 60 and self.blink_led:
            if self.button.get_color() != OFF:
                self.button.set_color(OFF)
        elif self.n >= 60:
            if self.button.get_color() != RED:
                self.button.set_color(RED)
        else:
            if self.button.get_color() != [self.n, 60 - self.n, 0]:    
                self.button.set_color([self.n, 60 - self.n, 0])
        b_leds = []
        for led_i in range(0, self.n):
            if led_i == self.n - 1 and self.blink_led:
                r = 0
                g = 0
                b = 0
            elif led_i == self.n - 1 and not self.blink_led:
                r = led_i
                g = 60 - led_i
                b = 0
            else:
                r = led_i
                g = 60 - led_i
                b = 0
            b_leds.append((r, g, b))
        b_leds.extend([[0, 0, 0]] * (LED_COUNT - self.n))
        self.tape.send_list(b_leds)

    def n_tick(self):
        if self.n <= 60:
            self.n += 1


if __name__ == "__main__":
    ptimer = pitimer()
    ptimer.start()
    while True:
        pass
