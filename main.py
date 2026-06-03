from app.controllers.vote_controller import VotingController
from app.gui.application import Application
from app.repositories.vote_repository import VoteRepository
from app.services.question_flow_service import QuestionFlowService
from app.services.question_service import QuestionService
from app.services.session_service import SessionService
from app.services.vote_service import VoteService


# Monta as dependências principais da aplicação e devolve o controller pronto para uso.
def build_controller():
    repository = VoteRepository()
    session_service = SessionService(repository)
    vote_service = VoteService(repository, session_service)
    question_service = QuestionService()
    question_flow_service = QuestionFlowService()

    return VotingController(
        session_service,
        vote_service,
        question_service,
        question_flow_service,
    )


# Ponto de entrada da aplicação: monta o controller e inicia a interface CustomTkinter.
def main():
    controller = build_controller()
    app = Application(controller)
    app.run()


if __name__ == "__main__":
    main()
