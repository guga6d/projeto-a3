import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image


# Botão usado para navegação secundária (Voltar, Próximo, Voltar ao início).
class NavButton(ctk.CTkButton):
    def __init__(self, master, text: str, command=None, icon: str = ""):
        self._icon = icon
        icon_size = (22, 16)
        icon_path = None
        ctk_image = None

        if icon == "back":
            icon_path = ui_assets.ICON_BACK
        elif icon == "forward":
            icon_path = ui_assets.ICON_NEXT

        if icon_path:
            ctk_image = load_ctk_image(icon_path, icon_size)

        self._image_enabled = ctk_image
        self._image_disabled = None

        if icon == "forward":
            self._image_disabled = load_ctk_image(ui_assets.ICON_NEXT_DISABLED, icon_size)

        if ctk_image is not None and icon == "back":
            super().__init__(
                master,
                text=f"  {text}",
                image=ctk_image,
                compound="left",
                command=command,
                fg_color=ui_theme.SECONDARY_BUTTON,
                hover_color=ui_theme.SECONDARY_BUTTON_HOVER,
                text_color=ui_theme.ACCENT_TEXT,
                font=ui_theme.FONT_BUTTON,
                corner_radius=ui_theme.BUTTON_RADIUS,
                height=44,
                width=140,
                border_width=0,
            )
        elif ctk_image is not None and icon == "forward":
            super().__init__(
                master,
                text=f"{text}  ",
                image=ctk_image,
                compound="right",
                command=command,
                fg_color=ui_theme.SECONDARY_BUTTON,
                hover_color=ui_theme.SECONDARY_BUTTON_HOVER,
                text_color=ui_theme.ACCENT_TEXT,
                font=ui_theme.FONT_BUTTON,
                corner_radius=ui_theme.BUTTON_RADIUS,
                height=44,
                width=140,
                border_width=0,
            )
        else:
            super().__init__(
                master,
                text=text,
                command=command,
                fg_color=ui_theme.SECONDARY_BUTTON,
                hover_color=ui_theme.SECONDARY_BUTTON_HOVER,
                text_color=ui_theme.ACCENT_TEXT,
                font=ui_theme.FONT_BUTTON,
                corner_radius=ui_theme.BUTTON_RADIUS,
                height=44,
                width=140,
                border_width=0,
            )

    def configure(self, require_redraw=False, **kwargs):
        if self._icon == "forward" and "state" in kwargs:
            if kwargs["state"] == "disabled" and self._image_disabled is not None:
                kwargs["image"] = self._image_disabled
            elif self._image_enabled is not None:
                kwargs["image"] = self._image_enabled

        super().configure(require_redraw=require_redraw, **kwargs)
