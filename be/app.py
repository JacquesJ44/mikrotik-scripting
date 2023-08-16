import routeros_api
import contextlib
import io

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from datetime import datetime
from basic_config import address_list, fwrules, admin_user_pw, new_users, disabled, allowed_interfaces, security_profile, wlan1_config, wlan2_config, sntp


app = Flask(__name__)

# Connect to router
def connect_router():
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

    # print(connection)
    return connection



@app.route('/', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'], headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'], supports_credentials=True, origins='http://localhost:3000')
def main():
   
    # if request.method == 'GET':
    #     print('GET method')
    #     return {}

    if request.method == 'POST':
       
        obj = request.get_json()
        print(obj)
        # input()
        captured_output = io.StringIO()
        # Connect to router
        try:
            api = connect_router().get_api()
        except:
            return jsonify({"error": "Unable to connect!"})
        
        with contextlib.redirect_stdout(captured_output):
            print("Connected!" + '\n')
        
        # First, let's set the time
        now = datetime.now()
        clock = api.get_resource('/system/clock')
        today = now.strftime('%b/%d/%Y')
        time1 = now.time()
        time1 = time1.strftime('%H:%M:%S')
        clock.set(date=today, time=time1)

        y = clock.get()
        with contextlib.redirect_stdout(captured_output):
            print(y)
            print('\n')

        # STEP ONE - create address list
        addresses =  api.get_resource('/ip/firewall/address-list')
        for i in address_list:
            addresses.add(address=i['address'], comment=i['comment'], list=i['list'])

        y = addresses.get()
        with contextlib.redirect_stdout(captured_output):
            print('ADDRESS LIST ADDED')
            print(y)
            print('\n')

        # STEP TWO - create firewall rule using the address list
        fwadd = api.get_resource('/ip/firewall/filter')
        for i in fwrules:
            fwadd.add(chain=i['chain'], action=i['action'], src_address_list=i['src-address-list'], log=i['log'], log_prefix=i['log-prefix'], place_before=i['place-before'], comment=i['comment'])

        y = fwadd.get()
        with contextlib.redirect_stdout(captured_output):
            print('FIREWALL RULE(S) ADDED')
            print(y)
            print('\n')

        # STEP THREE - add users and change default passwords
        users = api.get_resource('/user')
        users.set(id="*1", password=admin_user_pw)
        for i in new_users:
            users.add(name=i['name'], password=i['password'], group=i['group'])

        y = users.get()
        with contextlib.redirect_stdout(captured_output):
            print('USER(S) ADDED')
            print(y)
            print('\n')

        # STEP FOUR - set MAC Telnet and MAC winbox service interfaces
        mac_telnet = api.get_resource('/tool/mac-server')
        mac_telnet.set(allowed_interface_list=allowed_interfaces)
        y = mac_telnet.get()
        with contextlib.redirect_stdout(captured_output):
            print('MAC TELNET ENABLED')
            print(y)
            print('\n')
        mac_winbox = api.get_resource('/tool/mac-server/mac-winbox')
        mac_winbox.set(allowed_interface_list=allowed_interfaces)
        y = mac_winbox.get()
        with contextlib.redirect_stdout(captured_output):
            print('MAC WINBOX ENABLED')
            print(y)
            print('\n')

        # Step FIVE - set neighbor discovery interface list
        neighbors = api.get_resource('/ip/neighbor/discovery-settings')
        neighbors.set(discover_interface_list=allowed_interfaces)
        y = neighbors.get()
        with contextlib.redirect_stdout(captured_output):
            print('NEIGHBOR DISCOVERY SETTING ENABLED')
            print(y)
            print('\n')

        # Step SIX - set identity
        router_id = api.get_resource('/system/identity')
        router_id.set(name=obj['router_id'])

        y = router_id.get()
        with contextlib.redirect_stdout(captured_output):
            print('ROUTER NAME')
            print(y)
            print('\n')

        # Step SIX(b) - set up wireless security profile and wireless SSID
        # Setup up 'Basic-Security' Profile
        basic_sec = api.get_resource('/interface/wireless/security-profiles')
        basic_sec.add(authentication_types=security_profile['authentication-types'], mode=security_profile['mode'], name=security_profile['name'], supplicant_identity=security_profile['supplicant-identity'], wpa_pre_shared_key=obj['wpa_pass'], wpa2_pre_shared_key=obj['wpa2_pass'])

        y = basic_sec.get()
        with contextlib.redirect_stdout(captured_output):
            print('SECURTIY PROFILE')
            print(y)
            print('\n')

        # Configure wireless profiles
        wireless_wlan = api.get_resource('/interface/wireless')

        wlan1 = wireless_wlan.get(default_name='wlan1')
        if wlan1:
            with contextlib.redirect_stdout(captured_output):
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
            ssid=obj['ssid24'], 
            wireless_protocol=wlan1_config['wireless-protocol']
            )
        else:
            with contextlib.redirect_stdout(captured_output):
                print('no wlan1 found')
                print('\n')

        wlan1 = wireless_wlan.get(default_name='wlan1')
        with contextlib.redirect_stdout(captured_output):
            print('WLAN1 CONFIG')
            print(wlan1)
            print('\n')

        wlan2 = wireless_wlan.get(default_name='wlan2')
        if wlan2:
            with contextlib.redirect_stdout(captured_output):
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
            ssid=obj['ssid58'], 
            wireless_protocol=wlan2_config['wireless-protocol']
            )
        else:
            with contextlib.redirect_stdout(captured_output):
                print('no wlan2 found')
                print('\n')

        wlan2 = wireless_wlan.get(default_name='wlan2')
        with contextlib.redirect_stdout(captured_output):
            print('WLAN2 CONFIG')
            print(wlan2)
            print('\n')

        # Step SEVEN - set SNTP Client
        ntp = api.get_resource('/system/ntp/client')
        ntp.set(enabled=sntp['enabled'], server_dns_names=sntp['server-dns-names'])

        y = ntp.get()
        with contextlib.redirect_stdout(captured_output):
            print('SET SNTP CLIENT')
            print(y)
            print('\n')

        # Step EIGHT - disable services
        ip_services = api.get_resource('/ip/service')
        # y = ip_services.get()
        # print(y)
        for i in disabled:
            ip_services.set(id=i['id'], disabled=i['disabled'])

        y = ip_services.get()
        with contextlib.redirect_stdout(captured_output):
            print('SERVICES DISABLED')
            print(y)
            print('\n')

        connect_router().disconnect()
        with contextlib.redirect_stdout(captured_output):
            print('Router configured successfully!')
            print('Disconnected - you will not be able to reconnect. Use Winbox from here onwards...')
            print('\n')

        captured_string = captured_output.getvalue()

        return jsonify({"msg": "Successful"}, captured_string) 

if __name__ == "__main__":
    CORS(app, supports_credentials=True, resource={r"/*": {"origins": "*"}})
    app.run(debug=True)