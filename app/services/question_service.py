from app.data.votes_data import (
    DESTINATIONS_BY_ANSWERS,
    PRIMARY_QUESTIONS,
    SECONDARY_QUESTION,
)
from app.views.components.image_utils import resolve_image


class QuestionService:
    # Carrega em memória as perguntas e os destinos definidos no arquivo de dados.
    # Também monta uma única vez o lookup por nome (usado nas telas de resultado).
    def __init__(self):
        self.primary_questions = PRIMARY_QUESTIONS
        self.secondary_question = SECONDARY_QUESTION
        self.destinations_by_answers = DESTINATIONS_BY_ANSWERS
        self._destination_by_name = self._build_destination_name_lookup()

    # Percorre DESTINATIONS_BY_ANSWERS e monta {nome → meta} para busca
    # nas telas que só recebem o nome do destino (resultado parcial, vencedor).
    def _build_destination_name_lookup(self):
        lookup = {}

        for primary_group in self.destinations_by_answers.values():
            for destinations in primary_group.values():
                for destination in destinations:
                    lookup[destination["name"]] = destination

        return lookup

    # Devolve a lista de perguntas iniciais do fluxo.
    def get_primary_questions(self):
        return self.primary_questions

    # Devolve a pergunta secundária fixa (mesma para todos os participantes).
    def get_secondary_question(self):
        return self.secondary_question

    # Valida a combinação (primária, secundária) e devolve os destinos correspondentes
    # já com o meta pronto para a UI (apenas o image é validado em disco).
    def get_destinations_meta(self, primary_answer, secondary_answer):
        if primary_answer not in self.destinations_by_answers:
            raise ValueError("Resposta primária inválida.")

        secondary_map = self.destinations_by_answers[primary_answer]

        if secondary_answer not in secondary_map:
            raise ValueError("Resposta secundária inválida.")

        return [self._with_resolved_image(item) for item in secondary_map[secondary_answer]]

    # Lista somente os nomes dos destinos disponíveis para validar o voto.
    def get_destinations(self, primary_answer, secondary_answer):
        return [item["name"] for item in self.get_destinations_meta(primary_answer, secondary_answer)]

    # Devolve nome + imagem (resolvida) + descrição de um destino. Se o destino
    # não existir no índice, retorna defaults vazios para não quebrar a UI.
    def get_destination_meta(self, name):
        entry = self._destination_by_name.get(name)

        if entry is None:
            return {"name": name, "image": None, "description": ""}

        return self._with_resolved_image(entry)

    # Busca a opção dentro de uma pergunta pelo label exibido.
    def get_option_by_label(self, question: dict, label: str):
        for option in question.get("options", []):
            if option.get("label") == label:
                return option

        return None

    # Junta todos os destinos cadastrados, sem repetições.
    def get_all_destinations(self):
        return sorted(self._destination_by_name.keys())

    # Aplica resolve_image apenas no campo image (mantém o fallback de arquivo ausente).
    def _with_resolved_image(self, entry):
        return {
            "name": entry["name"],
            "image": resolve_image(entry.get("image")),
            "description": entry.get("description", ""),
        }
