# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        string="Packaging",
        domain="[('product_id','=',product_id)]",
        check_company=True,
    )
    # En v18 el campo homónimo de stock es computado sin inverse (readonly); al
    # redefinirlo hay que desactivar el compute explícitamente para que quede
    # como campo editable (ver README: nº de paquetes + cálculo automático de la
    # cantidad mediante los onchange de abajo).
    product_packaging_qty = fields.Float(
        string="Packaging Quantity",
        compute=False,
        precompute=False,
        readonly=False,
        store=True,
    )

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id:
            self.product_packaging_qty = 1
            self.quantity = self.product_packaging_id.qty
        else:
            self.product_packaging_qty = 0
            self.quantity = 1

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        if self.product_packaging_id and self.product_packaging_qty:
            self.quantity = self.product_packaging_qty * self.product_packaging_id.qty
