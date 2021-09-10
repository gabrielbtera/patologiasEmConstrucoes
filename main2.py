import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

import matplotlib.pyplot as plt
import pandas as pd


def ler_planilha(nome):
    """faz a leitura do arquivo excell e retorna a planilha"""
    xl = pd.ExcelFile("ferramenta-gut.xlsx")
    planilha = xl.parse(nome)
    return planilha


planilha = ler_planilha("Planilha1")


def universo():
    """Retorna o conjunto universo"""
    return planilha["G X U X T"].max() + 1


def retorna_lista_de_planilha(nome_planilha, coluna):
    """Esta funcao retorna uma lista de coluna pertencente a uma planilha"""
    return ler_planilha(nome_planilha)[coluna].values[::-1]



# -----------------------------------------------------------------------

# Variaveis universo do problema
gravidade = ctrl.Antecedent(np.arange(1, 6, 1), "gravidade")
urgencia = ctrl.Antecedent(np.arange(1, 6, 1), "urgencia")
tendencia = ctrl.Antecedent(np.arange(1, 6, 1), "tendencia")
saida = ctrl.Consequent(np.arange(1, 6, 1), "saida")

# atribuindo variaveis difusas
gravidade.automf(names= retorna_lista_de_planilha("Plan2", "Gravidade"))
urgencia.automf(names= retorna_lista_de_planilha("Plan2", "Urgência"))
tendencia.automf(names= retorna_lista_de_planilha("Plan2", "Tendência"))
saida.automf(names= ['Muito pouco', 'Pouco', 'Meio', "Muito", "Extremamente"]) 

# ------------------------------------------------------------------------------



def regras(g, u , t):

    """ esta função gera as regras e retorna uma lista delas
    """
    regras = []
    if g >= u and g >= t:

        regra1 = ctrl.Rule(gravidade["Extremante grave"] | urgencia["Precisa de ação"] & tendencia["Irá piorar rapidamente"], saida["Extremamente"])
        regra2 = ctrl.Rule(gravidade["Muito grave"] | urgencia["É urgente"] & tendencia["Irá piorar em pouco tempo"], saida["Muito"])
        regra3 = ctrl.Rule(gravidade["Grave"] | urgencia["O mais rápido possível"] & tendencia["Irá piorar"], saida["Meio"])
        regra4 = ctrl.Rule(gravidade["Pouco grave"] | urgencia["Pouco urgente"] & tendencia["Irá piorar a longo prazo"], saida["Pouco"])
        regra5 = ctrl.Rule(gravidade["Sem gravidade"] | urgencia["Pode esperar"] & tendencia["Não irá mudar"], saida["Muito pouco"])
        regras = [regra1, regra2, regra3, regra4, regra5]

    if u >= g and u >= t:
        regra1 = ctrl.Rule(urgencia["Precisa de ação"] | gravidade["Extremante grave"] & tendencia["Irá piorar rapidamente"], saida["Extremamente"])
        regra2 = ctrl.Rule(urgencia["É urgente"] | gravidade["Muito grave"] & tendencia["Irá piorar em pouco tempo"], saida["Muito"])
        regra3 = ctrl.Rule(urgencia["O mais rápido possível"] | gravidade["Grave"] & tendencia["Irá piorar"], saida["Meio"])
        regra4 = ctrl.Rule(urgencia["Pouco urgente"] | gravidade["Pouco grave"] & tendencia["Irá piorar a longo prazo"], saida["Pouco"])
        regra5 = ctrl.Rule(urgencia["Pode esperar"] | gravidade["Sem gravidade"] & tendencia["Não irá mudar"], saida["Muito pouco"])
        regras = [regra1, regra2, regra3, regra4, regra5]

    if t >= g and t >= u:
        regra1 = ctrl.Rule(tendencia["Irá piorar rapidamente"] | gravidade["Extremante grave"] & urgencia["Precisa de ação"] , saida["Extremamente"])
        regra2 = ctrl.Rule(tendencia["Irá piorar em pouco tempo"] | gravidade["Muito grave"] &  urgencia["É urgente"], saida["Muito"])
        regra3 = ctrl.Rule(tendencia["Irá piorar"] | gravidade["Grave"] & urgencia["O mais rápido possível"], saida["Meio"])
        regra4 = ctrl.Rule(tendencia["Irá piorar a longo prazo"] | gravidade["Pouco grave"] & urgencia["Pouco urgente"], saida["Pouco"])
        regra5 = ctrl.Rule(tendencia["Não irá mudar"] | gravidade["Sem gravidade"] & urgencia["Pode esperar"] , saida["Muito pouco"])
        regras = [regra1, regra2, regra3, regra4, regra5]
    return regras


def out_system(g, u,  t ):
    """
    Esta função recebe os parametros do metodo gut e retorna
    o numero gerado de acordo com as regras da função regras()
    """

    # instanciando o controle do sitema
    variavel_ctrl = ctrl.ControlSystem(regras(g , u, t))
    variavel_simulador = ctrl.ControlSystemSimulation(variavel_ctrl)

    variavel_simulador.input["gravidade"] = g
    variavel_simulador.input["urgencia"] = u
    variavel_simulador.input["tendencia"] = t

    variavel_simulador.compute()
    

    return variavel_simulador.output["saida"]



def analise_difusa():
    """
    Esta função faz a operação da analise difusa em todos os itens da planilha

    """

    g = list(planilha["G"][1:])
    u = list(planilha["U"][1:])
    t = list(planilha["T"][1:])

    lista = []
    for i in range(len(g)):
        lista.append(out_system(g[i], u[i], t[i]))


    return lista



def seta_valores_difusos(valor , intervalo = 3):
    """
    esta função trasforma os valores difusos em ordem de prioridade que está
    delimitada pelo, parametro intervalo
    """
    check = list()
    
    if int(valor) - valor == 0:
        lista = []
        for i in range(intervalo):
            lista.append("prioridade "+ str((i + 1)))

        return [lista[::-1][int(valor) -1]]

    else :
        temp = "prioridade "

        def fconc(intervalo, valor = 0):
            """Esta funcao faz um concatenação das prioridades"""
            return temp + str(intervalo + valor)
        
        numeros = [1.5, 2.5, 3.5, 4.5]

        cont = 1
        for i in numeros:

            if i < intervalo:
                if int(i) == int(valor):
                    if valor > i:
                        check.append(fconc(intervalo, - cont))
                        
                    
                    if valor == i:
                        check.append(fconc(intervalo, -cont))
                        check.append(fconc(intervalo, -(cont-1)))
                        
                        
                    
                    if valor < i and int(i) == 1:
                        check.append(fconc(intervalo))
                    
                    elif valor < i:
                        check.append(fconc(intervalo, - (cont - 1)))
            
            cont += 1
        
        return check


def formata_proridade(valor, intervalo = 3):

    """
    esta função retorna a string formada pela lista de prioridade
    para escrever no arquivo excell
    """
    lista = seta_valores_difusos(valor, intervalo)
    
    if len(lista) == 1:
        return lista[0]

    elif len(lista) > 1:

        string = ""
        flag = 1

        for i in lista:

            if flag % 2 != 0:
                string += i + " e "
            else:
                string += i

            flag +=1

        return string


def escreve_prioridades(intervalo=3):

    lista_prioridades = [formata_proridade(valor, intervalo) for valor in analise_difusa()]

    serie = pd.Series([float("nan")] + lista_prioridades, name="vals2")

    return serie, lista_prioridades

