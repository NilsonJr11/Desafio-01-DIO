from datetime import datetime
import json

# Constantes do sistema
MAX_CONTAS_POR_USUARIO = 3
LIMITE_SAQUES = 3

# Funções de negócio
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


def cpf_ja_registrado(cpf: str, lista_usuarios: list[dict]) -> bool:
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    return any(usuario['cpf'] == cpf_limpo for usuario in lista_usuarios)


def nome_ja_registrado(nome: str, lista_usuarios: list[dict]) -> bool:
    nome_normalizado = nome.strip().lower()
    return any(usuario['nome'].strip().lower() == nome_normalizado for usuario in lista_usuarios)


def encontrar_usuario_por_cpf(cpf: str, lista_usuarios: list[dict]) -> dict | None:
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    for usuario in lista_usuarios:
        if usuario['cpf'] == cpf_limpo:
            return usuario
    return None


def criar_conta_para_usuario(usuario: dict, agencia: str) -> dict:
    contas = usuario.get('contas', [])
    
    if len(contas) >= MAX_CONTAS_POR_USUARIO:
        print(f"\n@@@ Operação falhou! Usuário já possui o máximo de {MAX_CONTAS_POR_USUARIO} contas. @@@")
        return None
    
    numero_conta = f"{agencia}-{len(contas) + 1:06d}"
    tipo_conta = "Corrente" if len(contas) == 0 else "Poupança"
    
    nova_conta = {
        "numero": numero_conta,
        "agencia": agencia,
        "saldo": 0.0,
        "tipo": tipo_conta,
        "criada_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    contas.append(nova_conta)
    usuario['contas'] = contas
    
    return nova_conta


def listar_agencias() -> list[dict]:
    return [
        {"codigo": "0001", "nome": "Agência Central", "endereco": "Rua Principal, 100", "cidade": "São Paulo", "estado": "SP"},
        {"codigo": "0002", "nome": "Agência Norte", "endereco": "Avenida Norte, 200", "cidade": "São Paulo", "estado": "SP"},
        {"codigo": "0003", "nome": "Agência Sul", "endereco": "Rua Sul, 300", "cidade": "Rio de Janeiro", "estado": "RJ"},
    ]


def exibir_agencia_selecionada(agencia_codigo: str):
    agencias = listar_agencias()
    agencia = next((a for a in agencias if a['codigo'] == agencia_codigo), None)
    if agencia:
        print(f"\n=== AGÊNCIA SELECIONADA ===")
        print(f"Nome: {agencia['nome']}")
        print(f"Código: {agencia['codigo']}")
        print(f"Endereço: {agencia['endereco']}, {agencia['cidade']} - {agencia['estado']}")
        print("============================\n")


def selecionar_agencia() -> str:
    agencias = listar_agencias()
    print("\n=== Selecione uma Agência ===")
    for i, agencia in enumerate(agencias, 1):
        print(f"[{i}] {agencia['nome']} (Código: {agencia['codigo']})")
        print(f"    Endereço: {agencia['endereco']}, {agencia['cidade']} - {agencia['estado']}")
    
    while True:
        try:
            opcao = int(input("\nDigite o número da agência: ")) - 1
            if 0 <= opcao < len(agencias):
                return agencias[opcao]['codigo']
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Digite um número válido.")


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
        if len(nome.strip().split()) < 2:
            print("Informe nome e sobrenome.")
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
        "contas": []
    }


def listar_usuarios(lista_usuarios: list[dict]) -> None:
    if not lista_usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    print("\n================ USUÁRIOS CADASTRADOS ================")
    usuarios_ordenados = sorted(lista_usuarios, key=lambda x: x['precedencia'])
    
    for usuario in usuarios_ordenados:
        print(f"#{usuario['precedencia']} | Nome: {usuario['nome']} | CPF: {usuario['cpf']}")
        print(f"Nascimento: {usuario['data_nascimento']} | Endereço: {usuario['endereco']}")
        
        if 'agencia' in usuario:
            print(f"Agência: {usuario['agencia']}")
        
        contas = usuario.get('contas', [])
        if contas:
            print(f"Contas ({len(contas)}/{MAX_CONTAS_POR_USUARIO}):")
            for conta in contas:
                print(f"  - {conta['numero']} ({conta['tipo']}) | Saldo: R$ {conta['saldo']:.2f}")
        else:
            print("Nenhuma conta associada.")
        print("-" * 50)


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    lista_usuarios: list[dict] = []
    usuario_logado = None
    agencia_selecionada = "0001"

    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNovo usuário
    [u]\tListar usuários
    [a]\tSelecionar agência
    [v]\tValidar usuário por CPF
    [c]\tCriar conta para usuário
    [q]\tSair
    => """

    while True:
        # Exibir agência selecionada prominentemente
        exibir_agencia_selecionada(agencia_selecionada)
        
        if usuario_logado:
            print(f"=== Usuário Logado: {usuario_logado['nome']} ===")
            contas = usuario_logado.get('contas', [])
            print(f"Contas: {len(contas)}/{MAX_CONTAS_POR_USUARIO} (CPF: {usuario_logado['cpf']})")
        
        opcao = input(menu).strip().lower()

        if opcao == "d":
            if not usuario_logado:
                print("Por favor, valide um usuário primeiro.")
                continue
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            if not usuario_logado:
                print("Por favor, valide um usuário primeiro.")
                continue
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
            novo_usuario = coletar_nova_conta(lista_usuarios)
            novo_usuario['agencia'] = agencia_selecionada
            lista_usuarios.append(novo_usuario)
            print(f"\n=== Novo usuário #{novo_usuario['precedencia']} cadastrado com sucesso! ===")
            print(f"Agência: {agencia_selecionada}")

        elif opcao == "u":
            listar_usuarios(lista_usuarios)

        elif opcao == "a":
            agencia_selecionada = selecionar_agencia()
            print(f"\n=== Agência {agencia_selecionada} selecionada! ===")

        elif opcao == "v":
            cpf = input("Digite o CPF para validação: ").strip()
            usuario = encontrar_usuario_por_cpf(cpf, lista_usuarios)
            if usuario:
                usuario_logado = usuario
                print(f"\n=== Usuário {usuario['nome']} validado com sucesso! ===")
                print(f"CPF: {usuario['cpf']} | Contas: {len(usuario.get('contas', []))}/{MAX_CONTAS_POR_USUARIO}")
            else:
                print("\n@@@ CPF não encontrado no sistema. @@@")
                usuario_logado = None

        elif opcao == "c":
            if not usuario_logado:
                print("Por favor, valide um usuário primeiro.")
                continue
            
            nova_conta = criar_conta_para_usuario(usuario_logado, agencia_selecionada)
            if nova_conta:
                print(f"\n=== Conta {nova_conta['numero']} criada com sucesso! ===")
                print(f"Agência: {agencia_selecionada} | CPF: {usuario_logado['cpf']}")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente.")


if __name__ == "__main__":
    main()




