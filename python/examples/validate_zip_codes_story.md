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

## It is more complex than it seems (20230330)

Depending on how I look at the data, I can get more or less bad data. (O_o)

### Fewer bad zip codes...

I updated the script based on conversation with colleagues. First, I did a query to find the `id` for every auditee in 2020; I pulled that from the `auditee` table. From there, I then reached into the `federal_award` table, and looked fort he zip code associated with each of those ids.

This is what I found:


```
Starting with auditee ids, and working through to zips.
Sum of 5- and 9-digit zips: 17567
Good zips: 17557, bad: 10

Zips that did not match the pattern:
['99689NELL', '30286Resh', '92363Robe', '40977Albe', '99762Step', '70586Domi', '26681Debr', '01609MARK', '99750Brad', '20036Robe']
```

When a sequence of queries is constructed as above, there were very few "bad" zip codes. That is, only 10 zip codes do not match the pattern we have defined (for the new FAC) for a valid zip code. So, some made it through in 2020 that should not have.

### More bad zip codes...

However, I can structure the query so that I just pull *every zip code from the auditee table that I can find*. By "find" I mean "every one." 

Now, I get a very different result. There are 1161 zip codes that do not match our pattern. How did this information make it into the database? How, given the dumps from the FAC, do I know what data is *good*, and what is *bad*? 

And, of course, we want to prevent this going forward. But, this is the historical data, and it is clearly *not simple* to work with, given that a naive query can turn up more (rather than less) noise.

