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

    def _build_ranked_results(self, results: dict[str, int]):
        total_votes = sum(results.values())

        if total_votes == 0:
            return []

        sorted_votes = sorted(
            results.items(),
            key=lambda item: (-item[1], item[0]),
        )

        ranked_results = []

        for position, (destination, votes) in enumerate(sorted_votes, start=1):
            percentage = round((votes / total_votes) * 100, 1)

            ranked_results.append({
                "position": position,
                "destination": destination,
                "votes": votes,
                "percentage": percentage,
            })

        return ranked_results

    # Devolve o ranking completo dos destinos que já receberam ao menos um voto.
    def get_partial_results(self):
        session = self.session_service.get_active_session()

        results = self.vote_repository.read_session_results(session.name)
        ranked_results = self._build_ranked_results(results)

        return [
            result
            for result in ranked_results
            if result["votes"] > 0
        ]

    def get_winning_results(self):
        session = self.session_service.get_active_session()

        results = self.vote_repository.read_session_results(session.name)
        ranked_results = self._build_ranked_results(results)

        if not ranked_results:
            return []

        highest_vote_total = ranked_results[0]["votes"]

        return [
            result
            for result in ranked_results
            if result["votes"] == highest_vote_total
        ]
