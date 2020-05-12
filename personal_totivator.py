from datetime import datetime, timedelta, date
import re
from google.colab import drive
import ast

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

    
    if atividades_log is None:      
      self.minhas_atividades = {}
      self.log_atividades = None
      self.cadastrar_novas_atividades()
    else:
      #self.minhas_atividades = atividades_log
      pass
    

  def cadastrar_log(self):
    """
    """
    
    if self.log_atividades is None:
      self.log_atividades = {}
      self.log_atividades[self.today] = {}
      print("####################################\n Identificamos que você não possui nenhum Log de atividades ainda...")

    if len(self.log_atividades[self.today]) == 0:

      print("\n###################################### Aeee, primeiro cadastro de atividade do dia " +
            self.today +
            ", parabéns!")

      for i in self.minhas_atividades:
        atividades = i
        meta = self.minhas_atividades[i]['tempo_min'] 
        print('Bora lá, para a atividade: \n' + atividades + '\nvocê indicou que atuaria: \n' + str(meta) + ' minutos diários...'  )
        tempo_hoje = questionator_validator('#### Quantos minutos foram realizados da atividade ' + atividades + ' hoje?\n', float)
        self.log_atividades[self.today][atividades] = tempo_hoje

    else:
      print("\n####################################################################\nHoje, dia " +
            self.today +
            ", você já atuou nas seguintes atividades \n")
      
      for atividade in self.log_atividades[self.today]:
        atuacao = self.log_atividades[self.today][atividade]

        print('\nAtividade: ', atividade)
        print('Atuação: ', atuacao)
      
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
          

    return

  def save_results(self):

    drive.mount('/content/drive')

    # make new JSON file
    with open(self.drive_path + self.drive_filename + '.json', 'w') as f:
      f.write(str({'self.minhas_atividades': self.minhas_atividades,
                    'self.log_atividades' : self.log_atividades}))



 