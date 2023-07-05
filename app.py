import routeros_api

connection = routeros_api.RouterOsApiPool(
    '192.168.88.1',
    username='admin',
    password=' ',
    port=8291,
    plaintext_login=True,
)
api = connection.get_api()

# list_address =  api.get_resource('/ip/firewall/address-list')
# list_address.add(address="192.168.0.1",comment="P1",list="10M")

# list_address.get(comment="P1")
list_queues = api.get_resource('/queue/simple')
list_queues.get()