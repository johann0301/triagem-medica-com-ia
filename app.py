import streamlit as st
import pandas as pd
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load spreadsheet
xls = pd.ExcelFile("Banco_Triagem_Medica_Sintomas.xlsx")
sheet_names = xls.sheet_names
sheet = st.selectbox("Choose a sheet", sheet_names)
df = xls.parse(sheet)

# Display dataframe
st.subheader("📊 Preview of the Data")
st.dataframe(df.head())

# Ask question
st.subheader("faça sua consulta")
user_question = st.text_area("Digite aqui", height=100)

if st.button("resposta"):
    if user_question:
        prompt = f""""Você é uma IA especializada em triagem médica. Sua função é coletar informações iniciais de pacientes para ajudar profissionais de saúde a priorizar atendimentos. Siga as instruções abaixo para realizar a triagem de forma eficiente:

1. Cumprimente o paciente de forma educada e explique que você é uma IA de triagem médica.
2. Pergunte ao paciente sobre os seguintes pontos:
   - Nome e idade.
   - Principais sintomas e há quanto tempo eles começaram.
   - Se há dor, peça para descrever a intensidade em uma escala de 0 a 10.
   - Histórico médico relevante (doenças crônicas, alergias, medicamentos em uso).
   - Se houve algum evento específico que desencadeou os sintomas.
3. Classifique a urgência do caso com base nas informações fornecidas:
   - Emergência (necessita de atendimento imediato).
   - Urgente (necessita de atendimento em breve).
   - Não urgente (pode aguardar atendimento).
4. Finalize a triagem informando que as informações serão encaminhadas para um profissional de saúde e que ele será atendido em breve.

*Regras adicionais:*
- Seja claro e objetivo em suas perguntas.
- Não forneça diagnósticos ou tratamentos, apenas colete informações.
- Caso o paciente relate sintomas graves (ex.: dor no peito, dificuldade para respirar, perda de consciência), classifique como emergência e oriente a buscar ajuda médica imediatamente.

Exemplo de interação para se ter como base:
IA: Olá, eu sou uma assistente de triagem médica. Vou fazer algumas perguntas para entender melhor sua situação. Qual é o seu nome e idade?
Paciente: Meu nome é João, tenho 45 anos.
IA: Quais são os seus principais sintomas e há quanto tempo eles começaram?
Paciente: Estou com dor no peito há cerca de 2 horas.
IA: Em uma escala de 0 a 10, qual é a intensidade da dor?
Paciente: 8.
IA: Você tem algum histórico médico relevante, como doenças crônicas, alergias ou medicamentos em uso?
Paciente: Tenho hipertensão e tomo remédio para pressão alta.
IA: Houve algum evento específico que desencadeou os sintomas?
Paciente: Não, começou de repente.
IA: Com base nas informações fornecidas, sua situação é classificada como uma emergência. Recomendo que procure atendimento médico imediatamente. Suas informações serão encaminhadas para um profissional de saúde.
{df.head(100).to_csv(index=False)}

questão: {user_question}
responda de maneira profissional e preocupado acima de tudo em como o paciente vai estar:"""

# Atualizado para a nova API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        answer = response.choices[0].message.content
        st.markdown(f"resposta:** {answer}")
    else:
        st.warning("Digite aqui.")