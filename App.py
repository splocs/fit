import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import SessionState

# Função para criar ou conectar ao banco de dados SQLite
def create_connection():
    conn = sqlite3.connect('nutricao.db')
    return conn

# Função para criar a tabela de refeições no banco de dados
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS refeicoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 data DATE,
                 refeicao TEXT,
                 alimentos TEXT)''')
    conn.commit()
    conn.close()

# Função para criar a tabela de receitas no banco de dados
def create_recipe_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receitas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT,
                 ingredientes TEXT,
                 modo_preparo TEXT)''')
    conn.commit()
    conn.close()

# Função para criar a tabela de progresso de peso no banco de dados
def create_weight_progress_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progresso_peso
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 data DATE,
                 peso REAL)''')
    conn.commit()
    conn.close()

# Função para criar a tabela de usuários no banco de dados
def create_users_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 age INTEGER,
                 gender TEXT,
                 health_goal TEXT)''')
    conn.commit()
    conn.close()

# Função para registrar um novo usuário
def register_user(username, password, age, gender, health_goal):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, age, gender, health_goal) VALUES (?, ?, ?, ?, ?)", 
              (username, password, age, gender, health_goal))
    conn.commit()
    conn.close()

# Função para verificar se um usuário existe no banco de dados
def check_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Função para registrar uma refeição no banco de dados
def registrar_refeicao(data, refeicao, alimentos):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO refeicoes (data, refeicao, alimentos) VALUES (?, ?, ?)", (data, refeicao, alimentos))
    conn.commit()
    conn.close()

# Função para exibir a lista de refeições registradas
def exibir_refeicoes():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM refeicoes")
    refeicoes = c.fetchall()
    conn.close()
    return refeicoes

# Função para registrar uma nova receita no banco de dados
def registrar_receita(nome, ingredientes, modo_preparo):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO receitas (nome, ingredientes, modo_preparo) VALUES (?, ?, ?)", 
              (nome, ingredientes, modo_preparo))
    conn.commit()
    conn.close()

# Função para obter todas as receitas cadastradas
def obter_receitas():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM receitas")
    receitas = c.fetchall()
    conn.close()
    return receitas

# Função para registrar o progresso do peso no banco de dados
def registrar_progresso_peso(data, peso):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO progresso_peso (data, peso) VALUES (?, ?)", (data, peso))
    conn.commit()
    conn.close()

# Função para obter o progresso do peso ao longo do tempo
def obter_progresso_peso():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM progresso_peso")
    progresso_peso = c.fetchall()
    conn.close()
    return progresso_peso

# Função para calcular o IMC (Índice de Massa Corporal)
def calcular_imc(peso, altura):
    if peso <= 0 ou altura <= 0:
        return None
    else:
        imc = peso / (altura ** 2)
        return imc

# Função para o fórum de comunidade
def forum_comunidade():
    st.subheader("Fórum de Comunidade")
    st.write("Bem-vindo ao nosso fórum de comunidade! Aqui você pode interagir com outros usuários, compartilhar dicas, receitas e experiências relacionadas à nutrição e saúde.")
    # Adicione aqui a lógica para o fórum de comunidade

# Função para enviar notificação de lembrete
def enviar_lembrete_notificacao():
    st.success("Lembrete: Não se esqueça de registrar suas refeições hoje!")

# Função para simular a integração com dispositivos de monitoramento de saúde
def integracao_dispositivos_monitoramento():
    st.subheader("Integração com Dispositivos de Monitoramento de Saúde")
    st.write("Integre seu aplicativo de nutrição com dispositivos de monitoramento de saúde para coletar dados adicionais sobre sua saúde e atividade física.")
    st.write("Por enquanto, esta funcionalidade é apenas uma simulação.")
    connect_button = st.button("Conectar Dispositivo")
    if connect_button:
        st.success("Dispositivo conectado com sucesso!")

# Título do aplicativo
st.title('Aplicativo de Nutrição')

# Criar tabelas ao iniciar o aplicativo
create_table()
create_recipe_table()
create_weight_progress_table()
create_users_table()

# Verifica se o usuário está autenticado
session_state = SessionState.get(logged_in=False, user=None)

# Menu principal
menu = st.sidebar.radio('Menu Principal', ['Login', 'Registro', 'Registrar Refeição', 'Adicionar Receita', 
                                           'Visualizar Receitas', 'Registro de Peso', 'Visualizar Progresso de Peso',
                                           'Calcular IMC', 'Sugestões de Receitas Personalizadas', 
                                           'Enviar Notificação de Lembrete', 'Fórum de Comunidade',
                                           'Integração com Dispositivos de Monitoramento de Saúde'])

