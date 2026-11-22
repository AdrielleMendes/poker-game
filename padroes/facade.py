from padroes.template_partida import IniciarPartidaPadrao


class PokerFacade:
    def __init__(self, iniciar_partida_template: IniciarPartidaPadrao | None = None):
        self.iniciar_partida_template = iniciar_partida_template or IniciarPartidaPadrao()

    def iniciar_partida(
        self,
        partida: dict,
        jogadores_ids: list[int],
        solicitante_id: int,
        on_iniciar=None,
    ) -> dict:
        if on_iniciar is not None:
            self.iniciar_partida_template.on_iniciar = on_iniciar

        return self.iniciar_partida_template.executar(
            partida=partida,
            jogadores_ids=jogadores_ids,
            solicitante_id=solicitante_id,
        )