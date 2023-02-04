class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 游戏刚启动时处于活动状态
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_hp = self.settings.ship_limit
        self.score = 0  # 游戏分数
        self.level = 1  # 游戏等级
        self.settings.initialize_dynamic_settings()
