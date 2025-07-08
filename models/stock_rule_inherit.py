from odoo import models

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _run_manufacture(self, procurements):
        lines_computed_id = []
        for procurement, rule in procurements:
            sale_line = self.env['sale.order.line'].search([
                ('order_id', '=', procurement.origin),
                ('product_id', '=', procurement.product_id.id),
                ('id', 'not in', lines_computed_id)
            ], limit=1)
            lines_computed_id.append(sale_line.id)
            if sale_line and sale_line.bom_id:
                procurement.values['bom_id'] = sale_line.bom_id
        return super()._run_manufacture(procurements)