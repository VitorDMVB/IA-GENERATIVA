# RAG Simplificado

import os


def load_conhecimento():
    """
    Carrega o arquivo de conhecimento.
    Usa caminho relativo baseado no local do arquivo,
    evitando erro de diretório no Windows.
    """
    base_dir = os.path.dirname(__file__)
    caminho = os.path.join(base_dir, "conhecimento", "conhecimento.txt")

    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def simple_retriever(query, conhecimento):
    """
    Busca trechos relevantes dentro da base de conhecimento.
    Divide o texto em seções separadas por duas quebras de linha.
    """
    query = query.lower()
    conhecimento = conhecimento.lower()

    relevant_chunks = []
    sections = conhecimento.split("\n\n")

    for section in sections:
        if query in section:
            relevant_chunks.append(section)

    if relevant_chunks:
        return "\n\n".join(relevant_chunks)
    else:
        return "Não encontrei informações relevantes na base de conhecimento."