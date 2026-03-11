# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from datetime import datetime
import xlrd
import pytz
import unicodedata


class AccountMoveImport(models.Model):
    _name = "account.move.import"
    _inherit = "base.import"
    _description = "Wizard to import account move"

    import_line_ids = fields.One2many(
        comodel_name="account.move.import.line",
    )
    account_move_count = fields.Integer(
        string="# Client Invoices",
        compute="_compute_account_move_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        if row_values:
            account_partner_code = row_values.get("codigocliente", "")
            account_partner_name = row_values.get("nombrecliente", "")
            account_invoice_date = row_values.get("fechafactura", "")
            # if account_invoice_date:
            #     account_invoice_date = account_invoice_date[0:19]
            #     account_invoice_date = datetime.strptime(
            #         account_invoice_date, "%Y-%m-%d %H:%M:%S")
            if not account_invoice_date:
                account_invoice_date = False
            account_invoice_date_due = row_values.get("fechavencimiento", "")
            # if account_invoice_date_due:
            #     account_invoice_date_due = xlrd.xldate.xldate_as_datetime(
            #         account_invoice_date_due, 0)
            #     account_invoice_date_due = timezone.localize(
            #         account_invoice_date_due).astimezone(pytz.UTC)
            #     account_invoice_date_due = account_invoice_date_due.replace(
            #         tzinfo=None)
            if not account_invoice_date_due:
                account_invoice_date_due = False
            account_amount_untaxed_signed = row_values.get("totalsinimpuestos", "")
            account_amount_total_signed = row_values.get("totalconimpuestos", "")
            account_origin = row_values.get("entrada", "")
            account_product_code = row_values.get("codigoproducto", "")
            account_product_name = row_values.get("nombreproducto", "")
            account_quantity = row_values.get("cantidad", "")
            account_price_unit = row_values.get("preciounitario", "")
            account_discount = row_values.get("descuento", "")
            account_tax_name = row_values.get("impuesto", "")
            account_state = row_values.get("estado", "")
            log_info = ""
            values.update(
                {
                    "account_partner_code": convert2str(
                        account_partner_code),
                    "account_partner_name": account_partner_name.title(),
                    "account_invoice_date": account_invoice_date,
                    "account_invoice_date_due": account_invoice_date_due,
                    "account_amount_untaxed_signed": account_amount_untaxed_signed,
                    "account_amount_total_signed": account_amount_total_signed,
                    "account_origin": convert2str(account_origin),
                    "account_product_code": convert2str(
                        account_product_code),
                    "account_product_name": convert2str(
                        account_product_name),
                    "account_quantity": account_quantity,
                    "account_price_unit": account_price_unit,
                    "account_discount": account_discount,
                    "account_tax_name": account_tax_name,
                    "account_state": convert2str(account_state),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = len(
                record.mapped("import_line_ids.account_invoice_id"))

    def button_open_account_move(self):
        self.ensure_one()
        orders = self.mapped("import_line_ids.account_invoice_id")
        action = self.env.ref("account.account_form_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", orders.ids)], safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict


class AccountMoveImportLine(models.Model):
    _name = "account.move.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import account move lines"

    @api.model
    def _get_selection_account_type(self):
        return self.env["account.move"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_account_type(self):
        default_dict = self.env["account.move"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="account.move.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    account_invoice_id = fields.Many2one(
        string="Account Invoice",
        comodel_name="account.move")
    account_partner_code = fields.Char(
        string="Partner Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_partner_name = fields.Char(
        string="Partner Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_invoice_date = fields.Datetime(
        string="CreateDate",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_invoice_date_due = fields.Datetime(
        string="DateDue",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_amount_untaxed_signed = fields.Float(
        string="Untaxed Amount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_amount_total_signed = fields.Float(
        string='Total Amount',
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_origin = fields.Char(
        string="Origin",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
        )
    account_quantity = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_price_unit = fields.Float(
        string="Price Unit",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_discount = fields.Float(
        string="Discount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_tax_name = fields.Char(
        string="Tax",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_state = fields.Char(
        string="State",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            origin = product = partner = False
            if line.account_origin:
                origin, log_info = line._check_origin()
                if log_info:
                    update_values = {
                        "account_origin": origin,
                        "log_info": log_info,
                        "state": "error",
                        "action": "nothing",
                        }
            if not log_info:
                partner, log_info_partner = line._check_partner()
                if log_info_partner:
                    log_info += log_info_partner
                product, log_info_product = line._check_product()
                if log_info_product:
                    log_info += log_info_product
                tax, log_info_tax = line._check_tax()
                if log_info_tax:
                    log_info += log_info_tax
                state = "error" if log_info else "pass"
                action = "nothing"
                if state != "error":
                    action = "create"
                update_values = {
                    "account_origin": origin,
                    "account_partner_id": partner and partner.id,
                    "account_product_id": product and product.id,
                    "account_tax_id": tax and tax.id,
                    "log_info": log_info,
                    "state": state,
                    "action": action,
                    }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        origins = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.action == "create":
                if not line.account_origin:
                    log_info = ""
                    account = line._create_account_move()
                    line._create_account_move_line(account_move=account)
                if line.account_origin and (
                    line.account_origin) not in (
                        origins):
                    if self.filtered(lambda l: l.account_origin == (
                        line.account_origin) and (
                            l.state == "error")):
                        log_info = _(
                            "Error: There is another line with the same" +
                            " origin document with some errors.")
                    else:
                        origin, log_info = line._check_origin()
                        if not log_info:
                            origins.append(origin)
                            account = line._create_account_move()
                            same_origin = self.filtered(
                                lambda l: l.account_origin == (
                                    line.account_origin))
                            for record in same_origin:
                                record._create_account_move_line(
                                    account_move=account)
                if account:
                    # account.button_set_checked()
                    account.date = line.account_invoice_date_due
            else:
                continue
            state = "error" if log_info else "done"
            line.write({
                "account_invoice_id": account.id,
                "log_info": log_info,
                "state": state})
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "account_invoice_id": account.id,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_origin(self):
        self.ensure_one()
        account_obj = self.env["account.move"]
        # search_domain = [("partner_ref", "=", self.account_origin)]
        log_info = ""
        accounts = account_obj.search(search_domain)
        if accounts:
            log_info = _("Error: Previously uploaded invoice.")
        return self.account_origin, log_info

    def _check_partner(self):
        self.ensure_one()
        log_info = ""
        if self.account_partner_id:
            return self.account_partner_id, log_info
        partner_obj = self.env["res.partner"]
        if self.account_partner_code and not self.account_partner_name:
            search_domain = [("ref", "=", self.account_partner_code)]
        elif self.account_partner_name and not self.account_partner_code:
            search_domain = [("name", "=ilike", self.account_partner_name)]
        elif self.account_partner_code and self.account_partner_name:
            search_domain = [
                '|', ("name", "=ilike", self.account_partner_name),
                ("ref", "=", self.account_partner_code)]
        partners = partner_obj.search(search_domain)
        if not partners:
            partners = False
            log_info = _("Error: No partner found.")
        elif len(partners) > 1:
            if self.account_partner_code and self.account_partner_name:
                search_domain = [
                ("name", "=ilike", self.account_partner_name),
                ("ref", "=", self.account_partner_code)]
                partners = partner_obj.search(search_domain)
                if not len(partners) == 1:
                    partners = False
                    log_info = _("Error: More than one partner found.")
        return partners and partners[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.account_product_id:
            return self.account_product_id, log_info
        product_obj = self.env["product.product"]
        if self.account_product_name:
            name = self.account_product_name.replace(" ","")
            name = ''.join((c for c in unicodedata.normalize('NFD',name) if unicodedata.category(c) != 'Mn'))
        if self.account_product_code and not self.account_product_name:
            search_domain = [
                ("default_code", "=", self.account_product_code)]
        elif self.account_product_name and not self.account_product_code:
            search_domain = [("trim_name", "=ilike", name)]
        elif self.account_product_code and self.account_product_name:
            search_domain = [
                '|', ("trim_name", "=ilike", name),
                ("default_code", "=", self.account_product_code)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            if self.account_product_code and self.account_product_name:
                search_domain = [
                ("trim_name", "=ilike", name),
                ("default_code", "=", self.account_product_code)]
                products = product_obj.search(search_domain)
                if not len(products) == 1:
                    products = False
                    log_info = _(
                        "Error: More than one product with the same name or " +
                        "code found.").format(self.account_product_name,
                                              self.account_product_code)
        return products and products[:1], log_info


    def _check_tax(self):
        self.ensure_one()
        log_info = ""
        if self.account_tax_id:
            return self.account_tax_id, log_info
        tax_obj = self.env["account.tax"]
        if self.account_partner_name:
            search_domain = [("name", "=ilike", self.account_tax_name)]
        taxs = tax_obj.search(search_domain)
        if not taxs:
            taxs = False
            log_info = _("Error: No tax found.")
        elif len(taxs) > 1:
            if self.account_tax_name:
                search_domain = [
                ("name", "=ilike", self.account_tax_name)]
                taxs = tax_obj.search(search_domain)
                if not len(taxs) == 1:
                    taxs = False
                    log_info = _("Error: More than one tax found.")
        return taxs and taxs[:1], log_info

    def _create_account_move(self):
        account_invoice_obj = self.env["account.move"]
        values = self._account_move_values()
        account = account_invoice_obj.create(values)
        return account

    def _create_account_move_line(self, account_move=False):
        if account_move:
            if not self.account_quantity:
                self.account_quantity = 1
            account_move.line_ids = [(0, 0, {
                "product_id": self.account_product_id.id,
                "quantity": self.account_quantity,
                "name": self.account_product_id.display_name,
                "move_id": account_move,
                "price_unit": self.account_price_unit,
                "tax_line_id": self.account_tax_id.id,
                "discount": self.account_discount})]

    def _account_move_values(self):
        return {
            "partner_id": self.account_partner_id.id,
            "move_type": "out_invoice",
            "invoice_date": self.account_invoice_date,
            "invoice_date_due": self.account_invoice_date_due,
            "amount_untaxed_signed": self.account_amount_untaxed_signed,
            "amount_total_signed": self.account_amount_total_signed
        }
