# Copyright 2022 Berezi Amubieta - AvanzOSC
# Copyright 2023 Manuel Calomarde - KLO Ingeniería Informática S.L.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Import Wizard",
    "version": "15.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC-KLO",
    "website": "http://www.klo.es",
    "depends": [
        "purchase",
        "base_import_wizard",
        "purchase_discount",
        "product_trim_name"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/purchase_import_wizard_security.xml",
        "views/purchase_order_import_line_views.xml",
        "views/purchase_order_import_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
