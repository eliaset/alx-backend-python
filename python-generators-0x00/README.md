\# Python Generators - ALX Backend Project



\## Overview

This project demonstrates the use of \*\*Python generators\*\* to efficiently stream and process data from a MySQL database.



\## Tasks

1\. \*\*Stream rows from SQL\*\* - Fetch one row at a time using a generator (`0-stream\_users.py`).

2\. \*\*Batch processing\*\* - Process users in batches and filter users over 25 (`1-batch\_processing.py`).

3\. \*\*Lazy pagination\*\* - Fetch paginated data lazily on demand (`2-lazy\_paginate.py`).

4\. \*\*Memory-efficient aggregation\*\* - Compute average age without loading all data at once (`4-stream\_ages.py`).



\## Setup

1\. Create MySQL database `ALX\_prodev`.

2\. Populate table `user\_data` using `seed.py` and `user\_data.csv`.

3\. Run the scripts to test generator functionality.



\## Usage

```bash

python 0-main.py

python 1-main.py

python 2-main.py

python 3-main.py

python 4-stream\_ages.py

