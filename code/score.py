from . import db_proxy
from datetime import datetime

class ScoreManager:
    """Gerencia a lógica de pontuação e o ranking de high scores."""

    def __init__(self):
        self._current_kill_count = 0
        self.high_scores = self._load_and_sort_high_scores()

    def reset(self):
        """Zera o contador de abates para uma nova partida."""
        self._current_kill_count = 0

    def add_kill(self, count=1):
        """Adiciona uma ou mais mortes ao contador da partida atual."""
        self._current_kill_count += count

    def get_current_score(self):
        """Retorna o score da partida atual."""
        return self._current_kill_count

    def _load_and_sort_high_scores(self):
        """Carrega e ordena os high scores usando o db_proxy."""
        scores = db_proxy.load_data()
        scores.sort(key=lambda item: item['score'], reverse=True)
        return scores

    def save_current_score_if_high(self):
        """Salva o score atual se ele for um dos 10 melhores."""
        new_score_entry = {
            "score": self._current_kill_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.high_scores.append(new_score_entry)
        self.high_scores.sort(key=lambda item: item['score'], reverse=True)
        self.high_scores = self.high_scores[:10]
        db_proxy.save_data(self.high_scores)

    def get_high_scores(self):
        """Retorna a lista de high scores."""
        return self.high_scores