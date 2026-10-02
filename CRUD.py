from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from database import get_collection, serialize_document
from models.cliente import ClienteCreate
from models.reserva import ReservaCreate
from models.restaurante import RestauranteCreate

ENTIDADES = {
    "1": {
        "nome": "Restaurantes",
        "colecao": "restaurantes",
        "modelo": RestauranteCreate,
        "campos": {
            "nome": "Nome",
            "endereco": "Endereco",
            "telefone": "Telefone",
            "categoria": "Categoria",
        },
    },
    "2": {
        "nome": "Clientes",
        "colecao": "clientes",
        "modelo": ClienteCreate,
        "campos": {
            "nome": "Nome",
            "email": "Email",
            "telefone": "Telefone",
        },
    },
    "3": {
        "nome": "Reservas",
        "colecao": "reservas",
        "modelo": ReservaCreate,
        "campos": {
            "restaurante_id": "ID do restaurante",
            "cliente_id": "ID do cliente",
            "data": "Data (AAAA-MM-DD)",
            "horario": "Horario",
            "quantidade_pessoas": "Quantidade de pessoas",
        },
    },
}


def criar(collection, modelo, campos):
    dados = coletar_dados(modelo, campos)
    resultado = collection.insert_one(dados.model_dump(mode="json"))
    print(f"Registro criado com ID: {resultado.inserted_id}")


def listar(collection):
    documentos = [serialize_document(documento) for documento in collection.find()]
    if not documentos:
        print("Nenhum registro encontrado.")
        return

    for documento in documentos:
        print(documento)


def buscar(collection):
    object_id = ler_id()
    documento = collection.find_one({"_id": object_id})
    if documento is None:
        print("Registro nao encontrado.")
        return

    print(serialize_document(documento))


def atualizar(collection, modelo, campos):
    object_id = ler_id()
    if collection.find_one({"_id": object_id}) is None:
        print("Registro nao encontrado.")
        return

    dados = coletar_dados(modelo, campos)
    collection.update_one({"_id": object_id}, {"$set": dados.model_dump(mode="json")})
    print("Registro atualizado.")


def excluir(collection):
    object_id = ler_id()
    resultado = collection.delete_one({"_id": object_id})
    if resultado.deleted_count == 0:
        print("Registro nao encontrado.")
        return

    print("Registro excluido.")


def coletar_dados(modelo, campos):
    valores = {
        campo: input(f"{rotulo}: ").strip()
        for campo, rotulo in campos.items()
    }
    return modelo(**valores)


def ler_id():
    valor = input("ID: ").strip()
    if not ObjectId.is_valid(valor):
        raise ValueError("ID invalido.")
    return ObjectId(valor)


def menu_entidades():
    print("\n=== CRUD de Reservas ===")
    for opcao, entidade in ENTIDADES.items():
        print(f"{opcao}. {entidade['nome']}")
    print("0. Sair")
    return input("Escolha uma entidade: ").strip()


def menu_operacoes():
    print("\n1. Criar")
    print("2. Listar")
    print("3. Buscar por ID")
    print("4. Atualizar")
    print("5. Excluir")
    print("0. Voltar")
    return input("Escolha uma operacao: ").strip()


def executar():
    while True:
        opcao_entidade = menu_entidades()
        if opcao_entidade == "0":
            print("Encerrado.")
            return

        entidade = ENTIDADES.get(opcao_entidade)
        if entidade is None:
            print("Opcao invalida.")
            continue

        while True:
            opcao_operacao = menu_operacoes()
            if opcao_operacao == "0":
                break

            try:
                collection = get_collection(entidade["colecao"])
                if opcao_operacao == "1":
                    criar(collection, entidade["modelo"], entidade["campos"])
                elif opcao_operacao == "2":
                    listar(collection)
                elif opcao_operacao == "3":
                    buscar(collection)
                elif opcao_operacao == "4":
                    atualizar(collection, entidade["modelo"], entidade["campos"])
                elif opcao_operacao == "5":
                    excluir(collection)
                else:
                    print("Opcao invalida.")
            except ValidationError as erro:
                print(f"Dados invalidos: {erro}")
            except ValueError as erro:
                print(erro)
            except (RuntimeError, PyMongoError) as erro:
                print(f"Erro ao acessar o MongoDB: {erro}")


if __name__ == "__main__":
    executar()
