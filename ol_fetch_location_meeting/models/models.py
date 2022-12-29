# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv.expression import AND
from odoo.exceptions import UserError
from datetime import datetime
from odoo.addons.sale_crm.models.crm_lead import CrmLead as CL


class inheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    meeting_location = fields.Char(
        string='Location', store=True)

    sale_order_meeting_count = fields.Integer(
        string='Meetings', compute='_compute_so_calendar_event_count')
    
    def _compute_so_calendar_event_count(self):
        for record in self:
            model_id = self.env['ir.model'].search([('model','=',self._name)]).id
            get_meetings = self.env['calendar.event'].search([('res_model_id','=',model_id),('res_id','=',self.id)])
            record.sale_order_meeting_count = len(get_meetings)
    
    def action_schedule_meeting_so(self, smart_calendar=True):
        """ Open meeting's calendar view to schedule meeting on current opportunity.

            :param smart_calendar: boolean, to set to False if the view should not try to choose relevant
              mode and initial date for calendar view, see ``_get_opportunity_meeting_view_parameters``
            :return dict: dictionary value for created Meeting view
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        partner_ids = self.env.user.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        model_id = self.env['ir.model'].search([('model','=',self._name)]).id
        action['context'] = {
            # 'search_default_opportunity_id': current_opportunity_id,
            # 'default_opportunity_id': current_sale_order_id,
            'default_res_model_id': model_id,
            'default_res_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            'default_location': self.meeting_location,
            # 'default_team_id': self.team_id.id,
            'default_name': self.name,
        }

        if smart_calendar:
            action['context'].update({'default_mode': 'week', 'initial_date': datetime.today().strftime('%Y-%m-%d')})

        return action

class inheritCRM(models.Model):
    _inherit = 'crm.lead'

    meeting_location = fields.Char(
        string='Location', store=True)

    def action_new_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_meeting_location': self.meeting_location if self.meeting_location else False,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)]
        }
        if self.team_id:
            action['context']['default_team_id'] = self.team_id.id,
        if self.user_id:
            action['context']['default_user_id'] = self.user_id.id
        return action
    CL.action_new_quotation = action_new_quotation


class inheritCalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def default_get(self, fields):
        defaults = super(inheritCalendarEvent, self).default_get(fields)
        opportunity = self.env['crm.lead'].search([('id','=',defaults.get('opportunity_id', False))])
        if opportunity:
            defaults['location'] = opportunity.meeting_location
        # if model_name:
        #     if model_name.model == 'crm.lead':
        #         record = self.env['crm.lead'].search([('id','=',defaults.get('res_id', False))])
        #         if record:
        #             raise UserError(record.meeting_location)
        #             defaults['location'] = record.meeting_location
        #     if model_name.model == 'sale.order':
        #         record = self.env['sale.order'].search([('id','=',defaults.get('res_id', False))])
        #         if record:
        #             defaults['location'] = record.meeting_location
        return defaults

