# Logger

Esta pequena aplicação faz parte da infraestrutura do curso *Python for APIs*.

Seu objeto é receber logs em formato JSON, validar um token JWT com um serviço chamado **auth** e então cadastrar o log em um SQLite.

## Instalação

```bash
git clone https://github.com/hector-vido/python-logger.git
cd python-jwt
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
mv .env-example .env
# editar .env
flask run
```

## Inicialização

É possível preencher valores no banco de dados utilizando o script `fill.py`:

```bash
python3 fill.py
```

## Utilização:

Abaixo o nome das rotas necessárias e um exemplo de consumo.

### /find - GET

```bash
curl 'localhost:5000/remove/2010-07-31%2016:29:12' # procura em um intervale de 1 segundo antes e depois
curl 'localhost:5000/find/?ini=2010-07-31%2016:29:12&end=2020-07-31%2022:29:12'
```

### /insert - POST

```bash
curl -d '{"data" : "2010-07-31 16:29:12", "texto" : "Sed fugiat rerum amet atque. Cumque voluptas ut consequuntur et illum quia. Quam eveniet officia ipsum et ut consequatur. Est ratione ea quidem voluptatibus numquam incidunt. Quidem et optio blanditiis beatae."}' -H 'Content-Type: application/json' localhost:5000/insert
```

### /remove - DELETE

```bash
curl -X DELETE 'localhost:5000/remove/2010-07-31%2016:29:12' # remove um intervale de 1 segundo antes e depois
curl -X DELETE 'localhost:5000/remove/?ini=2010-07-31%2016:29:12&end=2020-07-31%2022:29:12'
```
