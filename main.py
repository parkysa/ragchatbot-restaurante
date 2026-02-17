from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama

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


def perguntar():
    pergunta = input("Escreva sua pergunta: ")

    # carregar o banco de dados
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

    # comparar a pergunta do usuario (embedding) com o meu banco de dados. (k é o numero de chunk)
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=2)
    if len(resultados) == 0:
        print("Não consegui encontrar informações relevantes na base")
        return
    
    # extrai só o texto de cada chunk e coloca numa lista
    textos_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        textos_resultado.append(texto)
    
    # junta toda a lista de textos numa string com um separador
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)
    
    #passando os valores pro prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})

    modelo = ChatOllama(
        model="phi3:mini",
        temperature=0.2 # nivel de criatividade
    )

    # manda prompt pro ollama e pega só o texto de resposta
    texto_resposta = modelo.invoke(prompt).content

    print("Resposta da IA:", texto_resposta)

perguntar()