# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # Estos campos se calculan al vuelo. No se almacenan para evitar que la
    # instalación tenga que recalcularlos sobre todos los stock.move.line.
    egg = fields.Boolean(string="Egg", related="product_id.egg")
    batch_location_id = fields.Many2one(
        string="Mother Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
    )
    batch_category_type_id = fields.Many2one(
        string="Batch Section",
        comodel_name="category.type",
        related="batch_location_id.type_id",
    )
    product_category_type_id = fields.Many2one(
        string="Product Category Section",
        comodel_name="category.type",
        related="product_category_id.type_id",
    )
    show_in_report = fields.Boolean(
        string="Show in Report", related="picking_id.show_in_report"
    )
