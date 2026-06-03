import customtkinter as ctk

from app.config import ui_theme
from app.views.components.nav_button import NavButton
from app.views.components.option_card import OptionCard
from app.views.components.progress_indicator import ProgressIndicator


# Tela de pergunta reutilizável usada para a pergunta primária e secundária.
# Recebe o dicionário de pergunta (id/question/options) já pronto pelo controller
# e dispara on_select quando o usuário escolhe uma opção (ou clica em Próximo).
class QuestionView(ctk.CTkFrame):
    def __init__(self, master, question: dict, step: int, total_steps: int,
                 on_select, on_back):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.question = question
        self.step = step
        self.total_steps = total_steps
        self.on_select = on_select
        self.on_back = on_back

        self.selected_option: str | None = None
        self.option_cards: list[OptionCard] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self._build_progress()
        self._build_title()
        self._build_options()
        self._build_footer()

    def _build_progress(self):
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=0, column=0, pady=(40, 24))

        progress = ProgressIndicator(
            progress_frame,
            total_steps=self.total_steps,
            current_step=self.step,
        )
        progress.pack()

    def _build_title(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=1, column=0, sticky="ew", padx=20)
        title_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            title_frame,
            text=self.question.get("question", ""),
            font=ui_theme.FONT_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
            wraplength=720,
            justify="center",
        )
        title.grid(row=0, column=0, padx=20)

        subtitle = ctk.CTkLabel(
            title_frame,
            text="Escolha uma opção",
            font=ui_theme.FONT_SUBTITLE,
            text_color=ui_theme.TEXT_SECONDARY,
        )
        subtitle.grid(row=1, column=0, pady=(10, 0))

    def _build_options(self):
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=3, column=0, sticky="n", padx=20)
        options_frame.grid_columnconfigure(0, weight=1)

        options = self.question.get("options", [])

        for index, option in enumerate(options):
            card = OptionCard(
                options_frame,
                option_text=option["label"],
                icon_path=option.get("icon"),
                description=option.get("description", ""),
                command=self._on_option_clicked,
            )
            card.configure(width=520)
            card.grid(row=index, column=0, sticky="ew", pady=8)
            self.option_cards.append(card)

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=5, column=0, sticky="ew", padx=30, pady=24)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)
        footer.grid_columnconfigure(2, weight=1)

        self.back_button = NavButton(
            footer,
            text="Voltar",
            command=self.on_back,
            icon="back",
        )
        self.back_button.grid(row=0, column=0, sticky="w")

        self.step_label = ctk.CTkLabel(
            footer,
            text=f"{self.step} de {self.total_steps}",
            font=ui_theme.FONT_BUTTON_SMALL,
            text_color=ui_theme.TEXT_MUTED,
        )
        self.step_label.grid(row=0, column=1, padx=10)

        self.next_button = NavButton(
            footer,
            text="Próximo",
            command=self._confirm_selection,
            icon="forward",
        )
        self.next_button.grid(row=0, column=2, sticky="e")
        self.next_button.configure(state="disabled")

    def _on_option_clicked(self, option_text: str):
        self.selected_option = option_text

        for card in self.option_cards:
            card.set_selected(card.option_text == option_text)

        self.next_button.configure(state="normal")

    def _confirm_selection(self):
        if self.selected_option is None:
            return

        self.on_select(self.selected_option)
