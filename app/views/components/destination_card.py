import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image, resolve_image


# Card de destino usado na tela de votação. Mostra imagem, nome e botão "Votar".
class DestinationCard(ctk.CTkFrame):
    IMAGE_SIZE = (240, 160)

    def __init__(self, master, destination: str, image_path: str | None = None,
                 subtitle: str = "", command=None):
        super().__init__(
            master,
            fg_color=ui_theme.CARD_BACKGROUND,
            corner_radius=ui_theme.CARD_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
        )

        self.destination = destination
        self.image_path = image_path
        self.subtitle = subtitle
        self.command = command

        self.grid_columnconfigure(0, weight=1)

        self._build_card()

    def _build_card(self):
        resolved = resolve_image(self.image_path) or resolve_image(ui_assets.NOT_FOUND_IMAGE)
        ctk_image = load_ctk_image(resolved, size=self.IMAGE_SIZE)

        if ctk_image is not None:
            self.image_label = ctk.CTkLabel(self, image=ctk_image, text="")
        else:
            self.image_label = ctk.CTkLabel(
                self,
                text="(imagem)",
                width=self.IMAGE_SIZE[0],
                height=self.IMAGE_SIZE[1],
                fg_color=ui_theme.BACKGROUND_COLOR,
                text_color=ui_theme.TEXT_MUTED,
                corner_radius=ui_theme.CARD_RADIUS,
            )

        self.image_label.grid(row=0, column=0, padx=18, pady=(18, 12))

        self.title_label = ctk.CTkLabel(
            self,
            text=self.destination,
            font=ui_theme.FONT_OPTION_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
        )
        self.title_label.grid(row=1, column=0, padx=18, pady=(0, 2))

        if self.subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self,
                text=self.subtitle,
                font=ui_theme.FONT_OPTION_DESC,
                text_color=ui_theme.TEXT_MUTED,
            )
            self.subtitle_label.grid(row=2, column=0, padx=18, pady=(0, 10))

        self.vote_button = ctk.CTkButton(
            self,
            text="Votar",
            command=self._on_vote,
            fg_color=ui_theme.PRIMARY_BUTTON,
            hover_color=ui_theme.PRIMARY_BUTTON_HOVER,
            text_color="#FFFFFF",
            font=ui_theme.FONT_BUTTON,
            corner_radius=ui_theme.BUTTON_RADIUS,
            height=40,
            width=160,
        )
        self.vote_button.grid(row=3, column=0, padx=18, pady=(0, 22))

    def _on_vote(self):
        if self.command is not None:
            self.command(self.destination)
