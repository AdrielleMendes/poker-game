import unittest
from padroes.template_partida import IniciarPartidaPadrao


class TestIniciarPartidaPadrao(unittest.TestCase):
    def test_iniciar_partida_e_distribui(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        tpl = IniciarPartidaPadrao()
        res = tpl.executar(partida, [10, 20], solicitante_id=10)
        self.assertTrue(res["sucesso"])
        self.assertEqual(partida["status"], "iniciada")
        self.assertEqual(len(res["cartas"]["distribuicao"][10]), 2)

    def test_bloqueia_nao_criador(self):
        partida = {"id": 1, "id_criador": 10, "status": "aberta"}
        tpl = IniciarPartidaPadrao()
        with self.assertRaises(PermissionError):
            tpl.executar(partida, [10, 20], solicitante_id=20)


if __name__ == "__main__":
    unittest.main()