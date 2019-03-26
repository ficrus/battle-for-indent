import arcade


class Check:
    def check_mouse_enter_for_buttons(x, y, button_list):
        for button in button_list:
            if (x < button.center_x + button.width / 2) and (x > button.center_x - button.width / 2) \
                    and (y < button.center_y + button.height / 2) and (y > button.center_y - button.height / 2):
                button.on_enter()
                break
            else:
                button.on_leave()

    def check_mouse_press_for_buttons(x, y, button_list):
        """ Given an x, y, see if we need to register any button clicks. """
        for button in button_list:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()

    def check_mouse_release_for_buttons(x, y, button_list):
        """ If a mouse button has been released, see if we need to process
            any release events. """
        for button in button_list:
            if button.pressed:
                button.on_release()


class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 face_entered_color=arcade.color.ALMOND,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.entered = False
        self.face_color = face_color
        self.face_entered_color = face_entered_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        if not self.entered:
            color1 = self.face_color
        else:
            color1 = self.face_entered_color

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, color1)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def on_enter(self):
        self.entered = True

    def on_leave(self):
        self.entered = False

