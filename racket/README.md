# API queries from Racket

Racket (https://racket-lang.org/) is a descendant of Scheme, which is a descendant of LISP. 

## Installing Racket

Visit the Racket website and follow the instructions there. Most users use DrRacket as the programming and execution environment. 

## Setting up your environment

The setup for Racket is not different from other languages. You will need to export `API_GOV_KEY` and `API_GOV_URL` in your environment. Then, either run `drracket` from the shell containing those variables, or run the code from the shell.


## Running queries

From the shell, 

```
racket -it queries.rkt
```

will load the `queries.rkt` file and let you interact with it. Given the prompt, you can then run something like

```
Welcome to Racket v8.6 [cs].
> (overview-by-cfda 23 2020)
```

which will then run some example queries for CFDA 23. 

## About the code

The dissemination API client code was prototyped in Racket, and that initial exploration was then ported to Python. The code is kept here for reference. We don't expect agencies to be using Racket, although it is a fun language to work in.

Racket is interesting in that it can be easily compiled into an executable on all major operating systems; in this regard, it has benefits over Python. In theory, this could be the starting point for a small .exe that could be used by agencies to run common/regular queries (e.g. "How many new submissions did we receive last week?")