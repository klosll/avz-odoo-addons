# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockQuant(models.Model):
    # v14: this field was on stock.inventory.line. In v18 inventory adjustment
    # lines are stock.quant records, so the field is kept there.
    _inherit = "stock.quant"

    container = fields.Integer()
