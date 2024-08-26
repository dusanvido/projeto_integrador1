import mysql.connector
from tabulate import tabulate

# Conexão com o banco de dados mysql
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="19782002",
        database="projeto"
    )
    print("Conexão bem sucedida!")
    print()
    print('+----------------------------------------------------------------------+')
    print('|                                                                      |')
    print('|                    PROGRAMA DE GESTÃO DE ESTOQUE                     |')
    print('|                                                                      |')
    print('|Nando Balzaneli, Gabriel Pinheiro, Eduardo Sanvido, Matheus Polizinani|')
    print('|                                                                      |')
    print('|                       FASE 2 PROFESSOR CHACON                        |')
    print('|                                                                      |')
    print('+----------------------------------------------------------------------+')
    print()

except mysql.connector.Error as e:
    print("Erro ao conectar ao banco de dados:", e)
    exit(1)

def ler_produto_codigo():
    print()
    codigo = int(input('Digite o código do produto: '))

    cursor = db_connection.cursor()

    # Verificar se o produto com o código fornecido existe
    cursor.execute("SELECT * FROM produtos WHERE codigo = %s", (codigo,))
    produto = cursor.fetchone()

    if produto is None:
        print(f'O produto com código {codigo} não foi encontrado!')
    else:
        # Extrair os dados do produto existente
        codigo = produto[0]
        nome = produto[1]
        descricao = produto[2]
        cp = float(produto[3])
        cf = float(produto[4])
        cv = float(produto[5])
        iv = float(produto[6])
        ml = float(produto[7])

        # Calculo do preço de venda
        pv = cp / (1 - ((cf + cv + iv + ml) / 100))
        pv = round(pv, 2)

        # Calculo da receita bruta
        rc = round(pv - cp, 2)

        # Calculo dos outros custos
        oc = round(((cf * pv) / 100) + ((cv * pv) / 100) + ((iv * pv) / 100), 2)

        # Calculo da rentabilidade
        rt = round(rc - oc, 2)

        # Calculo dos impostos
        ip = round((iv * pv) / 100, 2)

        # Classificação de lucro
        if ml > 20:
            classificacao = 'Alto'
        elif ml > 10 and ml <= 20:
            classificacao = 'Médio'
        elif ml > 0 and ml <= 10:
            classificacao = 'Baixo'
        elif ml == 0:
            classificacao = 'Equilíbrio'
        else:
            classificacao = 'Prejuízo'

        # Exibir os dados do produto
        lista_produtos = [
            ['Descrição', 'Valor', '%'],
            ['Produto', nome, ''],
            ['Descricao', descricao, ''],
            ['Codigo', codigo, ''],
            ['A. Preço de venda', pv, '100%'],
            ['B. Custo de Aquisição (Fornecedor)', round(cp, 2), round((cp / pv) * 100, 2)],
            ['C. Receita Bruta', rc, round((rc / pv) * 100, 2)],
            ['D. Custo Fixo/Administrativo', round((cf * pv) / 100, 2), cf],
            ['E. Comissão de Vendas', round((cv * pv) / 100, 2), cv],
            ['F. Impostos', round((iv * pv) / 100, 2), iv],
            ['G. Outros Custos', oc, round((oc / pv) * 100, 2)],
            ['H. Rentabilidade', rt, round((rt / pv) * 100, 2)],
            ['I. Classificação de Lucro', classificacao, '']
        ]

        print()
        print(tabulate(lista_produtos, headers='firstrow'))
        print()

