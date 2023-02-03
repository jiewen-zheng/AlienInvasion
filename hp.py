import pygame

from pygame.sprite import Sprite


class ShipHp(Sprite):
    """描述飞船hp的类"""

    def __init__(self, ship):
        """初始化生命值并设置位置"""
        super().__init__()
        self.screen = ship.screen
        self.screen_rect = ship.screen_rect

        # 加载飞船hp图像
        self.image = pygame.image.load('images/hp.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
