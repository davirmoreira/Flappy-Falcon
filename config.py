"""Configuracoes do Flappy Falcon: tamanhos, fisica, cores, pilotos e cenarios.

Para mudar a dificuldade do jogo, mexa so neste arquivo.
"""

# ======================================================================
# CONSTANTES (tamanhos, fisica, cores, personagens e cenarios)
# Para mudar a dificuldade, mexa aqui.
# ======================================================================
LARGURA = 800
ALTURA = 600
COMECAR_EM_TELA_CHEIA = False  # True abre o jogo ja em tela cheia (a tecla F alterna durante o jogo)
CHAO = 560  # altura do chao: a nave perde uma vida se tocar nele
FPS = 60

# ---------- Nave ----------
FORCA_PULO = -8  # velocidade para cima logo depois do pulo
TEMPO_INVULNERAVEL = 120  # quadros sem levar dano depois de bater (2 segundos)
VELOCIDADE_LASER = 12

# ---------- Canos e alvos ----------
LARGURA_CANO = 70
BURACO = 190  # espaco por onde a nave passa em um cano normal
BURACO_TRANCADO = 230  # o espaco e maior nos canos trancados (com alvo)
DISTANCIA_CANOS = 340  # distancia horizontal entre dois canos normais
DISTANCIA_ANTES_TRANCADO = 520  # distancia ate um cano trancado (da tempo de acertar o alvo)
CHANCE_TRANCADO = 50  # chance (em %) de um cano vir trancado, com alvo
CANOS_POR_CENARIO = 6  # quantos canos a nave passa antes de trocar de cenario
ALVO_TAMANHO = 56  # tamanho do alvo
ALVO_DISTANCIA = 170  # distancia do alvo ate o cano que ele abre

# ---------- Chefao ----------
VIDA_CHEFE = 10  # acertos necessarios para derrotar o chefao
VELOCIDADE_LASER_CHEFE = 7

# Para testar o chefao sem passar pelos 30 canos, troque para True
TESTAR_CHEFE = False

# ---------- Imagens e sons ----------
USAR_IMAGENS = True  # False = desenha tudo com formas coloridas
USAR_SONS = True  # False = jogo mudo
ESTILO_FOGO = "laranja"  # cor do fogo do pulo: "laranja" ou "azul"
VOLUME_MUSICA = 0.3
VOLUME_EFEITOS = 0.7

# ---------- Cena "Eu sou seu pai" (entre a derrota do chefao e a tela de vitoria) ----------
TEMPO_POR_FALA = 45  # quadros em que cada pedaco da frase fica na tela
DURACAO_CENA = 330  # quadros ate a cena acabar sozinha (ESPACO pula depois de 1 segundo)

# ---------- Cores ----------
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 50, 50)
CINZA = (90, 90, 90)
CINZA_CLARO = (200, 200, 205)
AMARELO = (250, 220, 0)
LARANJA = (255, 140, 0)
AZUL = (80, 160, 255)
AZUL_CLARO = (90, 210, 255)

# ---------- Listas de cores e de movimentos usadas nas animacoes ----------
CORES_FOGO = [LARANJA, AMARELO, VERMELHO, BRANCO]
CORES_FAISCA = [AZUL_CLARO, BRANCO, AMARELO]
CORES_CONFETE = [VERMELHO, AMARELO, AZUL_CLARO, (120, 255, 120), (255, 120, 255)]
BALANCO = [-6, -2, 2, 6, 2, -2]  # vai e volta suave (titulo, capa do chefao, respiracao)
PULSO = [0, 2, 3, 2]  # o astro do cenario "respira" nesse ritmo
SALTOS = [0, -14, -24, -14, 0, 0]  # pulinhos do piloto na tela de vitoria

# ---------- Personagens (cada um tem um poder) ----------
PERSONAGENS = [
    {"nome": "Davi Skywalker", "poder": "Cai mais devagar", "cor": (225, 215, 190),
     "arquivo": "davi", "estilo": "jedi", "pele": (240, 200, 160), "cabelo": (225, 185, 80),
     "gravidade": 0.42, "vidas": 3, "espera_tiro": 15},
    {"nome": "Lucasbacca", "poder": "4 vidas", "cor": (110, 70, 30),
     "arquivo": "lucas", "estilo": "wookiee", "pele": (150, 110, 70), "cabelo": (100, 65, 30),
     "gravidade": 0.5, "vidas": 4, "espera_tiro": 15},
    {"nome": "Enzo Solo", "poder": "Tiro mais rápido", "cor": (235, 235, 235),
     "arquivo": "enzo", "estilo": "contrabandista", "pele": (240, 200, 160), "cabelo": (70, 45, 25),
     "gravidade": 0.5, "vidas": 3, "espera_tiro": 7},
]

# ---------- Efeitos de fundo: pecinhas que se mexem sozinhas no cenario ----------
# vx e vy: velocidade; forma: como desenhar; quantidade: quantas pecinhas
EFEITOS = {
    "poeira": {"vx": -2, "vy": 0, "cor": (255, 235, 190), "forma": "risco", "quantidade": 20},
    "nuvens": {"vx": -1, "vy": 0, "cor": (255, 255, 255), "forma": "nuvem", "quantidade": 6},
    "brasas": {"vx": -1, "vy": -1, "cor": (255, 150, 40), "forma": "ponto", "quantidade": 35},
    "vagalumes": {"vx": -1, "vy": 0, "cor": (230, 255, 120), "forma": "pisca", "quantidade": 22},
    "chuva": {"vx": -1, "vy": 5, "cor": (200, 215, 240), "forma": "risco_diag", "quantidade": 45},
    "estrelas": {"vx": -1, "vy": 0, "cor": (255, 255, 255), "forma": "pisca", "quantidade": 45},
}

# ---------- Cenarios (na ordem em que aparecem) ----------
CENARIOS = [
    {"nome": "TATOOINE", "arquivo": "tatooine", "fundo": (232, 178, 100), "chao": (194, 140, 70),
     "cano": (150, 105, 60), "borda": (110, 75, 40), "astro": (255, 240, 180),
     "velocidade": 3, "efeito": "poeira"},
    {"nome": "NABOO", "arquivo": "naboo", "fundo": (120, 190, 220), "chao": (70, 150, 90),
     "cano": (205, 195, 150), "borda": (160, 150, 110), "astro": (255, 255, 255),
     "velocidade": 4, "efeito": "nuvens"},
    {"nome": "MUSTAFAR", "arquivo": "mustafar", "fundo": (90, 20, 10), "chao": (40, 10, 10),
     "cano": (70, 70, 80), "borda": (40, 40, 50), "astro": (255, 120, 20),
     "velocidade": 4, "efeito": "brasas"},
    {"nome": "ENDOR", "arquivo": "endor", "fundo": (25, 70, 40), "chao": (60, 40, 20),
     "cano": (110, 75, 40), "borda": (75, 50, 25), "astro": (210, 230, 210),
     "velocidade": 5, "efeito": "vagalumes"},
    {"nome": "KAMINO", "arquivo": "kamino", "fundo": (60, 80, 110), "chao": (150, 165, 185),
     "cano": (225, 230, 240), "borda": (170, 180, 195), "astro": (200, 210, 230),
     "velocidade": 5, "efeito": "chuva"},
]
CENARIO_CHEFE = {"nome": "ESTRELA DA MORTE", "arquivo": "estrela", "fundo": (35, 40, 52),
                 "chao": (70, 75, 90), "astro": (120, 30, 30),
                 "velocidade": 3, "efeito": "estrelas"}

TOTAL_CANOS = CANOS_POR_CENARIO * len(CENARIOS)
