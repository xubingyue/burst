# -*- coding: utf-8 -*-

from share.mixins import RoutesMixin, BlueprintEventsMixin


class Blueprint(RoutesMixin, BlueprintEventsMixin):

    name = None
    app = None

    def __init__(self, name):
        RoutesMixin.__init__(self)
        BlueprintEventsMixin.__init__(self)
        self.name = name

    def register_to_app(self, app):
        """
        注册到app上
        """
        self.app = app
        # 注册上
        self.app.blueprints.append(self)