```
Pulling every zip from the auditee table.
Sum of 5- and 9-digit zips: 23888
Good zips: 23775, bad: 1161

Zips that did not match the pattern:
['98126Darc', '35640Rita', '36037Tamm', '36266Char', '99752JUDI', '72034Died', '96025Blak', '92408Toma', '32084Clin', '31639Juli', '31719Nata', '51502Beck', '50125Megh', '40444JENN', '42765Tres', '40359ROY ', '70527Nico', '01432FRED', '39150Shun', '38829Alic', '11901Jame', '43844Lee ', '44090Mark', '78364Meli', '43701Rhon', '98225Cind', '39773RICH', '98225Andy', '39532Dean', '33174Ana ', '99362Jean', '99630STEV', '79603Paul', '99576COUR', '11568Dian', '97470Gary', '59101Lisa', '99606JOAN', '99801Max ', '70466Mind', '52205Whit', '40906STEV', '99658RICH', '99801TERI', '15214Mark', '60608Paul', '19107Glen', '56228John', '77553Mark', '15203Mary', '07757JENN', '78705Ther', '70715Thi ', '59425Bren', '46312Meli', '70043Anth', '48105BIRG', '32209Step', '42141Jenn', '11590Meli', '60477John', '05855Mich', '98841Abby', '46278Mega', '01609MARK', '59072Tany', '49007Dani', '75247Mark', '59840Apri', '44308Chri', '11576Jame', '49534Dr N', '99588MARC', '22202Char', '32935Step', '77401Reve', '73127CHRI', '71201Tom ', '85003MARK', '99840SARA', '43138Juli', '97116Paul', '78641Ties', '44805MATT', '28352Luci', '63664Josh', '63645Alla', '23227Mart', '77019Amy ', '10018Alan', '95409STEV', '45402sand', '20024Rob ', '49686RICH', '90017ZERI', '02472Joe ', '30741JULI', '39345JOHN', '71301Robe', '70562Keit', '73023shar', '72401Marv', '62706Lori', '79701Davi', '6010', '6450', '6702', '6820', '6824', '6877', '6883', '6037', '6022', '6016', '6033', '6067', '6074', '67590488', '6787', '6413', '6416', '6035', '6776', '6360', '6470', '6078', '6475', '6518', '6238', '6762', '6477', '6483', '6482', '6716', '6525', '63391541', '6209', '6084', '62781530', '6374', '6902', '6810', '6443', '6103', '6480', '6457', '6418', '6460', '6514', '63606620', '6106', '6417', '67620395', '5401', '3811', '3750', '3301', '38205451', '33020877', '3064', '21385359', '2210', '4106', '3101', '4240', '34313748', '4005', '3833', '4084', '7102', '5478', '5827', '5201', '5753', '56412267', '5602', '4330', '40118445', '4364', '4212', '4769', '4785', '4742', '5466', '4011', '4901', '4468', '4073', '4732', '4039', '4412', '4345', '4217', '4453', '4427', '4443', '4426', '4086', '4967', '4950', '4958', '49889734', '4093', '4103', '21084805', '1301', '2149', '1752', '2048', '27662310', '1938', '1376', '1106', '1002', '1720', '2478', '1803', '1754', '2021', '2056', '2081', '23324499', '2043', '1507', '1527', '1540', '1473', '1475', '2601', '2664', '1201', '27220989', '2780', '2740', '1915', '1931', '18413649', '1844', '19502713', '1086', '1107', '2145', '1852', '1890', '2320', '2116', '1608', '1420', '1247', '2745', '1984', '1050', '1469', '1568', '1518', '1005', '5403', '2908', '3108', '3038', '3246', '3570', '3820', '3452', '3051', '3857', '3865', '86280360', '8360', '7834', '7871', '7882', '82322569', '3053', '7010', '7026', '70933327', '7094', '8540', '89042842', '8901', '8069', '72022690', '7065', '8002', '7603', '7628', '7410', '7430', '8088', '8505', '8108', '7041', '7003', '8028', '8066', '8071', '7032', '8822', '8801', '7735', '7730', '7849', '7940', '7896', '7866', '7876', '7930', '8734', '74703555', '8805', '8807', '8844', '7060', '8876', '7827', '7860', '7461', '7843', '7840', '8865', '5851', '2818', '2878', '2857', '2879', '2807', '2809', '29045647', '2896', '2806', '2452', '5301', '56010007', '5404', '5701', '3641', '53032275', '5655', '5843', '54042109', '6851603', '5001', '2127', '2115', '1103', '4092', '21164624', '2460', '63383008', '21482149', '41012437', '31012799', '4338', '2111', '8102', '2130', '8406', '4090', '3076', '1701', '4457', '6850', '6473', '2840', '88652624', '7929139', '2136', '681', '1605', '3077', '6381427', '5663', '6905', '4072', '2886', '6424', '1060', '4101', '4609', '65473249', '88620390', '79401811', '6340', '2861', '7712', '67980469', '6001', '687', '1801', '2888', '7029', '70262693', '65152687', '43382506', '41011802', '6032', '5604', '6604', '914', '77115806', '3302', '1089', '7621', '13012203', '4102', '51452455', '54042020', '4473', '2481', '5450', '2129', '2359', '3867', '7076', '31023546', '3801', '2720', '28852008', '2446', '2724', '2860', '19022513', '2631', '15811902', '1001', '43306835', '87012754', '1845', '7066', '7087', '4530', '2862', '1810', '2356', '18310751', '3110', '6270660', '2151', '2110', '7050', '82607379', '8691', '1609', '5819', '7462', '6120', '1880', '7645', '2108', '7936', '6610', '6043', '7652', '1970', '2169', '43305509', '1602', '1434', '2864', '8628', '3257', '2895', '4419', '2907', '602', '1730', '6451', '8541', '4736', '6071', '8835', '6013', '6139933', '70173141', '77016400', '70607431', '2150', '1501', '1952', '8332', '17571616', '1450', '7444', '5091', '7865', '704', '5363', '7465', '7670', '7405', '88764200', '1748', '18522106', '3229', '7035', '7044', '8611', '4786', '6112', '2093', '6052', '3042', '1940', '2139', '4430', '2114', '7006', '6042', '725', '612', '683', '7643', '73065943', '8982', '7039', '2632', '6492', '2871', '7042', '1886', '2119', '26681599', '8040', '7618', '74502504', '7030', '7002', '8401', '81031244', '78852431', '28052580', '2554', '3431', '7642', '14202697', '7101', '7306', '8232', '6053', '83021922', '1840', '2492', '7305', '7017', '80083926', '1606', '6254', '2457', '7201', '2467', '8812', '2454', '6605', '61083013', '80371875', '7107', '8648', '1960', '30544855', '7403', '6901', '7522', '6095', '32352026', '7203', '8833', '8723', '4841', '3054', '6712', '2466', '2138', '2184', '6498', '3045', '82262456', '7013', '7456', '6320', '8869', '7856', '2347', '7724', '2905', '24722790', '8103', '7050000', '1824', '8861', '2122', '7419', '8619', '70422713', '68511620', '7440', '6519', '3576', '3909', '6511', '7801', '7075', '2774', '21431310', '1841', '7054', '5641', '965', '8086', '61121556', '2109', '5402', '2909', '21697471', '7874', '1118', '2835', '1040', '1101', '21203225', '2828', '6026', '7661', '64220190', '2364', '56670320', '9360000', '7920', '962', '4210', '2746', '5673', '6410', '2035', '1854', '8260', '44012219', '2148', '2903', '1610', '2563', '7823', '7825', '1550', '86383955', '1831', '4963', '8402', '65151746', '1022', '11082821', '8034', '7416', '7417', '7059', '7028', '7740', '6371', '6513', '6409', '19400030', '6790', '4274', '7204', '2125', '4664', '4333', '1581', '4064', '2885', '4062', '5855', '2038', '2863', '3264', '4953', '7070', '8701', '2357', '2142', '8302', '1604', '43330059', '65115947', '2128', '13669500', '1902', '3060', '75051028', '6248', '6083', '6357', '9023970', '6801', '1949', '40436101', '2459', '85405913', '6105', '2889', '2891', '8101', '6854', '21084408', '6510', '11029000', '18302306', '2120', '2131', '29032282', '2147', '1440', '9194140', '1035', '1923', '2532', '7051', '16062092', '19705353', '6426', '23023993', '2816', '17301197', '24815399', '2325', '11093739', '3304', '7822', '7820', '8060', '920', '2135', '6226', '6484', '3109', '1851', '8690', '1085', '1950', '2493', '5060', '21502771', '8036', '2559', '8721', '8009', '5250', '5149', '87015907', '6108', '1749', '2881', '2920', '8059', '3581', '7304', '8724', '2360', '2657', '6517', '6446', '4605', '7503', '1571', '67020150', '76017077', '5759', '2324', '737', '15715000', '2301', '2458', '1453', '5491', '5452', '7302', '840', '7052', '3870', '5679', '2269', '5735', '4401', '7103', '21092720', '8837', '61340207', '5661', '2032', '64162027', '4009', '61032819', '2721', '1105', '2061', '2540', '8106', '6107', '1104', '4976', '6515', '1843', '1772', '984', '74702129', '27102999', '3278', '3105', '7666', '7180040', '2668', '6608', '1566', '8903', '8012', '1220', '2141', '1879', '2124', '3818', '7921', '6512', '1702', '3904', '7857', '2050', '2140', '8055', '6040', '7380031', '3102', '2143', '79221602', '1876', '8605', '7624', '1966', '7457', '7760', '21351011', '24582597', '1119', '2401', '80310000', '8928', '41013638', '4038', '2186', '2368', '4344', '2451', '21112670', '65115991', '2215', '2568', '2126', '4332', '1903', '2118', '2121', '1982', '18401251', '2155', '4416', '2772', '2646', '2660', '4765', '1901', '2494', '4263', '2723', '1062', '26013968', '4068', '1230', '2026', '4631', '2171', '2703', '1013', '1930', '1038', '1460', '21203401', '1545', '4643', '1742', '2144', '46683344', '1109', '2859', '29071435', '28404192', '2842', '29092459', '2832', '4544', '28892443', '2910', '6830', '6117', '65208327', '66062892', '6241', '6351', '3561', '6062', '6050', '27401708', '6051', '6860', '3755', '62682018', '6089', '71032842', '3120', '2472', '6127', '3242', '3461', '33021016', '7327313', '7190515', '910', '659', '680', '915', '27030963', '38332160', '3777', '18035085', '3743', '8234', '9023711', '1202', '15454176', '21442401', '6113', '7501', '6851', '2421', '7104', '28863077', '16101400', '21411001', '30793313', '1492', '7509', '2675', '6385', '6111', '1603', '6281', '3103', '99689NELL', '30286Resh', '92363Robe', '40977Albe', '99762Step', '70586Domi', '26681Debr', '99750Brad', '20036Robe', '65115966', '6611', '918', '48634119', '1945', '7728', '4104', '33022032', '40721539', '18521803', '927', '6896', '6461', '3598', '71021982', '4739', '4915', '56730566', '5068', '2655', '4938', '2642', '3878', '76017075', '919', '5743', '4224', '5074', '5482', '7062', '3063', '6114', '9012104', '6365', '8205', '33014020', '4693', '8244', '9180000', '4654', '6930000', '638', '926', '8030', '7438', '83322003', '8873', '6109', '5033', '7108', '1505', '4276', '67211503', '77541234', '1862', '1821', '31061045', '1077', '6098', '50011928', '2852', '1937', '6120000', '3903', '6794', '3814', '830', '4962', '917', '5154', '907', '4578', '4937', '7432', '8608', '9123150', '44015000', '1267', '8816', '7719', '9191227', '732', '4743', '65102047', '8904', '6489', '25431050', '4988', '42340000', '11192684', '16101477', '41120547', '10989753', '22155306', '5156', '7732', '9192379', '17301420', '8057', '2453', '6259', '22155450', '21103399', '2216', '2133', '47691116', '2189', '21222734', '2322', '43320587', '67763049', '7514', '4652', '1830', '18401401', '21502374', '24819181', '24455796', '3766', '2188', '38571843', '21555480', '16102473', '21182404', '42633348', '26013698', '1583', '21213213', '41040704', '2649', '42120713', '4074', '2067', '43320304', '4063', '21313907', '11093082', '18522103', '15453948', '21842692', '20383159', '6057', '2543', '21386095', '2917', '2918', '29036100', '28590312', '2892', '2919', '2914', '28321920', '28881524', '2906', '28133661', '68245195', '4672', '6516', '6549', '68251000', '6759', '28604003', '64732446', '7111', '63741229', '37551404', '68974028', '6232', '6880', '60851467', '61113954', '8054', '7470', '6705', '67763072', '61070365', '9363255', '9281345', '792', '9290132', '7150220', '9606032', '6311003', '716', '8224944', '6690379', '9101384', '6590907', '7230697', '9164457', '9280850', '7268518', '7781277', '9195678', '19010314', '2940', '62606001']
```

