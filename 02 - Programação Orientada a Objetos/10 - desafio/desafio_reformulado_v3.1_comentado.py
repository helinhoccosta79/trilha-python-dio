import textwrap # Importa o módulo textwrap para formatar strings, como remover espaços em branco e adicionar indentação.
from abc import ABC, abstractmethod # Importa as classes ABC (Abstract Base Class) e abstractmethod do módulo abc para criar classes abstratas e métodos abstratos.
from datetime import datetime # Importa o módulo datetime para trabalhar com datas e horas.

class Cliente: # Classe que representa um cliente.
    def __init__(self, endereco): # Método construtor da classe Cliente.
        self.endereco = endereco # Atributo que armazena o endereço do cliente.
        self.contas = [] # Atributo que armazena uma lista de contas bancárias do cliente.

    def realizar_transacao(self, conta, transacao): # Método para realizar uma transação bancária.
        transacao.registrar(conta) # Chama o método registrar da transação para processá-la na conta.

    def adicionar_conta(self, conta): # Método para adicionar uma conta à lista de contas do cliente.
        self.contas.append(conta) # Adiciona a conta à lista.

class PessoaFisica(Cliente): # Classe que representa um cliente pessoa física, herda da classe Cliente.
    def __init__(self, nome, data_nascimento, cpf, endereco): # Método construtor da classe PessoaFisica.
        super().__init__(endereco) # Chama o construtor da classe pai (Cliente) para inicializar o endereço.
        self.nome = nome # Atributo que armazena o nome da pessoa física.
        self.data_nascimento = data_nascimento # Atributo que armazena a data de nascimento da pessoa física.
        self.cpf = cpf # Atributo que armazena o CPF da pessoa física.

class Conta: # Classe que representa uma conta bancária.
    def __init__(self, numero, cliente): # Método construtor da classe Conta.
        self._saldo = 0 # Atributo que armazena o saldo da conta (privado por convenção).
        self._numero = numero # Atributo que armazena o número da conta (privado por convenção).
        self._agencia = "0001" # Atributo que armazena o número da agência (privado por convenção).
        self._cliente = cliente # Atributo que armazena o cliente titular da conta (privado por convenção).
        self._historico = Historico() # Atributo que armazena o histórico de transações da conta (privado por convenção).

    @classmethod # Decorador de método de classe, permite criar um método que pode ser chamado diretamente na classe sem precisar instanciar um objeto.
    def nova_conta(cls, cliente, numero): # Método de classe para criar uma nova conta.
        return cls(numero, cliente) # Retorna uma nova instância da classe Conta.

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def saldo(self): # Método getter para o saldo.
        return self._saldo # Retorna o saldo da conta.

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def numero(self): # Método getter para o número da conta.
        return self._numero # Retorna o número da conta.

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def agencia(self): # Método getter para o número da agência.
        return self._agencia # Retorna o número da agência.

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def cliente(self): # Método getter para o cliente titular da conta.
        return self._cliente # Retorna o cliente titular da conta.

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def historico(self): # Método getter para o histórico de transações da conta.
        return self._historico # Retorna o histórico de transações da conta.

    def sacar(self, valor): # Método para realizar um saque na conta.
        if valor <= 0: # Verifica se o valor do saque é inválido.
            print("\n>>> Operação falhou! O valor informado é inválido.") # Imprime mensagem de erro.
            return False # Retorna False para indicar que a operação falhou.

        if valor > self._saldo: # Verifica se o saldo é insuficiente para o saque.
            print("\n>>> Operação falhou! Você não tem saldo suficiente.") # Imprime mensagem de erro.
            return False # Retorna False para indicar que a operação falhou.

        self._saldo -= valor # Subtrai o valor do saque do saldo da conta.
        print("\n=== Saque realizado com sucesso! ===") # Imprime mensagem de sucesso.
        return True # Retorna True para indicar que a operação foi realizada com sucesso.

    def depositar(self, valor): # Método para realizar um depósito na conta.
        if valor <= 0: # Verifica se o valor do depósito é inválido.
            print("\n>>> Operação falhou! O valor informado é inválido.") # Imprime mensagem de erro.
            return False # Retorna False para indicar que a operação falhou.

        self._saldo += valor # Adiciona o valor do depósito ao saldo da conta.
        print("\n=== Depósito realizado com sucesso! ===") # Imprime mensagem de sucesso.
        return True # Retorna True para indicar que a operação foi realizada com sucesso.

