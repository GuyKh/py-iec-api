HEADERS_NO_AUTH = {
    "authority": "iecapi.iec.co.il",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,he;q=0.9",
    "dnt": "1",
    "origin": "https://www.iec.co.il",
    "referer": "https://www.iec.co.il/",
    "sec-ch-ua": '"Chromium";v="121", "Not A(Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36",
    "x-iec-idt": "1",
    "x-iec-webview": "1",
}

HEADERS_WITH_AUTH = HEADERS_NO_AUTH.copy()  # Make a copy of the original dictionary
HEADERS_WITH_AUTH["Authorization"] = "Bearer 1234"
HEADERS_WITH_AUTH["Cookie"] = "ARRAffinity=?; " "ARRAffinitySameSite=?;" " GCLB=?"

IEC_API_BASE_URL = "https://iecapi.iec.co.il//api/"
GET_ACCOUNTS_URL = IEC_API_BASE_URL + "outages/accounts"
GET_CONSUMER_URL = IEC_API_BASE_URL + "customer"
GET_REQUEST_READING_URL = IEC_API_BASE_URL + "Consumption/RemoteReadingRange/{contract_id}"
GET_ELECTRIC_BILL_URL = IEC_API_BASE_URL + "ElectricBillsDrawers/ElectricBills/{contract_id}/{bp_number}"
GET_CONTRACTS_URL = IEC_API_BASE_URL + "customer/contract/{bp_number}"
GET_DEFAULT_CONTRACT_URL = GET_CONTRACTS_URL + "?count=1"
GET_LAST_METER_READING_URL = IEC_API_BASE_URL + "Device/LastMeterReading/{contract_id}/{bp_number}"
AUTHENTICATE_URL = IEC_API_BASE_URL + "Authentication/{id}/1/-1?customErrorPage=true"
GET_DEVICES_URL = IEC_API_BASE_URL + "Device/{contract_id}"
GET_DEVICE_BY_DEVICE_ID_URL = GET_DEVICES_URL + "/{device_id}"
GET_DEVICE_TYPE_URL = IEC_API_BASE_URL + "Device/type/{bp_number}/{contract_id}/false"
GET_BILLING_INVOICES = IEC_API_BASE_URL + "billingCollection/invoices/{contract_id}/{bp_number}"
