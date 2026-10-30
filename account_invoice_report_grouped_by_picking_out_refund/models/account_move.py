# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    # NOTE (v18): the v14 override of lines_grouped_by_picking() provided by
    # this module (sign handling for out_refund credit notes, section/note
    # grouping and returned-quantity dedup) is now part of the base
    # account_invoice_report_grouped_by_picking module. Overriding it here
    # would only shadow the newer base implementation (losing the journal
    # toggle and refund dedup), so no override is kept.
    # See account_invoice_report_grouped_by_picking/models/account_move.py.
