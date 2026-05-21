CREATE TABLE "User" (
    "User ID"         SERIAL PRIMARY KEY,
    "User name"       TEXT    NOT NULL,
    "User type"       TEXT    NOT NULL,
    "Email"           TEXT    NOT NULL,
    "Phone number"    TEXT    NOT NULL,
    "Membership type" TEXT    NOT NULL
);

CREATE TABLE "User Authentication" (
    "Authentication ID"     SERIAL PRIMARY KEY,
    "User ID"               INTEGER REFERENCES "User" ("User ID") NOT NULL,
    "Password"              TEXT NOT NULL
);

CREATE TABLE "Schedule" (
    "ScheduleInstanceID"  SERIAL PRIMARY KEY,
    "User ID (member)"    INTEGER REFERENCES "User" ("User ID") NOT NULL,
    "User ID (trainer)"   INTEGER REFERENCES "User" ("User ID") NOT NULL,
    "Date/time"           TIMESTAMP NOT NULL
);

CREATE TABLE "Parking" (
    "ParkingInstanceID" SERIAL PRIMARY KEY,
    "User ID"           INTEGER REFERENCES "User" ("User ID") NOT NULL,
    "License plate"     TEXT    NOT NULL,
    "Payment"           NUMERIC NOT NULL,
    "Start timestamp"   TIMESTAMP NOT NULL,
    "End timestamp"     TIMESTAMP NOT NULL
);

CREATE TABLE "Credit Card Information" (
    "CreditCardID"  SERIAL PRIMARY KEY,
    "User ID"       INTEGER NOT NULL REFERENCES "User" ("User ID"),
    "Card number"   TEXT    NOT NULL,
    "Expiry"        TEXT    NOT NULL,
    "CVC"           INTEGER NOT NULL
);
