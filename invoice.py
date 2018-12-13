# This file is part account_invoice_customs module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['Invoice', 'InvoiceLine']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'
    customs = fields.Boolean('Customs')
    customs_tariff_codes = fields.Function(fields.Char('Customs Tariff Codes'),
        'get_customs_tariff_codes')

    @staticmethod
    def default_customs():
        return False

    def on_change_party(self):
        self.customs = None
        super(Invoice, self).on_change_party()
        if self.party and self.party.customs:
            self.customs = self.party.customs

    @classmethod
    def get_customs_tariff_codes(cls, records, names):
        res = {n: {r.id: None for r in records} for n in names}
        for name in names:
            for record in records:
                codes = set()
                for line in record.lines:
                    code = line.customs_tariff_code
                    if code:
                        codes.add(code.code)
                res[name][record.id] = (', '.join(sorted(codes))
                    if codes else None)
        return res


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    customs_tariff_code = fields.Function(
        fields.Many2One('customs.tariff.code',
        'Customs Tariff Codes'), 'get_customs_tariff_code')

    def get_customs_pattern(self, country=True):
        Date = Pool().get('ir.date')

        pattern = {}
        pattern['date'] = Date.today()
        if country and self.invoice:
            address = self.invoice.invoice_address
            if address and address.country:
                pattern['country'] = self.invoice.invoice_address.country.id
        else:
            pattern['country'] = None
        return pattern

    def get_tariff_code(self):
        pattern = self.get_customs_pattern()
        code = self.product.template.get_tariff_code(pattern)
        if not code:
            pattern = self.get_customs_pattern(country=False)
            code = self.product.template.get_tariff_code(pattern)
        return code

    @classmethod
    def get_customs_tariff_code(cls, records, names):
        res = {n: {r.id: None for r in records} for n in names}
        for name in names:
            for record in records:
                if ((record.invoice and not record.invoice.customs)
                        or not record.product or not record.type == 'line'):
                    continue
                code = record.get_tariff_code()
                res[name][record.id] = code.id if code else None
        return res
