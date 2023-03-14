
DROP FUNCTION IF EXISTS public.awards_between(_cfda TEXT, _start DATE, _end DATE);
CREATE OR REPLACE FUNCTION public.awards_between(_cfda TEXT, _start DATE, _end DATE)
  RETURNS TABLE(dbkey TEXT, audit_year TEXT)
  LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY 
    SELECT DISTINCT public.federal_award.dbkey::TEXT, public.federal_award.audit_year::TEXT
    FROM public.federal_award, public.general 
    WHERE 
        public.general.fac_accepted_date >= _start
        AND 
        public.general.fac_accepted_date < _end
        AND
        public.general.dbkey = public.federal_award.dbkey
        -- AND 
        -- public.general.audit_year = public.federal_award.audit_year
        AND 
        public.federal_award.direct = 'Y'
        AND 
        public.federal_award.agency_cfda LIKE concat(_cfda, '.%')
        -- AND
        -- public.federal_award.findings_count > 0
        ; 
END
$$;

GRANT EXECUTE ON FUNCTION public.awards_between TO anon;
NOTIFY pgrst, 'reload schema';