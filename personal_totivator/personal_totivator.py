from datetime import datetime, timedelta, date
import re
from google.colab import drive
import ast

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

#############
## Funções ##
#############

def tratamento_caracteres(texto_list):      
  """
  Função:
    - Retira os espaços por '_';
    - Substitúi caracteres especiais;
    - Remove espaços em branco do final;
  """

  #Lista que será substituída
  lista_replace = [ (' ', '_'),
                  (r'à|á|ã', 'a'),
                  (r'ç', 'c'),
                  (r'õ|ó|ò', 'o'),
                  (r'é|ê', 'e'),
                  (r'í|ì', 'i'),
                  (r'ú|ù', 'u')]
  res = []

  if isinstance(texto_list, str):
    texto = texto_list.lower()

    for termo in lista_replace:
      texto = re.sub(termo[0], termo[1], texto)
    
    #Removendo último caracterte em branco
    try:
      while texto[-1] == '_':
        texto = texto[0:-1]
    except:
      pass
    res = texto

  else:

    for texto in texto_list:
      texto = texto.lower()

      for termo in lista_replace:
        texto = re.sub(termo[0], termo[1], texto)

      try:
        while texto[-1] == '_':
          texto = texto[0:-1]
      except:
        pass

      res.append(texto)
  return res

def questionator_validator(questionamento, value_type = None, exp_values = []):           

  if len(exp_values) == 0:
    while True:  
      value = input(questionamento)       
      try:
        value = value_type(value)
        break
      except:
        print("\n BROOO não te pedi isso, tente de novo! Beijos \n ")
        pass
  else:
    while True:  
      value = tratamento_caracteres(input(questionamento)) 
      if value in exp_values:
        break
      else:
        print("\n BROOO não te pedi isso, tente de novo! Beijos \n ")
        pass


  return value  

