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
    site_name = fields.Char("Site Name")
    wix_ids = fields.Char('Wix Opportunity')

class wix(models.Model):
    _name ="wix.crm"

    cleint_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    access_token_field = fields.Char("Token")
    updated_date = fields.Datetime("Updated Date")
    refresh_token = fields.Char("Refresh Token")
    site_name = fields.Char("Site Name")
    
    def api_call(self,vals,offset):
        url = f"https://www.wixapis.com/contacts/v4/contacts?paging.limit=250&paging.offset={offset}&fieldsets=FULL&sort.fieldName=createdDate&sort.order=DESC"

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
        'Cookie': 'XSRF-TOKEN=1672644521|KHzDNH4IffLu'
        
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        
        return response
    def create_lead_schdule(self):
        wix_crms= self.env['wix.crm'].search([])

        for wix_crm in wix_crms:
            token = self.access_token(wix_crm.cleint_id,wix_crm.client_secret,wix_crm.refresh_token)
            
            wix_crm.access_token_field = token['access_token'] 
            customer = self.env['res.partner'].search([])
            crm_lead = self.env['crm.lead'].search([])
            offset = 0
            page = ""
            while(True):
                data = self.api_call(wix_crm.access_token_field,offset)
                if 'contacts' in data:
                    for i in data['contacts']:
                        customer = self.env['res.partner'].search([])
                        crm_lead = self.env['crm.lead'].search([])
                        wix_d = i['createdDate'].split("T")
                        time_split = wix_d[1].split(".")
                        p = wix_d[0]+" "+time_split[0]
                        
                        wix_date = datetime.strptime(p, '%Y-%m-%d %H:%M:%S')
                        
                        
                        odo_date= wix_crm.updated_date
                        
                        if wix_date > odo_date: 
                                
                            #if customer Exist
                            cus_exist = self.check_customer(i['id'],customer)
                            
                            if cus_exist[0]:
                                # check crm Lead
                                crm_l = self.check_Lead(i['id'],crm_lead)
                                
                                if crm_l[0]:
                                    pass
                                else:
                                    
                                    for k in cus_exist[1]:
                                        zip = ""
                                        if k.zip or k.city or k.street:
                                            zip =str(k.zip)+"-"+str(k.city)+"-"+str(k.street) 
                                        crm_dic = {
                                            'site_name':self.site_name,
                                            'wix_ids':i['id'], 
                                            'partner_id':k.id,
                                            'type':'opportunity',
                                            'name': zip +" | "+str(k.name) 
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
                                    crm_l = self.check_Lead(i['id'],crm_lead)
                                    if crm_l[0]:
                                        pass
                                    else:
                                        if id.zip or id.city or id.street:
                                            zip =str(id.zip)+"-"+str(id.city)+"-"+str(id.street)
                                        crm_dic ={
                                        'site_name':self.site_name,    
                                        'wix_ids':i['id'],
                                        'partner_id':id.id,
                                        'type':'opportunity',    
                                        'name': zip +" | "+ str(id.name)
                                        }
                                        
                                        l=crm_lead.create(crm_dic)
                                        
                        else:
                            page = data['pagingMetadata']['hasNext']
                            break                      
                    
                    
                    if page != False:
                        offset=offset+250
                    else:
                        self.updated_date =  datetime.now()
                        break

                else:
                    self.updated_date =  datetime.now()
                    break     
   

    def cretae_Lead(self):
        raise UserError(str(self.cleint_id))
        token = self.access_token(self.cleint_id,self.client_secret,self.refresh_token)
        
        self.access_token_field = token['access_token'] 
        customer = self.env['res.partner'].search([])
        crm_lead = self.env['crm.lead'].search([])
        offset = 0
        page = ""
        while(True):
            data = self.api_call(self.access_token_field,offset)
            if 'contacts' in data:
                for i in data['contacts']:
                    customer = self.env['res.partner'].search([])
                    crm_lead = self.env['crm.lead'].search([])
                    wix_d = i['createdDate'].split("T")
                    time_split = wix_d[1].split(".")
                    p = wix_d[0]+" "+time_split[0]
                    
                    wix_date = datetime.strptime(p, '%Y-%m-%d %H:%M:%S')
                    
                    
                    odo_date= self.updated_date
                    
                    if wix_date > odo_date: 
                            
                        #if customer Exist
                        cus_exist = self.check_customer(i['id'],customer)
                        
                        if cus_exist[0]:
                            # check crm Lead
                            crm_l = self.check_Lead(i['id'],crm_lead)
                            
                            if crm_l[0]:
                                pass
                            else:
                                
                                for k in cus_exist[1]:
                                    zip = ""
                                    if k.zip or k.city or k.street:
                                        zip =str(k.zip)+"-"+str(k.city)+"-"+str(k.street) 
                                    crm_dic = {
                                        'site_name':self.site_name,
                                        'wix_ids':i['id'], 
                                        'partner_id':k.id,
                                        'type':'opportunity',
                                        'name': zip +" | "+str(k.name) 
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
#                                     dic['city'] = address['city']
                                if 'city' in address:
                                    dic['city'] = address['city']
                                id = customer.create(dic)
                                #crm create
                                crm_l = self.check_Lead(i['id'],crm_lead)
                                if crm_l[0]:
                                    pass
                                else:
                                    if id.zip or id.city or id.street:
                                        zip =str(id.zip)+"-"+str(id.city)+"-"+str(id.street)
                                    crm_dic ={
                                    'site_name':self.site_name,    
                                    'wix_ids':i['id'],
                                    'partner_id':id.id,
                                    'type':'opportunity',    
                                    'name': zip +" | "+ str(id.name)
                                    }
                                    
                                    l=crm_lead.create(crm_dic)
                                    
                    else:
                        page = data['pagingMetadata']['hasNext']
                        break                      
                
                
                if page != False:
                    offset=offset+250
                else:
                    self.updated_date =  datetime.now()
                    break

            else:
                self.updated_date =  datetime.now()
                break            
  
    

                              
                    

            
            
                    
                
                

        


    
