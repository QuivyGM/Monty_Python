import pygame

pygame.init()
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Use the first connected joystick
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected!")

# ------------------------ 바탕 & 오브젝트에 텍스쳐 적용  ------------------------#
# Set up display
width, height = 1000, 600
window = pygame.display.set_mode((width, height))
# background = pygame.image.load('pixel_sky.png')
background = pygame.transform.scale(pygame.image.load('pixel_sky.png'), (width, height))
pygame.display.set_caption("Move Object with Controller")

# Set up object
object_size = 100
object_image = pygame.transform.scale(pygame.image.load('ufo.png'), (object_size, object_size))
# object_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('spaceship.png'), (object_size, object_size)), 45)  # Rotate by 45 degrees
object_x, object_y = width // 2, height // 2
object_speed = 5
# ------------------------------------------------------------------------------------#

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # ------------------------ 바탕 & 오브젝트 그리기  ------------------------#
    # Render background and object
    # window.blit : 이미지를 화면에 그리는 함수
    # blit 은 줄임말로 block transfer의 약자로, 이미지를 화면에 그리는 함수
    # blit(이미지, 위치) : 이미지를 화면의 위치에 그림
    window.blit(background, (0, 0)) # 바탕 이미지를 그림
    window.blit(object_image, (object_x, object_y))  # 오브젝트를 그림
    # ------------------------------------------------------------------------------------#

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()