# py-iec

A python wrapper for Israel Electric Company API

## Module Usage

```python
    try:
        client = IecApiClient("123456789")
        client.manual_login() # login with user inputs
        customer = client.get_customer()
        print(customer)

        contracts = client.get_contracts()
        for contract in contracts:
            print(contract)

        reading = client.get_last_meter_reading(customer.bp_number, contracts[0].contract_id)
        print(reading)
    except IECLoginError as err:
        logger.error("Failed Login: (Code %d): %s", err.code, err.error)
```
