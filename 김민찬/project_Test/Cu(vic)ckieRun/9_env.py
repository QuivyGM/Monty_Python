"""
Platformer Game with Controller Support
"""
import arcade
import pygame

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

PLAYER_START_X = 64
PLAYER_START_Y = 225

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene and player setup
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        # Game state
        self.score = 0
        self.reset_score = True
        self.end_of_map = 0
        self.level = 1

        # Pygame joystick support
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        """Set up the game here."""
        # Set up cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Reset or retain score
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Load map
        map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        layer_options = {
            LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
            LAYER_NAME_COINS: {"use_spatial_hash": True},
            LAYER_NAME_DONT_TOUCH: {"use_spatial_hash": True},
        }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Player setup
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Map boundary
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene[LAYER_NAME_PLATFORMS]
        )

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key in [arcade.key.UP, arcade.key.W] and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """Game logic."""
        self.physics_engine.update()

        # Handle coin collection
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_COINS]
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        # Check for falling off the map
        if self.player_sprite.center_y < -100:
            self.reset_player()

        # Check for collisions with "Don't Touch" layer
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]):
            self.reset_player()

        # Check for level completion
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            self.reset_score = False
            self.setup()

        # Update camera position
        self.center_camera_to_player()

        # Handle joystick input
        if self.joystick:
            axis_x = self.joystick.get_axis(0)  # Horizontal axis
            self.player_sprite.change_x = axis_x * PLAYER_MOVEMENT_SPEED
            if self.joystick.get_button(0) and self.physics_engine.can_jump():  # Button 0 for jump
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

    def reset_player(self):
        """Reset the player to the starting position."""
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        arcade.play_sound(self.game_over)

    def center_camera_to_player(self):
        """Center the camera on the player."""
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)
        self.camera.move_to((screen_center_x, screen_center_y), speed=0.1)

    def on_close(self):
        """Clean up resources on close."""
        if self.joystick:
            self.joystick.quit()
        pygame.quit()
        super().on_close()


def main():
    """Main function."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
