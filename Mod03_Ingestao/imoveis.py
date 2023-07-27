#%%
import time
import requests
import pandas as pd
import json
import logging


#%%
log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s  (%(name)s) :: %(levelname)s - %(message)s'
)

ch = logging.FileHandler('imoveis.log')
ch.setFormatter(formatter)
log.addHandler(ch)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%

def get_json_vivaReal(i):
    reqUrl = "https://glue-api.vivareal.com/v2/listings?business=SALE&facets=amenities&unitTypes=&unitSubTypes=&unitTypesV3=&usageTypes=&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount)%2Cpage%2CseasonalCampaigns%2CfullUriFragments%2Cnearby(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))%2Cexpansion(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier%2Cphones)%2Cdevelopments(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))%2Cowners(search(result(listings(listing(displayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2CunitTypes%2CnonActivationReason%2CpropertyType%2CunitSubTypes%2Cid%2Cportal%2CparkingSpaces%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2Cbedrooms%2CpricingInfos%2CshowPrice%2Cstatus%2CadvertiserContact%2CvideoTourLink%2CwhatsappNumber%2Cstamps)%2Caccount(id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2Cphones%2Ctier)%2Cmedias%2CaccountLink%2Clink))%2CtotalCount))&size=100&from={}&q=&developmentsSize=1&__vt=control%2CPBOT&levels=LANDING&ref=&pointRadius=&isPOIQuery="

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "x-domain": "www.vivareal.com.br" 
    }
    
    payload = ""
    
    response = requests.request("GET", reqUrl.format(i), data=payload,  headers=headersList)

    return json.loads(response.text)


#%%

i=0
j = get_json_vivaReal(i)
list_result = []
while 'search' in j:
    log.info(f"i: {i} | list_result: {len(list_result)}")
    for result in j['search']['result']['listings']:
        dict_result = {}
        
        try:
            dict_result['title'] = result['listing']['title']
        except:
            pass
        
        try:
            dict_result['description'] = result['listing']['description']
        except:
            pass

        try:
            dict_result['address'] = result['listing']['address']['street']
        except:
            pass

        try:
            dict_result['address'] = dict_result['address'] + ', ' + result['listing']['address']['streetNumber']
        except:
            pass

        try:
            dict_result['city'] = result['listing']['address']['city']    
        except:
            pass

        try:
            dict_result['area'] =  sum([int(x) for x in result['listing']['usableAreas']])
        except:
            pass

        try:
            dict_result['bedrooms'] = sum(result['listing']['bedrooms'])
        except:
            pass

        try:
            dict_result['bathrooms'] = sum(result['listing']['bathrooms'])
        except:
            pass

        try:
            dict_result['total_price'] = sum([float(x['price']) for x in result['listing']['pricingInfos']])
        except:
            pass

        try:
            dict_result['link'] = 'http://www.vivareal.com/'+result['link']['href']
        except:
            pass
        
        list_result.append(dict_result)
    i += 100
    time.sleep(1)
    j = get_json_vivaReal(i)

len(list_result)
# %%

# %%
df = pd.DataFrame(list_result)
df.shape
# %%
