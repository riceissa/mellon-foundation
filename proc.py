#!/usr/bin/env python3

import csv
import datetime
import sys

def main():
    if len(sys.argv) != 1+1:
        print("Please include the input CSV file as argument one.",
              file=sys.stderr)
        sys.exit()
    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries, affected_states,
        affected_cities, affected_regions) values""")

        first = True
        for row in reader:
            amount = row['amount']
            assert amount.startswith("$")
            amount = amount.replace("$", "").replace(",", "")
            donation_date = datetime.datetime.strptime(row['grant_date'],
                                                       "%Y-%m-%d %H:%M:%S")
            notes = "Program name: %s" % row["program"]
            int(amount)  # see if it can be converted to int
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Andrew W. Mellon Foundation"),  # donor
                mysql_quote(row['grantee']),  # donee
                amount,  # amount
                mysql_quote(donation_date.strftime("%Y-%m-%d")),  # donation_date
                mysql_quote("day"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(row["program"]),  # cause_area
                mysql_quote("https://mellon.org" + row["grantee_url"]),  # url
                mysql_quote(""),  # donor_cause_area_url
                mysql_quote(notes),  # notes
                mysql_quote(""),  # affected_countries
                mysql_quote(""),  # affected_states
                mysql_quote(""),  # affected_cities
                mysql_quote(""),  # affected_regions
            ]) + ")")
            first = False
        print(";")

def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)

if __name__ == "__main__":
    main()