class ContaCorrente(Conta): # Classe que representa uma conta corrente, herda da classe Conta.
    def __init__(self, numero, cliente, limite=500, limite_saques=3): # Método construtor da classe ContaCorrente.
        super().__init__(numero, cliente) # Chama o construtor da classe pai (Conta) para inicializar os atributos herdados.
        self._limite = limite # Atributo que armazena o limite da conta corrente (privado por convenção).
        self._limite_saques = limite_saques # Atributo que armazena o limite de saques da conta corrente (privado por convenção).

    def sacar(self, valor): # Método para realizar um saque na conta corrente (sobrescrito da classe pai).
        numero_saques = sum(1 for t in self.historico.transacoes if t["tipo"] == Saque.__name__) # Obtém o número de saques já realizados no histórico da conta.

        if valor > self._limite: # Verifica se o valor do saque excede o limite da conta corrente.
            print("\n>>> Operação falhou! O valor do saque excede o limite." # Imprime mensagem de erro.
            "O limite é R$ 500.00") # Imprime mensagem de erro.
            return False # Retorna False para indicar que a operação falhou.

        if numero_saques >= self._limite_saques: # Verifica se o número de saques já realizados atingiu o limite.
            print("\n>>> Operação falhou! Número máximo de saques excedido." # Imprime mensagem de erro.
            "Você só pode fazer 3 (três) saques.") # Imprime mensagem de erro.
            return False # Retorna False para indicar que a operação falhou.

        return super().sacar(valor) # Chama o método sacar da classe pai (Conta) para realizar o saque.

    def __str__(self): # Método especial que permite imprimir o objeto ContaCorrente de forma formatada.
        # Retorna uma string formatada com os dados da conta corrente.
        # Adiciona o número da agência, o número da conta e o nome do cliente, ambos formatados na string.
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico: # Classe para representar o histórico de transações de uma conta.
    def __init__(self): # Método construtor da classe Historico.
        self._transacoes = [] # Atributo que armazena a lista de transações (privado por convenção).

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def transacoes(self): # Método getter para a lista de transações.
        return self._transacoes # Retorna a lista de transações.

    def adicionar_transacao(self, transacao): # Método para adicionar uma transação ao histórico.
        self._transacoes.append({ # Adiciona um dicionário com os dados da transação à lista.
            "tipo": transacao.__class__.__name__, # Armazena o tipo da transação (nome da classe).
            "valor": transacao.valor, # Armazena o valor da transação.
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S") # Armazena a data e hora da transação formatadas.
        }) # Fecha o dicionário e o parêntese da chamada do método append.

class Transacao(ABC): # Classe abstrata que define o modelo para as transações bancárias.
    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    @abstractmethod # Decorador de método abstrato, indica que o método não possui implementação na classe base e deve ser implementado nas classes filhas.
    def valor(self): # Método abstrato para obter o valor da transação.
        pass # Não possui implementação na classe base.

    @abstractmethod # Decorador de método abstrato, indica que o método não possui implementação na classe base e deve ser implementado nas classes filhas.
    def registrar(self, conta): # Método abstrato para registrar a transação na conta.
        pass # Não possui implementação na classe base.

class Saque(Transacao): # Classe que representa um saque, herda da classe Transacao.
    def __init__(self, valor): # Método construtor da classe Saque.
        self._valor = valor # Atributo que armazena o valor do saque (privado por convenção).

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def valor(self): # Método getter para o valor do saque.
        return self._valor # Retorna o valor do saque.

    def registrar(self, conta): # Método para registrar o saque na conta.
        if conta.sacar(self.valor): # Chama o método sacar da conta para realizar o saque.
            conta.historico.adicionar_transacao(self) # Se o saque for realizado com sucesso, adiciona a transação ao histórico da conta.

