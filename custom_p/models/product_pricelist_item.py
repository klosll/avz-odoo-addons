# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    product_pricelist_price = fields.Float(
        string="Pricelist Price", compute="_compute_product_pricelist_price"
    )

    def _compute_product_pricelist_price(self):
        for item in self:
            if item.product_id and item.pricelist_id:
                # v18: product.product.price ya no existe; se usa la API de tarifas
                price = item.pricelist_id._get_product_price(item.product_id, 1.0)
            elif item.product_tmpl_id and item.pricelist_id:
                price = item.pricelist_id._get_product_price(
                    item.product_tmpl_id, 1.0
                )
            else:
                price = 0
            item.product_pricelist_price = price
