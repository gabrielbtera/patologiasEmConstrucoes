# Patologias em Construções
## Análise das manifestações patológicas na Câmara de Vereadores Casa Anísio Galvão – Pesqueira - PE.
#### Auxiliei em um TCC de um graduando em engenharia civil pelo IFS de Alagoas, que tem o objetivo de usar a Matriz de Priorização de GUT e fazer uma análise difusa com a linguagem python integrada a uma planilha Excell como interface. E com isso, detectar o grau de prioridade de correções na estrutura física do prédio da câmara de vereadores de Pesqueira - PE, gerando gráficos que ajudem ao Engenheiro Civil tomar a melhor decisão.

## Como começar:

#### Já com o código na máquina e o python instalado. No terminal do windows, usa-se o gerenciador de pacotes pip e se faz as seguintes instalações:

 #### numpy:
```
py -m pip install --user numpy
```

 #### skfuzzy:
```
py -m pip install -U scikit-fuzzy
```

#### matplotlib:
```
py -m pip install -U matplotlib
```

#### pandas:
```
py -m pip install -U pandas
```

#### xlrd:
```
py -m pip install -U xlrd
```
#### openpyxl:
```
py -m pip install -U openpyxl
```

## Funcionamento inicial:

#### Após isso o preechimento dos campos G U T da planilha é necessário, os valores são inteiros de 1 a 5, fora deste intervalo a análise será comprometida. A as colunas E e F são os resultados da análise difusa feita após a execução do código.


![planilha](https://user-images.githubusercontent.com/53129406/132886320-8651f524-43b6-4dc8-b2c1-6bdd777b4fe2.PNG)

#
#### Depois de tudo pronto, é só criar só executar no terminal o seguinte comando:
 ```
 py menu-main.py
```
#### Por enquanto o menu no terminal será este, estamos trabalhando para uma futura aplicação web se quiser contribuir com o projeto é só me mandar um e-mail em [gabrielsdej@gmail.com](gabrielsdej@gmail.com).

![Capturar](https://user-images.githubusercontent.com/53129406/132902704-35e7a520-289f-4840-9c7b-107afaaa985a.PNG)

#### Passos para uma correta execução:

* Preencher a planilha.
* Executar o código.  `py menu-main.py`
* Selecionar uma das opções do menu e seguir as instruções.

### Opção 1 do menu:
* Pede o maior numero existente em algumas colunas G, U ou T. 
* Pede o nome do arquivo excell de saída, essa nova planilha terá o resultado da ordem de prioridade que vai de 1 a 6, do valor difuso e da prioridade difusa de cada problema estrutural. Decisões já podem ser tomadas a partir daqui.
#### Nova planilha:
 ![Capturar](https://user-images.githubusercontent.com/53129406/132905635-2ee8c961-77c2-444b-9251-8a83a0996a3a.PNG)


### Opção 2 do menu:
#### Esse menu executa a plotagem dos gráficos de cada linha da tabela de saída

###
Veja o menu abaixo:
#### 1 - Graficos das entradas e saida.
#### 2 - Graficos que a analise difusa chega a 2 conclusoes.
#### 3 - Todos os graficos
#### 4 - Selecione uma linha para plotar o grafico

#### exemplo de gráfico obtido este o de Bolhas na Pintura.png:

![Corrosão em Esquadrias](https://user-images.githubusercontent.com/53129406/132906393-9e155554-12a9-479d-a5fb-405a4a23da89.png)

#### cada arquivo gerado vem com o nome do problema no prédio:
![Capturar](https://user-images.githubusercontent.com/53129406/132907239-d5f280cf-ad03-4fc5-818b-3b4c11e2c93e.PNG)

### Opção 3 do menu:
#### Finaliza a operação.

### Opção 4 do menu:
#### Faz uma analise com três números em sequência separados por um espaço, por exemplo:

```
4 - Testar Out system
Digite a sua opcao: 4
Digite os numeros separados por um espaço: 3 1 2
```
# 
### O programa tem a capacidade de tomar uma decisão sobre a ordem de consertos de uma estrutura, ajudando um engenheiro civil a tomar as melhores decisão. Em breve o projeto será atualizado em uma aplicação web. 

