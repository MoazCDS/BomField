from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    order_line_ids = fields.One2many('sale.order.line', 'product_template_id')
    is_mto = fields.Boolean(compute="_compute_is_mto", store=True)
    is_manufacture = fields.Boolean(compute="_compute_is_manufacture", store=True)

    @api.depends('order_line_ids', 'order_line_ids.is_mto')
    def _compute_is_mto(self):
        for rec in self:
            rec.is_mto = any(line.is_mto for line in rec.order_line_ids)

    @api.depends('route_ids', 'route_ids.rule_ids.action')
    def _compute_is_manufacture(self):
        for rec in self:
            rec.is_manufacture = any(rule.action == 'manufacture'for route in rec.route_ids for rule in route.rule_ids)