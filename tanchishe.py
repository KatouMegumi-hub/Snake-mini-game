import pygame
import random

# 初始化pygame模块
pygame.init()

# 设置游戏窗口大小和标题
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('贪吃蛇小游戏')

# 创建时钟对象控制游戏帧率
clock = pygame.time.Clock()

try:
    # 加载图像并转换为透明模式
    up_head = pygame.image.load('up_head.png').convert_alpha()
    down_head = pygame.image.load('down_head.png').convert_alpha()
    left_head = pygame.image.load('left_head.png').convert_alpha()
    right_head = pygame.image.load('right_head.png').convert_alpha()
    body = pygame.image.load('body.png').convert_alpha()
    food_img = pygame.image.load('food.png').convert_alpha()
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# 蛇头图片尺寸
head_image_size = up_head.get_width()

# 蛇身图片尺寸，这里假设为蛇头尺寸的80%
body_image_size = int(head_image_size * 0.8)

# 调整蛇身图片的尺寸
body = pygame.transform.scale(body, (body_image_size, body_image_size))

# 初始化蛇的位置和移动方向
snake_list = [[head_image_size // 2, head_image_size // 2]]  # 蛇头的起始位置调整为中心点
move_direction = 'RIGHT'

# 食物的半径和初始位置，确保食物不会生成在屏幕边界外
food_radius = 15
food_position = [random.randint(food_radius, 490 - food_radius), random.randint(food_radius, 490 - food_radius)]

# 游戏主循环标志
running = True

# 控制蛇移动的计数器
move_counter = 0
move_interval = 6  # 蛇每6帧移动一次

# 游戏主循环
while running:
    clock.tick(60)  # 保持帧率为60 FPS

    # 填充背景色
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 更改移动方向，但不能反向移动
            if event.key == pygame.K_UP and move_direction != 'DOWN':
                move_direction = 'UP'
            elif event.key == pygame.K_DOWN and move_direction != 'UP':
                move_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and move_direction != 'RIGHT':
                move_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and move_direction != 'LEFT':
                move_direction = 'RIGHT'

    # 移动蛇
    if move_counter >= move_interval:
        head = list(snake_list[0])
        if move_direction == 'UP': head[1] -= body_image_size
        elif move_direction == 'DOWN': head[1] += body_image_size
        elif move_direction == 'LEFT': head[0] -= body_image_size
        elif move_direction == 'RIGHT': head[0] += body_image_size

        # 蛇头碰到屏幕边缘时从另一侧出现
        head[0] %= 500
        head[1] %= 500

        # 检查是否撞到自己的身体
        if head in snake_list[1:]:
            running = False

        # 更新蛇的位置
        snake_list.insert(0, head)
        if abs(head[0] - food_position[0]) <= food_radius and abs(head[1] - food_position[1]) <= food_radius:
            # 吃到食物后随机生成新的食物位置
            food_position = [random.randint(food_radius, 490 - food_radius), random.randint(food_radius, 490 - food_radius)]
        else:
            # 如果没有吃到食物，蛇尾部缩短一节
            snake_list.pop()

        move_counter = 0  # 重置计数器

    move_counter += 1  # 计数器递增

    # 绘制食物
    screen.blit(food_img, food_position)

    # 绘制蛇身
    for index, segment in enumerate(snake_list):
        if index == 0:  # 蛇头
            x = segment[0] - head_image_size // 2
            y = segment[1] - head_image_size // 2
            # 根据移动方向绘制不同的蛇头图像
            if move_direction == 'UP':
                screen.blit(up_head, (x, y))
            elif move_direction == 'DOWN':
                screen.blit(down_head, (x, y))
            elif move_direction == 'LEFT':
                screen.blit(left_head, (x, y))
            elif move_direction == 'RIGHT':
                screen.blit(right_head, (x, y))
        else:  # 蛇身
            x = segment[0] - body_image_size // 2
            y = segment[1] - body_image_size // 2
            screen.blit(body, (x, y))

    pygame.display.flip()

# 清理pygame资源
pygame.quit()