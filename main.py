import numpy as np

import skfuzzy as fuzz

from skfuzzy import control as ctrl

import matplotlib.pyplot as plt

import pandas as pd

from openpyxl import load_workbook


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


def gera_valores_e_graficos_das_entradas_e_saida():
    """
    esta função gera os valores das variaveis para a analise difusa
    ela retorna um dicionario como {"nome da variavel": variavel}:
    {"gravidade" : gravidade, "urgencia" : urgencia, "tendencia": tendencia, "saida" : saida}
    """

    # Variaveis do problema
    gravidade = ctrl.Antecedent(np.arange(1, 6, 1), "gravidade")
    urgencia = ctrl.Antecedent(np.arange(1, 6, 1), "urgencia")
    tendencia = ctrl.Antecedent(np.arange(1, 6, 1), "tendencia")
    saida = ctrl.Consequent(np.arange(1, 6, 1), "saida")

    # Formação do grafico das variaveis de entrada
    gravidade.automf(names=retorna_lista_de_planilha("Plan2", "Gravidade"))
    urgencia.automf(names=retorna_lista_de_planilha("Plan2", "Urgência"))
    tendencia.automf(names=retorna_lista_de_planilha("Plan2", "Tendência"))

    # formação do grafico da saida
    saida.automf(names=['Muito pouco', 'Pouco',
                        'Meio', 'Muito', 'Extremamente'])

    dicionario = {"gravidade": gravidade, "urgencia": urgencia,
                  "tendencia": tendencia, "saida": saida}

    return dicionario


