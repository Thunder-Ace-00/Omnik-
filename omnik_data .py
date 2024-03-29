import requests

class Client:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def retrieve_status(self):
        url = f'http://{self.ip}/js/status.js'
        response = requests.get(url, auth=(self.username, self.password))
        response.raise_for_status()
        response_text = response.text

        vars_to_extract = ['version', 'm2mMid', 'wlanMac', 'm2mRssi', 'wanIp', 'nmac', 'fephy', 'webData']
        vars_values = {}

        for var in vars_to_extract:
            start_key = f'var {var}="'
            start_pos = response_text.find(start_key)
            if start_pos != -1:
                start_pos += len(start_key)
                end_pos = response_text.find('";', start_pos)
                vars_values[var] = response_text[start_pos:end_pos]
            else:
                raise Exception(f'Failed to find {var} in response')

        web_data = vars_values['webData'].split(',')
       
        # Use default value of 0 for missing fields
        vars_values['serial_number'] = str(web_data[0]) if web_data[0] else 'no data'
        vars_values['msvn']          = str(web_data[1]) if web_data[1] else 'no data'
        vars_values['ssvn']          = str(web_data[2]) if web_data[2] else 'no data'
        vars_values['pv_type']       = str(web_data[3]) if web_data[3] else 'no data'
        vars_values['currentW']      = int(web_data[5]) if web_data[5] else 0
        vars_values['dayKwh']        = int(web_data[6]) / 100 if web_data[6] else 0
        vars_values['totalKwh']      = int(web_data[7]) / 10 if web_data[7] else 0
        vars_values['alerts']        = int(web_data[8]) if web_data[8] else 0
        vars_values['update']        = int(web_data[9]) if web_data[9] else 0

        return vars_values


# Usage
client = Client('ipaddress', 'username', 'password')    # <- fill in ip Omnik setup webpage, Username and Password for login
                                                        # e.g. client = Client('192.168.1.10', 'myusername', 'ubrfu98yguiv')

try:
    data = client.retrieve_status()
    print(' Inverter serial number   : {}'.format(data['serial_number']))
    print(' Firmware version (main)  : {}'.format(data['msvn']))
    print(' Firmware version (slave) : {}'.format(data['ssvn']))
    print(' Inverter model           : {}'.format(data['pv_type']))
    print(' Firmware version         : {}'.format(data['version']))
    print(' Device serial number     : {}'.format(data['m2mMid']))
    print(' MAC address              : {}'.format(data['wlanMac']))
    print(' Signal power             : {}'.format(data['m2mRssi']))
    print(' IP address               : {}'.format(data['wanIp']))
    print(' nmac                     : {}'.format(data['nmac']))
    print(' fephy                    : {}'.format(data['fephy']))
    # enable for debugging
    # print(' webData                  : {}'.format(data['webData']))
    print(' Current power            : {} W'.format(data['currentW']))
    print(' Yield today              : {:.2f} kWh'.format(data['dayKwh']))
    print(' Total yield              : {:.2f} kWh'.format(data['totalKwh']))
    print(' Alerts                   : {}'.format(data['alerts']))
    print(' Last update              : {} min ago'.format(data['update']))

except Exception as e:
    print(f"Error retrieving data: {e}")

