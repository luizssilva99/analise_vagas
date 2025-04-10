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
- Tela inicial carregando o PDF e analisando a descrição da vaga
![image](https://github.com/user-attachments/assets/21e61850-82c5-4701-a323-42079968b1ec)

- Análise feita, ele comparou meu currículo com a descrição da vaga
![image](https://github.com/user-attachments/assets/dc045d43-d062-440b-9ba3-59d98652e105)

- Histórico de Analises de Vagas
![image](https://github.com/user-attachments/assets/e2331e60-b677-4aca-8ca7-a96b4a5d2c82)

![image](https://github.com/user-attachments/assets/a254aab4-ab78-4b3c-a95b-ca250793fe8b)
![image](https://github.com/user-attachments/assets/31b9f08e-4947-468e-aead-6aa8e403cc11)

Criado com ❤️ por Luiz Fernando Silva Monteiro.

Este projeto é uma vitrine de aprendizado e integração entre IA + Python. Sinta-se à vontade para clonar, contribuir e compartilhar!

