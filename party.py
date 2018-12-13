# This file is part account_invoice_customs module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    customs = fields.Boolean('Customs')

    @staticmethod
    def default_customs():
        return False
