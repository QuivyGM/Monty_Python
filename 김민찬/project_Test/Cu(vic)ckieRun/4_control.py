"""
Platformer Game with Fixed Controller Support
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Scaling and speed constants
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene and player setup
        self.scene = None
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Joystick support
        self.joystick = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here."""
        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the player
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Create some crates
        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

        # Set up joystick input
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.push_handlers(self)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key in [arcade.key.UP, arcade.key.W]:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when a key is released."""
        if key in [arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S]:
            self.player_sprite.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = 0

    def on_joybutton_press(self, button):
        """Called when a joystick button is pressed."""
        if button == 0:  # Assuming button 0 is jump
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED

    def on_joybutton_release(self, button):
        """Called when a joystick button is released."""
        if button == 0:  # Assuming button 0 is jump
            self.player_sprite.change_y = 0

    def on_joyaxis_motion(self, axis, value):
        """Called when a joystick axis moves."""
        if axis == "x":
            self.player_sprite.change_x = value * PLAYER_MOVEMENT_SPEED
        elif axis == "y":
            self.player_sprite.change_y = -value * PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        """Movement and game logic."""
        # Update joystick axis values if connected
        if self.joystick:
            self.player_sprite.change_x = self.joystick.x * PLAYER_MOVEMENT_SPEED
            self.player_sprite.change_y = -self.joystick.y * PLAYER_MOVEMENT_SPEED

        # Update the physics engine
        self.physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
