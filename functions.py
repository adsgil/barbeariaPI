import json
import threading

import pyrebase
import requests
from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.picker import MDDatePicker


global firebase2 
global lista2
global HORARIOS_SELECIONADOS

firebaseConfig = {



}


firebase2 = pyrebase.initialize_app(firebaseConfig)
lista2 = []
HORARIOS_SELECIONADOS = []  


# Redireciona para a tela inicial
def callbackregister(self, *args):
  MDApp.get_running_app().root.current = 'login'

# Registra usuário na base de dados
def create_post(self, nome, email, senha):
  firebase_url =
  auth_key =

  lista = []
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  try:        
    to_database = '{"Nome": 'f'{json.dumps(nome)}'', "E-mail" : 'f'{json.dumps(email)}'', "Senha" : 'f'{json.dumps(senha)}''}'

    
    if nome == "":
      self.ids.lbregister.text = "Insira nome"

    elif email == "":
      self.ids.lbregister.text = "Insira o E-mail"

    elif senha == "":
      self.ids.lbregister.text = "Insira a Senha"


    elif len(senha) < 10:
      self.ids.lbregister.text = "Senha precisa de pelo menos 10 caracteres"   

    elif email in res:
      self.ids.lbregister.text = "E-mail já cadastrado"

    else:
      #requests.post(url = self.firebase_url, json = to_database2)
      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbregister.text = "Cadastrado com sucesso! Redirecionando para a tela de login..."
      Clock.schedule_once(self.callbackregister, 3)


      lista.append(nome)
      lista.append(email)
      lista.append(senha)

    
      with open(f'{email}.txt',"w") as a:
        a.write(str(lista[0]))
        a.write("\n")
        a.write(str(lista[1]))
        a.write("\n")
        a.write(str(lista[2]))
    
  except ValueError:
    pass        

  lista.clear

# Redireciona para o dashboard
def callbacklogin(self, *args):
  MDApp.get_running_app().root.current = 'dashboard'

    
# Autentica o usuario
def get_post(self, email, senha):
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json())         
  
  
  if (email != '' and senha != ''):
    if (email in res) and (len(senha) >= 10 and senha in res):
      self.ids.lblogin.text = "Aguarde Enquanto te direcionamos para a tela inicial..."
      Clock.schedule_once(self.callbacklogin, 3)
      nome = list(open(f'{email}.txt', "r"))
      nome = nome[0]
      id = list(open(f'{email}.txt', "r"))
      id = id[2]
      with open("autenticado.txt", "w") as f:    
        f.write(str(nome))
        f.write(str(email))
        f.write("\n")
        f.write(str(id))  

    else: 
      self.ids.lblogin.text = "E-mail ou senha inválidos, tente novamente"


  else: 
    if(email == ''):
      self.ids.lblogin.text = "Insira o E-mail logar"

    elif(email == ''):
      self.ids.lblogin.text = "Insira a senha para logar"


    elif (email == '' and senha == ''):
      self.ids.lblogin.text = "Insira o E-mail e Senha para logar"


# Redefine senha
def redf_passwd(self, email, senha):
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if email == "":
    self.ids.lbredfsenha.text = "Insira o E-mail"
  elif email not in res:
    self.ids.lbredfsenha.text = "E-mail não cadastrado"
  elif senha == "": 
    self.ids.lbredfsenha.text = "Insira a nova senha"
  elif len(senha) < 10:
    self.ids.lbredfsenha.text = "Senha precisa ter pelo menos 10 caracteres"
    
  else:
    db = firebase2.database()
    user = db.child("Usuarios").get()
    for usuario in user.each():
      if usuario.val()['E-mail'] == f'{email}' :
        db.child("Usuarios").child(usuario.key()).update({'Senha': f'{senha}'})
        a = open(f'{email}.txt', "r")
        list_of_lines = a.readlines()    
        list_of_lines[2] = f'{senha}'
        a = open(f'{email}.txt', "w")
        a.writelines(list_of_lines) 
        a.close()
    
    self.ids.lbredfsenha.text = "Senha redefinida com sucesso!"


