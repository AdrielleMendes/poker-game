from abc import ABC, abstractmethod
from baralho import embaralhar_e_distribuir


class IniciarPartidaTemplate(ABC):
    def executar(self, partida: dict, jogadores_ids: list[int], solicitante_id: int) -> dict:
        self.validar(partida, jogadores_ids, solicitante_id)
        self.atualizar_status(partida)
        cartas = self.distribuir(jogadores_ids)
        return {"sucesso": True, "idPartida": partida["id"], "cartas": cartas}

    @abstractmethod
    def validar(self, partida: dict, jogadores_ids: list[int], solicitante_id: int):
        pass

    @abstractmethod
    def atualizar_status(self, partida: dict):
        pass

    def distribuir(self, jogadores_ids: list[int]) -> dict:
        return embaralhar_e_distribuir(jogadores_ids, cartas_por_jogador=2)


class IniciarPartidaPadrao(IniciarPartidaTemplate):
    def __init__(self, on_iniciar=None):
        self.on_iniciar = on_iniciar

    def validar(self, partida: dict, jogadores_ids: list[int], solicitante_id: int):
        if not partida:
            raise LookupError("Partida não encontrada.")
        if partida["id_criador"] != solicitante_id:
            raise PermissionError("Apenas o criador pode iniciar.")
        if partida["status"] != "aberta":
            raise RuntimeError("Partida já iniciada ou fechada.")
        if len(jogadores_ids) < 2:
            raise RuntimeError("Mínimo de 2 jogadores.")

    def atualizar_status(self, partida: dict):
        partida["status"] = "iniciada"
        if self.on_iniciar:
            self.on_iniciar(partida["id"])