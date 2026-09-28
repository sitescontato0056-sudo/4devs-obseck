#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4Devs TOOL - Geração e validação de dados brasileiros
Painel dark & clean para Termux.
"""

import os, sys, time, random, string, secrets, re, json
from datetime import datetime

try:
    import requests
    from colorama import Fore, Style, init
    import pyfiglet
except ImportError:
    os.system("pip install colorama requests pyfiglet")
    import requests
    from colorama import Fore, Style, init
    import pyfiglet

init(autoreset=True)

# ============ PALETA DARK ============
class C:
    DIM   = Style.DIM
    GREY  = Fore.LIGHTBLACK_EX
    SILVER= Fore.WHITE
    WHITE = Fore.LIGHTWHITE_EX
    OK    = Fore.LIGHTGREEN_EX
    ERR   = Fore.LIGHTRED_EX
    WARN  = Fore.LIGHTYELLOW_EX
    RS    = Style.RESET_ALL
    BR    = Style.BRIGHT

# ============ UTILS ============
def clear(): os.system("clear")
def linha(): print(f"{C.DIM}{'─' * 52}{C.RS}")

def titulo(txt):
    clear()
    art = pyfiglet.figlet_format(txt, font="small")
    print(f"{C.GREY}{art}{C.RS}")
    linha()

def pausar():
    input(f"\n{C.GREY}  ··· ENTER para voltar{C.RS}")

def ok(m):   print(f"{C.OK}  ✓{C.RS}  {C.WHITE}{m}{C.RS}")
def err(m):  print(f"{C.ERR}  ✗{C.RS}  {C.WHITE}{m}{C.RS}")
def warn(m): print(f"{C.WARN}  !{C.RS}  {C.WHITE}{m}{C.RS}")
def info(m): print(f"{C.GREY}  ·{C.RS}  {C.SILVER}{m}{C.RS}")

def loading(msg="processando", t=1.0):
    frames = ["·", "··", "···", "··"]
    end = time.time() + t
    i = 0
    while time.time() < end:
        print(f"\r{C.GREY}  {frames[i % len(frames)]:<4}{C.DIM}{msg}{C.RS}", end="")
        time.sleep(0.15)
        i += 1
    print(f"\r{C.OK}  ✓{C.RS}  {C.DIM}{msg}{C.RS}    ")

# ============ BANNER ============
def banner():
    clear()
    art = pyfiglet.figlet_format("4DEVS", font="slant")
    print(f"{C.GREY}{art}{C.RS}")
    print(f"{C.DIM}  ┌────────────────────────────────────────────────┐{C.RS}")
    print(f"{C.DIM}  │{C.RS}  {C.SILVER}4DEVS TOOL{C.RS}  {C.DIM}·{C.RS}  {C.GREY}v1.0{C.RS}                       {C.DIM}│{C.RS}")
    print(f"{C.DIM}  │{C.RS}  {C.DIM}dados brasileiros · geração · validação{C.RS}       {C.DIM}│{C.RS}")
    print(f"{C.DIM}  └────────────────────────────────────────────────┘{C.RS}")
    print(f"{C.DIM}  {os.getenv('USER','anon')}  ·  {datetime.now().strftime('%d.%m.%Y  %H:%M')}{C.RS}")
    linha()

# ============ MENU ============
def menu():
    print()
    print(f"  {C.GREY}PESSOAS & DOCUMENTOS{C.RS}")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}1{C.RS}   pessoa completa (nome, cpf, rg, endereço)")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}2{C.RS}   cpf")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}3{C.RS}   rg")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}4{C.RS}   cnh")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}5{C.RS}   título de eleitor")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}6{C.RS}   pis/pasep")
    print(f"  {C.DIM}└{C.RS}  {C.SILVER}7{C.RS}   certidões (nascimento/casamento/óbito)")
    print()
    print(f"  {C.GREY}EMPRESAS & VEÍCULOS{C.RS}")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}8{C.RS}   cnpj")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}9{C.RS}   empresa completa")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}10{C.RS}  veículo (marca, modelo, placa, renavam)")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}11{C.RS}  placa de veículo")
    print(f"  {C.DIM}└{C.RS}  {C.SILVER}12{C.RS}  renavam")
    print()
    print(f"  {C.GREY}BANCOS & FINANCEIRO{C.RS}")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}13{C.RS}  conta bancária")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}14{C.RS}  cartão de crédito")
    print(f"  {C.DIM}└{C.RS}  {C.SILVER}15{C.RS}  inscrição estadual")
    print()
    print(f"  {C.GREY}LOCALIZAÇÃO{C.RS}")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}16{C.RS}  cidades por uf")
    print(f"  {C.DIM}└{C.RS}  {C.SILVER}17{C.RS}  uf aleatória")
    print()
    print(f"  {C.GREY}VALIDADORES{C.RS}")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}18{C.RS}  validar cpf")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}19{C.RS}  validar cnpj")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}20{C.RS}  validar cnh")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}21{C.RS}  validar título de eleitor")
    print(f"  {C.DIM}├{C.RS}  {C.SILVER}22{C.RS}  validar pis/pasep")
    print(f"  {C.DIM}└{C.RS}  {C.SILVER}23{C.RS}  validar cartão de crédito")
    print()
    print(f"  {C.DIM}0   sair{C.RS}")
    linha()

# ============ DADOS BASE ============
NOMES_M = ["Lucas","Rafael","Gabriel","André","Bruno","Felipe","Thiago","Rodrigo","Diego","Gustavo",
           "Matheus","Pedro","João","Carlos","Eduardo","Vinícius","Leonardo","Henrique","Murilo","Otávio"]
NOMES_F = ["Marina","Beatriz","Sofia","Camila","Laura","Juliana","Patrícia","Fernanda","Letícia","Aline",
           "Carolina","Isabela","Amanda","Bruna","Larissa","Vanessa","Natália","Priscila","Tatiane","Jéssica"]
SOBRENOMES = ["Silva","Santos","Oliveira","Souza","Lima","Costa","Pereira","Almeida","Ferreira","Rodrigues",
              "Gomes","Martins","Araújo","Barbosa","Ribeiro","Cardoso","Moreira","Nascimento","Carvalho","Melo"]
RUAS = ["Rua das Flores","Av. Brasil","Rua São João","Av. Paulista","Rua XV de Novembro","Av. Getúlio Vargas",
        "Rua Rio Branco","Av. Santos Dumont","Rua da Praia","Av. Atlântica","Rua das Palmeiras","Av. Central"]
BAIRROS = ["Centro","Jardim América","Vila Nova","Boa Vista","Santa Rita","São José","Industrial","Alto da Serra"]
CIDADES = {
    "SP": ["São Paulo","Campinas","Santos","Ribeirão Preto","Sorocaba","São José dos Campos"],
    "RJ": ["Rio de Janeiro","Niterói","Petrópolis","Nova Iguaçu","Campos dos Goytacazes"],
    "MG": ["Belo Horizonte","Uberlândia","Contagem","Juiz de Fora","Betim"],
    "PR": ["Curitiba","Londrina","Maringá","Ponta Grossa","Cascavel"],
    "RS": ["Porto Alegre","Caxias do Sul","Pelotas","Canoas","Santa Maria"],
    "BA": ["Salvador","Feira de Santana","Vitória da Conquista","Camaçari"],
    "PE": ["Recife","Jaboatão","Olinda","Caruaru"],
    "CE": ["Fortaleza","Caucaia","Juazeiro do Norte","Sobral"],
    "SC": ["Florianópolis","Joinville","Blumenau","São José"],
    "GO": ["Goiânia","Aparecida de Goiânia","Anápolis","Rio Verde"],
}
UFS = list(CIDADES.keys())
MARCAS = ["Fiat","Volkswagen","Chevrolet","Ford","Toyota","Honda","Hyundai","Renault","Jeep","Nissan"]
MODELOS = {"Fiat":["Argo","Cronos","Mobi","Toro"],"Volkswagen":["Gol","Polo","T-Cross","Nivus"],
           "Chevrolet":["Onix","Tracker","Cruze","Spin"],"Ford":["Ka","EcoSport","Ranger"],
           "Toyota":["Corolla","Yaris","Hilux","SW4"],"Honda":["Civic","Fit","HR-V","City"],
           "Hyundai":["HB20","Creta","Tucson"],"Renault":["Kwid","Sandero","Duster"],
           "Jeep":["Renegade","Compass"],"Nissan":["Kicks","Versa","Frontier"]}
BANCOS = ["Banco do Brasil","Caixa Econômica","Itaú","Bradesco","Santander","Nubank","Inter","C6 Bank"]
BANDEIRAS = ["Visa","Mastercard","Elo","American Express","Hipercard"]

# ============ GERADORES ============
def gerar_cpf():
    """Gera CPF válido (algoritmo oficial)."""
    n = [random.randint(0,9) for _ in range(9)]
    for _ in range(2):
        soma = sum(v * (len(n)+1-i) for i,v in enumerate(n))
        dig = (soma * 10) % 11
        n.append(0 if dig == 10 else dig)
    return "".join(map(str,n))

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def validar_cpf(cpf):
    cpf = re.sub(r"\D","",cpf)
    if len(cpf) != 11 or cpf == cpf[0]*11: return False
    for i in range(9,11):
        soma = sum(int(cpf[j]) * (i+1-j) for j in range(i))
        dig = (soma * 10) % 11
        if dig == 10: dig = 0
        if dig != int(cpf[i]): return False
    return True

def gerar_cnpj():
    """Gera CNPJ válido (algoritmo oficial)."""
    n = [random.randint(0,9) for _ in range(8)] + [0,0,0,1]
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    for pesos in [pesos1, pesos2]:
        soma = sum(v*p for v,p in zip(n,pesos))
        dig = 11 - (soma % 11)
        n.append(0 if dig >= 10 else dig)
    return "".join(map(str,n))

def formatar_cnpj(cnpj):
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def validar_cnpj(cnpj):
    cnpj = re.sub(r"\D","",cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0]*14: return False
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    for i,pesos in enumerate([pesos1,pesos2]):
        soma = sum(int(cnpj[j])*pesos[j] for j in range(12+i))
        dig = 11 - (soma % 11)
        if dig >= 10: dig = 0
        if dig != int(cnpj[12+i]): return False
    return True

def gerar_rg(uf="SP"):
    return f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(0,9)}"

def gerar_cnh():
    n = [random.randint(0,9) for _ in range(9)]
    soma = sum(v * (9-i) for i,v in enumerate(n))
    dsc = soma % 11
    if dsc >= 10: dsc = 0
    n.append(dsc)
    soma2 = sum(v * (10-i) for i,v in enumerate(n))
    dsc2 = soma2 % 11
    if dsc2 >= 10: dsc2 = 0
    n.append(dsc2)
    return "".join(map(str,n))

def validar_cnh(cnh):
    cnh = re.sub(r"\D","",cnh)
    if len(cnh) != 11: return False
    n = [int(x) for x in cnh[:9]]
    soma = sum(v * (9-i) for i,v in enumerate(n))
    dsc = soma % 11
    if dsc >= 10: dsc = 0
    if dsc != int(cnh[9]): return False
    soma2 = sum(int(cnh[i]) * (10-i) for i in range(10))
    dsc2 = soma2 % 11
    if dsc2 >= 10: dsc2 = 0
    return dsc2 == int(cnh[10])

def gerar_titulo(uf="SP"):
    return f"{random.randint(10000000,99999999)}{random.randint(10,99)}"

def validar_titulo(titulo):
    titulo = re.sub(r"\D","",titulo)
    return len(titulo) == 12

def gerar_pis():
    n = [random.randint(0,9) for _ in range(10)]
    pesos = [3,2,9,8,7,6,5,4,3,2]
    soma = sum(v*p for v,p in zip(n,pesos))
    dig = 11 - (soma % 11)
    if dig >= 10: dig = 0
    return "".join(map(str,n)) + str(dig)

def validar_pis(pis):
    pis = re.sub(r"\D","",pis)
    if len(pis) != 11: return False
    pesos = [3,2,9,8,7,6,5,4,3,2]
    soma = sum(int(pis[i])*pesos[i] for i in range(10))
    dig = 11 - (soma % 11)
    if dig >= 10: dig = 0
    return dig == int(pis[10])

def gerar_renavam():
    n = [random.randint(0,9) for _ in range(10)]
    pesos = [2,3,4,5,6,7,8,9,2,3]
    soma = sum(v*p for v,p in zip(n,pesos))
    dig = 11 - (soma % 11)
    if dig >= 10: dig = 0
    return "".join(map(str,n)) + str(dig)

def gerar_placa():
    letras = string.ascii_uppercase
    return f"{random.choice(letras)}{random.choice(letras)}{random.choice(letras)}{random.randint(0,9)}{random.choice(letras)}{random.randint(0,9)}{random.randint(0,9)}"

def gerar_inscricao_estadual(uf="SP"):
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}"

def gerar_certidao(tipo="nascimento"):
    return f"{random.randint(100000,999999)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(2000,2024)} {random.randint(1,9)} {random.randint(10000,99999)} {random.randint(100,999)} {random.randint(1000000,9999999)}-{random.randint(10,99)}"

def gerar_conta_bancaria():
    banco = random.choice(BANCOS)
    return {"banco": banco, "agencia": f"{random.randint(1000,9999)}", "conta": f"{random.randint(10000,99999)}-{random.randint(0,9)}"}

def gerar_cartao():
    bandeira = random.choice(BANDEIRAS)
    prefixos = {"Visa":["4"],"Mastercard":["51","52","53","54","55"],"Elo":["4011","4312","5041","5067"],
                "American Express":["34","37"],"Hipercard":["606282"]}
    prefixo = random.choice(prefixos[bandeira])
    n = list(prefixo) + [str(random.randint(0,9)) for _ in range(15-len(prefixo))]
    soma = 0
    for i,d in enumerate(reversed(n)):
        v = int(d)
        if i % 2 == 1:
            v *= 2
            if v > 9: v -= 9
        soma += v
    n.append(str((10 - (soma % 10)) % 10))
    numero = "".join(n)
    val = f"{random.randint(1,12):02d}/{random.randint(2025,2030)}"
    cvv = f"{random.randint(100,999)}"
    return {"bandeira": bandeira, "numero": numero, "validade": val, "cvv": cvv}

def validar_cartao(numero):
    numero = re.sub(r"\D","",numero)
    if len(numero) not in [15,16]: return False
    soma = 0
    for i,d in enumerate(reversed(numero)):
        v = int(d)
        if i % 2 == 1:
            v *= 2
            if v > 9: v -= 9
        soma += v
    return soma % 10 == 0

def gerar_pessoa():
    sexo = random.choice(["M","F"])
    nome = random.choice(NOMES_M if sexo == "M" else NOMES_F)
    sobre = random.choice(SOBRENOMES)
    uf = random.choice(UFS)
    cidade = random.choice(CIDADES[uf])
    return {
        "nome": f"{nome} {sobre}",
        "cpf": formatar_cpf(gerar_cpf()),
        "rg": gerar_rg(uf),
        "cnh": gerar_cnh(),
        "pis": gerar_pis(),
        "nascimento": f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{random.randint(1960,2005)}",
        "endereco": f"{random.choice(RUAS)}, {random.randint(1,2000)}",
        "bairro": random.choice(BAIRROS),
        "cidade": cidade,
        "uf": uf,
        "cep": f"{random.randint(10000,99999)}-{random.randint(100,999)}",
        "telefone": f"({random.randint(11,99)}) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
    }

def gerar_empresa():
    nome = f"{random.choice(SOBRENOMES).upper()} {random.choice(['LTDA','ME','EIRELI','S.A.'])}"
    return {
        "razao_social": nome,
        "cnpj": formatar_cnpj(gerar_cnpj()),
        "inscricao_estadual": gerar_inscricao_estadual(),
        "endereco": f"{random.choice(RUAS)}, {random.randint(1,5000)}",
        "cidade": random.choice(CIDADES[random.choice(UFS)]),
        "cep": f"{random.randint(10000,99999)}-{random.randint(100,999)}",
    }

# ============ AÇÕES ============
def act_pessoa():
    titulo("pessoa")
    loading("gerando pessoa completa", 1.2)
    p = gerar_pessoa()
    print()
    for k,v in p.items():
        print(f"  {C.DIM}{k:<12}{C.RS}  {C.WHITE}{v}{C.RS}")
    pausar()

def act_cpf():
    titulo("cpf")
    loading("gerando cpf válido", 0.8)
    cpf = formatar_cpf(gerar_cpf())
    print()
    print(f"  {C.WHITE}{cpf}{C.RS}")
    print(f"  {C.DIM}válido segundo algoritmo oficial{C.RS}")
    pausar()

def act_rg():
    titulo("rg")
    loading("gerando rg", 0.8)
    uf = input(f"  {C.GREY}uf{C.RS} {C.DIM}(padrão SP){C.RS}  ").strip().upper() or "SP"
    rg = gerar_rg(uf)
    print()
    print(f"  {C.WHITE}{rg}{C.RS}  {C.DIM}({uf}){C.RS}")
    pausar()

def act_cnh():
    titulo("cnh")
    loading("gerando cnh válida", 0.8)
    cnh = gerar_cnh()
    print()
    print(f"  {C.WHITE}{cnh}{C.RS}")
    print(f"  {C.DIM}válida segundo algoritmo oficial{C.RS}")
    pausar()

def act_titulo():
    titulo("título de eleitor")
    loading("gerando título", 0.8)
    uf = input(f"  {C.GREY}uf{C.RS} {C.DIM}(padrão SP){C.RS}  ").strip().upper() or "SP"
    t = gerar_titulo(uf)
    print()
    print(f"  {C.WHITE}{t}{C.RS}  {C.DIM}({uf}){C.RS}")
    pausar()

def act_pis():
    titulo("pis/pasep")
    loading("gerando pis válido", 0.8)
    pis = gerar_pis()
    print()
    print(f"  {C.WHITE}{pis}{C.RS}")
    pausar()

def act_certidao():
    titulo("certidão")
    loading("gerando certidão", 0.8)
    tipo = input(f"  {C.GREY}tipo{C.RS} {C.DIM}(nascimento/casamento/óbito, padrão nascimento){C.RS}  ").strip().lower() or "nascimento"
    c = gerar_certidao(tipo)
    print()
    print(f"  {C.WHITE}{c}{C.RS}  {C.DIM}({tipo}){C.RS}")
    pausar()

def act_cnpj():
    titulo("cnpj")
    loading("gerando cnpj válido", 0.8)
    cnpj = formatar_cnpj(gerar_cnpj())
    print()
    print(f"  {C.WHITE}{cnpj}{C.RS}")
    print(f"  {C.DIM}válido segundo algoritmo oficial{C.RS}")
    pausar()

def act_empresa():
    titulo("empresa")
    loading("gerando empresa", 1.2)
    e = gerar_empresa()
    print()
    for k,v in e.items():
        print(f"  {C.DIM}{k:<18}{C.RS}  {C.WHITE}{v}{C.RS}")
    pausar()

def act_veiculo():
    titulo("veículo")
    loading("gerando veículo", 1.0)
    marca = random.choice(MARCAS)
    modelo = random.choice(MODELOS[marca])
    v = {
        "marca": marca,
        "modelo": modelo,
        "ano": f"{random.randint(2015,2025)}/{random.randint(2016,2026)}",
        "placa": gerar_placa(),
        "renavam": gerar_renavam(),
        "chassi": "".join(random.choices(string.ascii_uppercase+string.digits, k=17)),
    }
    print()
    for k,val in v.items():
        print(f"  {C.DIM}{k:<10}{C.RS}  {C.WHITE}{val}{C.RS}")
    pausar()

def act_placa():
    titulo("placa")
    loading("gerando placa", 0.6)
    print()
    print(f"  {C.WHITE}{gerar_placa()}{C.RS}")
    pausar()

def act_renavam():
    titulo("renavam")
    loading("gerando renavam", 0.6)
    print()
    print(f"  {C.WHITE}{gerar_renavam()}{C.RS}")
    pausar()

def act_conta():
    titulo("conta bancária")
    loading("gerando conta", 0.8)
    c = gerar_conta_bancaria()
    print()
    for k,v in c.items():
        print(f"  {C.DIM}{k:<8}{C.RS}  {C.WHITE}{v}{C.RS}")
    pausar()

def act_cartao():
    titulo("cartão de crédito")
    loading("gerando cartão", 0.8)
    c = gerar_cartao()
    print()
    for k,v in c.items():
        print(f"  {C.DIM}{k:<10}{C.RS}  {C.WHITE}{v}{C.RS}")
    pausar()

def act_ie():
    titulo("inscrição estadual")
    loading("gerando ie", 0.8)
    uf = input(f"  {C.GREY}uf{C.RS} {C.DIM}(padrão SP){C.RS}  ").strip().upper() or "SP"
    ie = gerar_inscricao_estadual(uf)
    print()
    print(f"  {C.WHITE}{ie}{C.RS}  {C.DIM}({uf}){C.RS}")
    pausar()

def act_cidades():
    titulo("cidades")
    print()
    print(f"  {C.GREY}ufs disponíveis:{C.RS}")
    for uf in UFS:
        print(f"  {C.DIM}·{C.RS} {C.SILVER}{uf}{C.RS}  {C.DIM}{', '.join(CIDADES[uf][:3])}...{C.RS}")
    print()
    uf = input(f"  {C.GREY}uf{C.RS}  ").strip().upper()
    if uf in CIDADES:
        loading(f"carregando cidades de {uf}", 0.8)
        print()
        for cid in CIDADES[uf]:
            print(f"  {C.OK}✓{C.RS}  {C.WHITE}{cid}{C.RS}")
    else:
        err(f"uf {uf} não disponível")
    pausar()

def act_uf():
    titulo("uf")
    loading("sorteando uf", 0.6)
    print()
    print(f"  {C.WHITE}{random.choice(UFS)}{C.RS}")
    pausar()

# ============ VALIDADORES ============
def act_validar_cpf():
    titulo("validar cpf")
    cpf = input(f"  {C.GREY}cpf{C.RS}  ").strip()
    loading("validando", 0.6)
    print()
    if validar_cpf(cpf):
        ok(f"{cpf}  {C.DIM}válido{C.RS}")
    else:
        err(f"{cpf}  {C.DIM}inválido{C.RS}")
    pausar()

def act_validar_cnpj():
    titulo("validar cnpj")
    cnpj = input(f"  {C.GREY}cnpj{C.RS}  ").strip()
    loading("validando", 0.6)
    print()
    if validar_cnpj(cnpj):
        ok(f"{cnpj}  {C.DIM}válido{C.RS}")
    else:
        err(f"{cnpj}  {C.DIM}inválido{C.RS}")
    pausar()

def act_validar_cnh():
    titulo("validar cnh")
    cnh = input(f"  {C.GREY}cnh{C.RS}  ").strip()
    loading("validando", 0.6)
    print()
    if validar_cnh(cnh):
        ok(f"{cnh}  {C.DIM}válida{C.RS}")
    else:
        err(f"{cnh}  {C.DIM}inválida{C.RS}")
    pausar()

def act_validar_titulo():
    titulo("validar título")
    t = input(f"  {C.GREY}título{C.RS}  ").strip()
    loading("validando", 0.6)
    print()
    if validar_titulo(t):
        ok(f"{t}  {C.DIM}formato válido{C.RS}")
    else:
        err(f"{t}  {C.DIM}inválido{C.RS}")
    pausar()

def act_validar_pis():
    titulo("validar pis")
    pis = input(f"  {C.GREY}pis{C.RS}  ").strip()
    loading("validando", 0.6)
    print()
    if validar_pis(pis):
        ok(f"{pis}  {C.DIM}válido{C.RS}")
    else:
        err(f"{pis}  {C.DIM}inválido{C.RS}")
    pausar()

def act_validar_cartao():
    titulo("validar cartão")
    num = input(f"  {C.GREY}número{C.RS}  ").strip()
    loading("validando luhn", 0.6)
    print()
    if validar_cartao(num):
        ok(f"{num}  {C.DIM}válido{C.RS}")
    else:
        err(f"{num}  {C.DIM}inválido{C.RS}")
    pausar()

# ============ MAIN ============
ACOES = {
    "1": act_pessoa, "2": act_cpf, "3": act_rg, "4": act_cnh, "5": act_titulo,
    "6": act_pis, "7": act_certidao, "8": act_cnpj, "9": act_empresa, "10": act_veiculo,
    "11": act_placa, "12": act_renavam, "13": act_conta, "14": act_cartao, "15": act_ie,
    "16": act_cidades, "17": act_uf, "18": act_validar_cpf, "19": act_validar_cnpj,
    "20": act_validar_cnh, "21": act_validar_titulo, "22": act_validar_pis, "23": act_validar_cartao,
}

def main():
    while True:
        banner()
        menu()
        op = input(f"\n  {C.GREY}›{C.RS}  ").strip()
        if op == "0":
            titulo("até logo")
            print(f"  {C.DIM}dados fictícios · uso responsável.{C.RS}")
            time.sleep(0.5)
            break
        acao = ACOES.get(op)
        if acao:
            try:
                acao()
            except KeyboardInterrupt:
                warn("interrompido")
                pausar()
            except Exception as e:
                err(f"erro: {e}")
                pausar()
        else:
            err("opção inválida")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.DIM}  encerrado.{C.RS}")
