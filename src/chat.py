from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Faça sua pergunta (digite 'sair' para encerrar).\n")

    while True:
        try:
            pergunta = input("PERGUNTA: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando o chat.")
            return

        if not pergunta:
            continue

        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Encerrando o chat.")
            return

        try:
            resposta = chain.invoke(pergunta)
        except Exception as erro:
            print(f"Erro ao responder: {erro}\n")
            continue

        print(f"RESPOSTA: {resposta}\n")

if __name__ == "__main__":
    main()