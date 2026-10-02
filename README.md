# API de Reservas de Restaurantes

API REST didática para o CRUD de restaurantes, clientes e reservas. Os dados são armazenados em três coleções MongoDB: `restaurantes`, `clientes` e `reservas`.

## Requisitos

- Python 3.10 ou superior
- MongoDB local ou uma instância MongoDB Atlas

## Instalação

No PowerShell, na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate` depois de criá-lo.

## Configuração do MongoDB

Defina a URI de conexão e, opcionalmente, o nome do banco. O nome padrão é `reserva_cariri`.

PowerShell:

```powershell
$env:MONGODB_URI = "mongodb+srv://usuario:senha@cluster.exemplo.mongodb.net/?retryWrites=true&w=majority"
$env:MONGODB_DATABASE = "reserva_cariri"
```

Linux ou macOS:

```bash
export MONGODB_URI="mongodb+srv://usuario:senha@cluster.exemplo.mongodb.net/?retryWrites=true&w=majority"
export MONGODB_DATABASE="reserva_cariri"
```

Para MongoDB local, a URI pode ser `mongodb://localhost:27017`. No Atlas, configure também o acesso de rede para permitir a conexão do seu ambiente.

## Execução local

Com o ambiente virtual ativado e as variáveis configuradas:

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://localhost:8000`. A documentação interativa do FastAPI fica em `http://localhost:8000/docs`.

### CRUD pelo terminal

Também é possível usar o menu interativo no terminal, com as mesmas variáveis de ambiente e o mesmo banco:

```bash
python CRUD.py
```

Escolha uma entidade e depois uma operação. Para reservas, informe a data no formato `AAAA-MM-DD` e use os IDs do restaurante e do cliente cadastrados.

## Endpoints

| Método | Endpoint | Ação |
| --- | --- | --- |
| POST | `/restaurantes` | Criar restaurante |
| GET | `/restaurantes` | Listar restaurantes |
| GET | `/restaurantes/{id}` | Buscar restaurante |
| PUT | `/restaurantes/{id}` | Atualizar restaurante |
| DELETE | `/restaurantes/{id}` | Excluir restaurante |
| POST | `/clientes` | Criar cliente |
| GET | `/clientes` | Listar clientes |
| GET | `/clientes/{id}` | Buscar cliente |
| PUT | `/clientes/{id}` | Atualizar cliente |
| DELETE | `/clientes/{id}` | Excluir cliente |
| POST | `/reservas` | Criar reserva |
| GET | `/reservas` | Listar reservas |
| GET | `/reservas/{id}` | Buscar reserva |
| PUT | `/reservas/{id}` | Atualizar reserva |
| DELETE | `/reservas/{id}` | Excluir reserva |

Os endpoints `PUT` recebem todos os campos da entidade. Um ID malformado retorna `400`; um ID válido que não existe retorna `404`. A exclusão bem-sucedida retorna `204` sem corpo.

## Exemplos JSON

Criar um restaurante com `POST /restaurantes`:

```json
{
  "nome": "Sabor do Cariri",
  "endereco": "Rua Central, 100",
  "telefone": "(88) 99999-1234",
  "categoria": "Regional"
}
```

Resposta `201 Created`:

```json
{
  "id": "66f1a5b208a80f83720c1234",
  "nome": "Sabor do Cariri",
  "endereco": "Rua Central, 100",
  "telefone": "(88) 99999-1234",
  "categoria": "Regional"
}
```

Criar um cliente com `POST /clientes`:

```json
{
  "nome": "Maria da Silva",
  "email": "maria@example.com",
  "telefone": "(88) 98888-4321"
}
```

Criar uma reserva com `POST /reservas`, usando os IDs retornados pelos cadastros:

```json
{
  "restaurante_id": "66f1a5b208a80f83720c1234",
  "cliente_id": "66f1a5b208a80f83720c5678",
  "data": "2026-10-20",
  "horario": "19:30",
  "quantidade_pessoas": 4
}
```

Resposta `201 Created`:

```json
{
  "id": "66f1a5b208a80f83720c9999",
  "restaurante_id": "66f1a5b208a80f83720c1234",
  "cliente_id": "66f1a5b208a80f83720c5678",
  "data": "2026-10-20",
  "horario": "19:30",
  "quantidade_pessoas": 4
}
```

A reserva armazena `restaurante_id` e `cliente_id` como referências simples; não verifica se esses documentos existem.

Para listar, buscar, atualizar ou excluir, use o método HTTP e o ID na URL conforme a tabela. Por exemplo, `GET /restaurantes/66f1a5b208a80f83720c1234` retorna um restaurante no mesmo formato do exemplo de criação.

## Publicação na Vercel

O arquivo `vercel.json` configura `main.py` como função Python e direciona as rotas para a aplicação FastAPI. Importe o projeto na Vercel e configure `MONGODB_URI` e `MONGODB_DATABASE` em **Settings > Environment Variables**. Faça um novo deploy após configurar as variáveis. A conexão usa uma instância reutilizada entre execuções quando possível.
