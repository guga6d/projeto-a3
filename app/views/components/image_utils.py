import os

import customtkinter as ctk
from PIL import Image


# Retorna o path apenas se o arquivo existir em disco, senão None.
# Permite que os componentes mostrem o fallback visual sem quebrar.
def resolve_image(path: str | None) -> str | None:
    if path and os.path.exists(path):
        return path

    return None


# Carrega um arquivo de imagem (PNG, JPG, etc.) e devolve um CTkImage pronto para uso.
def load_ctk_image(path: str | None, size: tuple[int, int]):
    if not path or not os.path.exists(path):
        return None

    try:
        pil_image = Image.open(path)
    except OSError:
        return None

    return ctk.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=size,
    )
