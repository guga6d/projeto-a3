

from app.repositories.vote_repository import VoteRepository
from app.models.session import Session


class SessionService:
    # Guarda o repositório usado para criar os arquivos e mantém a sessão atual em memória.
    def __init__(self, vote_repository: VoteRepository):
        self.repository = vote_repository
        self.current_session = None

    # Cria uma nova sessão de votação somente depois que o arquivo da sessão é criado com sucesso.
    def create_session(self, session_name: str, destinations: list[str]):
        if not session_name or not session_name.strip():
            raise ValueError("Nome da sessão inválido!")

        self.repository.create_session_results_file(session_name, destinations)
        self.current_session = Session(session_name)

        return self.current_session

    # Busca a sessão atual; se nenhuma sessão foi iniciada, avisa com erro.
    def get_active_session(self):
        if self.current_session is None:
            raise RuntimeError("Nenhuma sessão foi iniciada")

        return self.current_session

    # Confirma se existe uma sessão carregada e se ela ainda está aberta.
    def is_session_active(self):
        return (self.current_session is not None
                and self.current_session.is_active)

    # Fecha a sessão atual, marcando ela como inativa.
    def close_session(self):
        session = self.get_active_session()
        session.is_active = False

        return session
