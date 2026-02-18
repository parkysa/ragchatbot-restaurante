from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# configuração do servidor 
app = Flask(__name__)
CORS(app)

CAMINHO_DB = "db"

prompt_template = """
Você é um assistente corporativo.
Responda de forma objetiva e direta.
Use apenas as informações da base de conhecimento.
Se a pergunta pedir um valor específico, responda apenas com o valor e uma frase curta.
Não inclua informações adicionais que não foram solicitadas.

Pergunta:
{pergunta}

Base de conhecimento:
{base_conhecimento}
"""

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json()
    pergunta = dados.get("pergunta")

    if not pergunta:
        return jsonify({"resposta": "Pergunta não enviada."})

    # carregar o banco de dados
    db = Chroma(
        persist_directory=CAMINHO_DB,
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )

    resultados = db.similarity_search_with_relevance_scores(pergunta, k=2)

    if len(resultados) == 0:
        return jsonify({"resposta": "Não consegui encontrar informações relevantes na base."})

    textos_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        textos_resultado.append(texto)

    base_conhecimento = "\n\n----\n\n".join(textos_resultado)

    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({
        "pergunta": pergunta,
        "base_conhecimento": base_conhecimento
    })

    modelo = ChatOllama(
        model="phi3:mini",
        temperature=0.2
    )

    texto_resposta = modelo.invoke(prompt).content

    return jsonify({"resposta": texto_resposta})

if __name__ == "__main__":
    app.run(debug=True)
