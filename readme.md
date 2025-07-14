# 🎬 IMDb Technical Challenge

This project implements a complete IMDb-style system, including:

- A **REST API** for searching people and films.
- A **Python ETL pipeline** to download, process, and load IMDb data.
- Full support for **local** and **Dockerized** execution.

---

## 🧱 Project Structure

```text
.
├── cli/                # Interactive CLI to query the backend
│   ├── cli.py
│   ├── .env
│   └── requirements.txt
│
├── system_module_1/    # ETL module (Python)
│   ├── main.py
│   ├── etl/
│   ├── .env
│   └── requirements.txt
│
├── system_module_2/    # REST API server (Spring Boot)
│   ├── src/
│   ├── .env
│   └── pom.xml
│
├── docker-compose.yml
└── README.md
```

## ⚙️ Features
### ✅ REST API (Spring Boot)
* 🔍 Search people by name:
`GET /api/people?name=Bruce Lee`

* 🎬 Search films by title:
`GET /api/movies?title=Blacksmith Scene`

### ✅ ETL Pipeline (Python)
* Downloads .tsv.gz files from IMDb.
* Transforms and loads data into MySQL.
* Tracks all steps and allows CLI-based execution modes.

Supported modes:

* clean: Drop all tables info.

* reload: Clean and reload the entire dataset from scratch (batch or csv mode).

* update: Only apply new data changes not already in the database.

```text
🐳 By default, Docker runs the ETL in batch mode using real IMDb data.
```

## 🚀 How to Run

### 🐳 Easy Mode: Run Everything with Docker
From the root directory (where `docker-compose.yml` is located), run:

```bash
docker-compose up --build
```
This will automatically:
* 🛢️ Start a MySQL database container.

* 📥 Run the ETL module in batch mode to download and insert data.

* 🌐 Launch the Spring Boot API server (http://localhost:8080/api).

✅ After setup, all services will be up and data ready to query.

### 🧑‍💻 Using the CLI
You can now use the CLI tool to search people and films.

📦 Download the `.exe` file from the [GitHub Releases](https://github.com/juanjosetpc/imdb-challenge/releases) page.

cli.exe: Queries the API running from docker.

```bash
./cli.exe
```
No setup needed — just download and run.

## 🧪 Fully Manual Startup (Local Development)

> Requirements: Python 3.9+, Java 17+, Maven, MySQL (running on `localhost:3306`)

---

### 0. Clone the repository

```bash
git clone https://github.com/juanjosetpc/imdb-challenge.git
cd imdb-challenge
```

### 1. Start MySQL locally

### 2. Configure `.env` files
Make sure each module (`system_module_1`, `system_module_2`, and `cli`) has a .env file with appropriate MySQL credentials. Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=imdb_db
DB_USER=root
DB_PASSWORD=root
```
🔁 This step ensures that the ETL, API, and CLI modules connect to the same database instance.

### 3. Run the ETL pipeline manually
```bash
cd system_module_1
pip install -r requirements.txt
python main.py reload
```
🛠️ Other available modes:

```bash
python main.py clean      # Drop all tables
python main.py update     # Insert only new data (diff mode)
python main.py reload     # Load datasets in batch mode.
python main.py reload csv # Load datasets from a temp csv in a quickly manner (only for local deployment). 
```

### 4. Start the Spring Boot API
```bash
cd system_module_2
./mvnw spring-boot:run
```
Once running, test the API from your browser or CLI:

* http://localhost:8080/api/people?name=Bruce

* http://localhost:8080/api/movies?title=Matrix

### 5. Run the CLI
You have two options:

▶️ Run from source (with Python)
```bash
cd cli
pip install -r requirements.txt
python cli.py
```
📦 Run prebuilt executable (Windows)
Download from the Releases page:

Then execute:
```bash
./cli.exe
```

🧠 This executable is automatically generated and included with every GitHub release.






