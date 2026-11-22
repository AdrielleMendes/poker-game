import unittest
from padroes.facade import PokerFacade


class TestPokerFacade(unittest.TestCase):
    def test_iniciar_partida_pela_fachada_e_distribui_cartas(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        chamou_callback = []

        facade = PokerFacade()
        resultado = facade.iniciar_partida(
            partida=partida,
            jogadores_ids=[10, 20],
            solicitante_id=10,
            on_iniciar=lambda id_partida: chamou_callback.append(id_partida),
        )

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["idPartida"], 1)
        self.assertEqual(partida["status"], "iniciada")
        self.assertEqual(chamou_callback, [1])
        self.assertEqual(len(resultado["cartas"]["distribuicao"][10]), 2)
        self.assertEqual(len(resultado["cartas"]["distribuicao"][20]), 2)

    def test_fachada_bloqueia_solicitante_nao_criador(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        facade = PokerFacade()

        with self.assertRaises(PermissionError):
            facade.iniciar_partida(
                partida=partida,
                jogadores_ids=[10, 20],
                solicitante_id=20,
            )


if __name__ == "__main__":
    unittest.main()