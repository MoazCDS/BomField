from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for rec in self:
            for line in rec.order_line:
                if line.bom_id:
                    if line.product_uom_qty % line.bom_id.product_qty:
                        raise ValidationError("Product quantity must be equal to product bom quantity or a multiple to it")
                bom_ref = line.bom_id.code
                bom_name = line.bom_id.product_tmpl_id.name
                bom_id = line.bom_id.id
                rec.message_post(body=f"The BOM name is: {bom_ref if bom_ref else ""}: {bom_name}, And the BOM id is: {bom_id}")
                if line.product_uom_qty != line.bom_id.product_qty:
                    rec.message_post(body=f"A Quantity mis-match detected in the bom {bom_ref if bom_ref else ""}: {bom_name}")
        return super().action_confirm()