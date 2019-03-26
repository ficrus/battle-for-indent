import arcade
import random
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

MOVEMENT_SPEED = 5

COIN_COUNT = 50
COIN_SCALE = 0.5


class MyAnimation(arcade.Window):
        """ Main application class. """
        def __init__(self, width, height):
            """
            Initializer
            """
            super().__init__(width, height, update_rate=1/60)

            """ Set up the game and initialize the variables. """

            # Sprite lists
            self.all_sprites_list = None

            # Set up the player
            self.player = None

            self.coin_list = None

        def setup(self):
            self.all_sprites_list = arcade.SpriteList()
            self.coin_list = arcade.SpriteList()

            self.player = arcade.AnimatedWalkingSprite()

            character_scale = 0.75
            self.player.stand_right_textures = []
            self.player.stand_right_textures.append(arcade.load_texture("images/character0.png",
                                                                        scale=character_scale))
            self.player.stand_left_textures = []
            self.player.stand_left_textures.append(arcade.load_texture("images/character0.png",
                                                                       scale=character_scale, mirrored=True))

            self.player.walk_right_textures = []

            self.player.walk_right_textures.append(arcade.load_texture("images/characterw0.png",
                                                                       scale=character_scale))
            self.player.walk_right_textures.append(arcade.load_texture("images/characterw1.png",
                                                                       scale=character_scale))
            self.player.walk_right_textures.append(arcade.load_texture("images/characterw2.png",
                                                                       scale=character_scale))
            self.player.walk_right_textures.append(arcade.load_texture("images/characterw3.png",
                                                                       scale=character_scale))

            self.player.walk_left_textures = []

            self.player.walk_left_textures.append(arcade.load_texture("images/characterw0.png",
                                                                      scale=character_scale, mirrored=True))
            self.player.walk_left_textures.append(arcade.load_texture("images/characterw1.png",
                                                                      scale=character_scale, mirrored=True))
            self.player.walk_left_textures.append(arcade.load_texture("images/characterw2.png",
                                                                      scale=character_scale, mirrored=True))
            self.player.walk_left_textures.append(arcade.load_texture("images/characterw3.png",
                                                                      scale=character_scale, mirrored=True))

            self.player.texture_change_distance = 20

            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = SCREEN_HEIGHT // 2
            self.player.scale = 0.8
            self.player.texture_change_distance = 12
            self.all_sprites_list.append(self.player)

            for i in range(COIN_COUNT):
                coin = arcade.AnimatedTimeSprite()
                coin.texture_change_frames = 4
                arcade.AnimatedTimeSprite()
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)

                coin.textures = []
                coin.textures.append(arcade.load_texture("images/gold-1.png", scale=COIN_SCALE))
                coin.textures.append(arcade.load_texture("images/gold-2.png", scale=COIN_SCALE))
                coin.textures.append(arcade.load_texture("images/gold-3.png", scale=COIN_SCALE))
                coin.textures.append(arcade.load_texture("images/gold-4.png", scale=COIN_SCALE))
                coin.textures.append(arcade.load_texture("images/gold-3.png", scale=COIN_SCALE))
                coin.textures.append(arcade.load_texture("images/gold-2.png", scale=COIN_SCALE))

                self.coin_list.append(coin)
                self.all_sprites_list.append(coin)

            # Set the background color
            arcade.set_background_color(arcade.color.AMAZON)

        def on_draw(self):
            """
            Render the screen.
            """

            # This command has to happen before we start drawing
            arcade.start_render()

            # Draw all the sprites.
            self.all_sprites_list.draw()

        def on_key_press(self, key, modifiers):
            """
            Called whenever the mouse moves.
            """
            if key == arcade.key.UP:
                self.player.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player.change_x = MOVEMENT_SPEED

        def on_key_release(self, key, modifiers):
            """
            Called when the user presses a mouse button.
            """
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player.change_y = 0

            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player.change_x = 0

        def update(self, delta_time):



            """ Movement and game logic """

            self.all_sprites_list.update()
            self.all_sprites_list.update_animation()

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for coin in hit_list:
                coin.kill()


def main():
    """ Main method """
    window = MyAnimation(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