# Função para login do usuário
def login():
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Login")
    if login_button:
        user = check_user(username, password)
        if user:
            session_state.logged_in = True
            session_state.user = username
            st.success(f"Bem-vindo de volta, {username}!")
        else:
            st.error("Usuário ou senha incorretos. Por favor, tente novamente.")

# Função para registro de novo usuário com informações adicionais do perfil
def register():
    st.subheader("Registro de Novo Usuário")
    new_username = st.text_input("Novo Usuário")
    new_password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    age = st.number_input("Idade")
    gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
    health_goal = st.text_input("Objetivo de Saúde")
    register_button = st.button("Registrar")
    if register_button:
        if new_password == confirm_password:
            register_user(new_username, new_password, age, gender, health_goal)
            st.success("Usuário registrado com sucesso! Faça login para continuar.")
        else:
            st.error("As senhas não coincidem. Por favor, tente novamente.")

if menu == 'Login':
    if not session_state.logged_in:
        login()
    else:
        st.success(f"Você já está logado como {session_state.user}!")

elif menu == 'Registro':
    register()

elif menu == 'Registrar Refeição':
    if session_state.logged_in:
        st.subheader('Registrar Refeição')
        data = st.date_input('Data')
        refeicao = st.selectbox('Refeição', ['Café da Manhã', 'Almoço', 'Jantar', 'Lanche'])
        alimentos = st.text_area('Alimentos Consumidos')
        if st.button('Registrar'):
            registrar_refeicao(data, refeicao, alimentos)
            st.success('Refeição registrada com sucesso!')
    else:
        st.warning("Faça login para registrar uma refeição.")

elif menu == 'Adicionar Receita':
    if session_state.logged_in:
        st.subheader('Adicionar Receita')
        nome = st.text_input('Nome da Receita')
        ingredientes = st.text_area('Ingredientes')
        modo_preparo = st.text_area('Modo de Preparo')
        if st.button('Adicionar'):
            registrar_receita(nome, ingredientes, modo_preparo)
            st.success('Receita adicionada com sucesso!')
    else:
        st.warning("Faça login para adicionar uma receita.")

elif menu == 'Visualizar Receitas':
    if session_state.logged_in:
        st.subheader('Visualizar Receitas')
        receitas = obter_receitas()
        for receita in receitas:
            st.write(f"**{receita[1]}**")
            st.write(f"**Ingredientes:** {receita[2]}")
            st.write(f"**Modo de Preparo:** {receita[3]}")
            st.write('---')
    else:
        st.warning("Faça login para visualizar as receitas.")

elif menu == 'Registro de Peso':
    if session_state.logged_in:
        st.subheader('Registro de Peso')
        data = st.date_input('Data')
        peso = st.number_input('Peso (kg)', min_value=0.0, format="%.2f")
        if st.button('Registrar'):
            registrar_progresso_peso(data, peso)
            st.success('Progresso de peso registrado com sucesso!')
    else:
        st.warning("Faça login para registrar o peso.")

elif menu == 'Visualizar Progresso de Peso':
    if session_state.logged_in:
        st.subheader('Visualizar Progresso de Peso')
        progresso_peso = obter_progresso_peso()
        if progresso_peso:
            df = pd.DataFrame(progresso_peso, columns=['ID', 'Data', 'Peso'])
            df['Data'] = pd.to_datetime(df['Data'])
            fig = px.line(df, x='Data', y='Peso', title='Progresso de Peso ao Longo do Tempo')
            st.plotly_chart(fig)
        else:
            st.warning('Nenhum progresso de peso registrado.')
    else:
        st.warning("Faça login para visualizar o progresso de peso.")

elif menu == 'Calcular IMC':
    if session_state.logged_in:
        st.subheader('Calcular IMC')
        peso = st.number_input('Peso (kg)', min_value=0.0, format="%.2f")
        altura = st.number_input('Altura (m)', min_value=0.0, format="%.2f")
        if st.button('Calcular'):
            imc = calcular_imc(peso, altura)
            if imc:
                st.success(f'Seu IMC é {imc:.2f}')
            else:
                st.error('Peso e altura devem ser maiores que zero.')
    else:
        st.warning("Faça login para calcular o IMC.")

elif menu == 'Sugestões de Receitas Personalizadas':
    if session_state.logged_in:
        st.subheader('Sugestões de Receitas Personalizadas')
        st.write('Aqui você pode encontrar sugestões de receitas personalizadas com base em suas preferências e histórico.')
    else:
        st.warning("Faça login para ver sugestões de receitas personalizadas.")

elif menu == 'Fórum de Comunidade':
    forum_comunidade()

elif menu == 'Enviar Notificação de Lembrete':
    if session_state.logged_in:
        enviar_lembrete_notificacao()
    else:
        st.warning("Faça login para receber lembretes.")

elif menu == 'Integração com Dispositivos de Monitoramento de Saúde':
    integracao_dispositivos_monitoramento()






