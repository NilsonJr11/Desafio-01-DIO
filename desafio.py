from datetime import datetime

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def validar_cpf(cpf: str) -> bool:
    digits = ''.join(filter(str.isdigit, cpf))
    return len(digits) == 11


def validar_nome(nome: str) -> bool:
    partes = nome.strip().split()
    return len(partes) >= 2 and all(p.isalpha() for p in partes)


def cpf_ja_registrado(cpf: str, lista_usuarios: list[dict]) -> bool:
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    return any(usuario['cpf'] == cpf_limpo for usuario in lista_usuarios)


def nome_ja_registrado(nome: str, lista_usuarios: list[dict]) -> bool:
    nome_normalizado = nome.strip().lower()
    return any(usuario['nome'].strip().lower() == nome_normalizado for usuario in lista_usuarios)


def coletar_nova_conta(lista_usuarios: list[dict]) -> dict:
    while True:
        cpf = input("Informe o CPF (apenas números): ").strip()
        if not validar_cpf(cpf):
            print("CPF inválido. Digite 11 números (apenas dígitos).")
            continue
        
        if cpf_ja_registrado(cpf, lista_usuarios):
            print("CPF já registrado. Este CPF já está cadastrado no sistema.")
            continue
            
        break

    while True:
        nome = input("Informe o nome completo: ").strip()
        if not validar_nome(nome):
            print("Informe nome e sobrenome, usando apenas letras.")
            continue
        
        if nome_ja_registrado(nome, lista_usuarios):
            print("Nome já registrado. Este nome já está cadastrado no sistema.")
            continue
            
        break

    data_nascimento = input("Informe a data de nascimento (AAAA-MM-DD): ").strip()
    endereco = input("Informe o endereço completo: ").strip()

    precedencia = len(lista_usuarios) + 1

    return {
        "precedencia": precedencia,
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
    }


def listar_usuarios(lista_usuarios: list[dict]) -> None:
    if not lista_usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    print("\n================ USUÁRIOS CADASTRADOS ================")

    usuarios_ordenados = sorted(lista_usuarios, key=lambda x: x['precedencia'])
    
    for usuario in usuarios_ordenados:
        print(f"#{usuario['precedencia']} | Nome: {usuario['nome']} | CPF: {usuario['cpf']} | Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("-" * 50)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    lista_usuarios: list[dict] = []

    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNova conta
    [u]\tListar usuários
    [q]\tSair
    => """

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "n":
            novo_usuario = coletar_nova_conta(lista_usuarios, AGENCIA)
            # Se um novo usuário foi criado, adiciona à lista; se retornou None, a conta foi adicionada a um usuário existente
            if novo_usuario:
                lista_usuarios.append(novo_usuario)
                print(f"\n=== Novo usuário #{novo_usuario['precedencia']} cadastrado com sucesso! ===")

        elif opcao == "u":
            listar_usuarios(lista_usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente.")


if __name__ == "__main__":
    main()
