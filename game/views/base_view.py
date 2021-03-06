import arcade


class BaseView(arcade.View):
    def __init__(self, views):
        super().__init__()
        self.views = views
        self.previous_view = None

    def switch_to(self, viewname):
        new_view = self.views[viewname]
        new_view.previous_view = self

        if viewname != "game":
            self.window.set_viewport(0, self.window.width, 0, self.window.height)
        self.window.show_view(new_view)

    def switch_to_previous(self):
        self.window.show_view(self.previous_view)