## Checking another way

What if I use `sqlite3`? 

1. I download `gen20.txt` from Census.
1. I open `sqlite3`. 
1. I issue `.mode csv`
1. I issue `.separator |`
1. I create the table below.
1. I issue `.import gen20.txt general`

Now, I can issue a query.

```
SELECT count(zipcode) FROM general WHERE length(zipcode) != 5 AND length(zipcode) != 9;
```

The result is `1`, because the header is included in the import. Or, I can do the following:

```
SELECT count(zipcode) FROM general WHERE length(zipcode) = 5 OR length(zipcode) = 9;
```

which returns 39805.

Again, that's proably off by 1. Yep; `cat gen20.txt | wc -l` yields 39806, which would be the header plus the data rows.

So, this suggests that the zipcodes from 2020 are clean. 

A quick check suggests 2022 is clean as well.

It continues after the table, though...

```
drop table if exists general;

create table general (
    AUDITYEAR TEXT,
    DBKEY TEXT,
    TYPEOFENTITY TEXT,
    FYENDDATE TEXT,
    AUDITTYPE TEXT,
    PERIODCOVERED TEXT,
    NUMBERMONTHS TEXT,
    EIN TEXT,
    MULTIPLEEINS TEXT,
    EINSUBCODE TEXT,
    DUNS TEXT,
    MULTIPLEDUNS TEXT,
    AUDITEENAME TEXT,
    STREET1 TEXT,
    STREET2 TEXT,
    CITY TEXT,
    STATE TEXT,
    ZIPCODE TEXT,
    AUDITEECONTACT TEXT,
    AUDITEETITLE TEXT,
    AUDITEEPHONE TEXT,
    AUDITEEFAX TEXT,
    AUDITEEEMAIL TEXT,
    AUDITEEDATESIGNED TEXT,
    AUDITEENAMETITLE TEXT,
    CPAFIRMNAME TEXT,
    CPASTREET1 TEXT,
    CPASTREET2 TEXT,
    CPACITY TEXT,
    CPASTATE TEXT,
    CPAZIPCODE TEXT,
    CPACONTACT TEXT,
    CPATITLE TEXT,
    CPAPHONE TEXT,
    CPAFAX TEXT,
    CPAEMAIL TEXT,
    CPADATESIGNED TEXT,
    COG_OVER TEXT,
    COGAGENCY TEXT,
    OVERSIGHTAGENCY TEXT,
    TYPEREPORT_FS TEXT,
    SP_FRAMEWORK TEXT,
    SP_FRAMEWORK_REQUIRED TEXT,
    TYPEREPORT_SP_FRAMEWORK TEXT,
    GOINGCONCERN TEXT,
    REPORTABLECONDITION TEXT,
    MATERIALWEAKNESS TEXT,
    MATERIALNONCOMPLIANCE TEXT,
    TYPEREPORT_MP TEXT,
    DUP_REPORTS TEXT,
    DOLLARTHRESHOLD TEXT,
    LOWRISK TEXT,
    REPORTABLECONDITION_MP TEXT,
    MATERIALWEAKNESS_MP TEXT,
    QCOSTS TEXT,
    CYFINDINGS TEXT,
    PYSCHEDULE TEXT,
    TOTFEDEXPEND TEXT,
    DATEFIREWALL TEXT,
    PREVIOUSDATEFIREWALL TEXT,
    REPORTREQUIRED TEXT,
    MULTIPLE_CPAS TEXT,
    AUDITOR_EIN TEXT,
    FACACCEPTEDDATE TEXT,
    CPAFOREIGN TEXT,
    CPACOUNTRY TEXT,
    ENTITY_TYPE TEXT,
    UEI TEXT,
    MULTIPLEUEIS TEXT);
```

### Continuing to dig...


```
SELECT zipcode FROM general WHERE CAST(zipcode AS INTEGER) IS NOT zipcode;
```

This yields:

```
99689NELL
30286Resh
92363Robe
40977Albe
99762Step
70586Domi
26681Debr
01609MARK
99750Brad
20036Robe
```

which tracks in that those are 9 characters long, but they're definitely not zipcodes. This matches what I found in my auditee-id driven query path.

Are there any four digit zipcodes lurking?

```
select zipcode from general where length(zipcode) = 4;
```

No. None.

So, where did the zipcode mess in the `auditee` table come from?