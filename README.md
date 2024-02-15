# iec-api

A python wrapper for Israel Electric Company API

## Module Usage

```python
from iec_api import iec_client as iec

client = iec.IecClient("123456789")
try:
    client.manual_login()  # login with user inputs
except iec.exceptions.IECError as err:
    logger.error("Failed Login: (Code %d): %s", err.code, err.error)
    raise

customer = client.get_customer()
print(customer)

contracts = client.get_contracts()
for contract in contracts:
    print(contract)

reading = client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
print(reading)

```
