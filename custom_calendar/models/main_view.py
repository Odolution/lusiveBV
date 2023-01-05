
from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
import datetime
import requests
import json

class Calender_event(models.Model):
    _inherit='calendar.event'

    show_as = fields.Selection(
        [('free', 'Available '),
         ('busy', 'Busy'),
         ('working_elsewhere','Working Else Where'),
         ('out_of_office','Out Of Office'),
         ('tentative','Tentative')], 'Show as', default='busy', required=True,
        help="If the time is shown as 'busy', this event will be visible to other people with either the full \
        information or simply 'busy' written depending on its privacy. Use this option to let other people know \
        that you are unavailable during that period of time. \n If the time is shown as 'free', this event won't \
        be visible to other people at all. Use this option to let other people know that you are available during \
        that period of time.")
