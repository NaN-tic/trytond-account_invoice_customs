# This file is part account_invoice_customs module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import party
from . import invoice
from . import sale

def register():
    Pool.register(
        party.Party,
        invoice.Invoice,
        invoice.InvoiceLine,
        module='account_invoice_customs', type_='model')
    Pool.register(
        configuration.SaleConfiguration,
        sale.Sale,
        sale.SaleLine,
        depends=['sale'],
        module='account_invoice_customs', type_='model')
