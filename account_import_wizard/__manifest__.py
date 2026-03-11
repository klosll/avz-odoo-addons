# Copyright 2023 Manuel Calomarde - KLO Ingeniería Informática S.L.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Import Wizard",
    "version": "15.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "KLO Ingenieria Informatica S.L.L.",
    "website": "https://www.klo.es",
    "depends": [
        "account",
        "base_import_wizard",
        "product_trim_name"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/account_import_wizard_security.xml",
        "views/account_move_import_line_views.xml",
        "views/account_move_import_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
