## DISCLAIMER

This is unofficial and has no association with Cisco or any company.

It is offered with no guarantees that it will work, nor that it won't have any unintended side effects. User accepts all risk and responsibility for the safety of and results of usage.

No support is to be expected for this script, and can be offered or rejected at will.

All that said, the script was created to perform the desired outcome as safely and properly as the skills of the authors allow.

## PURPOSE

This is a script for deleting **all** Secure Malware Analytics samples via API.

## USAGE

The two values that **must** be updated are:

1. ACCESS_TOKEN = "your-api-access-token"

Your access token (API) available in your account > API key.

2. ORGANIZATION_ID = "your-organization-id"

Your organization ID, which can be found the dashboard > your account > click on your organization name > copy the ID from the URL

Python library requirement:
`requests` is the only required library

```
python -m pip install requests
```

Running the script:

```
python delete-all-samples.py
```

## Testing

You can customize the MAX_DELETES value if you want to test deleting only a limited number of samples.

## Authors

Matthew Jacobs, Brandon Macer
