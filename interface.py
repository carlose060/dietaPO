import os
import re
import pandas as pd
from PDF import PDF
from po import PlDieta
from string import ascii_letters

class Inicio:

    def __init__(self):
        self.alimentos_selecionados = []
        self.restricoes = []
        self.df_taco = pd.read_excel('df_taco.xlsx')
        

    def tela_inicial(self):
        print('******************************************')
        print('********** Tabela de Alimentos ***********')
        print('******************************************')
        if self.alimentos_selecionados:
            [print(f"{idx} {al['Alimento']}") for idx, al in enumerate(self.alimentos_selecionados)]
        else:
            print('Nenhum alimento selecionado')
        print()
        print('0 - Selecionar Alimentos')
        print('1 - Proxima etapa')
        print('2 - Adicionar alimento na tabela')
        print('3 - Rodar com valores para teste')
        op = input('Digite a opção desejada: ')
        if op == '0':
            self.selecionar_alimentos()
        elif op == '1':
            # execute clear in the terminal
            os.system('clear')
            self.proxima_etapa()
        elif op == '2':
            # execute clear in the terminal
            os.system('clear')
            row = {colunas: (input(f'Digite o valor para {colunas}: ')) for colunas in self.df_taco.columns.tolist()}
            self.df_taco = pd.concat([self.df_taco, pd.DataFrame(row, index=[0])], ignore_index=True)
        elif op == '3':
            # execute clear in the terminal
            os.system('clear')
            self.definir_valores_iniciais()
            self.rodar_algoritmo()
        else:
            # clear terminal
            os.system('clear')
            print('Opção inválida')
            self.tela_inicial()

    
    def selecionar_alimentos(self):
        alimento = input('Digite o nome do alimentos que deseja buscar: ')
        alimentos = self.df_taco[self.df_taco['Alimento'].str.contains(alimento, case=False)]    

        if alimentos.empty:
            os.system('clear')
            print('Nenhum alimento encontrado')
            self.selecionar_alimentos()
        else:
            print('Alimentos encontrados:')
            [print(f"{idx} - {alimento['Alimento']}") for idx,alimento in enumerate(alimentos.iloc())] 
            op = input('Digite o número do alimento que deseja selecionar (ou qualquer letra para voltar): ')
            if op.isdigit() and int(op) < len(alimentos['Alimento'].tolist()):
                self.alimentos_selecionados.append(alimentos.iloc()[int(op)])
                self.selecionar_alimentos()
            else:
                self.tela_inicial()


    def proxima_etapa(self):     
        self.prot = float(input('Digite a quantidade proteinas: '))
        self.carbo = float(input('Digite a quantidade carboidratos: '))
        self.gord = float(input('Digite a quantidade gorduras: '))

        self.func = input('0. Para maximar a quantidade de calorias.\n1.Para minimizar a quantidade de calorias.\nDigite a opção desejada: ')
        os.system('clear')
        self.definir_proporcoes()

    def definir_proporcoes(self):
        print('******************************************')
        print('********** Alimentos selecionados ********')
        print('******************************************')
        [print(f"{x} - {y['Alimento']}") for x,y in zip(ascii_letters, self.alimentos_selecionados)]
        print()
        print('Escreva a propoção usando as letras respectivas aos alimentos (dica: Digite somente um caracter para sair)')
        print()
        expressao = input('Exemplo: 3a - b == 0\nEntre com a expressão: ')
        
        if len(expressao) == 1:
            self.rodar_algoritmo()
        else:
            expressao_list = re.split(r'\s*([><+=-]+|[a-zA-Z]+)\s*', expressao)
            self.restricoes.append(expressao_list)
            os.system('clear')
            self.definir_proporcoes()

    def rodar_algoritmo(self):
        micros = {key: 0 for key in self.alimentos_selecionados[0].keys().tolist()[4:]}
        dieta = PlDieta(self.func)
        dieta.definir_parametros(self.alimentos_selecionados,self.restricoes, self.prot, self.carbo, self.gord)
        status = dieta.rodar_pl()
        print(f'Status da solução: {status}')
        kcal, variaveis = dieta.receber_resultados()
        
        print(f'Valor ótimo: {kcal:.2f}')
        for v in variaveis:
            idx_alimento = int(v.name[1:])
            gramas = v.varValue
            for key in list(micros.keys()):
                micros[key] += (self.alimentos_selecionados[idx_alimento][key]*gramas)

            print(f'{self.alimentos_selecionados[idx_alimento]["Alimento"]} = {gramas:.2f}')
        d_recomendado = {}
        with open('valores_recomendados.txt', 'r') as f:
            for line in f.readlines():
                if len(line[:-1].split(' ')) == 2:
                    key, value = line[:-1].split(' ')
                else:
                    key, key2, value = line[:-1].split(' ')
                    key = f'{str(key)} {str(key2)}'
                d_recomendado[key] = float(value)
        pdf = PDF()
        pdf.relatorio(kcal, variaveis, self.alimentos_selecionados, micros, d_recomendado)
        pdf.relatorio_substituicao()
        pdf.output('relatorioDieta.pdf', 'F')
            
        
    def definir_valores_iniciais(self):
        values = ['whey', 0, 404, 0, 76, 6, 0, 13.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        row = {colunas: value for colunas, value in zip(self.df_taco.columns.tolist(),values)}
        self.df_taco = pd.concat([self.df_taco, pd.DataFrame(row, index=[0])], ignore_index=True)
        self.alimentos_selecionados = [
            self.df_taco.iloc[2],
            self.df_taco.iloc[6],
            self.df_taco.iloc[47],
            self.df_taco.iloc[109],
            self.df_taco.iloc[125],
            self.df_taco.iloc[181],
            self.df_taco.iloc[461],    
            self.df_taco.iloc[573],  
            self.df_taco.iloc[383],   
            self.df_taco.iloc[-1],   
            ]
        self.restricoes = [
           
            ['', 'a', '', '<=', '3'],
            ['', 'b', '', '<=', '0.5'],
            ['', 'c', '', '<=', '1'],
            ['', 'd', '', '<=', '1'],
            ['', 'e', '', '<=', '1.5'],
            ['', 'f', '', '<=', '2'],
            ['', 'g', '', '<=', '0.2'],
            ['', 'h', '', '<=', '2'],
            ['', 'i', '', '<=', '3'],
            ['', 'j', '', '==', '0.3'],
        
        ]
        self.prot = 137.6
        self.carbo = 413
        self.gord = 61.2
        self.func = '1'



                