class personal_totivator:



  def __init__(self,
      atividades_log = None,
      read_from_drive = False,
      drive_path = None,
      drive_filename = None):
    
    self.today = date.today().strftime("%Y-%m-%d")    
    self.drive_path = drive_path
    self.drive_filename = drive_filename 
    

    ###################
    ## Setup Inicial ##
    ###################

    print("####################################\n Bem vindo ao seu personal totivator \n####################################")
    print('Hoje é dia', self.today, '\n\n')

    if read_from_drive:
      drive.mount('/content/drive')
      # open existing text file
      with open(self.drive_path + self.drive_filename + '.json') as f:
        minhas_atividades = f.read()
        minhas_atividades = ast.literal_eval(minhas_atividades)
        self.minhas_atividades = minhas_atividades['self.minhas_atividades']
        self.log_atividades = minhas_atividades['self.log_atividades']
        atividades_log = False
      self.color_palette = sns.color_palette("Set1", n_colors=len(self.minhas_atividades), desat=.5)

    
    if atividades_log is None:      
      self.minhas_atividades = {}
      self.log_atividades = None
      self.cadastrar_novas_atividades()
    else:
      #self.minhas_atividades = atividades_log
      pass
    

  def cadastrar_novas_atividades(self):

    if len(self.minhas_atividades) == 0:
      self.minhas_atividades = {}

    quantidade_de_atividades = questionator_validator('### Quantas atividades gostaria de cadastrar? \n', int)
    print(" \n### Agora me fala quais são essas atividades?\n")
    for i in range(0, quantidade_de_atividades):        
      atividade = questionator_validator("Qual seria a atividade número " + str(i + 1) + "? \n", str)
      tempo_min = questionator_validator("E quanto tempo(em minutos) por pretende atuar nela diáriamente? \n", float)
      self.minhas_atividades[atividade] = {'tempo_min': tempo_min,
                                            'data_cadastro': self.today}

  def cadastrar_log(self):
    """
    """
    
    if self.log_atividades is None:
      self.log_atividades = {}
      self.log_atividades[self.today] = {}
      print("####################################\n Identificamos que você não possui nenhum Log de atividades ainda...")

    try:
      self.log_atividades[self.today]
      print("\n####################################################################\nHoje, dia " +
            self.today +
            ", você já atuou nas seguintes atividades \n")
      
      for atividade in self.log_atividades[self.today]:
        atuacao = self.log_atividades[self.today][atividade]

        print('\nAtividade:##########\n', atividade)
        print('Atuação:##########\n', atuacao)
      
      atualizar = questionator_validator('##############################\nGostaria de atualizar suas atuações?(Sim ou Não)\n', 
                                         exp_values = ['sim', 'nao'])

      if atualizar == 'sim':
        for atividade in self.log_atividades[self.today]:
          print('#############################')
          print('Bora atualizar a atividade:')
          atuacao = self.log_atividades[self.today][atividade]
          meta = self.minhas_atividades[atividade]['tempo_min']
          print(atividade,'que já foram realizados', atuacao, 'minutos de', meta, 'estipulados!')

          tempo_hoje = questionator_validator('\n#### Quantos minutos foram realizados nessa atividade hoje?\n', float)
          self.log_atividades[self.today][atividade] = atuacao + tempo_hoje
    
    except:      
      self.log_atividades[self.today] = {}
      print("\n######################################\nAeee, primeiro cadastro de atividade do dia " +
            self.today +
            ", parabéns!")

      for i in self.minhas_atividades:
        atividades = i
        meta = self.minhas_atividades[i]['tempo_min'] 
        print('\nPara a atividade:############\n' + atividades + '\nvocê indicou que atuaria:#############\n' + str(meta) + ' minutos diários...'  )
        tempo_hoje = questionator_validator('\n####\nQuantos minutos foram realizados da atividade ' + atividades + ' hoje?\n', float)
        self.log_atividades[self.today][atividades] = tempo_hoje

    return

  def save_results(self):
    """
    Save the results on to google drive based on self.drive_path and self.drive_filename.
    """

    drive.mount('/content/drive')

    # make new JSON file
    with open(self.drive_path + self.drive_filename + '.json', 'w') as f:
      f.write(str({'self.minhas_atividades': self.minhas_atividades,
                    'self.log_atividades' : self.log_atividades}))
      
  def minhas_atividades_df(self):
    minhas_atividades_df = pd.DataFrame(self.minhas_atividades).T
    minhas_atividades_df = minhas_atividades_df.reset_index()
    minhas_atividades_df.columns = ['Atividades', 'Meta_por_dia', 'data_cadastro']

    return minhas_atividades_df

  def log_atividades_df(self):

    #Tratando DF de Log de atividades
    log_atividades_df = pd.DataFrame(self.log_atividades)
    log_atividades_df.index.name = 'Atividades'
    log_atividades_df = log_atividades_df.reset_index()
    log_atividades_df = pd.melt(log_atividades_df, 'Atividades', var_name='data', value_name='tempo')
    log_atividades_df['data'] = pd.to_datetime(log_atividades_df['data'], yearfirst= True)

    return log_atividades_df

  def plot_metas(self):

    minhas_atividades_df = self.minhas_atividades_df()

    ### Graficos de Atividades e Metas
    ##################################

    fig1, ax1 = plt.subplots(figsize=(22,4), nrows= 1, sharex=False)
    sns.barplot(data = minhas_atividades_df,
                x = 'Atividades', 
                y = 'Meta_por_dia',
                palette = self.color_palette,
                ax = ax1)

    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.set_title('Metas definidas')

    #Loop dos labels no gráfico 1
    for i, ativ in enumerate(minhas_atividades_df.Atividades):

      valor = minhas_atividades_df.Meta_por_dia[i]
      texto = ativ + ': ' + format(int(valor), ',d').replace(',','.') + 'min'

      ax1.text(i, valor, texto, 
                      fontsize=16, color='Black',ha='center', bbox=dict(facecolor='white', alpha=0.8)) 
      

  def plot_log_atividades(self, 
                          dados_cumulativos = False, 
                          plot_type =  sns.barplot, 
                          date_range = None, 
                          figsize=(11,7), 
                          sharex=True):
    """
    """

    log_atividades_df = self.log_atividades_df()
    log_atividades_df = pd.merge( log_atividades_df, self.minhas_atividades_df()[['Atividades', 'Meta_por_dia']], how='left', on='Atividades')

    if date_range is not None:
      log_atividades_df = log_atividades_df[date_range]

    ###########
    ## Plots ##
    ###########

    ### Graficos de Atividades diarias
    ##################################

    quantidade_atividades = len(self.minhas_atividades)
    fig2, axs = plt.subplots(figsize= figsize, nrows= (quantidade_atividades), sharex=sharex)

    for axe, ativ, cor in zip(axs, self.minhas_atividades.keys(), self.color_palette):
      #Tratando o DF
      df_plot = log_atividades_df[log_atividades_df.Atividades == ativ].copy()   

      if dados_cumulativos:
        df_plot['1.realizado_acumulado'] = df_plot['tempo'].cumsum()
        df_plot['2.planejado_acumulada'] = df_plot['Meta_por_dia'].cumsum()
        df_plot = pd.melt(df_plot[['Atividades', 'data', '1.realizado_acumulado', '2.planejado_acumulada']], id_vars=['Atividades', 'data'])
      else:
        df_plot.columns = ['Atividades', 'data', '1.realizado', '2.planejado']
        df_plot = pd.melt(df_plot, id_vars=['Atividades', 'data'])

      #Plot 1
      plot_type(data = df_plot,
                  x = 'data',
                  y = 'value',
                  hue = 'variable',
                  palette = [cor, 'gray'],
                  ax = axe)
      axe.legend(frameon=True, fancybox=True,loc='lower right')
      axe.set_xlabel('')
      axe.set_ylabel('')
      axe.set_title(ativ)

    # Turns off grid on the left Axis.
    sns.despine(bottom = True, left = True)
    #ajusta o layout dos subplots
    plt.tight_layout()