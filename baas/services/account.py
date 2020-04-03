from typing import List, Optional

from baas.models import Account, Debito, Credito


class AccountStorage:
    def __init__(self):
        self.clear()

    def clear(self):
        self.__data = dict()

    def save(self, acc_id: str, acc_data: Account) -> Account:
        self.__data[acc_id] = acc_data
        return acc_data

    def get_by_id(self, acc_id) -> Optional[Account]:
        return self.__data.get(acc_id)

    def list(self) -> List[Account]:
        return [acc[1] for acc in self.__data.items()]


class AccountService:

    storage = AccountStorage()

    @classmethod
    def save_account(cls, acc_id: str, acc_data: Account) -> Account:
        acc_no_banco = AccountService.get_by_id(acc_id)
        if acc_no_banco:
            return acc_no_banco
        return cls.storage.save(acc_id, acc_data)

    @classmethod
    def get_by_id(cls, acc_id: str) -> Optional[Account]:
        return cls.storage.get_by_id(acc_id)

    @classmethod
    def list(cls) -> List[Account]:
        return cls.storage.list()

    @classmethod
    def debita(cls, acc_id: str, debito: Debito) -> Optional[Account]:
        conta = AccountService.get_by_id(acc_id)
        if conta:
            if debito.valor > conta.saldo:
                raise Exception("Saldo nao pode ser negativo")
            conta.saldo -= debito.valor

    @classmethod
    def credita(cls, acc_id: str, credito: Credito):
        conta = AccountService.get_by_id(acc_id)
        if conta:
            conta.saldo += credito.valor
