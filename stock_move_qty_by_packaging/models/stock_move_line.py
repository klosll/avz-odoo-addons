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

    # HT02687: portado tal cual del modulo v14 (semantica: el palet es un
    # empaquetado generico, is_generic).
    palet_id = fields.Many2one(
        string="Palet",
        comodel_name="product.packaging",
        copy=False,
        domain="[('is_generic', '=', True)]",
    )
    palet_qty = fields.Float(
        string="Contained Palet Quantity", digits="Product Unit of Measure", copy=False
    )
    no_update_palet_qty = fields.Boolean(string="No update palet_qty", default=False)

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        self.no_update_palet_qty = True
        if self.product_packaging_id:
            self.product_packaging_qty = 1
            self.quantity = self.product_packaging_id.qty
            if self.product_packaging_id.palet_id:
                self.palet_id = self.product_packaging_id.palet_id.id
            else:
                self.palet_id = False
                self.palet_qty = 0
        if self.palet_id and self.quantity:
            self.palet_qty = self._get_palet_qty()
            self.no_update_palet_qty = False
        else:
            self.product_packaging_qty = 0
            self.quantity = 1
            self.palet_id = False
            self.palet_qty = 0

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        self.no_update_palet_qty = True
        if self.product_packaging_id and self.product_packaging_qty:
            self.quantity = self.product_packaging_qty * self.product_packaging_id.qty
        if self.palet_id and self.quantity:
            self.palet_qty = self._get_palet_qty()
            self.no_update_palet_qty = False

    @api.onchange("palet_qty")
    def _onchange_palet_qty(self):
        if (
            not self.no_update_palet_qty
            and self.product_id
            and self.product_packaging_id
            and self.palet_id
            and self.product_id.packaging_ids
            and self.palet_qty
        ):
            line = self.product_id.packaging_ids.filtered(
                lambda x: x.name
                and x.palet_id
                and x.name == self.product_packaging_id.name
                and x.palet_id == self.palet_id
            )
            if line and len(line) == 1:
                self.product_packaging_qty = self.palet_qty * line.palet_qty
        elif self.no_update_palet_qty:
            self.no_update_palet_qty = False

    def _get_palet_qty(self):
        return self.quantity / (
            self.product_packaging_id.qty * self.product_packaging_id.palet_qty
        )
