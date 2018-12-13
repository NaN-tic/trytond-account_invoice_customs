# This file is part account_invoice_customs module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['Sale', 'SaleLine']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    customs = fields.Boolean('Customs')
    customs_tariff_codes = fields.Function(fields.Char('Customs Tariff Codes'),
        'get_customs_tariff_codes')

    @staticmethod
    def default_customs():
        return False

    def on_change_party(self):
        self.customs = None
        super(Sale, self).on_change_party()
        if self.party and self.party.customs:
            self.customs = self.party.customs

    def _get_invoice_sale(self):
        invoice = super(Sale, self)._get_invoice_sale()
        invoice.customs = self.customs
        return invoice

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



class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    customs_tariff_code = fields.Function(
        fields.Many2One('customs.tariff.code',
        'Customs Tariff Codes'), 'get_customs_tariff_code')

    def get_customs_pattern(self, country=True):
        pool = Pool()
        Date = pool.get('ir.date')
        Configuration = pool.get('sale.configuration')

        config = Configuration(1)
        pattern = {}
        pattern['date'] = Date.today()
        if country and self.sale:
            address = getattr(self.sale, config.customs_address or 'invoice_address')
            if address and address.country:
                pattern['country'] = self.sale.invoice_address.country.id
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
                if ((record.sale and not record.sale.customs)
                        or not record.product or not record.type == 'line'):
                    continue
                code = record.get_tariff_code()
                res[name][record.id] = code.id if code else None
        return res
