import random as rd
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.utils import ImageReader


class Jogo:
    def __init__(self):
        self.lcm = ["peão", "bispo", "cavalo", "torre","rainha", "rei"]
        self.peao = {"PV":(3,5), "FA":(5,8), "FD":(5,8), "quant_habilidades":(0,1), "critico":(6)}
        self.bispo = {"PV":(5,10), "FA":(9,12), "FD":(9,12), "quant_habilidades":(1,1), "critico":(6)}
        self.cavalo = {"PV":(10,15), "FA":(9,12), "FD":(9,12), "quant_habilidades":(1,2), "critico":(6)}
        self.torre = {"PV":(15,20), "FA":(12,15), "FD":(12,15), "quant_habilidades":(1,1), "critico":(5,6)}
        self.rainha = {"PV":(20,25), "FA":(13,17), "FD":(13,17),"quant_habilidades":(1,2), "critico":(5,6)}
        self.rei = {"PV":(25,30), "FA":(13,17), "FD":(13,17), "quant_habilidades":(1,3), "critico":(4,5,6)}
        self.dgh = self.habilidadesjson("habilidades")
        self.caracteristicas = self.caracteristicasjson()
        self.temperos = self.temperosjson()
    def habilidadesjson(self, anome):
        with open(f"{anome}.json", "r", encoding="utf-8") as arquivo:
            habilidades = json.load(arquivo)
            return habilidades  
    def temperosjson(self):
        with open(f"temperos.json", "r", encoding="utf-8") as arquivo:
            temperos = json.load(arquivo)
            return temperos
    def gerar_ficha_pdf(self, classe, pv, fa, fd, desl, critico, habilidades):
        nome_arquivo = f"ficha_{classe}_{datetime.now().strftime('%H%M%S')}.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=landscape(A5))
        largura, altura = landscape(A5)

        # Fundo
        fundo = ImageReader("ficha.png")  # use o novo fundo que você mandou
        c.drawImage(fundo, 0, 0, width=largura, height=altura)

        # Fonte principal
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0, 0, 0)

       
        c.drawString(95, altura - 80, f"Classe: {classe}")
        c.drawString(360, altura - 80, f"Crítico: {critico}")

        
        c.setFont("Helvetica", 11)
        c.drawString(60, altura - 125, f"FA:{fa}")     # FA
        c.drawString(130, altura - 125, f"FD:{fd}")    # FD
        c.drawString(200, altura - 125, f"PV:{pv}")    # PV
        c.drawString(290, altura - 125, f"Deslc: {desl}")  # Deslc

        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, altura - 180, "Habilidades:")

        y = altura - 195
        c.setFont("Helvetica", 9)

        for nome, desc in habilidades.items():
            if y < 100:
                c.showPage()
                y = altura - 60
                c.setFont("Helvetica", 9)
            c.drawString(50, y, f"- {nome}:")
            y -= 12
            for linha in desc.split("\n"):
                c.drawString(60, y, linha.strip())
                y -= 11

       
        c.setFont("Helvetica-Bold", 12)
        y -= 20
        c.drawString(40, y, "Descrição:")
        y -= 15
        c.setFont("Helvetica", 9)
        for nome, desc in habilidades.items():
            for linha in desc.split("\n"):
                if y < 60:
                    c.showPage()
                    y = altura - 60
                c.drawString(60, y, linha.strip())
                y -= 11

        c.save()
        print(f"✅ PDF gerado com sucesso: {nome_arquivo}")

    def encontros_aleatorios(self):
        lista_encontros_aleatorios = [
        "Uma ameaça a espreita ",
        "Um perigo forte demais para lutar",
        "Um presságio!",                                                        
        "Um susto",
        "Algo bom!",
        "emboscada!",
        "Um pedido de ajuda",
        "Algo engraçado",
        "Patrulha inimiga!",
        "Uma batalha distante",
        "Um aliado inesperado",
        "Uma oportunidade arriscada",
        "Uma visão do passado",
        "Uma inconveniência",
        "Uma pista",
        "Uma peregrinação",
        "Rituais!",
        "Um mercador Viajante",
        "Cena de Fuga!",
        "Traição!",
        "Azar nos equipamentos"
        ]
        resp = rd.choice(lista_encontros_aleatorios)
        return resp
    def invocar(self, aclasse):
        classe = aclasse.lower()
        dados = getattr(self, classe)
        pv = rd.randint(*dados["PV"])
        fa = rd.randint(*dados["FA"])
        fd = rd.randint(*dados["FD"])
        desl = rd.randint(2,5)
        critico = dados["critico"]
        habilidades = {}
        quant = rd.randint(*dados["quant_habilidades"])
        chaves_possiveis = list(self.dgh.keys())
        if quant > 0 and chaves_possiveis:
            chaves_escolhidas = rd.sample(chaves_possiveis, min(quant, len(chaves_possiveis)))
            for chave in chaves_escolhidas:
                habilidades[chave] = self.dgh[chave]
        else:
            habilidades["Sem Habilidades"] = "   "
        descricao = ""
        for nome, desc in habilidades.items():
            descricao += f"\n      - {nome}:\n         {desc}"

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
        log_texto = f"[{agora}] [INVOCADO] {classe.capitalize()} | PV: {pv} | FA: {fa} | FD: {fd} | Crítico: {critico} | Habilidades: {', '.join(habilidades.keys())}\n"
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(log_texto)

        self.gerar_ficha_pdf(classe.capitalize(), pv, fa, fd, desl, critico, habilidades)
        resp = f'''
        ============== Invocando Monstro ================== 
        Classe: {classe.capitalize()} 
        PV: {pv} | FA: {fa} | FD: {fd} | Crítico: {critico} | Desl.{desl}:
        Habilidades: {", ".join(habilidades.keys()) if habilidades else "Nenhuma"}
        Descrição:{descricao}
        '''
        return resp.strip()
    def encontro(self, ahostilidade=0):
        hostilidade = ahostilidade
        d1 = rd.randint(1,6)
        d2 = rd.randint(1,6)
        valor = d1+d2+hostilidade
        if valor < 2:
            valor = 2
        if valor > 17:
            valor = 17
        lista_encontros_grupal = [
    "1d6+2 peões",                              
    "Bispo + 1d6 peões",                        
    "Cavalo + 1d6 peões",                       
    "Bispo + Cavalo + 1d6 peões",               
    "1 Torre",                                  
    "Torre + 1d6 peões",                        
    "Torre + Cavalo + 1d6 peões",               
    "Torre + Bispo + 1d6 peões",                
    "2 Torres",                                 
    "Rainha",                                   
    "Rainha + 1d6 peões",                       
    "Rainha + 1d3 (Bispo/Cavalo)",              
    "Rainha + 1d3 (Torre)",                     
    "Rei",                                      
    "Rei + 1d3 (Bispo/Cavalo)",                 
    "Rei + 1d3 (Torre ou Rainha)",              
        ]
        resultado = lista_encontros_grupal[valor-2]
        if "peões" in resultado:
            print(self.invocar("peao"))
        if "Cavalo" in "resultado":
            print(self.invocar("cavalo"))
        if "Bispo" in "resultado":
            print(self.invocar("bispo"))
        if "Torre" in "resultado":
            print(self.invocar("torre"))
        if "Rainha" in "resultado":
            print(self.invocar("rainha"))
        if "Rei" in "resultado":
            print(self.invocar("rei"))

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_texto = f"[{agora}] [ENCONTRO] D1: {d1} | D2: {d2} | Hostilidade: {ahostilidade} => {resultado}\n"


        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(log_texto)

        return resultado
    def caracteristicasjson(self):
        with open(f"caracteristicas.json", "r", encoding="utf-8") as arquivo:
            caracteristicas = json.load(arquivo)
            return caracteristicas
    def tipo_aleatorio(self):
        dados = self.caracteristicas
        tipo = rd.choice(dados["tipos"])
        return tipo
    def tipo_atributo(self):
        dados = self.caracteristicas
        tipo = rd.choice(dados["atributo"])
        return tipo
    def tipos_kemono(self):
        dados = self.caracteristicas
        tipo = rd.choice(dados["tipos_kemono"])
        return tipo
    def tipo_implantes(self):
        dados = self.caracteristicas
        tipo = rd.choice(dados["implantes"])
        return tipo
    def gerar_temperos(self):
        dados = self.temperosjson()           
        lista = dados["temperos"]              
        parte1 = rd.choice(lista)['parte1']
        parte2 = rd.choice(lista)['parte2']
        return f"Tempero: {parte1} | {parte2}"
    def run(self):
        print("="*40)
        resultado = int(input('''
        ! Bem vindo ! \n
[1]: Sortear um encontro Grupal 
[2]: Sortear monstro 
[3]: Tipo de Monstro 
[4]: Atributo 
[5]: Tipos Kemono 
[6]: Implantes 
[7]: Temperos
[8]: Encontros Aleatórios
======================================
Escolha: '''))
        if resultado == 1:
            print("="*40)
            hostilidade = int(input("Qual a hostilidade?: "))
            print(self.encontro(hostilidade))
            print("="*40)
        if resultado == 2:
            pecas = ["peao", "bispo", "cavalo", "torre","rainha", "rei"]
            print("="*40)
            result = int(input('''
[1]: Peão [2]: Bispo
[3]: Cavalo [4]: Torre
[5]: Rainha [6]: Rei
Escolha: '''))
            print("="*40)
            print(self.invocar(pecas[result-1]))
            print("="*40)
        if resultado == 3:
            print("="*40)
            print(f"O tipo é: {self.tipo_aleatorio()}")
            print("="*40)
        if resultado == 4:
            print("="*40)
            print(f"O atributo é: {self.tipo_atributo()}")
            print("="*40)
        if resultado == 5:
            print("="*40)
            print(f"O tipos kemono é: {self.tipos_kemono()}")
            print("="*40)
        if resultado == 6:
            print("="*40)
            print(f"O implantes é: {self.tipo_implantes()}")
            print("="*40)
        if resultado == 7:
            print("="*40)
            print(f"{self.gerar_temperos()}")
            print("="*40)
        if resultado == 8:
            print("="*40)
            print(f"{self.encontros_aleatorios()}")
            print("="*40)


        





p = Jogo()
p.run()
