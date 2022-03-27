from discord.ui import Button, View


class Disabled_View:
    def __init__(self, view: View) -> None:
        self.view = view

    def generate(self) -> View:
        buttons = [comp for comp in self.view.children if isinstance(comp, Button)]
        dis_view = View(timeout=self.view.timeout)
        for b in buttons:
            dis_button = Button(
                style=b.style,
                label=b.label,
                disabled=True,
                emoji=b.emoji,
                row=b.row,
            )
            dis_view.add_item(dis_button)
        return dis_view
