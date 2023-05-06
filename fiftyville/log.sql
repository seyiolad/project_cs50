-- Keep a log of any SQL queries you execute as you solve the mystery.

--Starting with the crime_scene_report table
-- We query the report at the said day and street
SELECT * FROM crime_scene_reports
    WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

--In the crime scene reports all the 3 witnesses mentioned the backery
-- So we will query the backery security table on the said day and hour


SELECT * FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10;

--from the above query, 2 entrances and exits were observed around the time the stealing occured
--So i will limit the display to 4 rows
SELECT * FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 LIMIT 4;


--Let us see what the 3 interviewed said about the bakery
SELECT * FROM interviews
    WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%thief%";

--Let me show the names and transcript of the interviewd (Ruth, Eugene and Raymond)
SELECT name, transcript FROM interviews
    WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%thief%";

--According to Ruth the theft took like 10 minutes so we could infer that the thief got
--there around 10.05hrs and the stealing lasted till 10.15hrs when the thief drove away

--According to Eugene,the second witness,she saw him that morning withdrawings ome money at the ATM on Leggett Street

--According to Raymond the third witness,about the time the thief was to leave the thief called and spoke with someone for less than a minute the thief was
--leaving. The call was made around 10.14hrs or so then.From the conversation the thief was to take the earliest flight out of
--fiftyville the next day(29th). The person he was talking with was to buy flight ticket(28th).


--Going back to the witness of Ruth, we can query the backery logs afresh with that understanding.Look at the enterance/arrival
---that occured like 10.00hrs
SELECT * FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 LIMIT 10;

--i will focus on the exit because around that time the thief was leaving it must be after 10:15hrs

--ok Let's check what the second witness Eugene said that the thief made a withdrawal at the ATM on Leggett Street
--Lets query the atm_transactions table for the said day, location and transaction type which is withdrawal
SELECT * FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28
    AND atm_location = "Leggett Street"
    AND transaction_type = "withdraw";

--Let's revisit the witness of Raymond the last witness.The thief was to fly out of fiftyville early next(29th)
--so the accomplice must without fail buy thier ticket on the 28th. The thief called less than one minute

--for the flight on 29th. it is a departure flight
SELECT * FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29;


--The filght was to leave very early. So lets look for flights leaving early
--So lets look for departing flights between 0hrs and 10hrs
SELECT * FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12);

-- Let us check passengers,flight and airpots details
SELECT * FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12);

--Let  me select some fields from the query above
SELECT flight_id, passport_number,full_name,seat FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12);


--Let us check the call the thief made which was less than a minute made around 10.14hrs or so.
SELECT id, caller ,receiver, duration FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28;

--Let's do where duration is less than 1 minute(<60s)
SELECT id, caller ,receiver, duration FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--check the bank_account, atm_transaction and link it with people
SELECT atm_transactions.account_number, name, phone_number, passport_number, license_plate
    FROM bank_accounts
    JOIN people ON bank_accounts.person_id = people.id
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2021 AND month = 7 AND day = 28
    AND atm_location = "Leggett Street"
    AND transaction_type = "withdraw";

--good. now to let us nab the thief i can :
--1)  compare phone number from the above query with phone number of caller
-- 2) run license plates from the crime scene with the one in the above query
-- 3) compare passport number in the query above with the passport numbers of flight leaving fiftyVille

--1)  compare phone number from the above query with phone number of caller
    --let's run the phone_call query with duration less than a minute again to see if there is match
SELECT id, caller ,receiver, duration FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--Result 1: names that show up
------ name     caller_phone    reciever_phone  call_duration   passport    account_number  license_plate
--     ---------------------------------------------------------------------------------------------------
---    Bruce    (367) 555-5533  (375) 555-8161       45         5773159633      49610011       94KL13X
---    Diana    (770) 555-1861  (725) 555-3243       49         3592750733      26013199       322W7JE
---    Kenny    (826) 555-1652  (066) 555-9701       55         9878712108      28296815       30G67EN
---    Taylor   (499) 555-9472  (717) 555-1342       50         1988161715      76054385       1106N58
---    Benista  (338) 555-6650  (704) 555-2131       54         9586786673      81061156       8X428L0

-- 2) run license plates from the crime scene with the one in the above query

-----Let's run the license plates at the crime_scene again and compare it with those of the suspected thieves

SELECT license_plate, activity FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
    AND license_plate IN ("94KL13X", "322W7JE", "30G67EN", "1106N58", "8X428L0");

