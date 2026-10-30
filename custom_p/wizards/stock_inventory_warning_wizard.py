# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class StockInventoryWarningWizard(models.TransientModel):
    _name = "stock.inventory.warning.wizard"
    _description = "Wizard for warning if the location is not assigned"

    text = fields.Text(
        string="Text",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(StockInventoryWarningWizard, self).default_get(fields_list)
        res.update(
            {
                "text": _(
                    "There is no location. The entire warehouse "
                    + "could be deleted and this could have serious consequences."
                )
            }
        )
        return res

    def continue_with_inventory(self):
        self.ensure_one()
        inventory = self.env["stock.inventory"].browse(
            self.env.context.get("active_id")
        )
        # v14: _action_start() + _check_company() + action_open_inventory_lines().
        # In v18 the stock_inventory (OCA) module starts the adjustment with
        # action_state_to_in_progress() (quants are edited right on the form).
        inventory.action_state_to_in_progress()
        return {"type": "ir.actions.act_window_close"}
