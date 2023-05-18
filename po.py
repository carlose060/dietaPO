import pulp
import pandas as pd

class PlDieta():
    lista = [int, int, int]
    df = pd.DataFrame
    def __init__(
            self,
            df_selecionados_taco: df,
            # [ Alimento 1, Alimento 2, proporção do alimento 1 em relação ao 2 ]
            restricoes: lista, 
            prot: int, 
            carbo: int, 
            gord: int, 
            func: str
        ):
        if func == '0':
            self.problem = pulp.LpProblem('Dieta', pulp.LpMaximize)
        else:
            self.problem = pulp.LpProblem('Dieta', pulp.LpMinimize)

        # Count how len row has in df_taco
        self.variaveis = [pulp.LpVariable(f"x{i}", 0, None, pulp.LpContinuous) for i in range(len(df_selecionados_taco))]
        
        self.problem += pulp.lpSum([alimento*var for var, alimento in zip(self.variaveis, df_selecionados_taco['Energia (kcal)'])])
        
        
        self.problem += pulp.lpDot(df_selecionados_taco['Proteína'], self.variaveis) == prot
        self.problem += pulp.lpDot(df_selecionados_taco['Carboidrato'], self.variaveis) == carbo
        self.problem += pulp.lpDot(df_selecionados_taco['Lipídeos'], self.variaveis) == gord

        for restricao in restricoes:
            self.problem += restricao[2]*self.variaveis[restricao[0]] - self.variaveis[restricao[1]] == 0
