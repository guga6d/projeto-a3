import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image
from app.views.components.nav_button import NavButton
from app.views.components.result_card import ResultCard


# Tela de resultado parcial mostrada depois que o usuário vota.
class PartialResultsView(ctk.CTkFrame):
    STACK_BREAKPOINT = 900

    def __init__(self, master, top_results: list[dict], on_vote_again, on_finish,
                 resolve_destination_meta=None):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.top_results = top_results
        self.on_vote_again = on_vote_again
        self.on_finish = on_finish
        self.resolve_destination_meta = resolve_destination_meta

        self.cards: list[ResultCard] = []
        self._stacked: bool | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_cards()
        self._build_footer()

        self.bind("<Configure>", self._on_resize)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(40, 12))
        header.grid_columnconfigure(0, weight=1)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.grid(row=0, column=0)

        success_icon = load_ctk_image(ui_assets.ICON_SUCCESS, (40, 40))

        if success_icon is not None:
            icon_label = ctk.CTkLabel(title_row, image=success_icon, text="")
            icon_label.pack(side="right", padx=(12, 0))

        title = ctk.CTkLabel(
            title_row,
            text="Voto registrado!",
            font=ui_theme.FONT_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header,
            text="Veja o resultado parcial:",
            font=ui_theme.FONT_SUBTITLE,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        subtitle.grid(row=1, column=0, pady=(8, 0))

    def _build_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="n", padx=30, pady=(24, 0))

        if not self.top_results:
            empty_label = ctk.CTkLabel(
                self.cards_frame,
                text="Ainda não há votos suficientes para exibir o resultado.",
                font=ui_theme.FONT_BODY,
                text_color=ui_theme.TEXT_MUTED,
            )
            empty_label.grid(row=0, column=0, padx=20, pady=40)
            return

        for entry in self.top_results:
            destination = entry["destination"]
            votes = entry["votes"]

            meta = self.resolve_destination_meta(destination) if self.resolve_destination_meta else {}

            card = ResultCard(
                self.cards_frame,
                destination=destination,
                votes_text=f"{votes} votos",
                image_path=meta.get("image"),
            )
            self.cards.append(card)

        self._layout_cards(stacked=False)

    def _layout_cards(self, stacked: bool):
        if self._stacked == stacked:
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

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=30, pady=24)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=1)
        footer.grid_columnconfigure(2, weight=1)

        vote_again_button = NavButton(
            footer,
            text="Votar novamente",
            command=self.on_vote_again,
        )
        vote_again_button.configure(width=180)
        vote_again_button.grid(row=0, column=0, sticky="w")

        thanks_text = ctk.CTkLabel(
            footer,
            text="Obrigado pelo seu voto!",
            font=ui_theme.FONT_BUTTON,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        thanks_text.grid(row=0, column=1, padx=12, sticky="ns")

        finish_button = NavButton(
            footer,
            text="Finalizar votação",
            command=self.on_finish,
        )
        finish_button.configure(width=180)
        finish_button.grid(row=0, column=2, sticky="e")

    def _on_resize(self, event):
        if event.widget is not self or not self.cards:
            return

        stacked = event.width < self.STACK_BREAKPOINT
        self._layout_cards(stacked=stacked)
