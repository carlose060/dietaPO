from datetime import datetime
from fpdf import FPDF

DIR_LOGO = 'imgs/ufsj.jpg'
DIR_TEXTS = 'texts/'

class PDF(FPDF):

    def __init__(self, orientation= 'P', unit= 'mm',format='A4'):
        super().__init__(orientation, unit,format)
        self.titulo     = 'Problema da dieta'
        self.header_footer = 'Trabalho pratico de Pesquisa Operacional para Computação- 2023.1 - UFSJ'

    def header(self):    
        self.image(DIR_LOGO, 5, 7, 15, 17, type='jpg')

        self.set_font('helvetica', 'B', 12)
        self.set_xy(20, 10)
        self.cell(w=0, txt=f"{self.header_footer}")
    

        self.set_font('helvetica', 'B', 12)
        self.set_xy(20, 16)
        self.cell(w=0, txt=f'Problema da Dieta')

        self.set_font('helvetica', 'B', 10)
        self.set_xy(20, 22)
        self.cell(w=0, txt=f"Carlos Eduardo da Silva")


        self.line(5, 26, 205, 26)

    def footer(self):

        self.line(5, 285, 205, 285)

        self.set_xy(5, -7)
        self.set_font('helvetica', 'I', 8)
        self.cell(w=0, txt=f"Emitido em {datetime.now().strftime('%d/%m/%Y')} {datetime.now().strftime('%H:%M')}")

        self.set_xy(60, -7)
        self.set_font('helvetica', 'I', 8)
        self.cell(w=0, txt=self.header_footer)
        
        self.set_xy(180, -7)
        self.set_font('helvetica', 'B', 8)
        self.alias_nb_pages()
        self.cell(w=0, txt='Página ' + str(self.page_no()) + ' de {nb}')


    def relatorio(self, kcal, variaveis, alimentos, valores_micros, recomendado):
        self.alimentos_selecionados = alimentos
        y_text = 35
        self.add_page()
        self.set_font('helvetica', 'B', 9) 
        self.set_xy(5, y_text)
        y_text += 6

        self.cell(w=0, txt=f'Lista de alimento da dieta')  
        self.set_xy(5, y_text)
        self.set_font('helvetica', 'I', 9)
        for v in variaveis:
            self.set_xy(10, y_text)
            idx_alimento = int(v.name[1:])
            gramas = v.varValue
            self.cell(w=0, txt=f'{round(gramas*100)}g de {self.alimentos_selecionados[idx_alimento]["Alimento"]}')
            y_text += 6
        
            if y_text  >= 275:
                self.add_page()
                y_text = 35

        self.line(5, y_text, 205, y_text)
        y_text += 6
        self.set_font('helvetica', 'B', 9) 
        self.set_xy(147, y_text)
        self.cell(w=0, txt=f"Total de calorias da Dieta = {round(kcal)}kcal")
        y_text += 10
        if y_text+99 >= 275:  
            self.add_page()
            y_text = 35
        self.set_xy(32, y_text)
        self.cell(w=0, txt=f"Valores de micronutrientes da dieta")
        self.set_xy(147, y_text)
        self.cell(w=0, txt=f"Valores de macronutrientes da dieta")
        y_text += 3

        self.line(10, y_text, 110, y_text)
        self.line(10, y_text+6, 110, y_text+6)
        self.line(10, y_text, 10, y_text+96)
        self.line(35, y_text, 35, y_text+96)
        self.line(60, y_text, 60, y_text+96)
        self.line(85, y_text, 85, y_text+96)
        self.line(110, y_text, 110, y_text+96)
        y_text += 3
        y_aux = y_text
        self.set_xy(10, y_text)
        self.cell(w=0, txt=f'Micros')
        self.set_xy(35, y_text)
        self.cell(w=0, txt=f'Valor na dieta')
        self.set_xy(60, y_text)
        self.cell(w=0, txt=f'Recomendado')
        self.set_xy(85, y_text)
        self.cell(w=0, txt=f'Deficiência')
        self.set_font('helvetica', 'I', 9)
        y_text += 6
        jump = 0     
        valores_micros.pop('Cinzas')
        valores_micros.pop('Colesterol (mg)')
        valores_micros.pop('RE(mcg)')
        valores_micros.pop('RAE (mcg)')
        for key,valor in valores_micros.items():
            if jump < 4:
                jump += 1        
                self.set_xy(150, y_aux)
                y_aux += 6
                self.cell(w=0, txt=f'{key} = {round(valor)}g')
            else:
                self.set_xy(10, y_text)
                self.cell(w=0, txt=f'{key}')
                self.set_xy(35, y_text)
                self.cell(w=0, txt=f'{valor:.2f}')
                self.set_xy(60, y_text)
                self.cell(w=0, txt=f'{recomendado[key]}')
                self.set_xy(85, y_text)
                self.cell(w=0, txt=f'{f"{recomendado[key]-valor:.2f}" if valor < recomendado[key] else "<= 0"}')
                y_text += 6
                self.line(10, y_text-3, 110, y_text-3)
                
                if y_text  >= 275:
                    self.add_page()
                    y_text = 35

    def relatorio_substituicao(self):
        y_text = 35
        self.add_page()

        self.set_font('helvetica', 'B', 9) 
        self.set_xy(5, y_text)
        self.cell(w=0, txt=f'Lista de substituição de alimentos') 
         
        y_text += 6
        self.set_xy(5, y_text)
        self.set_font('helvetica', 'I', 9)

        with open(f'{DIR_TEXTS}sub.txt', 'r') as f:
            for line in f.readlines():

                if line[:5] == 'Grupo':
                    self.set_font('helvetica', 'B', 9)  
                    self.set_xy(10, y_text)
                    self.cell(w=0, txt=line[:-1])
                    self.set_font('helvetica', 'I', 9)
                    y_text += 6
                else:
                    self.set_xy(15, y_text)
                    self.cell(w=0, txt=line[:-1])
                    y_text += 6

                if y_text  >= 275:
                    self.add_page()
                    y_text = 35
        

               
