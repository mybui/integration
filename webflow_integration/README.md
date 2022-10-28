# Webflow Integration

## Description

The program is implemented for the Webflow integration to DB. Currently, it supports the integration of data at the table `shops` and the collection `Partners` in Webflow.

## Getting Started

### Executing program

- For local development or to try out the program, where you DON'T want to publish the changes, use this command:

```
poetry run python3 main.py
```

- If you are sure that you want to publish the changes, use this command:

```
poetry run python3 main.py --live=1
```

### Program logic

#### Field matching for `shops`:

- `name` in Webflow: `name` in `shops`
- `business_id` in Webflow: `businessId` in `shops`
- `locations` in Webflow: `city` in `shops`

#### Logic

1. Get all companies with missing Webflow data for `webflowId` and in `shops`, and populate these fields (function `update_webflow_company_info` at `main.py`)
2. Get all `partners` that got changed within last 15 minutes in Webflow (function `main` at `main.py`)
3. For each of them,

- if exists in `shops`, update it.
- However, it must pass the verification that either its `updatedAt` field in `shops` is null (as this field was added in April 2022), or its `updatedAt` field in `shops` is greater than or equal to `updated-on` field in Webflow (to make sure data in `shops` is later than Webflow).
- if it does not exist in `shops`, insert it.

4. Log all the integration to the table `logsintegration`

#### Note

2. Consider rotating Webflow API key if possible every number of months.
3. At the time of implementation, the program does not integrate the collection `Partner Cities` as it is not required.
4. If it is required in the future, more steps such as updating the `Partner Cities` collection while updating/creating new data in the `Partners` should be done.

## Authors and Q&A

Mimi - my.bui.fi@gmail.com

## Version History

- 0.1.0: initial release
