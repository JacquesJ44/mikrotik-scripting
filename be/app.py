import routeros_api

from flask import Flask
from flask_cors import CORS, cross_origin

from datetime import datetime
from basic_config import address_list, fwrules, admin_user_pw, new_users, disabled, allowed_interfaces, name, security_profile, wlan1_config, wlan2_config, sntp


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
# @cross_origin(methods=['POST'], headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'], supports_credentials=True, origins='http://localhost:3000')
def main():
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
    print('\n')

    # First, let's set the time
    now = datetime.now()
    clock = api.get_resource('/system/clock')
    today = now.strftime('%b/%d/%Y')
    time1 = now.time()
    time1 = time1.strftime('%H:%M:%S')
    clock.set(date=today, time=time1)
    y = clock.get()
    print(y)
    print('\n')

    # STEP ONE - create address list
    addresses =  api.get_resource('/ip/firewall/address-list')
    for i in address_list:
        addresses.add(address=i['address'], comment=i['comment'], list=i['list'])

    print('ADDRESS LIST ADDED')
    y = addresses.get()
    print(y)
    print('\n')

    # STEP TWO - create firewall rule using the address list
    fwadd = api.get_resource('/ip/firewall/filter')
    for i in fwrules:
        fwadd.add(chain=i['chain'], action=i['action'], src_address_list=i['src-address-list'], log=i['log'], log_prefix=i['log-prefix'], place_before=i['place-before'], comment=i['comment'])

    print('FIREWALL RULES(S) ADDED')
    y = fwadd.get()
    print(y)
    print('\n')

    # STEP THREE - add users and change default passwords
    users = api.get_resource('/user')
    users.set(id="*1", password=admin_user_pw)
    for i in new_users:
        users.add(name=i['name'], password=i['password'], group=i['group'])

    print('USER(S) ADDED')
    y = users.get()
    print(y)
    print('\n')

    # STEP FOUR - set MAC Telnet and MAC winbox service interfaces
    mac_telnet = api.get_resource('/tool/mac-server')
    mac_telnet.set(allowed_interface_list=allowed_interfaces)
    y = mac_telnet.get()
    print('MAC TELNET ENABLED')
    print(y)
    print('\n')
    mac_winbox = api.get_resource('/tool/mac-server/mac-winbox')
    mac_winbox.set(allowed_interface_list=allowed_interfaces)
    y = mac_winbox.get()
    print('MAC WINBOX ENABLED')
    print(y)
    print('\n')

    # Step FIVE - set neighbor discovery interface list
    neighbors = api.get_resource('/ip/neighbor/discovery-settings')
    neighbors.set(discover_interface_list=allowed_interfaces)
    y = neighbors.get()
    print('NEIGHBOR DISCOVERY SETTING ENABLED')
    print(y)
    print('\n')

    # Step SIX - set identity
    router_id = api.get_resource('/system/identity')
    # a = qlist.get()
    # print(a)
    router_id.set(name=name)
    print('ROUTER NAME')
    y = router_id.get()
    print(y)
    print('\n')

    # Step SIX(b) - set up wireless security profile and wireless SSID
    # Setup up 'Basic-Security' Profile
    basic_sec = api.get_resource('/interface/wireless/security-profiles')
    basic_sec.add(authentication_types=security_profile['authentication-types'], mode=security_profile['mode'], name=security_profile['name'], supplicant_identity=security_profile['supplicant-identity'], wpa_pre_shared_key=security_profile['wpa-pre-shared-key'], wpa2_pre_shared_key=security_profile['wpa2-pre-shared-key'])
    print('SECURTIY PROFILE')
    y = basic_sec.get()
    print(y)
    print('\n')

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
        print('\n')

    wlan1 = wireless_wlan.get(default_name='wlan1')
    print('WLAN1 CONFIG')
    print(wlan1)
    print('\n')

    wlan2 = wireless_wlan.get(default_name='wlan2')
    if wlan2:
        print('wlan2 found - configuring')
        idwlan2 = wlan2[0]['id']
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
        print('\n')

    wlan2 = wireless_wlan.get(default_name='wlan2')
    print('WLAN2 CONFIG')
    print(wlan2)
    print('\n')

    # Step SEVEN - set SNTP Client
    ntp = api.get_resource('/system/ntp/client')
    ntp.set(enabled=sntp['enabled'], server_dns_names=sntp['server-dns-names'])
    print('SET SNTP CLIENT')
    y = ntp.get()
    print(y)
    print('\n')

    # Step EIGHT - disable services
    ip_services = api.get_resource('/ip/service')
    # y = ip_services.get()
    # print(y)
    for i in disabled:
        ip_services.set(id=i['id'], disabled=i['disabled'])

    print('SERVICES DISABLED')
    y = ip_services.get()
    print(y)
    print('\n')

    print('\n')
    print('Router configured successfully!')
    connection.disconnect()
    print('Disconnected - you will not be able to reconnect. Use Winbox from here onwards...')
    print('\n')


if __name__ == "__main__":
    CORS(app, supports_credentials=True, resource={r"/*": {"origins": "*"}})
    app.run(debug=True)