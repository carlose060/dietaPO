from string import ascii_letters
from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize
from pulp import LpContinuous, lpSum, lpDot, value

def isdigit(x):
        try:
            float(x)
            return True
        except:
            return x.isdigit()
        
class PlDieta():
    def __init__(self, func: str):
        self. func = func
        if func == '0':
            self.problem = LpProblem('Dieta', LpMaximize)
        else:
            self.problem = LpProblem('Dieta', LpMinimize)

       
    def definir_parametros(self,alimentos_select, restricoes, prot, carbo, gord):
        self.variaveis = [LpVariable(f"x{i}", 0, None, LpContinuous) for i in range(len(alimentos_select))]
        
        self.problem += lpSum([alimento['Energia (kcal)']*var for var, alimento in zip(self.variaveis, alimentos_select)])

        if self.func == '0': 
            self.problem += lpDot([s['Proteína']for s in alimentos_select], self.variaveis) <= (prot + prot*0.1)
            self.problem += lpDot([s['Carboidrato'] for s in alimentos_select], self.variaveis) <= (carbo + carbo*0.1)
            self.problem += lpDot([s['Lipídeos'] for s in alimentos_select], self.variaveis) <= (gord + gord*0.1)
        else:
            self.problem += lpDot([s['Proteína']for s in alimentos_select], self.variaveis) >= (prot - prot*0.1)
            self.problem += lpDot([s['Carboidrato'] for s in alimentos_select], self.variaveis) >= (carbo - carbo*0.1)
            self.problem += lpDot([s['Lipídeos'] for s in alimentos_select], self.variaveis) >= (gord - gord*0.1)

        dict_idx = {letras: idx for idx, letras in enumerate(ascii_letters)}
        for restricao in restricoes:
            coef = []
            var = []
            operador = ''
            constante = ''
            for i in range(len(restricao)):
                if restricao[i] in list(dict_idx.keys()) and not restricao[i] == '':
                    if i == 0:
                        coef.append(1)
                    elif isdigit(restricao[i-1]):
                        try:
                            if restricao[i-2] == '-':
                                coef.append(-float(restricao[i-1]))
                            else:
                                coef.append(float(restricao[i-1]))
                        except:
                            coef.append(float(restricao[i-1]))
                    else:
                        if restricao[i-1] == '':
                            try:
                                if restricao[i-2] == '-':
                                    coef.append(-1)
                                else:
                                    coef.append(1)
                            except:
                                coef.append(1)
                        else:
                            coef.append(1)
                    var.append(self.variaveis[dict_idx[restricao[i]]])
                elif restricao[i] in ['>', '<', '=', '==', '>=', '<='] and not restricao[i] == '':
                    operador = restricao[i]
                    constante = restricao[i+1]
                    break
            if operador == '>':
                self.problem += lpDot(coef, var) > float(constante)
            elif operador == '<':
                self.problem += lpDot(coef, var) < float(constante)
            elif operador == '=' or operador == '==':
                self.problem += lpDot(coef, var) == float(constante)
            elif operador == '>=':
                self.problem += lpDot(coef, var) >= float(constante)
            elif operador == '<=':
                self.problem += lpDot(coef, var) <= float(constante)
    
    def rodar_pl(self):
        """
        LpStatusOptimal (valor: 1): Indica que a solução ótima foi encontrada.
        LpStatusInfeasible (valor: -1): Indica que o problema é inviável.
        LpStatusUnbounded (valor: -2): Indica que o problema é ilimitado.
        LpStatusUndefined (valor: 0): Indica que o status da solução é indefinido. Isso pode ocorrer em casos excepcionais ou quando a solução não é alcançada devido a problemas numéricos.
        """
        status = self.problem.solve()
        return status

    def receber_resultados(self):
        return  value(self.problem.objective), self.problem.variables()
    