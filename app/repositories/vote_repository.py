import csv
import os
import re

from app.config.config import SESSION_FOLDER_PATH
class VoteRepository:
    # Define onde os arquivos das sessões ficam salvos e garante que a pasta exista.
    def __init__(self, folder_path=SESSION_FOLDER_PATH):
        self.folder_path = folder_path
        self.ensure_folder_exists()

    # Cria a pasta de sessões caso ela ainda não exista.
    def ensure_folder_exists(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    # Transforma o nome da sessão em um nome seguro para arquivo CSV.
    def format_session_filename(self, session_name):
        formatted_name = session_name.strip().lower()

        formatted_name = re.sub(r"\s+", "_", formatted_name)
        formatted_name = re.sub(r"[^a-z0-9_]", "", formatted_name)

        if not formatted_name:
            raise ValueError("Nome da sessão não é válido para gerar o repositório.")

        return formatted_name

    # Monta o caminho completo do CSV da sessão a partir do nome formatado.
    def get_session_file_path(self, session_name):
        formatted_name = self.format_session_filename(session_name)

        return f"{self.folder_path}/{formatted_name}.csv"

    # Cria o CSV da sessão com todos os destinos iniciando com zero votos.
    def create_session_results_file(self, session_name: str, destinations: list[str]):
        self.ensure_folder_exists()

        file_path = self.get_session_file_path(session_name)

        if os.path.exists(file_path):
            raise ValueError("Já existe uma sessão com esse nome.")

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["destination", "votes"])

            for destination in destinations:
                writer.writerow([destination, 0])

    # Lê o CSV da sessão e devolve os resultados no formato {destino: votos}.
    def read_session_results(self, session_name: str) -> dict[str, int]:
        file_path = self.get_session_file_path(session_name)

        results = {}

        if not os.path.exists(file_path):
            return results

        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if "destination" not in row or "votes" not in row:
                    raise ValueError("Arquivo de sessão inválido.")
                destination = row["destination"]

                try:
                    votes = int(row["votes"])
                except ValueError:
                    raise ValueError("Arquivo de sessão contém votos inválidos")
                results[destination] = votes

        return results

    # Salva no CSV o estado atualizado dos votos da sessão.
    def save_session_results(self, session_name: str, results: dict[str, int]):
        file_path = self.get_session_file_path(session_name)

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["destination", "votes"])

            for destination, votes in results.items():
                writer.writerow([destination, votes])

    # Soma um voto ao destino informado e grava o resultado atualizado.
    def increment_destination_vote(self, session_name: str, destination: str):
        results = self.read_session_results(session_name)

        if destination not in results:
            results[destination] = 0

        results[destination] += 1

        self.save_session_results(session_name, results)
