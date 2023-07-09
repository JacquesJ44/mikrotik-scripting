import routeros_api
import datetime
from basic_config import address_list, fwrules, admin_user_pw, new_users, disabled, allowed_interfaces, name, security_profile, wlan1_config, wlan2_config

# Connect to router
connection = routeros_api.RouterOsApiPool(
    host='192.168.88.1',
    username='admin',
    password='',
    port=None,
    # use_ssl=True,
    ssl_verify=False,
    ssl_verify_hostname=False,
    # ssl_context=False,
    plaintext_login=True
)
api = connection.get_api()
print('Connected!')

now = datetime.datetime.now()
print(now)
# input()

# STEP ONE - create address list
addresses =  api.get_resource('/ip/firewall/address-list')
for i in address_list:
    addresses.add(address=i['address'], comment=i['comment'], list=i['list'])

print('Address list added')
y = addresses.get()
print(y)


# STEP TWO - create firewall rule using the address list
fwadd = api.get_resource('/ip/firewall/filter')
for i in fwrules:
    fwadd.add(chain=i['chain'], action=i['action'], src_address_list=i['src-address-list'], log=i['log'], log_prefix=i['log-prefix'], place_before=i['place-before'], comment=i['comment'])

print('Firewall rule(s) added')
y = fwadd.get()
print(y)


# STEP THREE - add users and change default passwords
users = api.get_resource('/user')
users.set(id="*1", password=admin_user_pw)
for i in new_users:
    users.add(name=i['name'], password=i['password'], group=i['group'])

print('User(s) added')
y = users.get()
print(y)

# STEP FOUR - set MAC Telnet and MAC winbox service interfaces
mac_telnet = api.get_resource('/tool/mac-server')
mac_telnet.set(allowed_interface_list=allowed_interfaces)
y = mac_telnet.get()
print(y)

mac_winbox = api.get_resource('/tool/mac-server/mac-winbox')
mac_winbox.set(allowed_interface_list=allowed_interfaces)
y = mac_winbox.get()
print(y)

# Step FIVE - set neighbor discovery interface list
neighbors = api.get_resource('/ip/neighbor/discovery-settings')
neighbors.set(discover_interface_list=allowed_interfaces)
y = neighbors.get()
print(y)

# Step SIX - set identity
router_id = api.get_resource('/system/identity')
# a = qlist.get()
# print(a)
router_id.set(name=name)
y = router_id.get()
print(y)

# Step SIX(b) - set up wireless security profile and wireless SSID
# Setup up 'Basic-Security' Profile
basic_sec = api.get_resource('/interface/wireless/security-profiles')
basic_sec.add(authentication_types=security_profile['authentication-types'], mode=security_profile['mode'], name=security_profile['name'], supplicant_identity=security_profile['supplicant-identity'], wpa_pre_shared_key=security_profile['wpa-pre-shared-key'], wpa2_pre_shared_key=security_profile['wpa2-pre-shared-key'])
y = basic_sec.get()
print(y)

# Configure wireless profiles
wireless_wlan = api.get_resource('/interface/wireless')

wlan1 = wireless_wlan.get(default_name='wlan1')
if wlan1:
    print('wlan1 found - configuring')
    idwlan1 = wlan1[0]['id']
    wireless_wlan.set(id=idwlan1,
    band=wlan1_config['band'],
    channel_width=wlan1_config['channel-width'],
    country=wlan1_config['country'], 
    disabled=wlan1_config['disabled'], 
    distance=wlan1_config['distance'], 
    frequency=wlan1_config['frequency'], 
    installation=wlan1_config['installation'], 
    mode=wlan1_config['mode'],
    security_profile=wlan1_config['security-profile'], 
    ssid=wlan1_config['ssid'], 
    wireless_protocol=wlan1_config['wireless-protocol']
    )
else:
    print('no wlan1 found')

wlan1 = wireless_wlan.get(default_name='wlan1')
print(wlan1)

wlan2 = wireless_wlan.get(default_name='wlan2')
if wlan2:
    print('wlan2 found - configuring')
    idwlan2 = wlan2['id']
    wireless_wlan.set(id=idwlan2,
    band=wlan2_config['band'],
    channel_width=wlan2_config['channel-width'],
    country=wlan2_config['country'], 
    disabled=wlan2_config['disabled'], 
    distance=wlan2_config['distance'], 
    frequency=wlan2_config['frequency'], 
    installation=wlan2_config['installation'], 
    mode=wlan2_config['mode'],
    security_profile=wlan2_config['security-profile'], 
    ssid=wlan2_config['ssid'], 
    wireless_protocol=wlan2_config['wireless-protocol']
    )
else:
    print('no wlan2 found')

wlan2 = wireless_wlan.get(default_name='wlan2')
print(wlan2)

# Step SEVEN - disable services
ip_services = api.get_resource('/ip/service')
# y = ip_services.get()
# print(y)
for i in disabled:
    ip_services.set(id=i['id'], disabled=i['disabled'])

y = ip_services.get()
print(y)

print('Router configured succesfully')
connection.disconnect()
print('Disconnected')


