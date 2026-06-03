import customtkinter as ctk

from app.config import ui_theme
from app.views.components.destination_card import DestinationCard
from app.views.components.nav_button import NavButton


# Tela de votação. Mostra os 3 destinos resultantes do fluxo de perguntas e
# dispara on_vote quando o usuário clica em "Votar" em um dos cards.
# Em janelas estreitas, os cards passam a ser empilhados verticalmente.
class DestinationsView(ctk.CTkFrame):
    STACK_BREAKPOINT = 900

    def __init__(self, master, destinations: list[dict], on_vote, on_back):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.destinations = destinations
        self.on_vote = on_vote
        self.on_back = on_back

        self.cards: list[DestinationCard] = []
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

        title = ctk.CTkLabel(
            header,
            text="Com base nas suas respostas,\nseus destinos ideais são:",
            font=ui_theme.FONT_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
            justify="center",
        )
        title.grid(row=0, column=0, padx=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Escolha uma opção para votar!",
            font=ui_theme.FONT_SUBTITLE,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        subtitle.grid(row=1, column=0, pady=(12, 0))

    def _build_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="n", padx=30, pady=(24, 0))

        for destination in self.destinations:
            card = DestinationCard(
                self.cards_frame,
                destination=destination["name"],
                image_path=destination.get("image"),
                subtitle=destination.get("description", ""),
                command=self.on_vote,
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

        back_button = NavButton(
            footer,
            text="Voltar",
            command=self.on_back,
            icon="back",
        )
        back_button.grid(row=0, column=0, sticky="w")

    def _on_resize(self, event):
        if event.widget is not self:
            return

        stacked = event.width < self.STACK_BREAKPOINT
        self._layout_cards(stacked=stacked)
