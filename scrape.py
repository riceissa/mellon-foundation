#!/usr/bin/env python3

import pdb

import csv
import datetime
import requests
import sys
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 1+2:
        print("Unexpected arg count. Please run as\n"
              "    ./scrape.py max_page outfile\n"
              "where\n"
              "  * max_page is an integer that specifies the last page of\n"
              "    grants (e.g. if menu says Page 1 of 657, then max_page\n"
              "    is 657)\n"
              "  * outfile is the file in which to store the output (a CSV)")
        sys.exit()

    page = 1
    url_base = "https://mellon.org/grants/grants-database/advanced-search/?page="
    max_page = int(sys.argv[1])

    with open(sys.argv[2], "w", newline="") as f:
        fieldnames = ["grantee", "grantee_url", "project", "project_url",
                      "grant_date", "amount", "location", "program"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while page <= max_page:
            print("On page " + str(page), file=sys.stderr)
            url = url_base + str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            tables = soup.find_all("table", {"class": "grant-list"})
            assert len(tables) == 1, "Error: More than one grants table found"
            table = tables[0]

            headers_found = list(map(lambda x: x.text.strip(), table.find_all("th")))
            headers_expected = ['Grantee', 'Project', 'Date', 'Amount', 'Location',
                                'Program']
            assert headers_found == headers_expected
            # Build header access map so that we can say cells[h[key]] rather than
            # cells[idx]
            h = {key: idx for idx, key in enumerate(headers_expected)}

            # Loop through table rows, but skip the header row
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                grantee = cells[h["Grantee"]].text.strip()
                grantee_url = cells[h["Grantee"]].a.get("href").strip()
                project = cells[h["Project"]].text.strip()
                project_url = cells[h["Project"]].a.get("href").strip()
                grant_date = datetime.datetime.strptime(cells[h["Date"]].text.strip(),
                                                        "%m/%d/%y")
                amount = cells[h["Amount"]].text.strip()
                location = cells[h["Location"]].text.strip()
                program = cells[h["Program"]].text.strip()

                writer.writerow({
                    "grantee": grantee,
                    "grantee_url": grantee_url,
                    "project": project,
                    "project_url": project_url,
                    "grant_date": grant_date,
                    "amount": amount,
                    "location": location,
                    "program": program,
                })

            page += 1


if __name__ == "__main__":
    main()
