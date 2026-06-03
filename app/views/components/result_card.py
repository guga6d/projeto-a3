import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image, resolve_image


# Card de resultado, usado nas telas de resultado parcial e final. Mostra imagem,
# destino e quantidade de votos (ou texto customizado).
class ResultCard(ctk.CTkFrame):
    IMAGE_SIZE = (220, 150)

    def __init__(self, master, destination: str, votes_text: str,
                 image_path: str | None = None,
                 image_size: tuple[int, int] | None = None):
        super().__init__(
            master,
            fg_color=ui_theme.CARD_BACKGROUND,
            corner_radius=ui_theme.CARD_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
        )

        self.destination = destination
        self.votes_text = votes_text
        self.image_path = image_path
        self.image_size = image_size or self.IMAGE_SIZE

        self.grid_columnconfigure(0, weight=1)

        self._build_card()

    def _build_card(self):
        resolved = resolve_image(self.image_path) or resolve_image(ui_assets.NOT_FOUND_IMAGE)
        ctk_image = load_ctk_image(resolved, size=self.image_size)

        if ctk_image is not None:
            self.image_label = ctk.CTkLabel(self, image=ctk_image, text="")
        else:
            self.image_label = ctk.CTkLabel(
                self,
                text="(imagem)",
                width=self.image_size[0],
                height=self.image_size[1],
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
        self.title_label.grid(row=1, column=0, padx=18, pady=(0, 4))

        self.votes_label = ctk.CTkLabel(
            self,
            text=self.votes_text,
            font=ui_theme.FONT_BODY,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        self.votes_label.grid(row=2, column=0, padx=18, pady=(0, 20))
