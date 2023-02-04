import pygame.font

from ship import ShipHp


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (50, 50, 50)
        self.font = pygame.font.SysFont(None, 36)
        # 准备初始得分图像
        self.prep_score()
        self.prep_level()
        self.prep_shipHps()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score_str = "Score: {:,}".format(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, None)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(
            level_str, True, self.text_color, None)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    def prep_shipHps(self):
        """显示飞船生命值"""
        self.ship_lefts = pygame.sprite.Group()

        hp = ShipHp(self)
        hp_width, hp_height = hp.rect.size

        for number in range(self.stats.ship_hp):
            new_hp = ShipHp(self)
            new_hp.rect.x = new_hp.rect.x + (hp_width + hp_width//2) * number
            self.ship_lefts.add(new_hp)

    def show_score(self):
        """显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ship_lefts.draw(self.screen)  # 显示生命值
