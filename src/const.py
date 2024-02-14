
HEADERS_NO_AUTH = {
    'authority': 'iecapi.iec.co.il',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,he;q=0.9',
    'dnt': '1',
    'origin': 'https://www.iec.co.il',
    'referer': 'https://www.iec.co.il/',
    'sec-ch-ua': '"Chromium";v="121", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/121.0.0.0 Safari/537.36',
    'x-iec-idt': '1',
    'x-iec-webview': '1',
}

HEADERS_WITH_AUTH = HEADERS_NO_AUTH.copy()  # Make a copy of the original dictionary
HEADERS_WITH_AUTH['Authorization'] = 'Bearer 1234'
HEADERS_WITH_AUTH['Cookie'] = ('ARRAffinity=?; '
                               'ARRAffinitySameSite=?;'
                               ' GCLB=?')

IEC_API_BASE_URL = "https://iecapi.iec.co.il//api/"
GET_CONSUMER_URL = IEC_API_BASE_URL + "customer"
GET_REQUEST_READING_URL = IEC_API_BASE_URL + "Consumption/RemoteReadingRange"
GET_ELECTRIC_BILL_URL = IEC_API_BASE_URL + "ElectricBillsDrawers/ElectricBills/{contract_id}/{bp_number}"
GET_CONTRACTS_URL = IEC_API_BASE_URL + "customer/contract/{bp_number}?count=1"
GET_SINGLE_CONTRACT_URL = IEC_API_BASE_URL + "customer/contract/{bp_number}?count=1"
GET_LAST_METER_READING_URL = IEC_API_BASE_URL + "Device/LastMeterReading/{contract_id}/{bp_number}"
AUTHENTICATE_URL = IEC_API_BASE_URL + "Authentication/{id}/1/-1?customErrorPage=true"
GET_DEVICES_URL = IEC_API_BASE_URL + "Device/{bp_number}"
