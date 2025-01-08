import random
import os

class Personagem:
    def __init__(self, nome, vida, ataque, defesa, sorte, velocidade):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.sorte = sorte
        self.velocidade = velocidade
        self.canalizando = None  # Tipo de ação sendo canalizada ("ataque" ou "defesa")
        self.turnos_canalizando = 0  # Quantidade de turnos canalizando
        self.atordoado = False  # Indica se está atordoado
        self.modificador_ataque = 0
        self.modificador_defesa = 0

    def gerar_numeros_sorte(self):
        numeros = sorted([random.randint(1, 10) for _ in range(self.sorte)], reverse=True)
        return numeros

    def receber_dano(self, dano):
        self.vida -= dano
        return dano

    def status(self):
        numeros_sorte = self.gerar_numeros_sorte()
        return (
            f"{self.nome} - Vida: {self.vida}, Ataque: {self.ataque + self.modificador_ataque}, "
            f"Defesa: {self.defesa + self.modificador_defesa}, Velocidade: {self.velocidade}, "
            f"Sorte: {self.sorte}, Números da Sorte: {numeros_sorte}"
        )

class Acoes:
    def __init__(self):
        pass

    def fortificar(self, personagem, tipo):
        if personagem.canalizando is None:
            personagem.canalizando = tipo
            personagem.turnos_canalizando = 1
            print(f"{personagem.nome} começou a canalizar para fortificar {tipo}.")
        else:
            personagem.turnos_canalizando += 1
            print(f"{personagem.nome} continua canalizando {tipo} (turnos canalizando: {personagem.turnos_canalizando}).")

        if tipo == "ataque":
            personagem.modificador_ataque += 1
        elif tipo == "defesa":
            personagem.modificador_defesa += 1

    def interromper_canalizacao(self, atacante, defensor, dano):
        if defensor.canalizando:
            print(f"{defensor.nome} foi interrompido durante a canalização de {defensor.canalizando}!")
            if defensor.turnos_canalizando == 1:
                print(f"Interrupção no primeiro turno! {defensor.nome} toma +1 de dano.")
                dano += 1
            else:
                print(f"Interrupção após múltiplos turnos! {defensor.nome} toma +1 de dano e está atordoado.")
                dano += 1
                defensor.atordoado = True
            defensor.canalizando = None
            defensor.turnos_canalizando = 0
        return defensor.receber_dano(dano)

    def bater(self, atacante, defensor):
        numeros_atacante = atacante.gerar_numeros_sorte()
        numeros_defensor = defensor.gerar_numeros_sorte()

        maior_numero_atacante = numeros_atacante[0]
        maior_numero_defensor = numeros_defensor[0]

        if maior_numero_atacante == maior_numero_defensor:
            print(f"{atacante.nome} tentou atacar, mas {defensor.nome} bloqueou automaticamente!")
            return

        if maior_numero_atacante > maior_numero_defensor:
            dano = max((atacante.ataque + atacante.modificador_ataque - defensor.defesa - defensor.modificador_defesa) + 1, 0)
            dano_sofrido = self.interromper_canalizacao(atacante, defensor, dano)
            print(f"{atacante.nome} acertou o ataque! {defensor.nome} sofreu {dano_sofrido} de dano.")
        else:
            print(f"{atacante.nome} tentou atacar, mas {defensor.nome} defendeu com sucesso!")

    def bloquear(self, defensor, atacante):
        numeros_defensor = defensor.gerar_numeros_sorte()
        numeros_atacante = atacante.gerar_numeros_sorte()

        maior_numero_defensor = numeros_defensor[0]
        maior_numero_atacante = numeros_atacante[0]

        if maior_numero_defensor == maior_numero_atacante:
            print(f"{defensor.nome} bloqueou com sucesso a ação de {atacante.nome} e atordoou o atacante!")
            atacante.atordoado = True
            return 0  # O dano não é aplicado
        elif maior_numero_defensor > maior_numero_atacante:
            print(f"{defensor.nome} bloqueou com sucesso a ação de {atacante.nome}!")
            return 0  # O dano não é aplicado
        else:
            print(f"{defensor.nome} tentou bloquear, mas {atacante.nome} passou pela defesa!")
            return 1  # O atacante causa +1 de dano

# Função para limpar o prompt
def limpar_prompt():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função de batalha
def batalha(personagem1, personagem2):
    acoes = Acoes()
    turno = 0

    while personagem1.vida > 0 and personagem2.vida > 0:
        limpar_prompt()
        atacante = personagem1 if turno % 2 == 0 else personagem2
        defensor = personagem2 if turno % 2 == 0 else personagem1

        # Exibe apenas o status do personagem que está jogando
        print(f"Status de {atacante.nome}:\n{atacante.status()}\n")

        if atacante.atordoado:
            print(f"\n{atacante.nome} está atordoado e perdeu o turno!")
            atacante.atordoado = False
            turno += 1
            input("Pressione Enter para continuar...")
            continue

        print(f"Turno de {atacante.nome}:")
        print("Escolha sua ação:")
        print("1. Bater")
        print("2. Fortificar Ataque")
        print("3. Fortificar Defesa")
        print("4. Bloquear Ação")

        escolha = input("Digite o número da sua escolha: ").strip()

        if escolha == "1":
            acoes.bater(atacante, defensor)
        elif escolha == "2":
            acoes.fortificar(atacante, "ataque")
        elif escolha == "3":
            acoes.fortificar(atacante, "defesa")
        elif escolha == "4":
            dano = acoes.bloquear(defensor, atacante)
            if dano > 0:
                dano_sofrido = defensor.receber_dano(dano + 1)
                print(f"{atacante.nome} causou +1 de dano após falha no bloqueio!")
        else:
            print("Escolha inválida! Perdeu o turno.")

        if defensor.vida <= 0:
            limpar_prompt()
            print(f"\n{defensor.nome} foi derrotado!")
            break

        input("\nPressione Enter para passar para o próximo turno...")
        turno += 1

# Criando personagens balanceados
personagem1 = Personagem("Guerreiro", 20, 8, 4, 3, 6)
personagem2 = Personagem("Mago", 18, 10, 5, 4, 5)
personagem3 = Personagem("Ladino", 15, 7, 3, 7, 8)
personagem4 = Personagem("Arqueiro", 16, 9, 3, 5, 7)
personagem5 = Personagem("Bárbaro", 25, 12, 6, 2, 4)
personagem6 = Personagem("Sacerdote", 22, 6, 4, 6, 5)
personagem7 = Personagem("Paladino", 22, 9, 6, 4, 5)
personagem8 = Personagem("Assassino", 14, 11, 2, 5, 9)

# Lista de personagens
personagens = [personagem1, personagem2, personagem3, personagem4, personagem5, personagem6, personagem7, personagem8]

# Função para escolher personagens
def escolher_personagem():
    print("Escolha seu personagem:")
    for i, personagem in enumerate(personagens, 1):
        print(f"{i}. {personagem.nome} - {personagem.status()}")
    escolha = int(input("Digite o número do personagem escolhido: ")) - 1
    return personagens[escolha]

# Função principal para iniciar o jogo
def main():
    print("Bem-vindo ao Jogo de Batalha!")
    jogador1 = escolher_personagem()
    print(f"\nVocê escolheu: {jogador1.nome}")
    jogador2 = escolher_personagem()
    print(f"\nO oponente escolhido foi: {jogador2.nome}")
    input("\nPressione Enter para começar a batalha...")
    batalha(jogador1, jogador2)

# Iniciando o jogo
main()
