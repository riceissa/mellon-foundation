# Andrew W. Mellon Foundation

This is for Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

See https://github.com/vipulnaik/donations/issues/91 for the issue on DLW repo.

See https://mellon.org/grants/grants-database/advanced-search/ for data source.

## Files

- `scrape.py` scrapes the website and stores data in a CSV.
- `proc.py` takes the CSV file and transforms it into a SQL file to be used for DLW.

## Instructions for doing a run

```bash
# If you need to scrape data, run scrape.py. Make sure you change the date
# and set the correct max_page. Run the script without arguments to see an
# explanation.
./scrape.py  # Print instructions
./scrape.py 657 data-2019-01-13.csv  # get pages [1, 657] and store in the CSV

# Once you have the CSV, run proc.py
./proc.py data-2019-01-13.csv > data-2019-01-13.sql
```

## License

CC0 for scripts, not sure about the data.
