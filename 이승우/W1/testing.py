import pygame
import sys

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Check if a controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller detected!")
    pygame.quit()
    sys.exit()

# Initialize the first connected joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller connected: {joystick.get_name()}")

# Set up screen dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controller Layout Tester")

# Font for displaying text
font = pygame.font.Font(None, 24)

# Define layout with positions
layout = {
    "Left": {
        "L2": (50, 50),                # Left Trigger Axis (LT, swapped with Right Stick V)
        "L1": (50, 80),                # Left Bumper (LB)
        "Left Stick V": (50, 110),     # Left Stick Vertical Axis (swapped with Left Stick H)
        "Left Stick H": (50, 140),     # Left Stick Horizontal Axis (swapped with Left Stick V)
        "L3": (50, 170),               # Left Stick Button
        "D-Pad Up": (50, 200),         # D-Pad Up (hat position)
        "D-Pad Left": (50, 230),       # D-Pad Left
        "D-Pad Right": (50, 260),      # D-Pad Right
        "D-Pad Down": (50, 290),       # D-Pad Down
    },
    "Middle": {
        "Xbox Button": (WIDTH // 2 - 80, 50),     # Xbox Button (might not work)
        "Back": (WIDTH // 2 - 80, 80),            # Back Button
        "Start": (WIDTH // 2 + 80, 80),           # Start Button
        "Share": (WIDTH // 2 - 80, 110),          # Extra Button 11
    },
    "Right": {
        "R2": (WIDTH - 200, 50),                  # Right Trigger Axis (RT)
        "R1": (WIDTH - 200, 80),                  # Right Bumper (RB)
        "Y": (WIDTH - 200, 110),                  # Y Button
        "X": (WIDTH - 200, 140),                  # X Button
        "A": (WIDTH - 200, 170),                  # A Button
        "B": (WIDTH - 200, 200),                  # B Button
        "Right Stick H": (WIDTH - 200, 230),      # Right Stick Horizontal Axis (moved below B)
        "Right Stick V": (WIDTH - 200, 260),      # Right Stick Vertical Axis (moved below B and swapped with L2)
        "R3": (WIDTH - 200, 290),                 # Right Stick Button (moved below B)
    },
}

# Button and axis mappings
button_mapping = {
    "A": 0, "B": 1, "X": 2, "Y": 3,
    "L1": 4, "R1": 5, "Back": 6, "Start": 7,
    "L3": 8, "R3": 9,
    "Share": 11
}

axis_mapping = {
    "L2": 4, "R2": 5, "Left Stick V": 0, "Left Stick H": 1,   # Swapped Left Stick H and V, and L2 with Right Stick V
    "Right Stick H": 3, "Right Stick V": 2                    # Swapped Right Stick V and L2
}

# D-Pad (hat) directions
hat_directions = {
    "D-Pad Up": (0, 1),
    "D-Pad Down": (0, -1),
    "D-Pad Left": (-1, 0),
    "D-Pad Right": (1, 0)
}
hat_position = (0, 0)  # Initial D-pad position

# Function to render text on the screen
def draw_text(text, position, color=(255, 255, 255)):
    label = font.render(text, True, color)
    screen.blit(label, position)

# Main loop to display controller inputs
clock = pygame.time.Clock()
running = True
while running:
    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update D-pad (hat) state
    if joystick.get_numhats() > 0:
        hat_position = joystick.get_hat(0)

    # Display Left Section
    for name, position in layout["Left"].items():
        if name in axis_mapping:
            axis_value = joystick.get_axis(axis_mapping[name])
            draw_text(f"{name}: {axis_value:.2f}", position)
        elif name in hat_directions:
            color = (255, 0, 0) if hat_position == hat_directions[name] else (255, 255, 255)
            draw_text(name, position, color)
        elif name in button_mapping:
            button_state = joystick.get_button(button_mapping[name])
            color = (255, 0, 0) if button_state else (255, 255, 255)
            draw_text(name, position, color)

    # Display Middle Section
    for name, position in layout["Middle"].items():
        if name in button_mapping:
            button_state = joystick.get_button(button_mapping[name])
            color = (255, 0, 0) if button_state else (255, 255, 255)
            draw_text(name, position, color)
        else:
            draw_text(f"{name}: Not detected", position, (128, 128, 128))  # Placeholder for Xbox Button

    # Display Right Section
    for name, position in layout["Right"].items():
        if name in axis_mapping:
            axis_value = joystick.get_axis(axis_mapping[name])
            draw_text(f"{name}: {axis_value:.2f}", position)
        elif name in button_mapping:
            button_state = joystick.get_button(button_mapping[name])
            color = (255, 0, 0) if button_state else (255, 255, 255)
            draw_text(name, position, color)

    # Refresh the display
    pygame.display.flip()
    clock.tick(30)  # Limit the frame rate to 30 FPS

# Clean up
pygame.quit()
sys.exit()