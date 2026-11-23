# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Packaging Palet",
    "version": "18.0.1.1.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "stock",
        "sale_order_line_qty_by_packaging",
        # HT02687: para insertar Palet/Cantidad palet después de la pareja de
        # empaquetado (que mueve quantity) en operaciones detalladas
        "stock_move_qty_by_packaging",
    ],
    "data": [
        "views/product_packaging_views.xml",
        "views/sale_order_views.xml",
        "views/stock_move_line_view.xml",
    ],
    "installable": True,
}
