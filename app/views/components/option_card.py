import sys

import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image, resolve_image


# Card clicável usado nas telas de pergunta. Mostra um ícone redondo à esquerda
# e título/descrição à direita, como nos wireframes.
class OptionCard(ctk.CTkFrame):
    def __init__(self, master, option_text: str, icon_path: str | None = None,
                 description: str = "", command=None):
        super().__init__(
            master,
            fg_color=ui_theme.CARD_BACKGROUND,
            corner_radius=ui_theme.CARD_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
            height=92,
        )

        self.option_text = option_text
        self.icon_path = icon_path
        self.description = description
        self.command = command
        self._selected = False

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)

        self._build_card()
        self._bind_click(self)
        self._apply_pointer_cursor(self)

    def _pointer_cursor(self) -> str:
        if sys.platform == "darwin":
            return "pointinghand"
        return "hand2"

    def _apply_pointer_cursor(self, widget) -> None:
        widget.configure(cursor=self._pointer_cursor())

        for child in widget.winfo_children():
            self._apply_pointer_cursor(child)

    def _build_card(self):
        resolved = resolve_image(self.icon_path) or resolve_image(ui_assets.NOT_FOUND_IMAGE)
        icon_image = load_ctk_image(resolved, size=(56, 56))

        if icon_image is not None:
            self.icon_label = ctk.CTkLabel(self, image=icon_image, text="")
        else:
            self.icon_label = ctk.CTkLabel(
                self,
                text="",
                width=56,
                height=56,
                fg_color=ui_theme.BACKGROUND_COLOR,
                corner_radius=ui_theme.OPTION_ICON_RADIUS,
            )

        self.icon_label.grid(row=0, column=0, rowspan=2, padx=(20, 16), pady=14)

        self.title_label = ctk.CTkLabel(
            self,
            text=self.option_text,
            font=ui_theme.FONT_OPTION_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
            anchor="w",
        )
        self.title_label.grid(row=0, column=1, sticky="sw", pady=(18, 0))

        self.description_label = ctk.CTkLabel(
            self,
            text=self.description,
            font=ui_theme.FONT_OPTION_DESC,
            text_color=ui_theme.TEXT_MUTED,
            anchor="w",
        )
        self.description_label.grid(row=1, column=1, sticky="nw", pady=(0, 18))

    def _bind_click(self, widget):
        widget.bind("<Button-1>", self._on_click)

        for child in widget.winfo_children():
            self._bind_click(child)

    def _on_click(self, _event=None):
        if self.command is not None:
            self.command(self.option_text)

    def set_selected(self, selected: bool):
        self._selected = selected

        if selected:
            self.configure(border_color=ui_theme.PRIMARY_BUTTON, border_width=2)
        else:
            self.configure(border_color=ui_theme.CARD_BORDER, border_width=1)
