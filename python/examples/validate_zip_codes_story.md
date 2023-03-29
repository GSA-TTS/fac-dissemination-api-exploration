# Examining zip codes

As we announced at the last brown bag, we have released a "version 0" of tooling to let agencies begin exploring FAC data (and begin developing automations around that data). With time, the existence of the API will allow us (as a community) to develop and share tooling to use/explore this data.

**How bad are zip codes in 2020?** (Our demo data load is mostly 2020 data.)

I put together a short program (linked below) that does the following:

1. It looks at every unique zip code for every auditee in the database (from 2020, mostly).
2. It then counts how long each zip code is.

'unique zip codes' means that I don't care how often 04240 appears; I count it once as a 5 digit zip code. This yields around 26,000 zip codes for auditees, out of roughly 40,000 zip codes in the USA. At a glance, I'll buy those numbers.

Here's what I found:

* **There are 29 unique zip codes that are 3 digits long**.
* **There are 767 unique zip codes that are 4 digits long**.
* There are 15999 unique zip codes that are 5 digits long.
* **There are 37 unique zip codes that are 7 digits long**.
* **There are 215 unique zip codes that are 8 digits long**.
* There are 7889 unique zip codes that are 9 digits long.

I bolded the lines that should be impossible. There are no 3 digit zip codes.