def listar_produtos():
    cursor = db_connection.cursor()

    # Consulta para obter todos os produtos
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Não há produtos cadastrados.")
        return

    # Cabeçalho da tabela
    headers = ['Descrição', 'Valor', '%']

    # Lista para armazenar os dados dos produtos
    lista_produtos = []

    for produto in produtos:
        codigo = produto[0]
        nome = produto[1]
        descricao = produto[2]
        cp = float(produto[3])
        cf = float(produto[4])
        cv = float(produto[5])
        iv = float(produto[6])
        ml = float(produto[7])

        # Calculo do preço de venda
        pv = cp / (1 - ((cf + cv + iv + ml) / 100))
        pv = round(pv, 2)

        # Calculo da receita bruta
        rc = round(pv - cp, 2)

        # Calculo dos outros custos
        oc = round(((cf * pv) / 100) + ((cv * pv) / 100) + ((iv * pv) / 100), 2)

        # Calculo da rentabilidade
        rt = round(rc - oc, 2)

        # Calculo dos impostos
        ip = round((iv * pv) / 100, 2)

        # Classificação de lucro
        if ml > 20:
            classificacao = 'Alto'
        elif ml > 10 and ml <= 20:
            classificacao = 'Médio'
        elif ml > 0 and ml <= 10:
            classificacao = 'Baixo'
        elif ml == 0:
            classificacao = 'Equilíbrio'
        else:
            classificacao = 'Prejuízo'

        # Adiciona os dados do produto à lista
        lista_produtos.append(['', '', ''])
        lista_produtos.append(['Produto', nome, ''])
        lista_produtos.append(['Descricao', descricao, ''])
        lista_produtos.append(['Codigo', codigo, ''])
        lista_produtos.append(['A. Preço de venda', pv, '100%'])
        lista_produtos.append(['B. Custo de Aquisição (Fornecedor)', round(cp, 2), round((cp / pv) * 100, 2)])
        lista_produtos.append(['C. Receita Bruta', rc, round((rc / pv) * 100, 2)])
        lista_produtos.append(['D. Custo Fixo/Administrativo', round((cf * pv) / 100, 2), cf])
        lista_produtos.append(['E. Comissão de Vendas', round((cv * pv) / 100, 2), cv])
        lista_produtos.append(['F. Impostos', round((iv * pv) / 100, 2), iv])
        lista_produtos.append(['G. Outros Custos', oc, round((oc / pv) * 100, 2)])
        lista_produtos.append(['H. Rentabilidade', rt, round((rt / pv) * 100, 2)])
        lista_produtos.append(['I. Classificação de Lucro', classificacao, ''])

    # Exibe os produtos em formato tabular
    print()
    print(tabulate(lista_produtos, headers=headers))
    print()

