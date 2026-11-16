# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def post_init_hook(env):
    """Crea índices sobre stock.move.line durante la instalación.

    Los índices se crean aquí, no en la definición de campos, para mantener el
    código centralizado y evitar que la instalación falle si algún campo de una
    dependencia todavía no ha creado su columna.
    """
    cr = env.cr
    indexes = (
        ("stock_move_line_date_idx", "date"),
        ("stock_move_line_batch_id_idx", "batch_id"),
        ("stock_move_line_mother_id_idx", "mother_id"),
        ("stock_move_line_move_type_id_idx", "move_type_id"),
        ("stock_move_line_type_category_id_idx", "type_category_id"),
        ("stock_move_line_picking_type_id_idx", "picking_type_id"),
        ("stock_move_line_location_id_idx", "location_id"),
        ("stock_move_line_location_dest_id_idx", "location_dest_id"),
        ("stock_move_line_date_week_idx", "date_week"),
        ("stock_move_line_laying_week_idx", "laying_week"),
        ("stock_move_line_download_unit_idx", "download_unit"),
        ("stock_move_line_picking_partner_id_idx", "picking_partner_id"),
        ("stock_move_line_product_category_id_idx", "product_category_id"),
        ("stock_move_line_warehouse_id_idx", "warehouse_id"),
        ("stock_move_line_company_date_idx", "company_id, date"),
    )
    for index_name, columns in indexes:
        cr.execute(
            "CREATE INDEX IF NOT EXISTS %s ON stock_move_line (%s)"
            % (index_name, columns)
        )
