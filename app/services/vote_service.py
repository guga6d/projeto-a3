from app.repositories.vote_repository import VoteRepository
from app.services.session_service import SessionService


class VoteService:
    # Recebe as dependências necessárias para validar a sessão e persistir votos.
    def __init__(self, vote_repository: VoteRepository, session_service: SessionService):
        self.vote_repository = vote_repository
        self.session_service = session_service

    # Registra um voto em um destino válido dentro da sessão ativa.
    def register_vote(self, destination: str):
        session = self.session_service.get_active_session()

        if not session.is_active:
            raise RuntimeError("A sessão já foi encerrada!")

        results = self.vote_repository.read_session_results(session.name)

        if destination not in results:
            raise ValueError("Destino inválido para esta sessão.")

        self.vote_repository.increment_destination_vote(session.name, destination)

    # Lê os resultados atuais da sessão ativa.
    def get_current_results(self):
        session = self.session_service.get_active_session()

        return self.vote_repository.read_session_results(session.name)

    #Aqui pegamos a sessao e organizamos em uma lista do maior pro menor, pegando somente os 3 maiores, caso n tenha votos ainda, devolve uma lista vazia, depois no enumerate adicionamos as pos de cada um(visto que o sorted ja deixou na ordem)
    def get_top_results(self):
        session = self.session_service.get_active_session()

        results = self.vote_repository.read_session_results(session.name)

        total_votes = sum(results.values())

        if total_votes == 0:
            return []

        sorted_votes = sorted(
            results.items(),
            key=lambda item : item[1],
            reverse=True
            )

        top_three = sorted_votes[:3]

        top_results = []

        #enumerate serve para adicionar o n da pos de cada destination
        for position, item in enumerate(top_three, start=1):
            destination = item[0]
            votes = item[1]

            #round pega os numeros e "formata", alem de arredondar
            percentage = round((votes / total_votes) * 100, 1)

            top_results.append({
                "position": position,
                "destination": destination,
                "votes": votes,
                "percentage": percentage
            })

        return top_results