def inserir_produto():
    print()
    codigo = int(input('Digite o código do produto: '))
    nome = input('Digite o nome do produto: ')
    descricao = input('Digite a descrição do produto: ')
    cp = float(input('Digite o custo do produto: '))
    cf = float(input('Digite o custo fixo/administrativo: '))
    cv = float(input('Digite a comissão de vendas: '))
    iv = float(input('Digite os impostos: '))
    ml = float(input('Digite a margem de lucro: '))

    cursor = db_connection.cursor()

    try:
        # Insere o novo produto no banco de dados
        cursor.execute("INSERT INTO produtos (codigo, nome, descricao, cp, cf, cv, iv, ml) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (codigo, nome, descricao, cp, cf, cv, iv, ml))
        db_connection.commit()
        print()
        print("Produto inserido com sucesso.")
        print()
    except mysql.connector.Error as e:
        print()
        print("Erro ao inserir produto:", e)
        print()

def alterar_produto():
    print()
    codigo = int(input('Digite o código do produto que deseja alterar: '))
    print()

    cursor = db_connection.cursor()

    # Verificar se o produto com código fornecido existe
    cursor.execute("SELECT * FROM produtos WHERE codigo = %s", (codigo,))
    produto = cursor.fetchone()

    if produto is None:
        print(f'O produto com código {codigo} não foi encontrado!')
    else:
        print("Escolha a opção que deseja alterar:")
        print("1. Todos os dados")
        print("2. Nome")
        print("3. Descrição")
        print("4. Custo")
        print("5. Custo fixo/administrativo")
        print("6. Comissão de vendas")
        print("7. Impostos")
        print("8. Margem de lucro")
        print()
        opcao = input("Opção: ")
        print()

        try:
            if opcao == '1':
                # Altera todos os dados do produto
                nome = input('Novo nome: ')
                descricao = input('Nova descrição: ')
                cp = float(input('Novo custo: '))
                cf = float(input('Novo custo fixo/administrativo: '))
                cv = float(input('Nova comissão de vendas: '))
                iv = float(input('Novos impostos: '))
                ml = float(input('Nova Margem de lucro: '))

                cursor.execute("UPDATE produtos SET nome = %s, descricao = %s, cp = %s, cf = %s, cv = %s, iv = %s, ml = %s WHERE codigo = %s",
                              (nome, descricao, cp, cf, cv, iv, ml, codigo))
                db_connection.commit()
                print()
                print('Produto alterado com sucesso!')
                print()
            elif opcao in ['2', '3', '4', '5', '6', '7', '8']:
                # Altera apenas o dado escolhido
                nome = produto[1]
                descricao = produto[2]
                cp = produto[3]
                cf = produto[4]
                cv = produto[5]
                iv = produto[6]
                ml = produto[7]

                if opcao == '2':
                    nome = input('Novo nome: ')
                elif opcao == '3':
                    descricao = input('Nova descrição: ')
                elif opcao == '4':
                    cp = float(input('Novo custo: '))
                elif opcao == '5':
                    cf = float(input('Novo custo fixo/administrativo: '))
                elif opcao == '6':
                    cv = float(input('nova comissão de vendas: '))
                elif opcao == '7':
                    iv = float(input('Novos impostos: '))
                elif opcao == '8':
                    ml = float(input('Nova margem de lucro: '))

                # Atualiza apenas o dado escolhido
                cursor.execute("UPDATE produtos SET nome = %s, descricao = %s, cp = %s, cf = %s, cv = %s, iv = %s, ml = %s WHERE codigo = %s",
                              (nome, descricao, cp, cf, cv, iv, ml, codigo))
                
                db_connection.commit()
                print()
                print("Produto alterado com sucesso!")
                print()
            else:
                print()
                print("Opção inválida.")
                print()
        except mysql.connector.Error as e:
            print()
            print("Erro ao alterar o produto:", e)
            print()

def excluir_produto():
    print()
    codigo = int(input('Digite o código do produto que deseja excluir: '))

    cursor = db_connection.cursor()

    # Verifica se o produto com código fornecido existe
    cursor.execute("SELECT * FROM produtos WHERE codigo = %s", (codigo,))
    produto = cursor.fetchone()

    if produto is None:
        print()
        print(f'O produto com código {codigo} não foi encontrado!')
        print()
    else:
        try:
            # Remove o produto do banco de dados
            cursor.execute("DELETE FROM produtos WHERE codigo = %s", (codigo,))
            db_connection.commit()
            print()
            print("Produto excluido com sucesso.")
            print()
        except mysql.connector.Error as e:
            print()
            print("Erro ao excluir produto:", e)
            print()

def exibir_produtos():
    cursor = db_connection.cursor()

    # Consulta para obter todos os produtos
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Não há produtos cadastrados.")
        return
    
    # Cabeçalho da tabela
    headers = ['Descrição', 'Valor', '%', 'Classificação de Lucro']

    # Lista para armazenar os dados dos produtos
    lista_produtos = []

    for produto in produtos:
        codigo = produto[0]
        nome = produto[1]
        descricao = produto[2]
        cp = float(produto[3])
        cf = float(produto[4])
        cv = float(produto[5])
        iv = float(produto[6])
        ml = float(produto[7])

        # Calculo do preço de venda
        pv = cp / (1 - ((cf + cv + iv + ml) / 100))
        pv = round(pv, 2)

        # Calculo dos outros custos
        oc = round(((cf * pv) / 100) + ((cv * pv) / 100) + ((iv * pv) / 100), 2)

        # Calculo da rentabilidade
        rt = round(pv - cp - oc, 2)

        # Classificação de lucro
        if ml > 20:
            classificacao = 'Alto'
        elif ml > 10 and ml <= 20:
            classificacao = 'Médio'
        elif ml > 0 and ml <= 10:
            classificacao = 'Baixo'
        elif ml == 0:
            classificacao = 'Equilíbrio'
        else:
            classificacao = 'Prejuízo'

        # Adiciona os dados do produto à lista
        lista_produtos.append([descricao, pv, rt, classificacao])

    print()
    print(tabulate(lista_produtos, headers=headers))
    print()

# Menu de opções completo
while True:
    print("1. Consultar produto existente pelo código")
    print("2. Listar todos os produtos")
    print("3. Inserir novo produto")
    print("4. Alterar produto")
    print("5. Excluir produto")
    print("6. Exibir preços de venda e margens de lucro")
    print("7. Sair")
    print()

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        ler_produto_codigo()
    elif opcao == '2':
        listar_produtos()
    elif opcao == '3':
        inserir_produto()
    elif opcao == '4':
        alterar_produto()
    elif opcao == '5':
        excluir_produto()
    elif opcao == '6':
        exibir_produtos()
    elif opcao == '7':
        break
    else:
        print("Opção inválida. Tente novamente.")

db_connection.close()

