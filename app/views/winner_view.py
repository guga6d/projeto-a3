import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image
from app.views.components.nav_button import NavButton
from app.views.components.result_card import ResultCard


# Tela final mostrada depois que a sessão é encerrada.
class WinnerView(ctk.CTkFrame):
    STACK_BREAKPOINT = 900

    def __init__(self, master, winners: list[dict] | None, on_restart,
                 resolve_destination_meta=None):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.winners = winners or []
        self.on_restart = on_restart
        self.resolve_destination_meta = resolve_destination_meta
        self.cards: list[ResultCard] = []
        self._stacked: bool | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build_decoration()
        self._build_title()
        self._build_winner_cards()
        self._build_footer()

        self.bind("<Configure>", self._on_resize)

    def _format_vote_count(self, votes: int) -> str:
        return f"{votes} voto" if votes == 1 else f"{votes} votos"

    def _format_card_vote_count(self, votes: int) -> str:
        return f"{votes}\nVoto!" if votes == 1 else f"{votes}\nVotos!"

    def _build_decoration(self):
        plane_image = load_ctk_image(ui_assets.WINNER_BACKGROUND, (300, 300))

        if plane_image is not None:
            decoration = ctk.CTkLabel(self, image=plane_image, text="")
            decoration.place(relx=0, rely=0, x=0, y=0)

    def _build_title(self):
        if self.winners:
            is_tie = len(self.winners) > 1
            top_votes = self.winners[0]["votes"]
            congrats_icon = load_ctk_image(ui_assets.ICON_CONGRATS, (36, 36))

            if congrats_icon is not None:
                icon_label = ctk.CTkLabel(
                    self,
                    image=congrats_icon,
                    text="",
                    fg_color="transparent",
                    bg_color="transparent",
                )
                icon_label.grid(row=0, column=0, pady=(50, 10))

            title = ctk.CTkLabel(
                self,
                text=(
                    "Houve empate entre estes destinos:"
                    if is_tie
                    else f"O destino mais votado foi:\n{self.winners[0]['destination']}"
                ),
                font=ui_theme.FONT_TITLE,
                text_color=ui_theme.TEXT_PRIMARY,
                justify="center",
                fg_color="transparent",
                bg_color="transparent",
            )
            title.grid(row=1, column=0, padx=20)

            if is_tie:
                subtitle_text = f"Cada destino recebeu {self._format_vote_count(top_votes)}."
                subtitle = ctk.CTkLabel(
                    self,
                    text=subtitle_text,
                    font=ui_theme.FONT_SUBTITLE,
                    text_color=ui_theme.TEXT_SECONDARY,
                    justify="center",
                    fg_color="transparent",
                    bg_color="transparent",
                )
                subtitle.grid(row=2, column=0, pady=(8, 20), padx=20)
        else:
            title = ctk.CTkLabel(
                self,
                text="A votação foi encerrada sem votos registrados.",
                font=ui_theme.FONT_TITLE,
                text_color=ui_theme.TEXT_PRIMARY,
                justify="center",
                fg_color="transparent",
                bg_color="transparent",
            )
            title.grid(row=1, column=0, pady=(60, 30), padx=20)

    def _build_winner_cards(self):
        if not self.winners:
            return

        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=3, column=0, sticky="n", padx=30, pady=10)

        for winner in self.winners:
            destination = winner["destination"]
            meta = self.resolve_destination_meta(destination) if self.resolve_destination_meta else {}

            card = ResultCard(
                self.cards_frame,
                destination=destination,
                votes_text=self._format_card_vote_count(winner["votes"]),
                image_path=meta.get("image"),
                image_size=(320, 200),
            )
            self.cards.append(card)

        self._layout_cards(stacked=False)

    def _layout_cards(self, stacked: bool):
        if self._stacked == stacked or not self.cards:
            return

        self._stacked = stacked

        for child in self.cards_frame.winfo_children():
            child.grid_forget()

        if stacked:
            self.cards_frame.grid_columnconfigure(0, weight=1)

            for column in range(1, len(self.cards)):
                self.cards_frame.grid_columnconfigure(column, weight=0)

            for index, card in enumerate(self.cards):
                card.grid(row=index, column=0, padx=12, pady=10, sticky="ew")
        else:
            for index in range(len(self.cards)):
                self.cards_frame.grid_columnconfigure(index, weight=1)

            for index, card in enumerate(self.cards):
                card.grid(row=0, column=index, padx=12, pady=10, sticky="n")

    def _on_resize(self, event):
        if event.widget is not self or not self.cards:
            return

        stacked = event.width < self.STACK_BREAKPOINT
        self._layout_cards(stacked=stacked)

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=4, column=0, sticky="ew", padx=30, pady=24)
        footer.grid_columnconfigure(0, weight=1)

        restart_button = NavButton(
            footer,
            text="Voltar ao início",
            command=self.on_restart,
        )
        restart_button.configure(width=180)
        restart_button.grid(row=0, column=0, sticky="e")
