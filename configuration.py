# This file is part account_invoice_customs module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['SaleConfiguration']


class SaleConfiguration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'
    customs_address = fields.Selection([
        ('invoice_address', 'Invoice Address'),
        ('shipment_address', 'Shipment Address'),
        ], 'Customs Address')

    @staticmethod
    def default_customs_address():
        return 'invoice_address'
