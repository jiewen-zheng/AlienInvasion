import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 设置项
        self.settings = ai_game.settings

        # 飞船属性x存储小数，依据像素矩形的相对值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标记
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # 获取飞船速度
        speed = self.settings.get_ship_speed()
        # 更新飞船对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:  # self.rect.right 返回飞船外接矩形右边缘的x 坐标
            self.x += speed
        if self.moving_left and self.rect.left > 0:
            self.x -= speed
        if self.moving_up and self.rect.top > 0:
            self.y -= speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += speed

        # 根据self.x y更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
