class QuestionFlowService:
    # Mantém em memória as respostas do participante durante o fluxo atual.
    def __init__(self):
        self.primary_answer = None
        self.secondary_answer = None
        self.available_destinations = []

    # Salva a primeira resposta escolhida pelo participante.
    def save_primary_answer(self, answer):
        self.primary_answer = answer

    # Devolve a primeira resposta, exigindo que ela já tenha sido registrada.
    def get_primary_answer(self):
        if self.primary_answer is None:
            raise RuntimeError("Nenhuma resposta primária foi registrada.")

        return self.primary_answer

    # Salva a segunda resposta escolhida pelo participante.
    def save_secondary_answer(self, answer):
        self.secondary_answer = answer

    # Devolve a segunda resposta, exigindo que ela já tenha sido registrada.
    def get_secondary_answer(self):
        if self.secondary_answer is None:
            raise RuntimeError("Nenhuma resposta secundária foi registrada.")

        return self.secondary_answer

    # Guarda os destinos que ficaram disponíveis depois das respostas.
    def save_available_destinations(self, destinations):
        self.available_destinations = destinations

    # Devolve os destinos disponíveis para o voto atual.
    def get_available_destinations(self):
        return self.available_destinations

    # Limpa as respostas e destinos para começar o fluxo de outro participante.
    def reset_flow(self):
        self.primary_answer = None
        self.secondary_answer = None
        self.available_destinations = []
