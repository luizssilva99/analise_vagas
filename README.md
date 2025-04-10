# Analisar Descrição de Vaga para Currículo com IA 💼🤖

Este é um projeto desenvolvido com foco em integração entre Python, IA local e Streamlit. Ele permite que você cole a descrição de uma vaga e envie seu currículo em PDF ou TXT. A aplicação analisa os dois textos utilizando uma IA local (modelo **Gemma** rodando offline) e gera:

- Um **resumo** da vaga
- Uma lista de **skills** sugeridas
- Uma **dica personalizada** para seu currículo

## 📊 Objetivo do Projeto

Embora ferramentas como o ChatGPT já consigam fazer esse tipo de análise, o foco aqui foi **construir algo do zero**, com:

- Integração com IA local
- Interface interativa (via Streamlit)
- Banco de dados SQLite
- Geração de PDF para download

## 📅 Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit** (interface web)
- **SQLite3** (banco de dados local)
- **Gemma (3B ou 7B)** via API local (`http://localhost:1234`)
- **FPDF** e **pypdf** para leitura e geração de PDFs

## 🔧 Como Rodar Localmente

1. Clone este repositório:
```bash
git clone https://github.com/luizssilva99/analise_vagas.git
cd analise_vagas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Inicie o modelo Gemma (em ambiente local, como `text-generation-webui` com endpoint REST em `localhost:1234`)

4. Execute o app:
```bash
streamlit run app.py
```

## 👁 Funcionalidades

- Análise de vaga vs. currículo com IA local
- Identifica e extrai o cargo automaticamente
- Salva histórico de análises em banco local
- Marcar como favorito
- Exporta análise como PDF
- Dashboard com filtro por palavra-chave

## 📂 Estrutura do Projeto

```
.
├── app.py              # Interface principal Streamlit
├── database.py         # Gerenciamento do banco de dados SQLite
├── utils.py            # Funções auxiliares: IA, PDF, extração de texto
├── analises.db         # Arquivo SQLite (gerado automaticamente)
├── requirements.txt    # Lista de dependências
```

## 🚀 Prints Recomendados (para README ou LinkedIn)
- Tela de análise com resultado gerado
- Dashboard com histórico e função de favoritar
- Visual da exportação em PDF

## 📈 Possíveis Melhorias
- Suporte a mais idiomas
- Upload de vagas em PDF ou link
- Deploy remoto com UI otimizada

---

Criado com ❤️ por Luiz Fernando Silva Monteiro.

Este projeto é uma vitrine de aprendizado e integração entre IA + Python. Sinta-se à vontade para clonar, contribuir e compartilhar!

