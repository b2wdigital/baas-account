from typing import List, Optional

from aiohttp import web
from asyncworker.http.decorators import parse_path

from baas.app import app
from baas.http import parse_body
from baas.models import Account, Debito, Credito
from baas.services.account import AccountService


@app.http(["/accounts"], methods=["POST"])
@parse_body(Account)
async def create_account(acc: Account) -> Account:
    return AccountService.save_account(acc.cpf, acc)


@app.http(["/accounts"])
async def list_accounts() -> List[Account]:
    return AccountService.list()


@app.http(["/accounts/{acc_id}"])
@parse_path
async def get_by_id(acc_id: str) -> Optional[Account]:
    return AccountService.get_by_id(acc_id)


@app.http(["/accounts/{acc_id}/debito"], methods=["POST"])
@parse_body(Debito)
@parse_path
async def debita_account(acc_id: str, debito: Debito) -> Debito:
    AccountService.debita(acc_id, debito)
    return debito


@app.http(["/accounts/{acc_id}/credito"], methods=["POST"])
@parse_body(Credito)
@parse_path
async def credita_account(acc_id: str, credito: Credito) -> Credito:
    AccountService.credita(acc_id, credito)
    return credito


@app.http(["/health"])
async def health():
    return web.json_response({"OK": True})
