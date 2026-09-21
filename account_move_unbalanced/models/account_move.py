# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    unbalance = fields.Boolean(string="Not balanced")

    def _get_unbalanced_moves(self, container):
        # KLO. En v18 _check_balanced es @contextmanager y _get_unbalanced_moves devuelve
        # la lista de asientos desbalanceados. Excluimos de la comprobación los asientos
        # marcados con unbalance=True para permitir asientos desbalanceados.
        records = container['records'].filtered(lambda move: not move.unbalance)
        if not records:
            return []
        return super()._get_unbalanced_moves({**container, 'records': records})
