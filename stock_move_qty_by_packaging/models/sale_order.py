# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # HT02687: portado del v14: al confirmar se copian packaging y palet (con
    # sus cantidades) a las lineas de movimiento del albaran.
    def action_confirm(self):
        result = super().action_confirm()
        for sale in self:
            for picking in sale.picking_ids:
                for move in picking.move_ids_without_package:
                    if move.sale_line_id:
                        for line in move.move_line_ids:
                            line.product_packaging_id = (
                                move.sale_line_id.product_packaging_id.id
                            )
                            line.palet_id = move.sale_line_id.palet_id.id
                            line.product_packaging_qty = (
                                move.sale_line_id.product_packaging_qty
                            )
                            line.palet_qty = move.sale_line_id.palet_qty
        return result
