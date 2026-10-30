# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # NOTE (v18): the v14 override of _prepare_invoice_line() provided by this
    # module (linking stock moves to the created invoice lines through
    # get_stock_moves_link_invoice) is now done by the
    # sale_stock_picking_invoice_link module, with an extra to_refund filter.
    # Keeping the override here would only overwrite its result, so no
    # override is kept. See
    # sale_stock_picking_invoice_link/models/sale_order.py.
