import streamlit as st
import pandas as pd

st.title("Conselho de Classe dos Cursos Técnicos - IF Goiano campus Campos Belos - 2023")

DISCIPLINES_MAP = {
    "Disciplina.6432": "Química II",
    "Disciplina.6437": "Língua Port.",
    "Disciplina.6438": "Artes",
    "Disciplina.6439": "Ed.Física II",
    "Disciplina.6440": "Física II",
    "Disciplina.6449": "Biologia II",
    "Disciplina.6450": "Matemática II",
    "Disciplina.6451": "História II",
    "Disciplina.6452": "Geografia II",
    "Disciplina.6454": "Filosofia II",
    "Disciplina.6455": "Manut. de Comp.",
    "Disciplina.6456": "Desenv. Web II",
    "Disciplina.6457": "Banco de Dados",
    "Disciplina.6468": "Sociologia II",
    "Disciplina.6469": "Inglês Ap. II",
    "Disciplina.5060": "Banco de Dados",
    "Disciplina.7188": "Língua Port.",
    "Disciplina.7189": "Ed. Física",
    "Disciplina.7190": "Inglês",
    "Disciplina.7191": "Física",
    "Disciplina.7192": "Química",
    "Disciplina.7193": "Biologia",
    "Disciplina.7194": "Matemática",
    "Disciplina.7195": "História",
    "Disciplina.7196": "Geografia",
    "Disciplina.7197": "Sociologia",
    "Disciplina.7198": "Filosofia",
    "Disciplina.7295": "Eixo de I",
    "Disciplina.7296": "Fund. Comput.",
    "Disciplina.7297": "Lógica de Prog.",
    "Disciplina.7298": "Desenv. WEB I"
    "Disciplina.6441": "Geografia III",
    "Disciplina.6443": "Sociologia III",
    "Disciplina.6444": "Filosofia III",
    "Disciplina.6445": "Desenv. Web III",
    "Disciplina.6446": "Análise e Desenv.",
    "Disciplina.6447": "Redes II",
    "Disciplina.6448": "Inglês Apl.III",
    "Disciplina.6459": "Língua Port. III",
    "Disciplina.6460": "Ed.Física III",
    "Disciplina.6461": "Espanhol III",
    "Disciplina.6462": "Física III",
    "Disciplina.6463": "Química III",
    "Disciplina.6464": "Biologia III",
    "Disciplina.6465": "Matemática III",
    "Disciplina.6466": "História III"
}

def import_sheets(file):
    sheets = ["Etapa 1", "Etapa 2", "Etapa 3", "Etapa Final"]
    data = {}
    
    for sheet in sheets:
        try:
            df = pd.read_excel(file, sheet_name=sheet)
            
            # Excluindo a primeira linha
            df = df.drop(index=0)
            df = df.drop(index=1)
            
            df.columns.values[0] = "Aluno"  # Renomeando a primeira coluna para "Aluno"
            
            # Removendo colunas que começam com "Unnamed:"
            df = df.drop(columns=[col for col in df.columns if col.startswith("Unnamed:")])
            
            # Renomeando as colunas de disciplinas
            df.rename(columns=DISCIPLINES_MAP, inplace=True)
            
            data[sheet] = df
        except Exception as e:
            st.write(f"Erro ao ler a sheet {sheet}: {e}")

    return data

def calculate_student_averages(data):
    # Estabelece a coluna 'Aluno' como índice
    etapa1_df = data["Etapa 1"].set_index('Aluno').apply(pd.to_numeric, errors='coerce')
    etapa2_df = data["Etapa 2"].set_index('Aluno').apply(pd.to_numeric, errors='coerce')
    etapa3_df = data["Etapa 3"].set_index('Aluno').apply(pd.to_numeric, errors='coerce')

    # Calcula a média das três etapas para cada disciplina (coluna) e aluno (linha)
    averages_df = ((etapa1_df*0.3) + (etapa2_df*0.3) + (etapa3_df*0.4))

    return averages_df.reset_index()




def red_for_values_below_6(val):
    """
    Retorna cor da letra vermelha se o valor for menor que 6.
    """
    color = 'red' if isinstance(val, (int, float)) and val < 6 else 'black'
    return f'color: {color}'

uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    data = import_sheets(uploaded_file)
    
    # Mostra os dados originais das etapas
    for sheet_name, df in data.items():
        st.subheader(f"Etapas: {sheet_name}")
        styled_df = df.style.applymap(red_for_values_below_6)
        st.dataframe(styled_df)

    # Calcula e mostra as médias
    averages = calculate_student_averages(data)
    styled_avg = averages.style.applymap(red_for_values_below_6)
    st.subheader("Médias dos Alunos sendo as três etapas com pesos")
    st.dataframe(styled_avg)

st.write("Faça upload do seu arquivo e as sheets 'Etapa 1', 'Etapa 2', 'Etapa 3' e 'Etapa Final' serão exibidas. As médias dos alunos serão calculadas e mostradas abaixo.")

