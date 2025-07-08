from odoo import models, fields, api

class SaleOrderLineBOM(models.Model):
    _inherit = "sale.order.line"


    bom_id = fields.Many2one('mrp.bom', string="BOM",
    domain="[('product_tmpl_id', '=', product_template_id), ('product_tmpl_id.route_ids', 'in', [1]),"
           "('product_tmpl_id.route_ids', 'in', [8])]")

    @api.onchange('product_id', 'product_template_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_template_id:
                bom = self.env['mrp.bom'].search([
                    ('product_tmpl_id', '=', rec.product_template_id.id),
                    ('product_tmpl_id.route_ids', 'in', [1]),
                    ('product_tmpl_id.route_ids', 'in', [8]),
                ], limit=1)
                rec.bom_id = bom