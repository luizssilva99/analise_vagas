import requests
import json
import re
from pypdf import PdfReader
from fpdf import FPDF
from datetime import datetime
import base64
import os
import streamlit as st

def extract_resume_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    return ""

def analyze_job_with_gemma(description: str, resume: str) -> str:
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    system_prompt = (
        "Você é um assistente de carreira especialista em análise de vagas. "
        "Sempre responda no seguinte formato com os títulos exatamente como indicados:\n\n"
        "Resumo: [parágrafo resumido da vaga]\n"
        "Skills: [skill1, skill2, skill3, ...]\n"
        "Sugestão: [sugestão personalizada para adaptar o currículo à vaga, com base no que está faltando no currículo abaixo]\n\n"
        "Não inclua explicações adicionais. A resposta deve ser direta e objetiva."
    )
    user_prompt = f"""
Aqui está a descrição de uma vaga de emprego:

{description}

E aqui está o currículo do candidato:

{resume}

Gere a análise seguindo as instruções fornecidas.
"""
    payload = {
        "model": "gemma-3-12b-it",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    raise Exception(f"Erro {response.status_code}: {response.text}")

def extrair_titulo_vaga(texto_vaga):
    # Primeiro tenta extrair do resumo com o padrão "A vaga busca um ..."
    match = re.search(r"(?i)a vaga busca (um|uma)\s+([^\n,.]+)", texto_vaga)
    if match:
        return match.group(2).strip().title()

    # Se não encontrar, tenta pegar alguma frase após "vaga de", "cargo de", etc
    match_alt = re.search(r"(?i)(vaga|cargo|oportunidade) de\s+([^\n,.]+)", texto_vaga)
    if match_alt:
        return match_alt.group(2).strip().title()

    # Fallback básico: primeiras palavras
    palavras = texto_vaga.strip().split()
    return " ".join(palavras[:4]).title() if palavras else "Cargo Indefinido"


def export_to_pdf(summary, skills, tip, vaga_texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=12)
    pdf.multi_cell(0, 10, "Resumo da Vaga:\n" + summary + "\n\nSkills Recomendadas:\n" + skills + "\n\nDica para seu Currículo:\n" + tip)

    data_str = datetime.now().strftime("%Y-%m-%d")
    titulo_base = extrair_titulo_vaga(vaga_texto)
    nome_arquivo = f"analise_{titulo_base}_{data_str}.pdf"
    pdf.output(nome_arquivo)

    with open(nome_arquivo, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nome_arquivo}">📄 Baixar Análise em PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

    os.remove(nome_arquivo)
