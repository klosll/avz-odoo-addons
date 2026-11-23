# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # HT02687: información de palet de la línea de venta (como en v14), para
    # mostrarla en las operaciones detalladas de los albaranes de carga.
    palet_id = fields.Many2one(
        string="Palet",
        comodel_name="stock.package.type",
        related="move_id.sale_line_id.palet_id",
        store=False,
    )
    palet_qty = fields.Float(
        string="Contained Palet Quantity",
        related="move_id.sale_line_id.palet_qty",
        store=False,
    )
