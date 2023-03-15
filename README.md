# Exploring FAC dissemination

This is code for exploring an early-stage prototype. No future services or consistency with these examples are implied or expressed. This is a pilot.

## Getting an API key

To use any of the code in this repository, you will need to obtain an API key from api.data.gov.

[https://api.data.gov/signup/](https://api.data.gov/signup/)

For purposes of verification during this pilot, you must use a Federal email address (.gov, .mil, etc.). You are able to have multiple keys associated with a single email address, if it becomes necessary for some reason.

You will receive an automatic email from api.data.gov containing your API key. This, however, is not yet enough to take part in the pilot.

## Requesting access

Please drop a note to fac@gsa.gov from the address you used to register your API key. Indicate that you would like to take part in the FAC public data dissemination pilot. We will add permissions to your key so that you can access the pilot API.

## Configuring your environment

The examples in this repository assume that you have two environment variables set; in a Bash shell, you would

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

## Read up on PostgREST

The API is generated automatically by [PostgREST](https://postgrest.org/en/stable/index.html). This open source tooling is designed to make the contents of a Postgres database available via a REST API. Queries against the data tables can be carried out using the operators described under [Tables and Views](https://postgrest.org/en/stable/api.html) in the PostgREST documentation. 

## Read up on the tables

We are still working on data export/import from Census. We're approaching stability, but some things are still a moving target. You can, in the `sql` directory, find the file `views.sql`. This describes all of the views that are available for you to query. For example, if you want to search for all the rows in the `federal_award` table with the dbkey of `101892`, you would issue the query:

```
curl -X GET -H "X-Api-Key: ${API_GOV_KEY}" https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination/federal_award?dbkey=eq.189201
```

Or, you can use the REST request library of your choice in the programming language of your choice. 

## Suggest API extensions

There are two ways we can (easily) extend the API:

1. Create views that limit or otherwise improve the search experience, and 
2. Add stored procedures that implement more advanced searches.

The file `procedures.sql` has an example of a stored procedure. It takes three parameters (`_cfda`, `_start`, and `_end`) and returns a list of awards between the start and end date provided for the CFDA prefix provided. It isn't a particularly *savvy* example, and (in truth) it could be a view. But, it shows that the API is actually implemented as SQL; therefore extending the API is a matter of adding new queries in the form of plain-old PostgreSQL queries.

## Got questions?

For the moment, use the fac@gsa.gov address; we will work on creating a developer-specific space for discussion soon, as we will want an ongoing space for conversation as the public dissemination API and other work takes place. We do not have an ETA on that developer-specific discussion space as of yet. Our goal was to release code quickly, so that we can iterate on the API in community with others.

# Revision history

The `git log` is the authoritative revision history.

* 2023/3/15 - First pass at docs.
* 2023/3/14 - First commit.