# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    # HT02687: semantica v14 (portada tal cual): el palet es un empaquetado
    # generico (is_generic) y se selecciona con domain is_generic.
    palet_id = fields.Many2one(
        string="Palet",
        comodel_name="product.packaging",
        copy=False,
        domain="[('is_generic', '=', True)]",
    )
    palet_qty = fields.Float(
        string="Contained Palet Quantity",
        default=1,
        digits="Product Unit of Measure",
        copy=False,
    )
    is_generic = fields.Boolean(string="Is generic", default=False)