# Edita as informações do usuário
def change_screen(self, nome, email):
  nome2 = list(open("autenticado.txt", "r"))
  nome2 = nome2[0]
  email2 = list(open("autenticado.txt", "r"))
  email2 = email2[1]
  id2 = list(open("autenticado.txt", "r"))
  id2 = id2[2]
    

  db = firebase2.database()
  user = db.child("Users").get()
  for usuario in user.each():
    if usuario.val()['Nome'] in nome2:
      if f'{nome}' != "":
        db.child("Users").child(usuario.key()).update({'Nome': f'{nome}'})
        
        f = open("autenticado.txt", "r")
        list_of_lines = f.readlines()    
        list_of_lines[0] = f'{nome}\n'
        f = open("autenticado.txt", "w")
        f.writelines(list_of_lines) 
        f.close()
        self.ids.lbchange.text = "Nome alterado com sucesso!"

          
    if usuario.val()['E-mail'] in email2:
      if f'{email2}' != "":
        db.child("Users").child(usuario.key()).update({'E-mail': f'{email2}'})

        a = open("autenticado.txt", "r")
        list_of_lines = a.readlines()    
        list_of_lines[1] = f'{email2}\n'
        a = open("autenticado.txt", "w")
        a.writelines(list_of_lines) 
        a.close()
        self.ids.lbchange.text = "E-mail alterado com sucesso!"
        

    if usuario.val()['Senha'] in id2:
      if f'{id}' != "":
        db.child("Users").child(usuario.key()).update({'Senha': f'{id}'})

        b = open("autenticado.txt", "r")
        list_of_lines = b.readlines()    
        list_of_lines[2] = f'{id}\n'
        b = open("autenticado.txt", "w")
        b.writelines(list_of_lines) 
        b.close()
        self.ids.lbchange.text = "ID alterado com sucesso!"

    self.ids.lbchange.text = "Dados alterados com sucesso!"
    
    with open(f'{email}.txt', "w") as op:
        op.write(str(nome))
        op.write("\n")
        op.write(str(email))
        op.write("\n")
        op.write(str(id))


# Salva a data escolhida pelo usuario
def on_save(self, instance, value, date_range):
  self.ids.data.text = str(value)  

# Mostra a mensagem quando o usuario cancela a data
def on_cancel(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

# Cria o calendario
def show_data_picker(self):
  date_dialog = MDDatePicker(year=2022, month=12, day=17)
  date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
  date_dialog.open()     


# Cria o agendamento e salva no banco de dados firebase
def check(self, especialidade, data, barbeiro):
  firebase_url =
  auth_key =
  firebase_url2 =


  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 

  request2 = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res2 = json.dumps(request2.json()) 

  if especialidade == "":
    self.ids.lbcheckin.text = "Insira a especialidade"
  elif barbeiro not in res2:
    self.ids.lbcheckin.text = "Barbeiro não registrado"
  elif barbeiro == "":
    self.ids.lbcheckin.text = "Insira Nome do barbeiro"

  else:
    to_database = '{"Especialidade": 'f'{json.dumps(especialidade)}'', "Data": 'f'{json.dumps(data)}'', "Nome Barbeiro": 'f'{json.dumps(barbeiro)}''}'
    db = firebase2.database()
    barbeiros = db.child("Barbeiros").get()
    for berbeiros2 in barbeiros.each():
      if barbeiros2.val()['Nome Barbeiro'] == f'{barbeiro}':
        db.child("Barbeiros").child(barbeiros2.key()).update({'Especialidade' : f'{especialidade}'})

    try:
      
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbcheckin.text = "Atendimento agendado com sucesso"

    except ValueError:
      pass

    # Cria a consulta e salva no banco de dados firebase


def check(self, especialidade, data, barbeiro):
  firebase_url = "https://barberdb-42826-default-rtdb.firebaseio.com/Agenda/.json"
  firebase_url2 = "https://barberdb-42826-default-rtdb.firebaseio.com/Barbeiros/.json"
  auth_key = 'sD1FxOLXPdsR0Iyfp5Oi3Pkx3oj5eDqC9p1KETzO'

  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json())

  request2 = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res2 = json.dumps(request2.json())

  if especialidade == "":
    self.ids.lbcheckin.text = "Insira a especialidade"
  elif barbeiro not in res2:
    self.ids.lbcheckin.text = "Barbeiro não registrado"
  elif barbeiro == "":
    self.ids.lbcheckin.text = "Insira o Nome do barbeiro"

  else:
    to_database = '{"Especialidade": 'f'{json.dumps(especialidade)}'', "Data": 'f'{json.dumps(data)}'', "Barbeiro": 'f'{json.dumps(barbeiro)}''}'
    db = firebase2.database()
    barbeiros = db.child("Barbeiros").get()
    for barbeiro2 in barbeiros.each():
      if barbeiro2.val()['Nome'] == f'{barbeiro}':
        db.child("Barbeiros").child(barbeiro2.key()).update({'Especialidade': f'{especialidade}'})

    try:

      requests.post(url=self.firebase_url, json=json.loads(to_database))
      self.ids.lbcheckin.text = "Atendimento agendado com sucesso!"


    except ValueError:
      pass


