import unittest
from padroes.template_partida import IniciarPartidaPadrao


class TestIniciarPartidaPadrao(unittest.TestCase):
    def test_iniciar_partida_e_distribui(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        tpl = IniciarPartidaPadrao()
        res = tpl.executar(partida, [10, 20], solicitante_id=10)

        self.assertTrue(res["sucesso"])
        self.assertEqual(partida["status"], "iniciada")
        distribuicao = res["cartas"]["distribuicao"]
        self.assertEqual(len(distribuicao[10]), 2)
        self.assertEqual(len(distribuicao[20]), 2)

        todas_cartas = [
            (c["valor"], c["naipe"])
            for cartas in distribuicao.values()
            for c in cartas
        ]
        self.assertEqual(len(todas_cartas), len(set(todas_cartas)))

    def test_bloqueia_nao_criador(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        tpl = IniciarPartidaPadrao()
        with self.assertRaises(PermissionError):
            tpl.executar(partida, [10, 20], solicitante_id=20)

    def test_bloqueia_menos_de_dois_jogadores(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        tpl = IniciarPartidaPadrao()
        with self.assertRaises(RuntimeError):
            tpl.executar(partida, [10], solicitante_id=10)

    def test_bloqueia_partida_nao_aberta(self):
        partida = {"id": 1, "id_criador": 10, "status": "iniciada"}
        tpl = IniciarPartidaPadrao()
        with self.assertRaises(RuntimeError):
            tpl.executar(partida, [10, 20], solicitante_id=10)


if __name__ == "__main__":
    unittest.main()