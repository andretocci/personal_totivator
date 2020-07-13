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
        print("\n BROOO não te pedi isso, tente de novo! Beijos \n")
        pass
  else:
    while True:
      value = input(questionamento)
      value_tratado = tratamento_caracteres(value) 
      if value_tratado in tratamento_caracteres(exp_values):
        break
      else:
        print("\n BROOO não te pedi isso, tente de novo! Beijos \n ")
        print("Você tem as seguintes opções:\n", ';\n;'.join(exp_values))
        pass


  return value  

class personal_totivator:



  def __init__(self,
      read_dict_file = None,
      read_from_drive = False,
      drive_path = None,
      drive_filename = None):
    
    self.today = date.today().strftime("%Y-%m-%d")    
    self.drive_path = drive_path
    self.drive_filename = drive_filename 
    

    ###################
    ## Setup Inicial ##
    ###################

    print("#########################################\n ## Bem vindo ao seu personal totivator ##\n#########################################")
    print('>>> Hoje é dia', self.today, '\n\n')

    ############################
    ## Lendo arquivo do drive ##
    ############################

    if read_from_drive:
      drive.mount('/content/drive')
      # open existing text file
      with open(self.drive_path + self.drive_filename + '.json') as f:
        dict_file = f.read()
        dict_file = ast.literal_eval(dict_file)

        #Atribuindo valores
        self.minhas_atividades = dict_file['minhas_atividades']
        self.log_atividades = dict_file['log_atividades']
        self.atividades_arquivadas = dict_file['atividades_arquivadas']
        self.color_palette = sns.color_palette("Set1", n_colors=len(self.minhas_atividades), desat=.5)

      #Setando para não ler arquivo local
      read_dict_file = False

    
    ############################
    ## Lendo arquivo do Local ##
    ############################

    if isinstance(read_dict_file, dict):

      dict_file = read_dict_file

      #Atribuindo valores
      self.minhas_atividades = dict_file['minhas_atividades']
      self.log_atividades = dict_file['log_atividades']
      self.atividades_arquivadas = dict_file['atividades_arquivadas']
      self.color_palette = sns.color_palette("Set1", n_colors=len(self.minhas_atividades), desat=.5)

      #Setando para não ler arquivo local
      read_dict_file = False
    
    #########################
    ## Criando objeto novo ##
    #########################

    if read_dict_file is None:      
      self.minhas_atividades = {}
      self.log_atividades = {}
      self.cadastrar_novas_atividades()
      self.atividades_arquivadas = {}
      self.color_palette = {}
    else:      
      print('Arquivo com historico lido!')
      self.plot_log_atividades()
   
  

  def cadastrar_novas_atividades(self):

    if len(self.minhas_atividades) == 0:
      self.minhas_atividades = {}

    quantidade_de_atividades = questionator_validator('### Quantas atividades gostaria de cadastrar? \n', int)
    print(" \n### Agora me fala quais são essas atividades?\n")
    for i in range(0, quantidade_de_atividades):        
      atividade = questionator_validator(">>> Qual seria a atividade número " + str(i + 1) + "? \n", str)
      tempo_min = questionator_validator(">>> E quanto tempo(em minutos) por pretende atuar nela diáriamente? \n", float)
      self.minhas_atividades[atividade] = {'tempo_min': tempo_min,
                                            'data_cadastro': self.today}

    #atualizando palleta de cores
    self.color_palette = sns.color_palette("Set1", n_colors=len(self.minhas_atividades), desat=.5)

  def cadastrar_log(self, force_date=None):
    """
    Método 
    """

    if force_date is None:
      data_avaliada = self.today
    else:
      data_avaliada = force_date
    
    if len(self.log_atividades) == 0:
      self.log_atividades[data_avaliada] = {}
      print("####################################\n Identificamos que você não possui nenhum Log de atividades ainda...")
    
    #Printando atividades já atuadas no dia de hoje
    if data_avaliada in self.log_atividades:
      print("\n####################################################################\nHoje, dia " +
            data_avaliada +
            ", você já atuou nas seguintes atividades \n")
      
      for atividade in self.log_atividades[data_avaliada]:
        atuacao = self.log_atividades[data_avaliada][atividade]

        print('\nAtividade:##########\n', atividade)
        print('Atuação:##########\n', atuacao)
      
      atualizar = questionator_validator('##############################\nGostaria de atualizar suas atuações?(Sim ou Não)\n', 
                                         exp_values = ['sim', 'nao'])

      if atualizar == 'sim':
        for atividade in self.minhas_atividades:
          print('#############################')
          print('Bora atualizar a atividade:')
          meta = self.minhas_atividades[atividade]['tempo_min']
          print(atividade,'que já foram realizados', atividade, 'minutos de', meta, 'estipulados!')

          tempo_hoje = questionator_validator('>>> Quantos minutos foram realizados nessa atividade hoje?\n', float)
          self.log_atividades[data_avaliada][atividade] = atividade + tempo_hoje
    
    else:      
      self.log_atividades[data_avaliada] = {}
      print("\n######################################\nAeee, primeiro cadastro de atividade do dia " +
            data_avaliada +
            ", parabéns!")

      for i in self.minhas_atividades:
        atividades = i
        meta = self.minhas_atividades[i]['tempo_min'] 
        print('\n### Para a atividade ' + atividades + ' você indicou que atuaria: ' + str(meta) + ' minutos diários...'  )
        tempo_hoje = questionator_validator('>>> Quantos minutos foram realizados da atividade ' + atividades + ' hoje?\n', float)
        self.log_atividades[data_avaliada][atividades] = tempo_hoje

    return

  def save_results(self):
    """
    Save the results on to google drive based on self.drive_path and self.drive_filename.
    """

    drive.mount('/content/drive')

    # make new JSON file
    with open(self.drive_path + self.drive_filename + '.json', 'w') as f:
      f.write(str(self.__dict__))

  def arquivar_atividades(self, nome_da_atividade, retomar_atividade = False):

    if isinstance(nome_da_atividade, str):
      nome_da_atividade = [nome_da_atividade]

    if len(self.atividades_arquivadas) > 0:
      print('>>> Encontramos as seguintes atividades arquivadas\n')
      for ativ in self.atividades_arquivadas:
        print('Atividade:', ativ)
        print('Motivo:', self.atividades_arquivadas[ativ]['arquivamento']['motivo'])
        print('Data de Arquivamento:', self.atividades_arquivadas[ativ]['arquivamento']['data_arquivamento'])
        print('\n')

    if not retomar_atividade:
      for ativ in nome_da_atividade:
        while ativ not in self.minhas_atividades:
          print('###\nNão encontramos a seguinte atividade nos seus cadastros:\n', ativ)
          print("""\n#####################################\n
                  >>> Essas são suas atividades cadastradas:\n""", ';\n'.join(self.minhas_atividades.keys()))
          ativ = questionator_validator('##############################\nQual seria a atividade que gostaria de remover??\n', 
                                          exp_values = self.minhas_atividades.keys())
          if ativ in self.minhas_atividades:
            break
        
        self.atividades_arquivadas[ativ] = self.minhas_atividades[ativ]
        motivo = questionator_validator("""\n##############################\n
                                            >>> Por que você está arquivando essa atividade? A atividade foi concluída ou paudada?\n""", 
                                          exp_values = ['Concluida', 'Pausada', 'PQ tu ta querendo saber isso manoww'])
        #Validando se a chave arquivamento existe
        if 'arquivamento' not in self.atividades_arquivadas[ativ]:
          self.atividades_arquivadas[ativ]['arquivamento'] = {}
          self.atividades_arquivadas[ativ]['arquivamento']['motivo'] = [motivo]
          self.atividades_arquivadas[ativ]['arquivamento']['data_arquivamento'] = [self.today]
          del self.minhas_atividades[ativ]
        else:
          self.atividades_arquivadas[ativ]['arquivamento']['motivo'].append(motivo)
          self.atividades_arquivadas[ativ]['arquivamento']['data_arquivamento'].append(self.today)
    else:
      for ativ in nome_da_atividade:
        while ativ not in self.atividades_arquivadas:
          print('###\nNão encontramos a seguinte atividade nos seus cadastros:\n', ativ)
          print(""">>> Essas são suas atividades arquivadas:\n""", ';\n'.join(self.atividades_arquivadas.keys()))
          ativ = questionator_validator('>>> Qual seria a atividade que gostaria de retomar??\n', 
                                          exp_values = self.atividades_arquivadas.keys())
          print(ativ, ativ in self.atividades_arquivadas)
          
          if ativ in self.atividades_arquivadas:
            break
      if 'retomada' not in self.atividades_arquivadas[ativ]['arquivamento']:
        self.atividades_arquivadas[ativ]['arquivamento']['retomada'] = [self.today]
      else:
        self.atividades_arquivadas[ativ]['arquivamento']['retomada'].append(self.today)
      self.minhas_atividades[ativ] = self.atividades_arquivadas[ativ]
      del self.atividades_arquivadas[ativ]

    #atualizando palleta de cores
    self.atualizar_paleta()
      
    return ativ

  def minhas_atividades_df(self):
    """
    Retorna um DataFrame contendo as atividades cadastradas.
    Colunas = ['Atividades', 'Meta_por_dia', 'data_cadastro']
    """
    minhas_atividades_df = pd.DataFrame.from_dict(self.minhas_atividades, orient='index')
    minhas_atividades_df = minhas_atividades_df.reset_index()
    minhas_atividades_df.columns = ['Atividades', 'Meta_por_dia', 'data_cadastro', 'arquivamento']

    return minhas_atividades_df


  def log_atividades_df(self, fill_missing_days = False):
    """
    Retorna um DataFrame contendo o log de atividades realizadas e cadastradas.
    Colunas = ['data', 'Atividades', 'tempo']

    fill_missing_days = Caso True, preenche com zero datas sem atividades;
    """

    #Tratando DF de Log de atividades
    log_atividades_df = pd.DataFrame(self.log_atividades)
    log_atividades_df.index.name = 'Atividades'
    log_atividades_df = log_atividades_df.reset_index()
    log_atividades_df = pd.melt(log_atividades_df, 'Atividades', var_name='data', value_name='tempo')
    log_atividades_df['data'] = pd.to_datetime(log_atividades_df['data'], yearfirst= True)

    if fill_missing_days:
      res_missing = []

      for i in set(log_atividades_df['Atividades']):
        df = log_atividades_df[log_atividades_df['Atividades'] == i].copy()
        r = set(pd.date_range(start=df.data.min(), end=df.data.max()))
        r = pd.DataFrame(r.symmetric_difference(set(log_atividades_df['data'])))
        r.columns = ['data']
        r['tempo'] = 0
        r['Atividades'] = i
        res_missing.append(r)

      log_atividades_df = pd.concat([log_atividades_df] + res_missing)
    
    log_atividades_df.sort_values('data', inplace=True)
    log_atividades_df['data'] = log_atividades_df['data'].dt.strftime('%Y-%m-%d')

    return log_atividades_df


  def atualizar_paleta(self, palette = "Set1"):
    """
    Atualiza a paletta de acordo com a quantidade de atividades cadastrada;
    """
  
    self.color_palette = sns.color_palette(palette=palette , n_colors=len(self.minhas_atividades), desat=.5)

  def plot_metas(self):

    minhas_atividades_df = self.minhas_atividades_df()
    self.atualizar_paleta()

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
                      fontsize=16, color='White',ha='center', bbox=dict(facecolor=self.color_palette[i], alpha=0.8)) 
      

  def plot_log_atividades(self, 
                          fill_missing_days=False,
                          dados_cumulativos = False, 
                          plot_type =  sns.barplot, 
                          date_range = None, 
                          figsize=(11,7), 
                          sharex=True):
    """
    """

    log_atividades_df = self.log_atividades_df(fill_missing_days=fill_missing_days)
    self.atualizar_paleta()
    log_atividades_df = pd.merge( log_atividades_df, self.minhas_atividades_df()[['Atividades', 'Meta_por_dia']], how='left', on='Atividades')

    if date_range is not None:
      log_atividades_df = log_atividades_df[date_range]

    ###########
    ## Plots ##
    ###########

    ### Graficos de Atividades diarias
    ##################################

    quantidade_atividades = len(self.minhas_atividades)
    fig, axs = plt.subplots(figsize= figsize, nrows= (quantidade_atividades), sharex=sharex)

    for axe, ativ, cor in zip(axs, self.minhas_atividades.keys(), self.color_palette):
      #Tratando o DF
      df_plot = log_atividades_df[log_atividades_df.Atividades == ativ].copy()


      df_plot.columns = ['Atividades', 'data', '1.realizado', '2.planejado']

      #Plot 1
      plot_type(data = df_plot,
                  x = 'data',
                  y = '1.realizado',
                  color = cor,
                  ax = axe)
      axe.set_xlabel('')
      axe.set_ylabel('')
      axe.set_title(ativ)
      axe.axhline(y = self.minhas_atividades[ativ]['tempo_min'],
                  color='gray',
                  linestyle = '--',
                  lw = 3)
      axe.axhline(y = 0, color='black', lw = 5)
      axe.text(0, 
               self.minhas_atividades[ativ]['tempo_min'], 
               'Meta diária: ' + str(self.minhas_atividades[ativ]['tempo_min']) + ' minutos',
               fontsize=16, 
               color='White',
               ha='center', 
               bbox=dict(facecolor=cor, alpha=1)) 
      axe.set_facecolor('white')
    fig.autofmt_xdate()

    # Turns off grid on the left Axis.
    sns.despine(bottom = True, left = True)
    #ajusta o layout dos subplots
    plt.tight_layout()

  def old_plot_log_atividades(self, 
                          dados_cumulativos = False, 
                          plot_type =  sns.barplot, 
                          max_date = None, 
                          min_date = None, 
                          figsize=(11,7), 
                          sharex=True):
    """
    """

    log_atividades_df = self.log_atividades_df()
    log_atividades_df = pd.merge( log_atividades_df, self.minhas_atividades_df()[['Atividades', 'Meta_por_dia']], how='left', on='Atividades')

    if (min_date is not None) | (max_date is not None) :
      log_atividades_df = log_atividades_df[min_date :max_date]

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
      axe.set_facecolor('white')

    # Turns off grid on the left Axis.
    sns.despine(bottom = True, left = True)
    #ajusta o layout dos subplots
    plt.tight_layout()

  def plot_describe(self, plot_type = sns.boxplot):
    """
    plot_type = Pode ser um dos sns.boxplot, ou sns.swarmplot, ou sns.violinplot
    """

    #Criando DF do log
    df = self.log_atividades_df()
    # Filtrando dados zerados
    df = df[df.tempo > 0].copy()

    #Criando figura
    # ax = sns.swarmplot(x="Atividades", y="tempo", data=df, palette= personal_t2.color_palette,  edgecolor = 'white', linewidth=2,size=10)
    fig, axs = plt.subplots(1, 2, sharey= True, figsize=(20,5))
    plot_type(y="Atividades", x="tempo", data=df, palette= personal_t2.color_palette, linewidth=2, ax = axs[1])


    #Agrupando dados por atividades
    df2 = df.groupby(['Atividades'])['tempo'].sum().reset_index() #.agg({'tempo': ['sum']})
    sns.barplot(y="Atividades", x="tempo", data= df2, palette= personal_t2.color_palette, ax = axs[0])

    for axe in axs:
      # axe.legend(frameon=True, fancybox=True,loc='lower right')
      # axe.set_xlabel('')
      # axe.set_ylabel('')
      # axe.set_title(ativ)
      axe.set_facecolor('white')

    # Turns off grid on the left Axis.
    sns.despine(bottom = True, left = True)
    #ajusta o layout dos subplots
    plt.tight_layout()