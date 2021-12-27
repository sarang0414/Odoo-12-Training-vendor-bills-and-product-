
from odoo import api, fields, models

class SetVendorBillsSalesPrice(models.Model):
    _inherit = "account.invoice.line"

    selling_price = fields.Float(string="Sales Price",store=True)

    @api.onchange('product_id')
    def onchange_bills_product_id(self):
        for rec in self:
            print("Record lst price...",rec.product_id.lst_price)
            rec.selling_price = rec.product_id.lst_price



class UpdateSalesPrice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        for rec in self:
            record = rec.invoice_line_ids.product_id
            record.write({
                'lst_price':rec.invoice_line_ids.selling_price,
                'standard_price':rec.invoice_line_ids.price_unit
            })
        return super().action_invoice_open()



class ProductSalesPrice(models.Model):
    _inherit = "product.product"


    @api.onchange('lst_price')
    def onchange_sale_price(self):
        for rec in self:
            prod_id = self._origin.id
            record = self.env["account.invoice.line"].search([('product_id', '=', prod_id)])
            record.write({
                'selling_price':rec.lst_price
            })

    @api.onchange('standard_price')
    def onchange_standard_price(self):
        for rec in self:
            prod_id = self._origin.id
            record = self.env["account.invoice.line"].search([('product_id', '=', prod_id)])
            record.write({
                'price_unit': rec.standard_price
            })


