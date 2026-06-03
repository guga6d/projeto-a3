from tkinter import messagebox

import customtkinter as ctk

from app.config import ui_theme
from app.controllers.vote_controller import VotingController
from app.views.welcome_view import WelcomeView
from app.views.question_view import QuestionView
from app.views.destinations_view import DestinationsView
from app.views.partial_results_view import PartialResultsView
from app.views.winner_view import WinnerView


# Janela principal da aplicação. Gerencia a navegação entre as views, mantém
# o tema do CustomTkinter e centraliza o tratamento de erros lançados pelas
# camadas inferiores. Toda chamada ao VotingController acontece a partir daqui.
class Application(ctk.CTk):
    def __init__(self, controller: VotingController):
        super().__init__()

        self.controller = controller

        self._configure_window()
        self._build_container()

        self._views: dict[str, ctk.CTkFrame] = {}
        self._current_view: ctk.CTkFrame | None = None

        self._winner_payload = None
        self._secondary_question = None

        self.show_welcome()

    def _configure_window(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Descubra sua viagem dos sonhos")

        default_width, default_height = ui_theme.WINDOW_DEFAULT_SIZE
        min_width, min_height = ui_theme.WINDOW_MIN_SIZE

        self.geometry(f"{default_width}x{default_height}")
        self.minsize(min_width, min_height)

        self.configure(fg_color=ui_theme.BACKGROUND_COLOR)

    def _build_container(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color=ui_theme.BACKGROUND_COLOR)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _swap_view(self, new_view: ctk.CTkFrame):
        if self._current_view is not None:
            self._current_view.grid_forget()
            self._current_view.destroy()

        self._current_view = new_view
        self._current_view.grid(row=0, column=0, sticky="nsew")

    # Helpers para reportar erros de validação ou de regra de negócio.
    def _show_error(self, message: str):
        messagebox.showerror("Atenção", message)

    def _safe_call(self, action, error_message: str | None = None):
        try:
            value = action()
        except (ValueError, RuntimeError) as error:
            self._show_error(error_message or str(error))

            return False, None

        return True, value

    # Navegação entre telas.
    def show_welcome(self):
        view = WelcomeView(self.container, on_start=self.handle_start_session)
        self._swap_view(view)

    def show_primary_question(self):
        questions = self.controller.get_primary_questions()

        if not questions:
            self._show_error("Nenhuma pergunta cadastrada.")
            return

        primary_question = questions[0]

        view = QuestionView(
            self.container,
            question=primary_question,
            step=1,
            total_steps=2,
            on_select=self.handle_primary_answer,
            on_back=self.show_welcome,
        )
        self._swap_view(view)

    def show_secondary_question(self):
        if self._secondary_question is None:
            self._show_error("Responda a primeira pergunta antes de continuar.")
            return

        view = QuestionView(
            self.container,
            question=self._secondary_question,
            step=2,
            total_steps=2,
            on_select=self.handle_secondary_answer,
            on_back=self.show_primary_question,
        )
        self._swap_view(view)

    def show_destinations(self):
        destinations = self.controller.get_available_destinations_meta()

        if not destinations:
            self._show_error("Nenhum destino disponível. Reinicie o questionário.")
            self.show_primary_question()
            return

        view = DestinationsView(
            self.container,
            destinations=destinations,
            on_vote=self.handle_vote,
            on_back=self.show_secondary_question,
        )
        self._swap_view(view)

    def show_partial_results(self):
        top_results = self.controller.get_top_results()

        view = PartialResultsView(
            self.container,
            top_results=top_results,
            on_vote_again=self.show_primary_question,
            on_finish=self.handle_finish_session,
            resolve_destination_meta=self.controller.get_destination_meta,
        )
        self._swap_view(view)

    def show_winner(self):
        view = WinnerView(
            self.container,
            winner=self._winner_payload,
            on_restart=self.handle_restart,
            resolve_destination_meta=self.controller.get_destination_meta,
        )
        self._swap_view(view)

    # Handlers chamados pelas views.
    def handle_start_session(self, session_name: str):
        success, _ = self._safe_call(
            lambda: self.controller.start_new_session(session_name),
        )

        if not success:
            return

        self.show_primary_question()

    def handle_primary_answer(self, answer: str):
        success, secondary = self._safe_call(
            lambda: self.controller.answer_primary_question(answer),
        )

        if not success:
            return

        self._secondary_question = secondary
        self.show_secondary_question()

    def handle_secondary_answer(self, answer: str):
        success, _ = self._safe_call(
            lambda: self.controller.answer_secondary_question(answer),
        )

        if not success:
            return

        self.show_destinations()

    def handle_vote(self, destination: str):
        available = self.controller.get_available_destinations()

        if destination not in available:
            self._show_error("Destino inválido para esta etapa.")
            return

        success, _ = self._safe_call(
            lambda: self.controller.register_vote(destination),
        )

        if not success:
            return

        self.show_partial_results()

    def handle_finish_session(self):
        top_results = self.controller.get_top_results()

        if top_results:
            self._winner_payload = top_results[0]
        else:
            self._winner_payload = None

        self._safe_call(self.controller.finish_session)

        self.show_winner()

    def handle_restart(self):
        self._winner_payload = None
        self._secondary_question = None
        self.show_welcome()

    def run(self):
        self.mainloop()