class Deposito(Transacao): # Classe que representa um depósito, herda da classe Transacao.
    def __init__(self, valor): # Método construtor da classe Deposito.
        self._valor = valor # Atributo que armazena o valor do depósito (privado por convenção).

    @property # Decorador de propriedade, permite acessar o atributo como se fosse uma propriedade, sem precisar usar métodos get.
    def valor(self): # Método getter para o valor do depósito.
        return self._valor # Retorna o valor do depósito.

    def registrar(self, conta): # Método para registrar o depósito na conta.
        if conta.depositar(self.valor): # Chama o método depositar da conta para realizar o depósito.
            conta.historico.adicionar_transacao(self) # Se o depósito for realizado com sucesso, adiciona a transação ao histórico da conta.

def menu(): # Função para exibir o menu de opções.
    # String com o menu de opções formatado.
    menu = """
        ================ MENU ================
        [1]\tDepositar
        [2]\tSacar
        [3]\tExtrato
        [4]\tNovo usuário
        [5]\tNova conta
        [6]\tListar contas
        [0]\tSair

        >>> """ # Finaliza a string com o menu de opções.
    return input(textwrap.dedent(menu)) # Exibe o menu e retorna a opção escolhida pelo usuário.

def filtrar_cliente(cpf, clientes): # Função para buscar um cliente pelo CPF.
    return next((c for c in clientes if c.cpf == cpf), None) # Utiliza generator expression e next para encontrar o cliente com o CPF informado.

def escolher_conta(cliente): # Função para que o usuário escolha uma das contas do cliente para fazer alguma operação, caso o clliente tenha mais que uma conta corrente.
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    else:
        print("\nContas do cliente:")
        for i, conta in enumerate(cliente.contas):
            print(f"[{i + 1}] Agência: {conta.agencia} | C/C: {conta.numero}")

        while True: # O usuário deve escolher o número de sequência da conta na lista e não o número da conta corrente.
            try:
                escolha = int(input("Digite o número de sequência '[]' da conta para a operação: "))
                if 1 <= escolha <= len(cliente.contas):
                    return cliente.contas[escolha - 1]
                else:
                    print("Número de conta inválido. Tente novamente.")

            except ValueError:
                print("Entrada inválida. Digite um número.")

def depositar(clientes): # Função para realizar um depósito.
    cpf = input("Informe o CPF do cliente: ") # Solicita o CPF do cliente.
    cliente = filtrar_cliente(cpf, clientes) # Busca o cliente pelo CPF.

    if not cliente: # Verifica se o cliente foi encontrado.
        print("\n>>> Cliente não encontrado!") # Imprime mensagem de erro.
        return # Sai da função.

    conta = escolher_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: ")) # Solicita o valor do depósito.
    transacao = Deposito(valor) # Cria um objeto Deposito com o valor informado.

    cliente.realizar_transacao(conta, transacao) # Realiza a transação de depósito na conta do cliente.

def sacar(clientes): # Função para realizar um saque.
    cpf = input("Informe o CPF do cliente: ") # Solicita o CPF do cliente.
    cliente = filtrar_cliente(cpf, clientes) # Busca o cliente pelo CPF.

    if not cliente: # Verifica se o cliente foi encontrado.
        print("\n>>> Cliente não encontrado!") # Imprime mensagem de erro.
        return # Sai da função.

    conta = escolher_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: ")) # Solicita o valor do saque.
    transacao = Saque(valor) # Cria um objeto Saque com o valor informado.

    cliente.realizar_transacao(conta, transacao) # Realiza a transação de saque na conta do cliente.

