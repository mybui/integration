# HubSpot Integration

## Description

- The program is implemented for the HubSpot integration to DB. Currently, it supports the integration of `companies` data at tables `providers` and `shops`.
- In HubSpot, `providers` are those companies that got `customer_type_vapaus` equals "Benefit Bike Customer" or "Shared Fleet Customer".
- While `shops` are those companies that got `customer_type_vapaus` equals "Bike Shop Partner".

## Getting Started

### Executing program

- Use this command for every daily 10-minute run:

```
poetry run python3 main.py
```

### Program logic

#### Field matching for tables `providers` and `shops`:

https://docs.google.com/spreadsheets/d/1k3yvZug-TrnJRpc5oxeCsaXyF-9IuA6t4QD03XOCbqs/edit?usp=sharing

#### Logic

1. Get all companies with missing HubSpot data for `hubspotId` and `employeeCount` in tables `providers` and `shops`, and populate these fields (function `update_hubspot_company_info` at `main.py`)
2. Get all `providers` and `shops` that got changed within last 15 minutes in HubSpot (function `main` at `main.py`)
3. For each of them,

- if exists in `providers` or `shops`, update it.
- However, it must pass the verification that either its `updatedAt` field in DB is null (as this is a field was added in April 2022), or its `updatedAt` field in DB is smaller than or equal to `hs_lastmodifeddate` field in HubSpot (to make sure data in HubSpot is later than DB).
- if it does not exist in `providers` or `shops`, insert it.

4. Log all the integration to the table `logsintegration`

#### Note

1. HubSpot API key should be rotated at least every 6 months. This is not compulsory, but should be done for security.
2. Currently, the API limit for free account is about 10 calls/second. The program is throttled to stay under this limit. Consider un-throttle it to make the program run faster, if this API limit is expanded or for local development.

## Authors and Q&A

Mimi - my.bui.fi@gmail.com

## Version History

- 0.1.0: initial release
