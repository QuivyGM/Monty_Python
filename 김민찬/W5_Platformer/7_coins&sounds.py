"""
Platformer Game with Controller Support, Randomized Coins, and Infinite Ground
"""
import arcade
import pygame
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

GROUND_TILE_WIDTH = 64
COIN_SPAWN_CHANCE = 0.3  # 30% chance to spawn a coin per ground tile
COIN_HEIGHT_RANGE = (150, 300)  # Random coin height range above ground


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene and player setup
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None

        # Camera
        self.camera = None

        # Track ground spawning
        self.ground_tiles_spawned = 0

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

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here."""
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins")

        # Set up the player
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Initial ground
        for x in range(0, SCREEN_WIDTH + GROUND_TILE_WIDTH, GROUND_TILE_WIDTH):
            self.add_ground_tile(x)

        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def add_ground_tile(self, x):
        """Add a ground tile at the given x position."""
        ground = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
        ground.center_x = x
        ground.center_y = 32
        self.scene.add_sprite("Walls", ground)

        # Randomly spawn a coin above the ground
        if random.random() < COIN_SPAWN_CHANCE:
            self.add_coin(x)

        self.ground_tiles_spawned += 1

    def add_coin(self, x):
        """Add a coin at a random height above the given x position."""
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = random.randint(*COIN_HEIGHT_RANGE)  # Random height
        self.scene.add_sprite("Coins", coin)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera.use()  # Activate camera
        self.scene.draw()

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

    def on_update(self, delta_time):
        """Movement and game logic."""
        self.physics_engine.update()

        # Spawn new ground tiles and coins as the player moves right
        camera_right_edge = self.camera.position[0] + SCREEN_WIDTH
        while self.ground_tiles_spawned * GROUND_TILE_WIDTH < camera_right_edge + SCREEN_WIDTH:
            self.add_ground_tile(self.ground_tiles_spawned * GROUND_TILE_WIDTH)

        # Check for coin collisions
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Remove collected coins and play sound
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        # Center the camera to follow the player
        self.center_camera_to_player()

        # Handle joystick input
        if self.joystick:
            axis_x = self.joystick.get_axis(0)  # Horizontal axis
            self.player_sprite.change_x = axis_x * PLAYER_MOVEMENT_SPEED

            # Jump button (e.g., button 0 for "A")
            if self.joystick.get_button(0) and self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def center_camera_to_player(self):
        """Smoothly center the camera on the player."""
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Ensure the camera doesn't scroll below 0
        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        self.camera.move_to((screen_center_x, screen_center_y), speed=0.1)

    def on_close(self):
        """Clean up resources when the window is closed."""
        if self.joystick:
            self.joystick.quit()
        pygame.quit()
        super().on_close()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
