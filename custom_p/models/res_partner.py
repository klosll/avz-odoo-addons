# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _risk_account_groups(self):
        super(ResPartner, self)._risk_account_groups()
        max_date = self._max_risk_date_due()
        company_domain = self._get_risk_company_domain()
        # v18: results of these groups are unpacked as
        # (partner, account, currency, amount_residual, amount_residual_currency)
        # by _prepare_risk_account_vals, so "fields"/"group_by" must keep this
        # shape. account_internal_type is now account_type (and the proforma
        # states are gone since 17.0).
        fields = [
            "amount_residual:sum",
            "amount_residual_currency:sum",
        ]
        group_by = ["partner_id", "account_id", "currency_id"]
        return {
            "draft": {
                "domain": company_domain
                + [
                    ("move_id.move_type", "in", ["out_invoice", "out_refund"]),
                    ("account_type", "=", "asset_receivable"),
                    ("parent_state", "in", ["draft"]),
                ],
                "fields": fields,
                "group_by": group_by,
            },
            "open": {
                "domain": company_domain
                + [
                    ("reconciled", "=", False),
                    ("account_type", "=", "asset_receivable"),
                    ("date_maturity", "!=", False),
                    ("parent_state", "=", "posted"),
                ],
                "fields": fields,
                "group_by": group_by,
            },
            "unpaid": {
                "domain": company_domain
                + [
                    ("reconciled", "=", False),
                    ("account_type", "=", "asset_receivable"),
                    "&",
                    ("date_maturity", "=", False),
                    ("date", "<", max_date),
                    ("parent_state", "=", "posted"),
                ],
                "fields": fields,
                "group_by": group_by,
            },
        }
