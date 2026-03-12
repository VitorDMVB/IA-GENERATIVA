from openai import OpenAI
from dotenv import load_dotenv
from tools import data_atual
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Persona inicial
historico_mensagens = [
    {"role": "system", "content": "Você é um assistente educacional claro e direto."}
]


def salvar_json():
    with open("historico.json", "w", encoding="utf-8") as f:
        json.dump(historico_mensagens, f, indent=2, ensure_ascii=False)


def carregar_json():
    global historico_mensagens

    if os.path.exists("historico.json"):
        with open("historico.json", "r", encoding="utf-8") as f:
            historico_mensagens = json.load(f)


def salvar_historico(mensagem):
    historico_mensagens.append(mensagem)

    # limitar histórico a 10 mensagens
    if len(historico_mensagens) > 10:
        historico_mensagens.pop(1)

    salvar_json()


def chat(pergunta):
    salvar_historico({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=historico_mensagens
    )

    resposta_conteudo = resposta.choices[0].message.content

    salvar_historico({"role": "assistant", "content": resposta_conteudo})

    return resposta_conteudo


# carregar histórico salvo
carregar_json()


while True:
    pergunta = input("Você: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando o chat. Até mais!")
        break

    if pergunta.lower() == "limpar":
        historico_mensagens.clear()
        historico_mensagens.append(
            {"role": "system", "content": "Você é um assistente educacional claro e direto."}
        )
        salvar_json()
        print("Histórico apagado.")
        continue

    if "data" in pergunta.lower() or "dia" in pergunta.lower():
        resposta = "Hoje é " + str(data_atual())
        salvar_historico({"role": "assistant", "content": resposta})
        print("Assistente:", resposta)
        continue

    resposta = chat(pergunta)
    print("Assistente:", resposta)