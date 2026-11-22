"""Logica do jogo: o que acontece em cada quadro (canos, tiros, dano, chefao, fim)."""
import random
from config import *
from recursos import toca
from efeitos import *
from nave import *
from obstaculos import *
from chefe import *


# ======================================================================
# LOGICA DO JOGO (o que acontece em cada quadro)
# ======================================================================
def novo_jogo(personagem):
    """Devolve o estado de uma partida nova (um dicionario)."""
    jogo = {
        "personagem": personagem,
        "nave": Nave(personagem),
        "chefe": Chefe(),
        "fase": "canos",  # "canos" ou "chefe"
        "canos": [],
        "lasers": [],  # tiros da nave
        "lasers_inimigos": [],  # tiros do chefao
        "pontos": 0,
        "canos_passados": 0,
        "proximo_cano": 0,  # numero do proximo cano a ser criado
        "proximo_trancado": False,  # o proximo cano vai ser trancado?
        "banner": 120,  # quadros mostrando o nome do cenario na tela
        # ---------- animacoes ----------
        "tempo": 0,  # conta quadros desde o inicio da partida
        "particulas": [],  # fogo, faiscas e explosoes
        "enfeites": [],  # poeira, nuvens, chuva... do cenario atual
        "efeito": "",  # nome do efeito de fundo que esta valendo
        "chao_x": 0,  # quanto o chao ja andou (para as listras do chao se mexerem)
        "tremor": 0,  # quadros de tremida da tela
        "resultado": "",  # "" = partida rolando, "fim" ou "vitoria" = acabando
        "espera_fim": 0,  # quadros de explosao antes de mostrar a tela final
    }
    if TESTAR_CHEFE:
        jogo["fase"] = "chefe"
        jogo["canos_passados"] = TOTAL_CANOS
    return jogo


def indice_cenario(jogo):
    """Descobre em qual cenario o jogo esta, pelo numero de canos passados."""
    indice = jogo["canos_passados"] // CANOS_POR_CENARIO
    if indice >= len(CENARIOS):
        indice = len(CENARIOS) - 1
    return indice


def cenario_atual(jogo):
    """Devolve o dicionario do cenario que esta na tela agora."""
    if jogo["fase"] == "chefe":
        return CENARIO_CHEFE
    return CENARIOS[indice_cenario(jogo)]


def cria_cano(jogo):
    """Cria o proximo cano na direita da tela e ja decide se o seguinte sera trancado."""
    indice = jogo["proximo_cano"]
    trancado = jogo["proximo_trancado"]
    x = LARGURA
    if indice == 0:
        x = LARGURA + 150  # o primeiro vem mais longe, para dar tempo de comecar
    jogo["canos"].append(Cano(x, indice, trancado))
    jogo["proximo_cano"] += 1
    # os 2 primeiros sao livres e nunca vem dois trancados seguidos
    proximo = False
    if indice + 1 >= 2 and not trancado:
        proximo = random.randint(1, 100) <= CHANCE_TRANCADO
    jogo["proximo_trancado"] = proximo


def atualiza_canos(jogo, velocidade):
    """Move os canos, cria novos, conta pontos e apaga os que sairam da tela."""
    nave = jogo["nave"]
    if jogo["proximo_cano"] < TOTAL_CANOS:
        # antes de um cano trancado a distancia e maior, para dar tempo de acertar o alvo
        distancia = DISTANCIA_CANOS
        if jogo["proximo_trancado"]:
            distancia = DISTANCIA_ANTES_TRANCADO
        if len(jogo["canos"]) == 0 or jogo["canos"][-1].cima.x <= LARGURA - distancia:
            cria_cano(jogo)

    restantes = []
    for cano in jogo["canos"]:
        cano.atualiza(velocidade)
        # faiscas saindo do portao enquanto ele abre
        if cano.abrindo and cano.tampa.height > 0:
            x = cano.tampa.x + random.randint(0, LARGURA_CANO)
            jogo["particulas"].append(Particula(x, cano.tampa.bottom, random.randint(-1, 1),
                                                random.randint(-3, -1), sorteia(CORES_FAISCA), 15, 4, 0.1))
        if not cano.passou and cano.cima.right < nave.rect.left:
            cano.passou = True
            jogo["pontos"] += 10
            jogo["canos_passados"] += 1
            if jogo["canos_passados"] % CANOS_POR_CENARIO == 0:
                jogo["banner"] = 150  # mostra o nome do cenario novo
        if cano.cima.right > 0:
            restantes.append(cano)
    jogo["canos"] = restantes


def atualiza_lasers(jogo):
    """Tiros da nave: somem ao sair da tela, bater no cano, acertar alvo ou o chefao."""
    chefe = jogo["chefe"]
    for laser in jogo["lasers"]:
        laser.atualiza()
        # rastro de brilho atras do laser
        if jogo["tempo"] % 2 == 0:
            jogo["particulas"].append(Particula(laser.rect.left, laser.rect.centery, 0, 0, laser.cor, 10, 3, 0))
    restantes = []
    for laser in jogo["lasers"]:
        existe = laser.rect.left < LARGURA
        for cano in jogo["canos"]:
            if cano.acerta_alvo(laser.rect):
                existe = False
                jogo["pontos"] += 5
                toca("alvo")
                # o alvo explode
                explosao(jogo["particulas"], cano.alvo.rect.centerx, cano.alvo.rect.centery, 22, CORES_FOGO, 5)
            elif cano.bloqueia(laser.rect):
                existe = False
                explosao(jogo["particulas"], laser.rect.right, laser.rect.centery, 5, CORES_FAISCA, 2)
        if jogo["fase"] == "chefe" and not chefe.entrando and chefe.vida > 0 and laser.rect.colliderect(chefe.rect):
            existe = False
            chefe.recebe_dano()
            jogo["pontos"] += 20
            explosao(jogo["particulas"], laser.rect.right, laser.rect.centery, 14, CORES_FAISCA, 4)
        if existe:
            restantes.append(laser)
    jogo["lasers"] = restantes


