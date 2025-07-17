from odoo import models, fields, api

class SaleOrderLineBOM(models.Model):
    _inherit = "sale.order.line"


    bom_id = fields.Many2one('mrp.bom', string="BOM")
    is_mto_and_manufacture = fields.Boolean(compute="_compute_is_mto_and_manufacture", store=True)

    @api.depends('product_template_id', 'product_template_id.route_ids')
    def _compute_is_mto_and_manufacture(self):
        for line in self:
            line.is_mto_and_manufacture = False
            product = line.product_template_id
            if line.is_mto:
                for route in product.route_ids:
                    for rule in route.rule_ids:
                        if rule.action == 'manufacture':
                            line.is_mto_and_manufacture = True

    @api.onchange('is_mto_and_manufacture')
    def _onchange_is_mto_and_manufacture(self):
        for line in self:
            bom = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', line.product_template_id.id)
            ], limit=1)
            line.bom_id = bom