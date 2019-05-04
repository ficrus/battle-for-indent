class Event:
    def __init__(self):
        self.type = "none"


class PressEvent(Event):
    def __init__(self, x, y):
        super().__init__()
        self.type = "press"
        self.x = x
        self.y = y


class ReleaseEvent(Event):
    def __init__(self, x, y):
        super().__init__()
        self.type = "release"
        self.x = x
        self.y = y


class Listener:
    def __init__(self):
        self.listening_for = []

    pass


class ButtonListener(Listener):
    def __init__(self, button_list):
        super().__init__()
        self.listening_for.append("press")
        self.listening_for.append("release")
        self.button_list = button_list

    def press(self, press_event: PressEvent):
        for button in self.button_list:
            if press_event.x > button.center_x + button.width / 2:
                continue
            if press_event.x < button.center_x - button.width / 2:
                continue
            if press_event.y > button.center_y + button.height / 2:
                continue
            if press_event.y < button.center_y - button.height / 2:
                continue
            button.on_press()

    def release(self, release_event: ReleaseEvent):
        for button in self.button_list:
            if button.pressed:
                button.on_release()


class ListenersSupport:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)

    def remove_listener(self, listener: Listener):
        self.listeners.remove(listener)

    def on_event(self, event: Event):
        for listener in self.listeners:
            if event.type in listener.listening_for:
                getattr(listener, event.type)(event)
