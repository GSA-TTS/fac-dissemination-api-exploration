#lang racket
(require net/http-easy
         csv-reading)
(provide (all-defined-out))

(define MAX-RESULTS 1000000)

(define cfda-mapping
  (let ([h (make-hash)])
    (for ([pair (csv->list (open-input-file "../sql/agency-cfda.csv"))])
      (hash-set! h (first pair) (second pair)))
    h))

;; Structures
(struct PK (dbkey audit-year))
(struct Select (columns))
(struct Query (op column value))
(struct Or (loq))
(struct And (lhs rhs))
(struct API (endpoint lop))
(struct Param (key value))

(define (render-api-call q)
  (match q
    [(struct API (endpoint lop))
       (define params
         (apply string-append
                (add-between
                 (map render-api-call lop) "&")))
       (format "~a?~a" endpoint params)]
    [(struct Param (key value))
     (format "~a=~a" key value)]
    ))

(define (make-api-call api)
  (format "~a/rpc/~a"
          (getenv "API_GOV_URL")
          (render-api-call api)))

(define (render-or-operands q)
  [match q
    [(struct Or (loq))
     (map render-or-operands loq)]
    [else
     (render-query q #:notation ".")]
    ])

(define (render-query q #:notation [notation "="])
  (match q
    [(struct PK (dbkey audit-year))
     (format "dbkey=eq.~a&audit_year=eq.~a" dbkey audit-year)]
    [(struct Select (columns))
     (format "select=~a"
             (apply string-append
                    (add-between (map (λ (o) (format "~a" o)) columns) ",")))]
    [(struct Query (op column value))
     (format "~a~a~a.~a" column notation op value)]
    [(struct Or (loq))
     (format "or=(~a)"
             (apply
              string-append
              (add-between (map render-or-operands loq) ",")))]
    [(struct And (lhs rhs))
     (format "and=(~a,~a)"
             (render-query lhs #:notation ".")
             (render-query rhs #:notation "."))]
    ))

(define (render-queries loq)
  (apply string-append (add-between (map render-query loq) "&")))

(define (uniq ls #:accessor [acc (lambda (v) v)])
  (cond
    [(empty? ls) '()]
    [(member (acc (first ls)) (map acc (rest ls)))
     (uniq (rest ls) #:accessor acc)]
    [else (cons (first ls) (uniq (rest ls) #:accessor acc))]))

(define (make-query table loq)
  (format "~a/~a?~a" (getenv "API_GOV_URL") table (render-queries loq)))

(define (get-results qurl #:start [start 0] #:end [end 10] #:debug [debug? false])
  (when debug? (printf "[ ~a ]~n" qurl))
  (let loop ([start 0]
             [responses empty])
    (cond
      [(> start end)
       responses]
      [else
       (define step-end (+ start 10000))
       (define json
         (response-json (get qurl
                             #:headers (hasheq 'Range-Unit "items"
                                               'Range (format "~a-~a" start step-end)
                                               'X-Api-Key (getenv "API_GOV_KEY")
                                               ))))
       (if (empty? json)
           responses
           (loop step-end (append json responses)))])))
    
