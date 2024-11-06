import pytz

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

TIMEZONE = pytz.timezone("Asia/Jerusalem")
IEC_API_BASE_URL = "https://iecapi.iec.co.il/api/"
IEC_FAULT_PORTAL_API_URL = "https://masa-faultsportalapi.iec.co.il/api/"
IEC_MASA_BASE_URL = "https://masaapi-wa.azurewebsites.net/"
IEC_MASA_API_BASE_URL = IEC_MASA_BASE_URL + "api/"
IEC_MASA_LOOKUP_BASE_URL = IEC_MASA_BASE_URL + "lookup/"
IEC_MASA_MAINPORTAL_API_BASE_URL = "https://masa-mainportalapi.iec.co.il/api/"

GET_ACCOUNTS_URL = IEC_API_BASE_URL + "outages/accounts"
GET_CONSUMER_URL = IEC_API_BASE_URL + "customer"
GET_REQUEST_READING_URL = IEC_API_BASE_URL + "Consumption/RemoteReadingRange/{contract_id}"
GET_ELECTRIC_BILL_URL = IEC_API_BASE_URL + "ElectricBillsDrawers/ElectricBills/{contract_id}/{bp_number}"
GET_CONTRACTS_URL = IEC_API_BASE_URL + "customer/contract/{bp_number}"
GET_CHECK_CONTRACT_URL = IEC_API_BASE_URL + "customer/checkContract/{{contract_id}}/6"
GET_EFS_MESSAGES_URL = IEC_API_BASE_URL + "customer/efs"
GET_DEFAULT_CONTRACT_URL = GET_CONTRACTS_URL + "?count=1"
GET_LAST_METER_READING_URL = IEC_API_BASE_URL + "Device/LastMeterReading/{contract_id}/{bp_number}"
AUTHENTICATE_URL = IEC_API_BASE_URL + "Authentication/{id}/1/-1?customErrorPage=true"
GET_DEVICES_URL = IEC_API_BASE_URL + "Device/{contract_id}"
GET_TENANT_IDENTITY_URL = IEC_API_BASE_URL + "Tenant/Identify/{device_id}"
GET_DEVICE_BY_DEVICE_ID_URL = GET_DEVICES_URL + "/{device_id}"
GET_DEVICE_TYPE_URL = IEC_API_BASE_URL + "Device/type/{bp_number}/{contract_id}/false"
GET_BILLING_INVOICES_URL = IEC_API_BASE_URL + "BillingCollection/invoices/{contract_id}/{bp_number}"
GET_INVOICE_PDF_URL = IEC_API_BASE_URL + "BillingCollection/pdf"
GET_KWH_TARIFF_URL = IEC_API_BASE_URL + "content/he-IL/content/tariffs/contentpages/homeelectricitytariff"
GET_PREIOD_CALCULATOR_URL = IEC_API_BASE_URL + "content/he-IL/calculators/period"
GET_CALCULATOR_GADGET_URL = IEC_API_BASE_URL + "content/he-IL/calculators/gadget"
GET_OUTAGES_URL = IEC_API_BASE_URL + "outages/transactions/{account_id}/2"
SEND_CONSUMPTION_REPORT_TO_MAIL_URL = IEC_API_BASE_URL + "/Consumption/SendConsumptionReportToMail/{contract_id}"

GET_MASA_CITIES_LOOKUP_URL = IEC_MASA_MAINPORTAL_API_BASE_URL + "cities"
GET_MASA_USER_PROFILE_LOOKUP_URL = IEC_MASA_MAINPORTAL_API_BASE_URL + "contacts/userprofile"
GET_MASA_ORDER_TITLES_URL = IEC_MASA_API_BASE_URL + "accounts/{account_id}/orders/titles"
GET_MASA_ORDER_LOOKUP_URL = IEC_MASA_API_BASE_URL + "orderLookup"
GET_MASA_VOLT_LEVELS_URL = IEC_MASA_API_BASE_URL + "voltLevels/active"
GET_MASA_EQUIPMENTS_URL = IEC_MASA_BASE_URL + "equipments/get?accountId={account_id}&pageNumber=1&pageSize=10"
GET_MASA_LOOKUP_URL = IEC_MASA_BASE_URL + "lookup/all"

GET_USER_PROFILE_FROM_FAULT_PORTAL_URL = IEC_FAULT_PORTAL_API_URL + "contacts/userprofile"
GET_OUTAGES_FROM_FAULT_PORTAL_URL = IEC_FAULT_PORTAL_API_URL + "accounts/{account_id}/tranzactions/2"
ERROR_FIELD_NAME = "Error"
ERROR_SUMMARY_FIELD_NAME = "errorSummary"
