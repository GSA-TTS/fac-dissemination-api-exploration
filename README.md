# FAC Dissemination API 

Last updated 2023-04-17

## Overview

The FAC Dissemination API currently exposes historical, public data from the FAC. This is a living system (not yet "released"). We are exposing this API early so that Federal partners can work with us to right-size and right-shape the API for integration into their systems. Therefore, things *will* change (which means things *will* break), and we ask that teams and developers working with us remain engaged and curious.

The API is fronted by [api.data.gov](https://api.data.gov/). You will need to:

1. [Obtain a key from api.data.gov](https://api.data.gov/signup/), using a .gov or other government email address.
2. Write fac@gsa.gov from that same email address and ask for your key to be approved for use with the pilot.

At this time, we are manually approving keys (because we are in the early days of a pilot). That means a human being reads your email, goes into an admin panel, finds your account, and pushes a button. The human being may require a day or two in order to catch the email and push the buttons.

Our instructions assume you are comfortable as a developer using the command line. The instructions here should "just work" for someone using a Mac, a Linux workstation, or a Windows "git bash" shell. Powershell users should be able to adapt these instructions in a fairly straight-forward manner.

### Toward community

By launching our pilot early, we hope to develop an understanding of the needs of Federal oversight teams, so that we can extend the API and provide the best interface possible for the work that needs to be done. In other words, oversight teams should be saying things like "You know, if you had a call that did *this* for me, it would accelerate our workflow a meeelion times over..."

As we proceed, we welcome documentation suggestions/fixes, as well as code we can share. Ultimately, our goal is to build a thriving ecosystem around the API to benefit Federal and public users of this data. 

## Getting started

Once you have a key from api.data.gov, you're ready to start exploring. The examples in this repository assume that you have two environment variables set; in a Bash shell, you would

```
export API_GOV_KEY="..."
export API_GOV_URL="https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination"
```

Those two environment variables must be present in your shell for the code provided to work "as is." If you are on Windows, you can either use the Windows Subshell for Linux (WSL) to run the code, or in a Windows command shell:

```
set API_GOV_KEY="..."
set API_GOV_URL= as above...
```

*We have not tested this code under Windows; if you do, please report back how things work, or feel free to offer additions to this repository for others to benefit from.*

Once you do this, you should be able to

```
curl -X "GET" -H "X-Api-Key: ${API_GOV_KEY}" "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_auditee?limit=5"
```

This will return an [array of JSON objects](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON). Each object will represent a row in the auditee table, which (roughly) maps to the auditee table that Census exports from their download page.

## The API spec

It is possible to get a JSON spec of the entire API. We don't find this document terribly useful, but you might want it for some reason we cannot predict.

Point your browser (or `curl`) at:

```
https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination?api_key=YOUR_API_KEY_HERE
```

and api.data.gov will authenticate you, and then pass you through to the API backend without a query. The result is that you will receive the JSON spec for the entire API.

Personally, we find this almost completely unreadable. It may be of use for some automated integration with your systems, however.

### The Swagger-ified spec

We are using [Swagger](https://swagger.io) to present an interactive, readable version of the API documentation. 

[https://fac-dev-swagger.app.cloud.gov/#/](https://fac-dev-swagger.app.cloud.gov/#/)

The page presents a list of API endpoints that you can explore; these map to the tables that the Census FAC export CSV files (roughly). Or: if you are familiar with the historical export data, much of this will look familiar. We have presented these as views into the underlying tables; hence the `vw` prefix. 

If you visit that page (and, find your way down to the `vw_general` table), you can see that the table has a large set of parameters that you can use to explore. Each of these API parameters maps to a column in the underlying table. 

## Constructing queries

The API is visualized using Swagger; it is exposed using [PostgREST](https://postgrest.org/en/stable/). PostgREST is a small web service that automates the process of exposing Postgres tables as API services. Because the FAC is built on open software (and, in particular, uses Postgres as the underlying database engine), it makes sense to leverage PostgREST for this purpose.

We highlight this because you [can, should, and must use the PostgREST API documentation](https://postgrest.org/en/stable/api.html) for query construction. "For free," we get all of the expressive power of PostgREST as part of the FAC Dissemination API.

### Example queries

#### How many entries are in the `vw_general` table?

```
curl -X "GET" -H "x-api-key: ${API_GOV_KEY}" \
    "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_general?limit=1" \
    -H "prefer: count-estimated" \
    -I
```

This will return a set of headers, and the answer will live in the `content-range` key:

```
HTTP/2 206 
...
content-range: 0-0/22015
...
```

### How can I get the first 10 results for audit year 2022

```
curl -X "GET" -H "x-api-key: ${API_GOV_KEY}" \
    "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_general?audit_year=eq.2022&limit=10" 
```

The query is composed by asking for the `audit_year` column, where we set it equal to the `eq` operator with the value `2022`. [This is the first operator documented in the PostgREST documentation](https://postgrest.org/en/stable/api.html?highlight=count#horizontal-filtering-rows:~:text=HTTP/1.1-,Operators,equals,-gt). We are using the `limit` operator to keep the result set small.

PostgREST returns an array of JSON objects by default. Each object in the array represents a row in the database. We recommend the tool `jq` to prettify the results. For eaxmple, 


```
curl -X "GET" -H "x-api-key: ${API_GOV_KEY}" \
    "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_general?audit_year=eq.2022&limit=1" \ 
    | jq 
```

becomes (collapsed for readability)

<details>
  <summary>Expand result object</summary>
  
```
[
  {
    "id": 1,
    "dollar_threshold": 750000,
    "special_framework_required": null,
    "going_concern": false,
    "material_weakness": false,
    "material_noncompliance": false,
    "dup_reports": false,
    "low_risk": true,
    "condition_or_deficiency_major_program": false,
    "material_weakness_major_program": false,
    "questioned_costs": false,
    "current_or_former_findings": false,
    "prior_year_schedule": false,
    "report_required": null,
    "total_fed_expenditures": 3781298,
    "cognizant_agency": null,
    "oversight_agency": 93,
    "entity_type": "Non-profit",
    "period_covered": "A",
    "special_framework": null,
    "type_of_entity": "908",
    "fy_start_date": null,
    "fy_end_date": "2022-04-30",
    "auditee_date_signed": "2023-01-05",
    "cpa_date_signed": "2023-01-05",
    "initial_date_received": null,
    "form_date_received": null,
    "component_date_received": null,
    "completed_date": null,
    "previous_completed_on": null,
    "fac_accepted_date": "2023-01-05",
    "number_months": null,
    "audit_type": "S",
    "type_report_financial_statements": "U",
    "type_report_special_purpose_framework": null,
    "type_report_major_program": "U",
    "dbkey": "100003",
    "audit_year": "2022",
    "date_published": "2023-01-10",
    "previous_date_published": null,
    "cognizant_agency_over": "O",
    "revision_id": null,
    "create_date": "2023-03-27T16:42:08.237083+00:00",
    "data_source": "public downloads",
    "is_public": true,
    "modified_date": "2023-03-27T16:42:08.526967+00:00",
    "auditee_id": 1,
    "reportable_condition": false,
    "significant_deficiency": null,
    "primary_auditor_id": 1,
    "pdf_urls": null,
    "auditee_name": "NORTHEAST OKLAHOMA COMMUNITY ACTION AGENCY, INC.",
    "cpa_firm_name": "SAUNDERS & ASSOCIATES, PLLC",
    "secondary_auditor_id": null,
    "federal_award_id": [
      125603,
      125604,
      125605,
      125606,
      125607,
      125608,
      125609,
      125610,
      125611,
      125612,
      125613,
      125614,
      125615,
      125616,
      125617,
      125618
    ],
    "finding_id": null,
    "finding_text_id": null,
    "note_id": [
      35882,
      35881,
      35883,
      35884
    ],
    "cap_text_id": null,
    "passthrough_id": [
      196939,
      196940,
      196941,
      196942,
      196933,
      196934,
      196935,
      196936,
      196937,
      196938,
      198287
    ]
  }
]

```
</details>

&nbsp;

### Given an entry from the general table, find the awards associated with it

Our views are not direct mappings of the CSVs from Census; we have done some work for you. For example, in the `general` result above, you can see that `federal_award_id` is an array. In this regard, we have collapsed the one-to-many relationship into a more useful form for you when using the API.

On the command line, we can extract that array using `jq`, and loop through those IDs to find the associated award objects. First, grab the array of values:

```
ARR=$(curl -X "GET" -H "x-api-key: ${API_GOV_KEY}"     "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_general?audit_year=eq.2022&limit=1" | jq -c '.[0].federal_award_id[]')
```

Then, loop. Note how `jq` is being used to deconstruct the JSON array/object in both commands. (If you're working in a programming language like Python, this will be *much* simpler...)

```
for i in `echo $ARR` 
do curl -s -X "GET" -H "x-api-key: ${API_GOV_KEY}" \
    "https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/vw_federal_award?id=eq.$i" |
    jq '.[0].agency_cfda';
done
```

This yields:

```
"93.600"
"81.042"
"97.024"
"45.310"
"93.600"
"93.569"
"14.231"
"97.024"
"93.569"
"93.558"
"93.569"
"93.568"
"10.558"
"14.235"
"14.231"
"14.239"
```

## In practice

In practice, you're going to often start your queries with the `vw_general` endpoint, and then drill down into other tables from there. Note that PostgREST has the ability to do rich searches against text fields, greater-than and less-than on numbers, and so on; as a result, you can create queries that allow you to zero in on the contents of the SF-SAC as well as select (for example) specific date ranges.

We have [some example code](https://github.com/GSA-TTS/fac-dissemination-api-exploration) you can use to continue your explorations. We will gladly add additional examples, update this documentation, etc. as members of the community engage.

### CSV vs. JSON

It is possible to get the results from any query in multiple formats. If you are authoring queries using a library like `requests` (in Python), you will probably want the JSON response format. However, you might also want a query to come back natively in (say) CSV. PostgREST allows you to [set the response format to CSV](https://postgrest.org/en/stable/api.html#response-format), which we think some members of the community will find useful. 

Ultimately, we again recommend reading through the PostgREST documentation to learn what is possible with the FAC API.

## Expanding the API

New API endpoints can be expressed against the underlying database as SQL stored procedures. This means that, for us to create a new API endpoint, we [simply need to write the query](https://postgrest.org/en/stable/api.html#custom-queries). We can also use languages like plPgSQL for our API endpoints, if straight SQL is not rich enough to capture the query... or, even, wrap more complex queries up as part of the FAC Django web application. 

We note this because we suspect that the community will want richer endpoints than those made available here. An example that we anticipate is the ability to download CSV files that are similar/identical to those currently provided by Census. (Or, if not like those provided by Census, there may be a desire to get an audit submission *package* as a single zipfile, for example.) This would be a custom endpoint that, if there is demand/desire, we can provide.

## Bulk download

We anticipate the desire for bulk download, and have not investigated it at this time. That does not mean we are not considering it; it does mean that we prioritized getting the API up and live for testing before we worked on a problem that essentially amounts to dumping the database.

## Got questions?

For the moment, use the fac@gsa.gov address; we will work on creating a developer-specific space for discussion soon, as we will want an ongoing space for conversation as the public dissemination API and other work takes place. We do not have an ETA on that developer-specific discussion space as of yet. Our goal was to release code quickly, so that we can iterate on the API in community with others.

# Revision history

The `git log` is the authoritative revision history.

* 2023/04/17 - Revised for new tables, Swagger release.
* 2023/03/15 - First pass at docs.
* 2023/03/14 - First commit.