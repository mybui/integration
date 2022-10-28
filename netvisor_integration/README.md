# Netvisor Integration

## Description

The program is implemented for the Netvisor integration from DB. Currently, it supports the integration of data at the table `providers` and the entity `Customer Register` in Netvisor.

## Getting Started

### Executing program

```
poetry run python3 main.py
```

### Program logic

#### Field matching for `providers`:

https://vapaus.atlassian.net/l/c/LNg1jttE

#### Logic

1. Get all companies with missing Netvisor data for `netvisorId` and in `providers`, and populate these fields (function `update_netvisor_company_info` at `main.py`)
2. Get all `customers` that got changed within last 8 minutes in Netvisor (function `main` at `main.py`)
3. For each of them,

- if exists in Netvisor, update it.
- However, it must pass the verification that either its `updatedAt` field in `providers` is null (as this field was added in April 2022), or its `updatedAt` field in `providers` is greater than or equal to last updated field in Netvisor (to make sure data in `providers` is later than Netvisor).
- if it does not exist in Netvisor, insert it.

4. Log all the integration to the table `logsintegration`

#### Note

1. Data being sent as a POST body (functions `update_a_customer` and `create_a_customer` at `netvisor_operations.py`) must be reformatted correctly in an XML format. See https://support.netvisor.fi/en/support/solutions/articles/77000466758-resources-customer-register and download sample request bodies to see more. 

## Authors and Q&A

Mimi - my.bui.fi@gmail.com

## Version History

- 0.1.0: initial release
