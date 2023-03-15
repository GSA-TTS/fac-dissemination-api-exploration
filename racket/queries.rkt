#lang racket/gui

(provide (all-defined-out))
(require net/http-easy
         "support.rkt")

;; What if I want to find submissions from my agency that have funding?
(define (submissions-by-cfda cfda year #:columns [columns '(dbkey audit_year)])
  (get-results
   (make-query 'federal_award
               (list (Query 'like 'agency_cfda (format "~a.*" cfda))
                     (Query 'eq 'audit_year year)
                     (Select columns)
                     ))
   #:end MAX-RESULTS))

(define (direct-by-cfda cfda year #:columns [columns '(dbkey audit_year)])
  (get-results
   (make-query 'federal_award
               (list (Query 'like 'agency_cfda (format "~a.*" cfda))
                     (Query 'eq 'audit_year year)
                     (Query 'eq 'direct "Y")
                     (Select columns)))
   #:end MAX-RESULTS))

(define (findings-for-cfda cfda year #:columns [columns '(dbkey audit_year)])
  (get-results
   (make-query 'federal_award
               (list (Query 'like 'agency_cfda (format "~a.*" cfda))
                     (Query 'eq 'audit_year year)
                     (Query 'eq 'direct "Y")
                     (Query 'gt 'findings_count 0)
                     (Select columns)))
   #:end MAX-RESULTS))

(define (total-dollars-direct cfda year)
  (define results (direct-by-cfda cfda year #:columns '(amount)))
  (apply +
         (for/list ([r results])
           (hash-ref r 'amount 0))))

(define (findings-by-date cfda start-date end-date)
  (get-results
   (make-api-call (API 'awards_between
                       (list
                        (Param '_cfda cfda)
                        (Param '_start start-date)
                        (Param '_end end-date)
                        )))
   #:end MAX-RESULTS))
  
(define (overview-by-cfda cfda year #:monthly? [monthly? true])
  (printf "CFDA ~a: ~a~n"
          cfda
          (hash-ref cfda-mapping (format "~a" cfda)))
  (printf "------------------------------------~n")
  (printf "Prorgam lines in year ~a: ~a~n"
          year
          ;; #:accessor (lambda (h) (hash-ref h 'dbkey))
          (length (submissions-by-cfda cfda year)))
  (printf "Program lines with direct funding in ~a: ~a~n"
          year
          (length (direct-by-cfda cfda year)))
  (printf "Program lines with direct funding and findings: ~a~n"
          (length (findings-for-cfda cfda year)))
  (define dollars (total-dollars-direct cfda year))
  (printf "Total direct dollars granted: ~a~n" dollars)
  (when monthly?
    (for ([year (range (+ 1 year) 2023)])
      (for ([month (range 1 12)])
        (printf "Program lines accepted between ~a-~a-1 and ~a-~a-1: ~a~n"
                year month year (+ 1 month)
                (length
                 (findings-by-date cfda
                                   (format "~a-~a-1" year month)
                                   (format "~a-~a-1" year (+ 1 month))))
                ))))
  (printf "---------------------------------------------~n")
  )


(define (show-all-cfdas)
  (for ([(k v) cfda-mapping])
    (overview-by-cfda k 2020 #:monthly? false)))
