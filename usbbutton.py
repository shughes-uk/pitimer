import threading
from time import sleep

import hid

SET_LEADING_BYTES = [0, 80, 221, 0, 0, 0]


class USBButton(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.h = hid.device()
        self.running = False
        self.h.open(53769, 4608)
        self.h.set_nonblocking(1)
        self.current_rgb = [0, 0, 0]
        self.new_rgb = [0, 0, 0]
        self.button_pressed = False
        self.button_callbacks = []

    def subscribe_button(self, callback):
        self.button_callbacks.append(callback)

    def set_color(self, rgb):
        self.new_rgb = rgb

    def get_color(self):
        return self.current_rgb

    def run(self):
        self.running = True
        while self.running:
            if self.current_rgb != self.new_rgb:
                self.send_color(self.new_rgb)
                self.current_rgb = self.new_rgb
            # request button status
            self.send([0x00, 0x02, 0x00, 0x00, 0x00])
            # wait
            sleep(0.05)
            rsp = self.h.read(1)
            if rsp:
                button_pressed = bool(rsp[0])
                if self.button_pressed != button_pressed:
                    self.button_pressed = button_pressed
                    for callback in self.button_callbacks:
                        callback(self.button_pressed)

    def send_color(self, rgb):
        self.send([0, 80, 221, 0, 0])
        self.send([0, rgb[0], rgb[1], rgb[2], rgb[0]])
        self.send([0, rgb[1], rgb[2], 0, 0])
        for x in range(1, 14):
            self.send([0, 0, 0, 0, 0])

    def send(self, byte_list):
        self.h.write(byte_list)


def press(status):
    print "Button %s" % status


if __name__ == "__main__":
    x = USBButton()
    x.start()
    x.subscribe_button(press)
    while True:
        pass
