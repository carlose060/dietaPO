import os
import pandas as pd
from po import PlDieta

class Inicio:

    def __init__(self):

        self.alimentos_selecionados = []
        self.restricoes = []
        self.df_taco = pd.read_excel('Taco_4a_edicao_2011.xlsx')
        # Retirar campos Tr, NA e valores em branco por 0
        self.df_taco = self.df_taco.replace('Tr', 0).replace('NA', 0).fillna(0)
    
    def get_alimentos(self):
        return self.df_taco['Alimento'].tolist()
    
 
    def get_macro_alimentos_selecionados_df(self):
        # Select two columns in Serie frame
        if self.alimentos_selecionados:
            return self.df_taco[self.df_taco['Alimento'].isin(self.alimentos_selecionados)][['Energia (kcal)', 'Proteína', 'Carboidrato', 'Lipídeos']]
        else:
            return 'Nenhum alimento selecionado'
    
    def selecionar_alimentos(self):
        alimento = input('Digite o nome do alimentos que deseja buscar: ')
        # mount the regex for alimento
        alimento = alimento.replace(' ', '.*')  
        # select the alimento
        # Query the df_taco with the regex
        alimentos = self.df_taco[self.df_taco['Alimento'].str.contains(alimento, case=False)]
        
        #alimentos = self.df_taco[self.df_taco['Alimento'].str.contains(alimento, case=False)]['Alimento'].tolist()
        
        if alimentos.empty:
            os.system('clear')
            print('Nenhum alimento encontrado')
            self.selecionar_alimentos()
        else:
            print('Alimentos encontrados:')
            #for alimento in alimentos.iloc():
            #    print(f"{alimento['id']} - {alimento['Alimento']}")
            [print(f"{alimento['id']} - {alimento['Alimento']}") for alimento in alimentos.iloc()] 
            op = input('Digite o número do alimento que deseja selecionar (ou qualquer letra para voltar): ')
            if op.isdigit() and int(op) in alimentos['id'].tolist():
                self.alimentos_selecionados.append(alimentos[alimentos['id'] == int(op)])

                self.selecionar_alimentos()
            else:
                self.tela_inicial()
        
    def proxima_etapa(self):
        
        self.prot = input('Digite a quantidade proteinas: ')
        self.carbo = input('Digite a quantidade carboidratos: ')
        self.gord = input('Digite a quantidade gorduras: ')
        self.func = input('0. Para maximar a quantidade de calorias\n1.Para minimizar a quantidade de calorias \nDigite a opção desejada:')
        os.system('clear')
        self.definir_proporcoes()
              
    def rodar_algoritmo(self):
        PlDieta(self.get_macro_alimentos_selecionados_df(), self.restricoes, self.prot, self.carbo, self.gord, self.func)

    def definir_proporcoes(self):
        print('******************************************')
        print('********** Alimentos selecionados ********')
        print('******************************************')
        [print(x, y['Alimento']) for x,y in enumerate(self.alimentos_selecionados)]
        print()
        print('Digite 0 nas 3 opções para finalizar')
        print('Selecione as proporcões dos alimentos pela sua id')
        alimento1 = input('digite a id do primeiro alimento: ')
        proporcao = input('digite a proporção do primeiro alimento em relação ao segundo alimento: ')
        alimento2 = input('digite a id do segundo alimento: ')
        # Selecionar o campo alimento com o campo id
        if alimento1 == '0' and alimento2 == '0' and proporcao == '0':
            self.rodar_algoritmo()
        else:
            nome_alimento1 = self.df_taco[self.df_taco['id'] == int(alimento1)]['Alimento'].tolist()[0]
            nome_alimento2 = self.df_taco[self.df_taco['id'] == int(alimento2)]['Alimento'].tolist()[0]
            self.restricoes.append([int(alimento1), int(alimento2), int(proporcao)])
            os.system('clear')
            print(f'{proporcao}*{nome_alimento1} = {nome_alimento2}')
            print()
            self.definir_proporcoes() 

    def tela_inicial(self):
        print('******************************************')
        print('********** Tabela de Alimentos ***********')
        print('******************************************')
        if self.alimentos_selecionados:
            [print(f"{al['id']} {al['Alimento']}") for al in self.alimentos_selecionados]
        else:
            print('Nenhum alimento selecionado')
        print()
        print('0 - Selecionar Alimentos')
        print('1 - Proxima etapa')
        op = input('Digite a opção desejada: ')
        if op == '0':
            self.selecionar_alimentos()
        elif op == '1':
            # execute clear in the terminal
            os.system('clear')
            self.proxima_etapa()
        else:
            # clear terminal
            os.system('clear')
            print('Opção inválida')
            self.tela_inicial()

if __name__ == '__main__':
    inicio = Inicio()
    inicio.tela_inicial()


                