def exibir_extrato(clientes): # Função para exibir o extrato de uma conta.
    cpf = input("Informe o CPF do cliente: ") # Solicita o CPF do cliente.
    cliente = filtrar_cliente(cpf, clientes) # Busca o cliente pelo CPF.

    if not cliente: # Verifica se o cliente foi encontrado.
        print("\n>>> Cliente não encontrado!") # Imprime mensagem de erro.
        return # Sai da função.

    conta = escolher_conta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================") # Imprime o cabeçalho do extrato.
    transacoes = conta.historico.transacoes # Obtém a lista de transações da conta.

    if not transacoes: # Verifica se a conta possui transações.
        print("Não foram realizadas movimentações.") # Imprime mensagem informando que não há transações.
    else: # Se a conta possuir transações, exibe cada uma delas.
        for transacao in transacoes: # Itera sobre a lista de transações.
            print(f"\n{transacao['tipo']}: R$ {transacao['valor']:.2f}") # Imprime o tipo e o valor da transação formatados.

    print(f"\nSaldo: R$ {conta.saldo:.2f}") # Imprime o saldo atual da conta formatado.
    print("==========================================") # Imprime o rodapé do extrato.

def criar_cliente(clientes): # Função para criar um novo cliente.
    cpf = input("Informe o CPF (somente número): ") # Solicita o CPF do cliente.
    if filtrar_cliente(cpf, clientes): # Verifica se já existe um cliente com o CPF informado.
        print("\n>>> Já existe cliente com esse CPF!") # Imprime mensagem de erro.
        return # Sai da função.

    nome = input("Informe o nome completo: ") # Solicita o nome do cliente.
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ") # Solicita a data de nascimento do cliente.
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ") # Solicita o endereço do cliente.

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco) # Cria um objeto PessoaFisica com os dados informados.
    clientes.append(cliente) # Adiciona o cliente à lista de clientes.

    print("\n=== Cliente criado com sucesso! ===") # Imprime mensagem de sucesso.

def criar_conta(numero_conta, clientes, contas): # Função para criar uma nova conta.
    cpf = input("Informe o CPF do cliente: ") # Solicita o CPF do cliente.
    cliente = filtrar_cliente(cpf, clientes) # Busca o cliente pelo CPF.

    if not cliente: # Verifica se o cliente foi encontrado.
        print("\n>>> Cliente não encontrado, fluxo de criação de conta encerrado!") # Imprime mensagem de erro.
        return # Sai da função.

    conta = ContaCorrente.nova_conta(cliente, numero_conta) # Cria um objeto ContaCorrente com os dados informados.
    contas.append(conta) # Adiciona a conta à lista de contas.
    cliente.adicionar_conta(conta) # Adiciona a conta à lista de contas do cliente.

    print("\n=== Conta criada com sucesso! ===") # Imprime mensagem de sucesso.

def listar_contas(contas): # Função para listar todas as contas existentes.
    for conta in contas: # Itera sobre a lista de contas.
        print("=" * 40) # Imprime uma linha com 100 "=" para separar as informações de cada conta.
        print(textwrap.dedent(str(conta))) # Imprime os dados da conta formatados.

def main(): # Função principal do programa.
    clientes = [] # Lista para armazenar os clientes.
    contas = [] # Lista para armazenar as contas.

    while True: # Loop principal do programa.
        opcao = menu() # Exibe o menu e solicita a opção do usuário.

        if opcao == "1": # Se a opção for 1 (Depositar).
            depositar(clientes) # Chama a função depositar.
        elif opcao == "2": # Se a opção for 2 (Sacar).
            sacar(clientes) # Chama a função sacar.
        elif opcao == "3": # Se a opção for 3 (Extrato).
            exibir_extrato(clientes) # Chama a função exibir_extrato.
        elif opcao == "4": # Se a opção for 4 (Novo usuário).
            criar_cliente(clientes) # Chama a função criar_cliente.
        elif opcao == "5": # Se a opção for 5 (Nova conta).
            numero_conta = len(contas) + 1 # Gera o número da nova conta.
            criar_conta(numero_conta, clientes, contas) # Chama a função criar_conta.
        elif opcao == "6": # Se a opção for 6 (Listar contas).
            listar_contas(contas) # Chama a função listar_contas.
        elif opcao == "0": # Se a opção for 0 (Sair).
            print("\n>>> Muito obrigado por utilizar nossos sistemas.\n>>> Até mais!") # Imprime mensagem de agradecimento e despedida.
            break # Sai do loop principal.
        else: # Se a opção for inválida.
            print("\n>>> Operação inválida, por favor selecione novamente a operação desejada.") # Imprime mensagem de erro.

main() # Chama a função principal para iniciar o programa.