--Result 2: License plates that show up with corresponding name

--  license_plate  activity     name        passport
------------------------------------------------------
--  94KL13X         exit        Bruce      5773159633
--  322W7JE         exit        Diana      3592750733
--  1106N58         exit        Taylor     1988161715


-- 3) compare passport number in the query above with the passport numbers of flight leaving fiftyVille

--Let us the run the flight query again and compare the passport number with those of the suspects above
SELECT  passport_number, seat FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12)
    AND passport_number IN(5773159633, 3592750733, 1988161715);

--Result 3:
--  activity     name        passport       license_plate
------------------------------------------------------
--   exit        Bruce      5773159633      94KL13X
--   exit        Taylor     1988161715      1106N58


-- So we have two (2) suspects left. The thief was to take earliest flight out i.e the first flight

-- Let us check to see who took the earlist flight out.

SELECT hour, minute, passport_number, origin_airport_id, destination_airport_id, abbreviation  FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12)
    AND passport_number IN(5773159633,1988161715);

--According to the above query both of them left in the same flight to the same destination.
--So they both took the earleist flight!



-- Let us check the bakery security log again to clues
SELECT * FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
    AND license_plate IN ("94KL13X", "1106N58");

-- The query above for the 2 suspects is thurs
 id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58       |
+-----+------+-------+-----+------+--------+----------+---------------+
-- The robbery happened 10:15hrs according to crime scene report. Ruth said the robbery took like 10min.
--So the earlest time to have left was 10:18hrs according to the query above.
--if the thief didnt leave earliest after the theft he would have been apprehended.  So the thief couldn't have left
--at 10:35hrs.

-- So from the above, the Thief is the person with the license_plate "94KL13X" and that person is Bruce!!


--Let us find the city Bruce escaped to
SELECT flight_id, seat, origin_airport_id, destination_airport_id, abbreviation, full_name, city FROM passengers
    JOIN flights ON flights.id = passengers.flight_id
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND (hour = 0 OR hour <=12)
    AND passport_number IN(5773159633);

--From the above, the destination airport id is 4

--So let's check the destination airport id from the airports table to know where Bruce escaped to
SELECT city FROM airports WHERE id = 4;
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+

--The result above showed that Bruce escaped to New York City



-- Let us get who the accomplice is
-- The person whom Bruce called to get him flight ticket is the accomplice and his phone number is (375) 555-8161

-- Let us query the people table to see who owns the number
SELECT * FROM people WHERE phone_number = "(375) 555-8161";

+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 |                 | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+
--The query result above shows details of the accomplice who name is Robin!





---------------------------------------------------------------------------------------------------------------
--some of the useful information i used for quick overview
---------------------------------------------------------------------------------------------------------------



--Tables in the database
--airports              crime_scene_reports   people
--atm_transactions      flights               phone_calls
--bakery_security_logs  interviews
--bank_accounts         passengers


--my database schema
CREATE TABLE crime_scene_reports (
    id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    street TEXT,
    description TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE interviews (
    id INTEGER,
    name TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    transcript TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE atm_transactions (
    id INTEGER,
    account_number INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    atm_location TEXT,
    transaction_type TEXT,
    amount INTEGER,
    PRIMARY KEY(id)
);
CREATE TABLE bank_accounts (
    account_number INTEGER,
    person_id INTEGER,
    creation_year INTEGER,
    FOREIGN KEY(person_id) REFERENCES people(id)
);
CREATE TABLE airports (
    id INTEGER,
    abbreviation TEXT,
    full_name TEXT,
    city TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE flights (
    id INTEGER,
    origin_airport_id INTEGER,
    destination_airport_id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(origin_airport_id) REFERENCES airports(id),
    FOREIGN KEY(destination_airport_id) REFERENCES airports(id)
);
CREATE TABLE passengers (
    flight_id INTEGER,
    passport_number INTEGER,
    seat TEXT,
    FOREIGN KEY(flight_id) REFERENCES flights(id)
);
CREATE TABLE phone_calls (
    id INTEGER,
    caller TEXT,
    receiver TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    duration INTEGER,
    PRIMARY KEY(id)
);
CREATE TABLE people (
    id INTEGER,
    name TEXT,
    phone_number TEXT,
    passport_number INTEGER,
    license_plate TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE bakery_security_logs (
    id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    activity TEXT,
    license_plate TEXT,
    PRIMARY KEY(id)
);