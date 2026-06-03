import customtkinter as ctk

from app.config import ui_assets, ui_theme
from app.views.components.image_utils import load_ctk_image


# Espaço à esquerda do texto para não sobrepor o ícone (x do ícone + largura + folga).
ICON_TEXT_OFFSET = 46


# Tela de boas-vindas. Coleta o nome (usado como nome da sessão) e dispara
# a callback on_start.
class WelcomeView(ctk.CTkFrame):
    def __init__(self, master, on_start):
        super().__init__(master, fg_color=ui_theme.BACKGROUND_COLOR)

        self.on_start = on_start
        self._bg_label = None
        self._bg_image = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_background()
        self._build_header()
        self._build_card()

        self.bind("<Configure>", self._on_resize)

    def _build_background(self):
        self._bg_label = ctk.CTkLabel(self, text="")
        self._bg_label.place(relx=0, rely=0, relwidth=1, relheight=0.65)
        # self._bg_label.lower()

    def _on_resize(self, event):

        width = max(event.width, 1)
        height = max(event.height, 1)

        self._bg_image = load_ctk_image(ui_assets.WELCOME_BACKGROUND, (width, height))

        if self._bg_image is not None:
            self._bg_label.configure(image=self._bg_image)

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color=ui_theme.CARD_BACKGROUND,
            corner_radius=ui_theme.CARD_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
        )
        header.grid(row=0, column=0, pady=(40, 0))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Descubra sua\nviagem dos\nsonhos",
            font=ui_theme.FONT_TITLE_LARGE,
            text_color=ui_theme.TEXT_PRIMARY,
            justify="center",
        )
        title.grid(row=0, column=0, padx=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Responda algumas perguntas rápidas e veja\ndestinos perfeitos para você!",
            font=ui_theme.FONT_SUBTITLE,
            text_color=ui_theme.TEXT_SECONDARY,
            justify="center",
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(16, 16))

    def _build_card(self):
        card = ctk.CTkFrame(
            self,
            fg_color=ui_theme.CARD_BACKGROUND,
            corner_radius=ui_theme.CARD_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
        )
        card.grid(row=1, column=0, padx=20, pady=24)
        card.grid_columnconfigure(0, weight=1)

        card_title = ctk.CTkLabel(
            card,
            text="Nome da sessão",
            font=ui_theme.FONT_TITLE,
            text_color=ui_theme.TEXT_PRIMARY,
        )
        card_title.grid(row=0, column=0, padx=40, pady=(28, 16))

        input_wrap = ctk.CTkFrame(card, fg_color="transparent", width=360, height=44)
        input_wrap.grid(row=1, column=0, padx=40, pady=(0, 16))
        input_wrap.grid_propagate(False)

        self.name_entry = ctk.CTkEntry(
            input_wrap,
            placeholder_text="Digite o nome da sessão",
            font=ui_theme.FONT_BODY,
            height=44,
            width=360,
            corner_radius=ui_theme.BUTTON_RADIUS,
            border_width=1,
            border_color=ui_theme.CARD_BORDER,
            fg_color=ui_theme.CARD_BACKGROUND,
        )
        self.name_entry.place(x=0, y=0)
        self.name_entry.bind("<Return>", lambda _event: self._submit())
        self._apply_entry_text_padding()

        folder_icon = load_ctk_image(ui_assets.ICON_FOLDER, (22, 22))

        if folder_icon is not None:
            icon_label = ctk.CTkLabel(
                input_wrap,
                image=folder_icon,
                text="",
                fg_color=ui_theme.CARD_BACKGROUND,
            )
            icon_label.place(x=14, rely=0.5, anchor="w")
            icon_label.lift()

        input_wrap.bind("<Configure>", lambda _event: self._apply_entry_text_padding())

        start_icon = load_ctk_image(ui_assets.ICON_START, (28, 20))

        start_button = ctk.CTkButton(
            card,
            text="Começar  ",
            image=start_icon,
            compound="right",
            command=self._submit,
            fg_color=ui_theme.PRIMARY_BUTTON,
            hover_color=ui_theme.PRIMARY_BUTTON_HOVER,
            text_color="#FFFFFF",
            font=ui_theme.FONT_BUTTON_LARGE,
            corner_radius=ui_theme.BUTTON_RADIUS,
            height=46,
            width=360,
        )

        self.error_label = ctk.CTkLabel(
            card,
            text="",
            font=ui_theme.FONT_BUTTON_SMALL,
            text_color="#D64545",
        )
        self.error_label.grid(row=2, column=0, padx=40, pady=(0, 4))

        start_button.grid(row=3, column=0, padx=40, pady=(0, 12))

        footer = ctk.CTkLabel(
            card,
            text="Seus votos são anônimos e seguros.",
            font=ui_theme.FONT_BUTTON_SMALL,
            text_color=ui_theme.TEXT_MUTED,
        )
        footer.grid(row=4, column=0, padx=40, pady=(0, 28))

    def _apply_entry_text_padding(self):
        entry = self.name_entry

        if entry._corner_radius >= entry._minimum_x_padding:
            right_pad = min(
                entry._apply_widget_scaling(entry._corner_radius),
                round(entry._apply_widget_scaling(entry._current_height / 2)),
            )
        else:
            right_pad = entry._apply_widget_scaling(entry._minimum_x_padding)

        left_pad = entry._apply_widget_scaling(ICON_TEXT_OFFSET)

        entry._entry.grid_configure(padx=(left_pad, right_pad), sticky="nswe")

    def _submit(self):
        name = self.name_entry.get().strip()

        if not name:
            self.error_label.configure(text="Por favor, digite um nome para começar.")
            return

        self.error_label.configure(text="")
        self.on_start(name)