def on_save2(self, instance, value, date_range):
  self.ids.data.text = str(value)  

def on_cancel2(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

def show_data_picker2(self):
  date_dialog = MDDatePicker(year=2022, month=6, day=17)
  date_dialog.bind(on_save=self.on_save2, on_cancel=self.on_cancel2)
  date_dialog.open()          

# Cria a retirada de medicamentos 

def checkout(self, med, data, paciente2):
  #firebase_url = " "    
  #firebase_url2 = " "
  #firebase_url3 = " "
  #auth_key = ' '
  
  request = requests.get(self.firebase_url3 + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  request2 = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res2 = json.dumps(request2.json()) 

  if med not in res2:
    self.ids.lbcheckout.text = "Medicamento fora de estoque"
  elif med == "":
    self.ids.lbcheckout.text = "Insira nome do medicamento "
  elif paciente2 not in res:
    self.ids.lbcheckout.text = "Paciente não registrado"
  elif paciente2 == "":
    self.ids.lbcheckout.text = "Insira ID do paciente"

  else:
    to_database = '{"Medicamento": 'f'{json.dumps(med)}'', "Data": 'f'{json.dumps(data)}'', "ID Paciente": 'f'{json.dumps(paciente2)}''}'
    #to_database1 = '{"Data": 'f'{data}''}'

    try:
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbcheckout.text = "Retirada agendada com sucesso!"
      #requests.post(url = self.firebase_url, json = json.dumps(to_database1))

    except ValueError:
      pass  


# Cria o estoque de medicamentos (entrada e saida dos mesmos)

def create_post_meds(self, nome_med, quantidade, id_med):
  #firebase_url = " "  
  #auth_key = ' ' 
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if nome_med == "":
    self.ids.lbmeds.text = "Insira medicamento"
  elif quantidade == "":
    self.ids.lbmeds.text = "Insira quantidade maior que 0"
  elif id_med == "":
    self.ids.lbmeds.text = "Insira o id do med"  

  else:
    try:        
      to_database = '{"Nome do medicamento": 'f'{json.dumps(nome_med)}'', "Quantidade" : 'f'{json.dumps(quantidade)}'', "ID medicamento" : 'f'{json.dumps(id_med)}''}'

      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbmeds.text = "Medicamento adicionado ao estoque!"        

    except ValueError:
      pass  

    lista2.append(int(quantidade))  

  with open("meds.txt", "a") as fp:
    for item in lista2:
      fp.write("%d\n" % item)     



@mainthread
def data_table(self, cols, values):    
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables)

# Mostra os dados sobre o usuário

def on_enter2(self):
  firebase_url =
  auth_key =
  
  nome = list(open('autenticado.txt', 'r'))
  nome = nome[0]
  email = list(open('autenticado.txt', 'r'))
  email = email[1]
  id = list(open('autenticado.txt', 'r'))
  id = id[2]
  self.ids.emailfuncionario.text = email
  self.ids.nomefuncionario.text = nome



# Registra os barbeirps no banco de dados

def callbackregisterpacientes(self, *args):
  MDApp.get_running_app().root.current = 'login'

def create_post_pacient(self, nome2, email2, senha2):
  firebase_url =
  auth_key =
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  try:        
    to_database = '{"Nome": 'f'{json.dumps(nome2)}'', "E-mail" : 'f'{json.dumps(email2)}'', "Senha" : 'f'{json.dumps(senha2)}''}'



    if len(senha2) < 10:
      self.ids.lbregister_pacient.text = "Senha precisa de pelo menos 10 caracteres"   

    elif email2 in res:
      self.ids.lbregister_pacient.text = "E-mail já cadastrado"

    else:
      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbregister_pacient.text = "Barbeiro cadastrado com sucesso!"

  except ValueError:
    pass  

# Registra horários de plantão e coloca os dados diretamente no banco de dados firebase

def callbackplantao(self, *args):
  MDApp.get_running_app().root.current = 'login'

def on_save3(self, instance, value, date_range):
  #self.ids.data2.text = f'{str(date_range[0])} - {str(date_range[-1])}'
  self.ids.data2.text = f'{str(date_range)}'

def on_cancel3(self, instance, value):
  self.ids.data2.text = "Você cliclou em cancelar"

def show_data_picker3(self):
  date_dialog = MDDatePicker(mode="range")
  date_dialog.bind(on_save=self.on_save3, on_cancel=self.on_cancel3)
  date_dialog.open()   

def create_post_hour(self, email_funcionario, data2, horario):
  request = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if email_funcionario not in res:
    self.ids.lbregister_hour.text = "E-mail não cadastrado"

  elif horario == "":
    self.ids.lbregister_hour.text = "Insira horário"

  else:

    try:        
      to_database = '{"E-mail funcionario": 'f'{json.dumps(email_funcionario)}'', "Data" : 'f'{json.dumps(data2)}'', "Horario" : 'f'{json.dumps(horario)}''}'


      
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbregister_hour.text = "Horario adicionado com sucesso!"

    except ValueError:
      pass  


# Cria tabela que mostra consultadas agendadas 

stop2 = threading.Event()

def on_stop2(self):
  self.stop2.set()

def on_enter4(self):
  self.start_second_thread()

def start_second_thread2(self):
  threading.Thread(target=self.load_data).start()

def load_data2(self, *args): 
  #get_request = requests.get(f' ')
  consultas_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for consultas, dado in consultas_data.items():
    lista = []
    lista.append(consultas)

    for key, info in dado.items():
      lista.append(info)
      
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)   

  
@mainthread
def data_table2(self, cols, values):    
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables)


