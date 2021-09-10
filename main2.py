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


