# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    unbalance = fields.Boolean(string="Not balanced")

    def _check_balanced(self):
        for record in self:
            if not record.unbalance:
                return super(AccountMove, record)._check_balanced()
        return True
