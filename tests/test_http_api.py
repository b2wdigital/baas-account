from http import HTTPStatus

from asynctest import TestCase
from asyncworker.testing import HttpClientContext

from baas.api import app
from baas.models import Account, Debito, Credito
from baas.services.account import AccountService


class AccountAPITest(TestCase):
    async def setUp(self):
        AccountService.storage.clear()

    async def test_health(self):
        async with HttpClientContext(app) as client:
            resp = await client.get("/health")

            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"OK": True}, data)

    async def test_salva_conta(self):
        async with HttpClientContext(app) as client:
            acc = Account(nome="Dalton", cpf="42")
            resp = await client.post("/accounts", json=acc.dict())

            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual(acc, data)

            resp_salvo = await client.get(f"/accounts/{acc.cpf}")
            self.assertEqual(HTTPStatus.OK, resp_salvo.status)

            data_salvo = await resp.json()
            self.assertEqual(acc, data_salvo)

    async def test_cria_conta_repetida(self):
        async with HttpClientContext(app) as client:
            acc_1 = Account(nome="Dalton", cpf="42")
            acc_2 = Account(nome="Dalton 2", cpf="42")
            await client.post("/accounts", json=acc_1.dict())
            resp = await client.post("/accounts", json=acc_2.dict())

            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual(acc_1, data)

    async def test_lista_contas_banco_vazio(self):
        async with HttpClientContext(app) as client:
            resp = await client.get("/accounts")

            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual([], data)

    async def test_lista_contas(self):
        acc = Account(nome="Dalton", cpf="42")
        async with HttpClientContext(app) as client:
            await client.post("/accounts", json=acc.dict())
            resp = await client.get("/accounts")

            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()

            self.assertEqual(1, len(data))
            acc_1 = Account(**data[0])
            self.assertEqual(acc_1, acc)

    async def test_debita_conta(self):
        acc = Account(nome="Dalton", cpf="42")
        debito = Debito(valor=300)
        async with HttpClientContext(app) as client:
            await client.post("/accounts", json=acc.dict())
            resp = await client.post(
                f"/accounts/{acc.cpf}/debito", json=debito.dict()
            )

            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual(debito, data)

            resp_salvo = await client.get(f"/accounts/{acc.cpf}")
            acc_salva = await resp_salvo.json()

            acc_modificada = Account(**acc_salva)

            self.assertEqual(9700, acc_modificada.saldo)

    async def test_credito_conta(self):
        acc = Account(nome="Dalton", cpf="42")
        credito = Credito(valor=300)
        async with HttpClientContext(app) as client:
            await client.post("/accounts", json=acc.dict())
            resp = await client.post(
                f"/accounts/{acc.cpf}/credito", json=credito.dict()
            )

            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual(credito, data)

            resp_salvo = await client.get(f"/accounts/{acc.cpf}")
            acc_salva = await resp_salvo.json()

            acc_modificada = Account(**acc_salva)

            self.assertEqual(10300, acc_modificada.saldo)
