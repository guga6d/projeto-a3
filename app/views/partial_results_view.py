import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image
from app.views.components.result_card import ResultCard


# Tela de resultado parcial mostrada depois que o usuário vota.
class PartialResultsView(ctk.CTkFrame):
    SINGLE_COLUMN_BREAKPOINT = 760
    TWO_COLUMN_BREAKPOINT = 1180
    MAX_COLUMNS = 3

    def __init__(self, master, partial_results: list[dict], on_vote_again, on_finish,
                 resolve_destination_meta=None):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.partial_results = partial_results
        self.on_vote_again = on_vote_again
        self.on_finish = on_finish
        self.resolve_destination_meta = resolve_destination_meta

        self.cards: list[ResultCard] = []
        self._columns: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_cards()
        self._build_footer()

        self.bind("<Configure>", self._on_resize)

    def _format_vote_count(self, votes: int) -> str:
        return f"{votes} voto" if votes == 1 else f"{votes} votos"

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(40, 12))
        header.grid_columnconfigure(0, weight=1)

        success_icon = load_ctk_image(ui_assets.ICON_SUCCESS, (40, 40))

        title = ctk.CTkLabel(
            header,
            text="Voto registrado!",
            font=ui_theme.FONT_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
            image=success_icon,
            compound="right",
            padx=0,
        )
        title.grid(row=0, column=0)

        subtitle = ctk.CTkLabel(
            header,
            text="Veja o resultado parcial:",
            font=ui_theme.FONT_SUBTITLE,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        subtitle.grid(row=1, column=0, pady=(8, 0))

    def _build_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(24, 0))
        self.cards_frame.grid_columnconfigure(0, weight=1)

        self.cards_grid = ctk.CTkFrame(self.cards_frame, fg_color="transparent")
        self.cards_grid.grid(row=0, column=0, pady=0)

        if not self.partial_results:
            empty_label = ctk.CTkLabel(
                self.cards_grid,
                text="Ainda não há votos suficientes para exibir o resultado.",
                font=ui_theme.FONT_BODY,
                text_color=ui_theme.TEXT_MUTED,
            )
            empty_label.grid(row=0, column=0, padx=20, pady=40)
            return

        for entry in self.partial_results:
            destination = entry["destination"]
            votes = entry["votes"]

            meta = self.resolve_destination_meta(destination) if self.resolve_destination_meta else {}

            card = ResultCard(
                self.cards_grid,
                destination=destination,
                votes_text=self._format_vote_count(votes),
                image_path=meta.get("image"),
            )
            self.cards.append(card)

        self._layout_cards(self.MAX_COLUMNS)

    def _resolve_columns(self, width: int) -> int:
        if width < self.SINGLE_COLUMN_BREAKPOINT:
            return 1

        if width < self.TWO_COLUMN_BREAKPOINT:
            return 2

        return self.MAX_COLUMNS

    def _layout_cards(self, columns: int):
        if self._columns == columns:
            return

        self._columns = columns

        for child in self.cards_grid.winfo_children():
            child.grid_forget()

        for column in range(self.MAX_COLUMNS):
            self.cards_grid.grid_columnconfigure(column, weight=0)

        for column in range(columns):
            self.cards_grid.grid_columnconfigure(column, weight=1)

        for index, card in enumerate(self.cards):
            row = index // columns
            column = index % columns
            card.grid(row=row, column=column, padx=12, pady=10, sticky="n")

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=30, pady=24)
        footer.grid_columnconfigure(0, weight=1)

        vote_again_button = ctk.CTkButton(
            footer,
            text="Adicionar voto",
            command=self.on_vote_again,
            fg_color=ui_theme.PRIMARY_BUTTON,
            hover_color=ui_theme.PRIMARY_BUTTON_HOVER,
            text_color="#FFFFFF",
            font=ui_theme.FONT_BUTTON,
            corner_radius=ui_theme.BUTTON_RADIUS,
            height=50,
            width=220,
            border_width=0,
        )
        vote_again_button.grid(row=0, column=0, pady=(0, 22))

        finish_button = ctk.CTkButton(
            footer,
            text="Finalizar votação",
            command=self.on_finish,
            fg_color=ui_theme.FINISH_BUTTON,
            hover_color=ui_theme.FINISH_BUTTON_HOVER,
            text_color="#FFFFFF",
            font=ui_theme.FONT_BUTTON,
            corner_radius=ui_theme.BUTTON_RADIUS,
            height=50,
            width=220,
            border_width=0,
        )
        finish_button.grid(row=1, column=0, pady=(0, 34))

        thanks_text = ctk.CTkLabel(
            footer,
            text="Obrigado pelo seu voto!",
            font=ui_theme.FONT_BODY_BOLD,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        thanks_text.grid(row=2, column=0)

    def _on_resize(self, event):
        if event.widget is not self or not self.cards:
            return

        columns = self._resolve_columns(event.width)
        self._layout_cards(columns)
