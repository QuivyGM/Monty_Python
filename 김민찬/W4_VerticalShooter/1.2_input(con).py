import pygame

pygame.init()

# ------------------------ 컨트롤러 init 및 입력 확인  ------------------------#
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")
    # ------------------------------------------------------------------------------------#

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move Object with Controller")

# Set up object
object_color = (255, 0, 0)
object_size = 50
object_x, object_y = width // 2, height // 2
object_speed = 5

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ------------------------ 컨트롤러 입력으로 변경  ------------------------#
    # Controller input
    if pygame.joystick.get_count() > 0:  # Check if a joystick is connected
        # Get the axis values (-1 to 1)
        axis_x = joystick.get_axis(0)  # Left stick horizontal
        axis_y = joystick.get_axis(1)  # Left stick vertical

        # Move the object based on the joystick position
        if abs(axis_x) > 0.1:  # Dead zone to ignore small inputs
            object_x += int(axis_x * object_speed)
        if abs(axis_y) > 0.1:  # Dead zone
            object_y += int(axis_y * object_speed)

    # Keep the object within the screen bounds
    object_x = max(0, min(width - object_size, object_x))
    object_y = max(0, min(height - object_size, object_y))
    # ------------------------------------------------------------------------------------#



    window.fill((0, 0, 0))

    pygame.draw.rect(window, object_color, (object_x, object_y, object_size, object_size))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()