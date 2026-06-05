# Movie Search Service (CLI Application)

A high-performance Command Line Interface (CLI) application designed for searching and analyzing movie records. The project implements a robust monolithic architecture with a strict separation between the presentation layer (UI) and the business logic, utilizing a dual-database approach (MySQL for relational data and MongoDB for analytical logging).

## Key Features

* **Layered Architecture**: Complete decoupling of visual formatting (`interface.py` via `tabulate`) and core application flows (`handler.py`).
* **Dual-Database Integration**:
  * **MySQL**: Stores primary movie entities, attributes, and genre classifications. Relies on window functions (`COUNT(*) OVER()`) to fetch total row counts efficiently within limited pagination slices.
  * **MongoDB**: Stores flattening historical logs of user queries. Performs complex analytical queries via aggregation pipelines to fetch recent and top-frequent operations.
* **Smart Local Caching**: In-memory page-level caching inside search flows to eliminate redundant database hits during reverse pagination navigation.
* **Fault-Tolerant Database Clients**: Custom decorators handle automatic failover reconnection loops (`ping(reconnect=True)`) and wrap driving execution parameters.
* **Unified Diagnostic Logging**: Custom logging wrapper tracking exact invocation arguments, method execution latency in milliseconds (`ms`), and dumping raw error traceback stacks directly into `app.log`.

---

## System Requirements

* Python 3.13
* MySQL Server 8.0+
* MongoDB Server 6.0+

---

## Installation & Setup

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:illaay/movies_cli_app.git
   cd movies_cli_app
   ```

2. Create and activate an isolated virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install required production dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environmental variables. Create a `.env` file in the root directory:
   ```env
   MYSQL_HOST=your_host
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_database_name

   MONGO_URI=mongodb://your_host/
   MONGO_DATABASE=your_mongo_db_name
   MONGO_COLLECTION=query_history
   ```

---

## Directory Structure

```text
movies-cli-app/
│
├── .venv/                   # Isolated virtual environment directory
│
├── db/
│   ├── __init__.py          # Database package initializer exposing clients
│   ├── mysql_client.py      # Connection manager and parameterized lookup queries
│   ├── mongo_client.py      # Resilient write pipelines and analytics aggregation
│   └── queries.py           # Static SQL strings and MongoDB aggregate statements
│
├── ui/
│   ├── __init__.py          # UI package layout documentation mapping
│   ├── handler.py           # Core routing controllers, input validators, and pagination
│   └── interface.py         # Presentation layout engines engineered via tabulate
│
├── .env                     # Local configuration override values (ignored by git)
├── .gitignore               # Specifications for untracked files to ignore
├── config.py                # Environment parser initializing configuration dictionaries
├── errors.py                # Domain-specific custom exception classes hierarchy
├── log_utils.py             # Performance profiling and crash lifecycle loggers
├── main.py                  # Isolated bootstrap endpoint executing application thread
├── README.md                # System documentation and operational architecture guide
└── requirements.txt         # Production dependencies assembly specification manifest
```

---

## Operational Guide

Execute the bootstrap script from the root directory to spin up the application process:

```bash
python main.py
```

### Available Interface Flows:
* `[k] / [keyword]`: Prompts string filters to parse match records in MySQL with real-time internal runtime caching.
* `[g] / [genre]`: Performs relational range evaluation matching a database-validated genre against dynamic year matrices.
* `[h] / [history]`: Leverages MongoDB aggregation arrays to print current system trends alongside the 5 latest query profiles.
* `[e] / [exit]`: Gracefully releases infrastructure dependencies and terminates the thread process with exit status 0.
