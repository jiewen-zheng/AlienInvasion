import pygame

from pygame.sprite import Sprite

from random import randint


class Alien(Sprite):
    """表示外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置rect属性
        self.type = randint(1, 4)
        self.hp = self.settings.alien_hp * self.type  # 按外星人类型计算生命值
        image = f"images/alien_{self.type}.png"
        # print(image)
        self.image = pygame.image.load(str(image))
        # self.image = pygame.image.load('images/alien_4.png')
        self.rect = self.image.get_rect()  # 获取图像rect属性

        # 初始化外星人初始位置
        self.rect.x = self.rect.width // 2
        self.rect.y = self.rect.height // 2

        # 此外星人移动方向
        self.direction = self.settings.alien_direction  # 默认方向

        # 存储外星人的水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """移动外星人"""
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x
        self.rect.y = self.y
