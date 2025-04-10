import streamlit as st
from database import init_db, corrigir_schema, salvar_analise, toggle_favorito
from utils import extract_resume_text, export_to_pdf, analyze_job_with_gemma, extrair_titulo_vaga
import sqlite3
import pandas as pd
import re
from collections import Counter

# ------------------ CONFIGURAÇÃO INICIAL ------------------
st.set_page_config(page_title="Análise Inteligente de Vagas", page_icon="💼", layout="centered")
init_db()
corrigir_schema()

# ------------------ MENU DE NAVEGAÇÃO ------------------
pagina = st.sidebar.selectbox("Navegar", ["📋 Nova Análise", "📊 Dashboard"])

# ------------------ PÁGINA DE ANÁLISE ------------------
if pagina == "📋 Nova Análise":
    st.title("💼 Análise Inteligente de Vagas com IA Local (Gemma)")
    st.markdown("Cole a descrição de uma vaga e envie seu currículo para obter um resumo, skills e sugestões personalizadas.")

    job_description = st.text_area("📄 Descrição da Vaga:", height=250)
    resume_file = st.file_uploader("📎 Currículo (.pdf ou .txt)", type=["pdf", "txt"])

    if "generated_summary" not in st.session_state:
        st.session_state.generated_summary = ""
        st.session_state.generated_skills = ""
        st.session_state.generated_tip = ""

    if st.button("🚀 Gerar Análise"):
        if not job_description.strip():
            st.error("⚠️ Descrição da vaga é obrigatória.")
        elif not resume_file:
            st.error("⚠️ Envie seu currículo.")
        else:
            with st.spinner("Analisando com IA local..."):
                try:
                    resume_text = extract_resume_text(resume_file)
                    result = analyze_job_with_gemma(job_description, resume_text)

                    summary = re.search(r"(?i)resumo:\s*(.+?)(?=skills:|sugest[ãa]o:|$)", result, re.DOTALL)
                    skills = re.search(r"(?i)skills:\s*(.+?)(?=sugest[ãa]o:|$)", result, re.DOTALL)
                    tip = re.search(r"(?i)sugest[ãa]o:\s*(.+)", result, re.DOTALL)

                    st.session_state.generated_summary = summary.group(1).strip() if summary else ""
                    st.session_state.generated_skills = skills.group(1).strip() if skills else ""
                    st.session_state.generated_tip = tip.group(1).strip() if tip else ""

                    if st.session_state.generated_summary:
                        st.subheader("📌 Resumo da Vaga")
                        st.write(st.session_state.generated_summary)

                    if st.session_state.generated_skills:
                        st.subheader("🧠 Skills Recomendadas")
                        st.write(st.session_state.generated_skills)

                    if st.session_state.generated_tip:
                        st.subheader("💡 Dica para seu Currículo")
                        st.write(st.session_state.generated_tip)

                    salvar_analise(
                        vaga=job_description,
                        resumo=st.session_state.generated_summary,
                        skills=st.session_state.generated_skills,
                        sugestao=st.session_state.generated_tip
                    )

                except Exception as e:
                    st.error(f"❌ Erro: {e}")

    if all([
        st.session_state.generated_summary,
        st.session_state.generated_skills,
        st.session_state.generated_tip
    ]):
        if st.button("📄 Exportar como PDF"):
            export_to_pdf(
                st.session_state.generated_summary,
                st.session_state.generated_skills,
                st.session_state.generated_tip,
                job_description
            )

# ------------------ PÁGINA DE DASHBOARD ------------------
elif pagina == "📊 Dashboard":
    st.title("📊 Histórico de Análises de Vagas")
    search = st.text_input("🔍 Buscar por palavra-chave:")

    # Requisição dos dados completos
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, vaga, resumo, skills, sugestao, favorito FROM analises ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    if search:
        rows = [r for r in rows if search.lower() in r[2].lower() or search.lower() in r[3].lower()]

    csv_data = []
    for analise_id, data, vaga, resumo, skills, sugestao, favorito in rows:
        cargo = extrair_titulo_vaga(resumo or vaga)
        with st.expander(f"📅 {data} — Vaga para {cargo}"):
            st.markdown(f"**🕒 Data/Hora:** `{data}`")
            st.markdown("**📄 Descrição Completa da Vaga:**")
            st.write(vaga)

            st.markdown("**📌 Resumo da Vaga:**")
            st.write(resumo)

            st.markdown("**🧠 Skills Recomendadas:**")
            st.write(skills)

            st.markdown("**💡 Sugestão para Currículo:**")
            st.write(sugestao)

            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("⭐ Favoritar" if not favorito else "✅ Favorito", key=f"fav_{analise_id}"):
                    toggle_favorito(analise_id, favorito)
                    st.rerun()

            csv_data.append({
                "Data": data,
                "Vaga": vaga,
                "Resumo": resumo,
                "Skills": skills,
                "Sugestão": sugestao,
                "Favorito": "Sim" if favorito else "Não"
            })
