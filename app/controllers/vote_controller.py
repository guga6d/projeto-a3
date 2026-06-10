from app.services.session_service import SessionService
from app.services.vote_service import VoteService
from app.services.question_service import QuestionService
from app.services.question_flow_service import QuestionFlowService
class VotingController:
    # Recebe os services usados pela aplicação e centraliza a comunicação entre tela e regras de negócio.
    def __init__(self, session_service: SessionService,
                 vote_service: VoteService,
                 question_service: QuestionService,
                 question_flow_service: QuestionFlowService):
        self.session_service = session_service
        self.vote_service = vote_service
        self.question_service = question_service
        self.question_flow_service = question_flow_service

    # Cria uma nova sessão já com todos os destinos possíveis preparados para receber votos.
    def start_new_session(self, session_name):
        all_destinations = self.question_service.get_all_destinations()

        return self.session_service.create_session(
            session_name,
            all_destinations
        )

    # Encerra a sessão de votação que estiver ativa no momento.
    def finish_session(self):
        return self.session_service.close_session()

    # Informa se existe uma sessão criada e ainda aberta para votação.
    def has_active_session(self):
        return self.session_service.is_session_active()

    # Registra o voto em um destino e limpa o fluxo de perguntas para o próximo participante.
    def register_vote(self, destination):
        self.vote_service.register_vote(destination)
        self.question_flow_service.reset_flow()

    # Busca os resultados da sessão ativa no formato {destino: quantidade_de_votos}.
    def get_current_results(self):
        return self.vote_service.get_current_results()

    def get_partial_results(self):
        return self.vote_service.get_partial_results()

    def get_winning_results(self):
        return self.vote_service.get_winning_results()

    # Devolve as perguntas iniciais que começam o fluxo de escolha do destino.
    def get_primary_questions(self):
        return self.question_service.get_primary_questions()

    # Guarda a primeira resposta e devolve a pergunta secundária fixa (mesma para todos).
    def answer_primary_question(self, primary_answer):
        self.question_flow_service.save_primary_answer(primary_answer)

        return self.question_service.get_secondary_question()

    # Guarda a segunda resposta e devolve os destinos (com metadados) para votação,
    # combinando primária + secundária para escolher o grupo correto.
    def answer_secondary_question(self, secondary_answer):
        self.question_flow_service.save_secondary_answer(secondary_answer)

        primary_answer = self.question_flow_service.get_primary_answer()
        destinations = self.question_service.get_destinations(primary_answer, secondary_answer)

        self.question_flow_service.save_available_destinations(destinations)

        return self.question_service.get_destinations_meta(primary_answer, secondary_answer)

    # Devolve apenas os nomes dos destinos disponíveis (usado para validar o voto).
    def get_available_destinations(self):
        return self.question_flow_service.get_available_destinations()

    # Devolve os destinos disponíveis com imagem e descrição prontos para a UI.
    def get_available_destinations_meta(self):
        names = self.question_flow_service.get_available_destinations()

        return [self.question_service.get_destination_meta(name) for name in names]

    # Devolve metadados de um destino específico (usado em telas de resultado).
    def get_destination_meta(self, name):
        return self.question_service.get_destination_meta(name)
