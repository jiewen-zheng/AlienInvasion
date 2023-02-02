import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        # 创建窗口
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_hight))

        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")

        # 创建飞船
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()
            self.ship.update()
            self._update_screen()

    def _check_event(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 飞船向右移动
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    # 飞船向左移动
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    # 飞船向右移动
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    # 飞船向左移动
                    self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
