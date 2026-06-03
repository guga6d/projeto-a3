import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image
from app.views.components.nav_button import NavButton
from app.views.components.result_card import ResultCard


# Tela final mostrada depois que a sessão é encerrada.
class WinnerView(ctk.CTkFrame):
    def __init__(self, master, winner: dict | None, on_restart,
                 resolve_destination_meta=None):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.winner = winner
        self.on_restart = on_restart
        self.resolve_destination_meta = resolve_destination_meta

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_decoration()
        self._build_title()
        self._build_winner_card()
        self._build_footer()

    def _build_decoration(self):
        plane_image = load_ctk_image(ui_assets.WINNER_BACKGROUND, (300, 300))

        if plane_image is not None:
            decoration = ctk.CTkLabel(self, image=plane_image, text="")
            decoration.place(relx=0, rely=0, x=0, y=0)

    def _build_title(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, pady=(60, 30), padx=20)
        header.grid_columnconfigure(0, weight=1)

        if self.winner is not None:
            destination = self.winner["destination"]

            title_row = ctk.CTkFrame(header, fg_color="transparent")
            title_row.grid(row=0, column=0)

            title = ctk.CTkLabel(
                title_row,
                text=f"O destino mais votado foi:\n{destination}",
                font=ui_theme.FONT_TITLE,
                text_color=ui_theme.TEXT_PRIMARY,
                justify="center",
            )
            title.pack(side="left")

            congrats_icon = load_ctk_image(ui_assets.ICON_CONGRATS, (36, 36))

            if congrats_icon is not None:
                icon_label = ctk.CTkLabel(title_row, image=congrats_icon, text="")
                icon_label.pack(side="left", padx=(10, 0), anchor="n", pady=(4, 0))
        else:
            title = ctk.CTkLabel(
                header,
                text="A votação foi encerrada sem votos registrados.",
                font=ui_theme.FONT_TITLE,
                text_color=ui_theme.TEXT_PRIMARY,
                justify="center",
            )
            title.grid(row=0, column=0)

    def _build_winner_card(self):
        if self.winner is None:
            return

        destination = self.winner["destination"]
        meta = self.resolve_destination_meta(destination) if self.resolve_destination_meta else {}

        card = ResultCard(
            self,
            destination=destination,
            votes_text=f"{self.winner['votes']}\nVotos!",
            image_path=meta.get("image"),
            image_size=(320, 200),
        )
        card.grid(row=1, column=0, pady=10)

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=30, pady=24)
        footer.grid_columnconfigure(0, weight=1)

        restart_button = NavButton(
            footer,
            text="Voltar ao início",
            command=self.on_restart,
        )
        restart_button.configure(width=180)
        restart_button.grid(row=0, column=0, sticky="e")
