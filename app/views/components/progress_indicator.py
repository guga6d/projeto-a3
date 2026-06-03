import customtkinter as ctk

from app.config import ui_theme


# Indicador de progresso usado nas telas de pergunta. Mostra dois nós ligados
# por uma linha, com o nó atual destacado, como nos wireframes "1 de 2" e "2 de 2".
class ProgressIndicator(ctk.CTkFrame):
    def __init__(self, master, total_steps: int = 2, current_step: int = 1):
        super().__init__(master, fg_color="transparent")

        self.total_steps = total_steps
        self.current_step = current_step

        self._build_indicator()

    def _build_indicator(self):
        for widget in self.winfo_children():
            widget.destroy()

        for step in range(1, self.total_steps + 1):
            is_reached = step <= self.current_step

            if is_reached:
                dot = ctk.CTkFrame(
                    self,
                    width=18,
                    height=18,
                    corner_radius=9,
                    fg_color=ui_theme.PROGRESS_INACTIVE,
                    border_width=0,
                )
            else:
                dot = ctk.CTkFrame(
                    self,
                    width=18,
                    height=18,
                    corner_radius=9,
                    fg_color="transparent",
                    border_width=2,
                    border_color=ui_theme.PROGRESS_INACTIVE,
                )

            dot.pack(side="left")
            dot.pack_propagate(False)

            if step < self.total_steps:
                line_reached = step < self.current_step

                if line_reached:
                    line = ctk.CTkFrame(
                        self,
                        width=120,
                        height=3,
                        fg_color=ui_theme.PROGRESS_INACTIVE,
                        border_width=0,
                    )
                else:
                    line = ctk.CTkFrame(
                        self,
                        width=120,
                        height=3,
                        fg_color="transparent",
                        border_width=1,
                        border_color=ui_theme.PROGRESS_INACTIVE,
                    )

                line.pack(side="left", padx=4)

    def set_step(self, current_step: int):
        self.current_step = current_step
        self._build_indicator()
