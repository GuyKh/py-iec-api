# iec-api

A python wrapper for Israel Electric Company API

## Module Usage

```python
from iec_api import iec_client as iec

client = iec.IecClient("123456789")
try:
    await client.manual_login()  # login with user inputs
except iec.exceptions.IECError as err:
    logger.error(f"Failed Login: (Code {err.code}): {err.error}")
    raise

customer = await client.get_customer()
print(customer)

contracts = await client.get_contracts()
for contract in contracts:
    print(contract)

reading = await client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
print(reading)

```


## Postman
To use the API manually through Postman - read [Postman Collection Guide](POSTMAN.md)