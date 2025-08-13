# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    def _default_project_currency(self):
        """Prefer GTQ if it exists in the DB, else fall back to company currency."""
        # Try by XML ID first (present in standard base data)
        gtq = self.env.ref("base.GTQ", raise_if_not_found=False)
        if gtq:
            return gtq.id
        # Fallback: search by code
        gtq_search = self.env["res.currency"].search([("name", "=", "GTQ")], limit=1)
        return gtq_search.id or self.env.company.currency_id.id

    project_currency_id = fields.Many2one(
        "res.currency",
        string="Project Currency",
        default=_default_project_currency,
        help="Currency used for Estimated Cost. Defaults to Guatemalan Quetzal (GTQ) if available; otherwise the company currency.",
    )

    estimated_cost = fields.Monetary(
        string="Estimated Cost",
        currency_field="project_currency_id",
        tracking=True,
        help="User-entered estimated total cost for the project.",
    )