# Cria tabela que mostra retirada de medicamentos agendadas

stop3 = threading.Event()

def on_stop3(self):
  self.stop3.set()

def on_enter5(self):
  self.start_second_thread()

def start_second_thread3(self):
  threading.Thread(target=self.load_data).start()

def load_data3(self, *args): 
  get_request = requests.get(f' ')
  consultas_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for consultas, data in consultas_data.items():
    lista = []
    lista.append(consultas)

    for key, info in data.items():
      lista.append(info)
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)  

@mainthread
def data_table3(self, cols, values):
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables) 


# Cria tabela que mostra horarios de plantão e remove horarios


stop4 = threading.Event()

def on_stop4(self):
  self.stop4.set()

def on_enter6(self):
  self.start_second_thread()

def start_second_thread4(self):
  threading.Thread(target=self.load_data).start()

def load_data4(self, *args): 
  firebase_url =
  auth_key =
  if HORARIOS_SELECIONADOS:
    for h_horarios in HORARIOS_SELECIONADOS:
      post_request = requests.delete(f'/{h_horarios}/.json')

  get_request = requests.get(f' ')
  horarios_dado = json.loads(get_request.content.decode())     
  count = 0
  cols = ["Código"]
  values = []
  try:

    for horarios, dado in horarios_dado.items():
      lista = []
      lista.append(horarios)

      for key, info in dado.items():
        lista.append(info)
        if count == 0:
          cols.append(key)        
      count+=1  
      values.append(lista)
      
  except AttributeError:
    pass    

  self.data_table(cols, values)  

def on_check_press(self, instance_table, current_row):

  '''Called when the check box in the table row is checked.'''
  if current_row[0] in HORARIOS_SELECIONADOS:
      HORARIOS_SELECIONADOS.remove(current_row[0])
  else:
      HORARIOS_SELECIONADOS.append(current_row[0])


@mainthread
def data_table4(self, cols, values):  

  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.data_tables.bind(on_check_press=self.on_check_press)
  self.add_widget(self.data_tables) 


# Cria tabela que mostra os barbeiros registrados

stop5 = threading.Event()

def on_stop(self):
  self.stop5.set()

def on_enter7(self):
  self.start_second_thread()

def start_second_thread5(self):
  threading.Thread(target=self.load_data).start()

def load_data5(self, *args): 
  get_request = requests.get(f' ')
  barbeiros_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for barbeiros1, data in barbeiros_data.items():
    lista = []
    lista.append(barbeiros1)

    for key, info in data.items():
      lista.append(info)
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)  

@mainthread
def data_table5(self, cols, values):
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables) 
