# Chatbot RAG para restaurante

Assistente corporativo desenvolvido com arquitetura **Frontend + Backend**, utilizando **RAG (Retrieval-Augmented Generation)** com LangChain, ChromaDB e Ollama.

O sistema responde perguntas sobre planejamento estratégico do restaurante com base em uma base de conhecimento vetorizada.

---

# Tecnologias Utilizadas

## Backend
- Python 3.10+
- Flask
- Flask-CORS
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Ollama (modelo `phi3:mini`)

## Frontend
- HTML5
- CSS3
- JavaScript (Fetch API)

---

# Como Rodar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd chatbot-restaurante
```

---

## 2️⃣ Criar ambiente virtual

### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Instalar dependências

```bash
pip install flask flask-cors langchain langchain-chroma langchain-community langchain-ollama chromadb sentence-transformers
```

---

##  4️⃣ Criar o Banco Vetorial (ChromaDB)

Antes de rodar o backend, é necessário gerar o banco vetorial.

Execute:

```bash
python criar_db.py
```

Esse script irá:

- Ler os documentos da pasta base
- Gerar embeddings com HuggingFace
- Criar o banco vetorial na pasta `db/`

⚠️ A pasta `db/` é gerada automaticamente e não deve ser versionada no GitHub.

---

##  5️⃣ Instalar e Configurar o Ollama

Baixe o Ollama:
https://ollama.com/download

Depois execute:

```bash
ollama pull phi3:mini
```

Teste:

```bash
ollama run phi3:mini
```

(Use CTRL+C para sair)

---

##  6️⃣ Rodar o Backend

```bash
python main.py
```

O backend agora estará aguardando requisições na rota:

```
POST http://localhost:5000/perguntar
```

---

##  7️⃣ Rodar o Frontend

Abra o arquivo:

```
index.html
```

no navegador.

Digite uma pergunta e o sistema enviará a requisição para o backend automaticamente.

---

##  Como Funciona

1. Usuário faz pergunta no chat
2. JavaScript envia requisição POST para o Flask
3. Backend:
   - Gera embedding da pergunta
   - Busca os chunks mais relevantes no ChromaDB
   - Monta o prompt com base na base recuperada
   - Envia para o modelo `phi3:mini` via Ollama
4. Resposta é retornada em JSON
5. Interface exibe a resposta no chat

---

##  Arquitetura

Frontend (HTML/CSS/JS)  
⬇  
API REST (Flask)  
⬇  
RAG (ChromaDB + Embeddings)  
⬇  
LLM Local (Ollama)

---

##  Observações Importantes

- O Ollama precisa estar rodando localmente.
- A pasta `db/` deve ser gerada antes de rodar o backend.
- A porta 5000 deve estar disponível.
- Caso o frontend não conecte, verifique se o backend está ativo.
