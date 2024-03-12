# Calling the API with Postman

I've done a lot of work exposing and automating the work for you if you want to manually use Postman to call IEC API.

You can download and import the [IEC Postman Collection]() and follow this guide:

# Step 1: Setup your UserID
In the Collection Variable configuration - adjust your `user_id` variable to match your User ID (תעודת זהות).

# Step 2: Obtaining an `id_token``
You can do this in multiple ways:

## Step 2A: Get refresh_token from [HomeAssistant Custom Component](https://github.com/GuyKh/iec-custom-component)
If you're using HomeAssistant Component, you can fetch the `refresh_token` and use it to get a fresh `id_token`

In your Home Assistant directory - run:
```
$ cat .storage/core.config_entries | grep iec -B5 -A20 | grep refresh_token
"refresh_token": "55rSzGfPGY3i9iONu_J_FGfYhWdZsszM_abcdEFG",
```

Copy the value of this token to `refresh_token` variable in Collection Variables.
Run step `OAuth/Refresh Token`.
If the call was successfull, the `id_token` should be automatically filled.

## Step 2B: Refresh The Token
If you already configured `refresh_token` sometime before, you can reuse it (up to some time after creation).
Simply run step `OAuth/Refresh Token`.
If the call was successfull, the `id_token` should be automatically filled.

## Step 2C: Manually go through the Login Process
Run the following Postman calls in this order:
- `OAuth/Step 1: Factor ID` 
- `OAuth/Step 2: Send OTP`
- At this point you should have gotten your OTP token by SMS or Email - fill it in `otpCode` variable in Collection Variables
- `OAuth/Step 3: Verify OTP`
- `OAuth/Step 4: Authorize Session`
- `OAuth/Step 5: Get AccessToken`
And at this point you should have gotten a response including a `refresh_token` and the desired `id_token`

# **Important** - if any of the next calls would return an _401 Unauthorized_ response, repeat Step2 to get new `id_token`

# Step 3: Fill `bp_number`
Run `Account` or `Customer`.
For `Account`, the `bp_number` variable is the `accountNumber` value.
For `Customer`, it's just the `bpNumber` value.
One way or another, the tests should populate the value automatically in the Collection Variables

# Step 4: Fill `contract_id`
Run `Contracts`
Value for `contract_id` is from field `contractId` and (like before) should be populated automatically

# Step 5: Fill `device_id`
Run `Devices`.
Value for `device_id` is from field `deviceNumber` and (like before) should be populated automatically

# Step 6: Enjoy
Now you have all the required variables for all the calls filled and you can run it by yourself