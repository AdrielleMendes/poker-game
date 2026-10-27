import random

NAIPES = ['Copas', 'Ouros', 'Espadas', 'Paus']
VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def criar_baralho():
    baralho = []
    for naipe in NAIPES:
        for valor in VALORES:
            baralho.append({'valor': valor, 'naipe': naipe})
    return baralho

def embaralhar_e_distribuir(jogadores, cartas_por_jogador=2):
    baralho = criar_baralho()
    random.shuffle(baralho)

    distribuicao = {}
    for jogador in jogadores:
        cartas_do_jogador = []
        for _ in range(cartas_por_jogador):
            if baralho:
                cartas_do_jogador.append(baralho.pop())
        distribuicao[jogador] = cartas_do_jogador

    return {
        "status": "sucesso",
        "mensagem": "Cartas distribuídas com sucesso!",
        "distribuicao": distribuicao,
        "cartas_restantes_no_baralho": len(baralho)
    }