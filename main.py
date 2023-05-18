import pandas as pd

# Lê a planilha "Tabela de Composição de Alimentos" do arquivo Excel da TACO
df_taco = pd.read_excel('Taco_4a_edicao_2011.xlsx')

# Retirar campos Tr por 0
df_taco = df_taco.replace('Tr', 0).replace('NA', 0)

# Retirar campos em branco por 0
df_taco = df_taco.fillna(0)

# Visualiza as primeiras linhas do dataframe
print(df_taco.head())

"""
" * " as análises estão sendo reavaliadas

Valores em branco nesta tabela: análises não solicitadas

Teores alcoólicos (g/100g): ¹ Cana, aguardente: 31,1 e ² Cerveja, pilsen: 3,6.

Abreviações: g: grama;
mg: micrograma; 
kcal: kilocaloria; 
kJ: kilojoule; 
mg:miligrama; 
NA: não aplicável; 
Tr: traço. Adotou-se traço nas seguintes situações: 
    a)valores de nutrientes arredondados para números que caiam entre 0 e 0,5; 
    b) valores de nutrientes arredondados para números com uma casa decimal que caiam entre 0 e 0,05; 
    c) valores de nutrientes arredondados para números com duas casas decimais que caiam entre 0 e 0,005 e; 
    d) valores abaixo dos limites de quantificação (29).

Limites de Quantificação: 
    a) composição centesimal: 0,1g/100g; 
    b) colesterol: 1mg/100g; 
    c) Cu, Fe, Mn, e Zn: 0,001mg/100g; 
    d) Ca, Na: 0,04mg/100g; 
    e) K e P: 0,001mg/100g; 
    f) Mg 0,015mg/100g; 
    g) tiamina, riboflavina e piridoxina: 0,03mg/100g; 
    h) niacina e vitamina C: 1mg/100g; 
    i) retinol em produtos cárneos e outros: 3μg/100g e; 
    j) retinol em lácteos: 20μg/100g.

Valores correspondentes à somatória do resultado analítico do retinol mais o valor calculado com base no teor de 
carotenóides segundo o livro Fontes brasileiras de carotenóides: tabela brasileira de composição de carotenóides em alimentos.

Valores retirados do livro Fontes brasileiras de carotenóides: tabela brasileira de composição de carotenóides em alimentos.

"""