def dano_na_nave(jogo):
    """A nave levou dano: explosao, tela tremendo e, se foi a ultima vida, comeca o fim."""
    nave = jogo["nave"]
    x = nave.rect.centerx
    y = nave.rect.centery
    explosao(jogo["particulas"], x, y, 30, CORES_FOGO, 6)
    toca("dano")
    nave.perde_vida()
    jogo["tremor"] = 15
    if nave.vidas <= 0:
        jogo["resultado"] = "fim"
        jogo["espera_fim"] = 90
        jogo["lasers"] = []
        jogo["lasers_inimigos"] = []
        explosao(jogo["particulas"], x, y, 60, CORES_FOGO, 9)
        toca("explosao")


def atualiza_chefe(jogo):
    """Move o chefao e os tiros dele; tiro que acerta a nave tira uma vida."""
    nave = jogo["nave"]
    jogo["chefe"].atualiza(jogo["lasers_inimigos"])
    restantes = []
    for laser in jogo["lasers_inimigos"]:
        laser.atualiza()
        if jogo["tempo"] % 2 == 0:
            jogo["particulas"].append(Particula(laser.rect.right, laser.rect.centery, 0, 0, VERMELHO, 10, 3, 0))
        existe = laser.rect.right > 0
        if nave.tempo_invulneravel == 0 and jogo["resultado"] == "" and laser.rect.colliderect(nave.rect):
            dano_na_nave(jogo)
            existe = False
        if existe:
            restantes.append(laser)
    jogo["lasers_inimigos"] = restantes


def atualiza_fundo(jogo, velocidade):
    """Anima o fundo: troca o efeito quando muda o cenario e mexe nas pecinhas."""
    cenario = cenario_atual(jogo)
    if jogo["efeito"] != cenario["efeito"]:
        jogo["efeito"] = cenario["efeito"]
        jogo["enfeites"] = cria_enfeites(cenario["efeito"])
    for enfeite in jogo["enfeites"]:
        enfeite.atualiza()
    jogo["chao_x"] += velocidade


def atualiza_final(jogo):
    """Quadro da partida que ja acabou: so as explosoes continuam. Devolve o estado."""
    chefe = jogo["chefe"]
    nave = jogo["nave"]
    chefe.tempo += 1
    if nave.tempo_dano > 0:
        nave.tempo_dano -= 1
    jogo["espera_fim"] -= 1
    if jogo["resultado"] == "vitoria":
        # explosoes pipocando pelo corpo do chefao
        if jogo["espera_fim"] % 6 == 0:
            x = chefe.rect.x + random.randint(0, chefe.rect.width)
            y = chefe.rect.y + random.randint(0, chefe.rect.height)
            explosao(jogo["particulas"], x, y, 18, CORES_FOGO, 5)
            toca("explosao")
            jogo["tremor"] = 8
        if jogo["espera_fim"] == 40:
            chefe.sumiu = True  # explosao final: ele desaparece
            explosao(jogo["particulas"], chefe.rect.centerx, chefe.rect.centery, 90, CORES_FOGO, 10)
            toca("explosao")
            jogo["tremor"] = 20
    if jogo["espera_fim"] <= 0:
        return jogo["resultado"]
    return "jogando"


def atualiza(jogo):
    """Atualiza um quadro. Devolve o estado: 'jogando', 'fim' ou 'vitoria'."""
    nave = jogo["nave"]
    jogo["tempo"] += 1
    velocidade = cenario_atual(jogo)["velocidade"]
    atualiza_fundo(jogo, velocidade)
    jogo["particulas"] = atualiza_particulas(jogo["particulas"])
    if jogo["tremor"] > 0:
        jogo["tremor"] -= 1
    if jogo["banner"] > 0:
        jogo["banner"] -= 1

    if jogo["resultado"] != "":
        return atualiza_final(jogo)

    nave.atualiza()
    if jogo["fase"] == "canos":
        atualiza_canos(jogo, velocidade)
        if jogo["canos_passados"] >= TOTAL_CANOS:
            jogo["fase"] = "chefe"  # acabaram os canos: comeca a luta contra o chefao
            jogo["canos"] = []
            jogo["banner"] = 180
    else:
        atualiza_chefe(jogo)
    atualiza_lasers(jogo)

    # colisoes com canos, teto e chao (nao conta enquanto a nave esta invulneravel)
    if nave.tempo_invulneravel == 0 and jogo["resultado"] == "":
        bateu = nave.toca_limite()
        for cano in jogo["canos"]:
            if cano.bate(nave.rect):
                bateu = True
        if bateu:
            dano_na_nave(jogo)

    # derrotou o chefao: comeca a sequencia de explosoes
    if jogo["fase"] == "chefe" and jogo["chefe"].vida <= 0 and jogo["resultado"] == "":
        jogo["resultado"] = "vitoria"
        jogo["espera_fim"] = 150
        jogo["pontos"] += 100
        jogo["lasers"] = []
        jogo["lasers_inimigos"] = []
    return "jogando"
