from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
import requests
import json
from datetime import datetime
class Partner(models.Model):
    _inherit ="res.partner"
    wix_id = fields.Char("Wix Customer ID")
class crm(models.Model):
    _inherit = 'crm.lead'
    channel = fields.Char('Channel')
    wix_ids = fields.Char('Wix Opportunity')

class wix(models.Model):
    _name ="wix.crm"

    cleint_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    access_token_field = fields.Char("Token")
    updated_date = fields.Datetime("Updated Date")
    refresh_token = fields.Html("Refresh Token")
    channel = fields.Char('Channel')
    
    def api_call(self,vals,offset):
        url = f"https://www.wixapis.com/contacts/v4/contacts?paging.limit=250&paging.offset={offset}&fieldsets=FULL&sort.fieldName=updatedDate&sort.order=DESC"

        payload={}
        headers = {
        'Authorization': vals,
        'Cookie': 'XSRF-TOKEN=1671695953|9tGA1BSCMuS8'
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response

    def check_customer(self,id,partner):
        pp = False
        for partnr in partner:
            
            if str(id) == str(partnr.wix_id):
                pp = True
                return (pp, partnr)
        return pp,partnr
        
    def check_Lead(self,id,crm):
        pp = False
        for lead in crm:
            
            if str(id) == str(lead.wix_ids):

                pp = True
                return (pp, lead)
        return pp,lead
    def access_token(self,id,sec_id,refresh_token):
        
        url = "https://www.wixapis.com/oauth/access"

        payload = json.dumps({
        "grant_type": "refresh_token",
        "client_id": str(id),
        "client_secret": str(sec_id),
        "refresh_token": str(refresh_token)
        })
        headers = {
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        raise UserError(payload)
        return response

    def cretae_Lead(self):
        instances = self.env['wix.crm'].search([])
        for ins in instances:
            token = self.access_token(ins.cleint_id,ins.client_secret,ins.refresh_token)
            raise UserError(str(token))
            ins["access_token_field"] = token['access_token'] 
            customer = self.env['res.partner'].search([])
            crm_lead = self.env['crm.lead'].search([])
            offset = 0
            while(True):
                data = ins.api_call(ins.access_token_field,offset)
                for i in data['contacts']:
                    customer = self.env['res.partner'].search([])
                    crm_lead = self.env['crm.lead'].search([])
                    wix_d = i['updatedDate'].split("T")
                    time_split = wix_d[1].split(".")
                    p = wix_d[0]+" "+time_split[0]
                    
                    wix_date = datetime.strptime(p, '%Y-%m-%d %H:%M:%S')
                    
                    
                    odo_date= ins.updated_date
                    if wix_date > odo_date: 
                        #if customer Exist
                        cus_exist = ins.check_customer(i['id'],customer)
                        
                        if cus_exist[0]:
                            # check crm Lead
                            crm_l = ins.check_Lead(i['id'],crm_lead)
                            
                            if crm_l[0]:
                                pass
                            else:
                                for k in crm_l[1]:
                                    crm_dic = {
                                        'wix_ids':k.wix_id, 
                                        'partner_id':k.id,
                                        'name':str(k.zip)+" "+str(k.city)+" "+str(k.street) +" | "+str(k.name),
                                        'channel':ins.channel,
                                        }
                                    
                                    s =crm_lead.create(crm_dic)
                 
                                #create Lead
                        else:
                            
                            #customer create
                            a= i.get('info')
                            dic ={
                                'wix_id':i['id']
                                }
                            
                            if 'name' in a:
                                if 'last' in a['name']:
                                    dic['name'] = a['name']['first'] +" "+ a['name']['last']    
                                else:
                                    dic['name'] = a['name']['first']

                                items_email = a['emails']['items']
                                dic['email'] = items_email[0]['email']
                                if 'phones' in a:
                                    items_phone = a['phones']['items']
                                    dic['phone'] = items_phone[0]['phone']
                                if 'addresses' in a:
                                    add = a['addresses']['items']
                                    address = add[0]['address']
                                    dic['street'] = address['addressLine']
                                    dic['zip'] = address['postalCode']
                                if 'city' in address:
                                    dic['city'] = address['city']
                                id = customer.create(dic)
                                #crm create
                                crm_l = ins.check_Lead(i['id'],crm_lead)
                                if crm_l[0]:
                                    pass
                                else:
                                    crm_dic ={
                                    'wix_ids':id.wix_id,
                                    'partner_id':id.id,
                                    'name': str(id.zip)+" "+str(id.city)+" "+str(id.street) +" | "+ str(id.name),
                                    'channel':ins.channel
                                    }
                                    
                                    l=crm_lead.create(crm_dic)
                    
                    else:
                        page = data['pagingMetadata']['hasNext']
                        break                      
                
                if page != False:
                    offset=offset+250
                else:
                    ins.updated_date =  datetime.now()
                    break            
        
   