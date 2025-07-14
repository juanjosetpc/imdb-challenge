# Changelog :: IMDB_CHALLENGE

## [v1.0.0] - 2025-07-10
- Initial stable release.
- Added ETL pipeline (Python) to process IMDb datasets and load into MySQL.
- Implemented REST API (Spring Boot) to query movies and people.
- Added Docker Compose setup to run full stack (MySQL, ETL, API).
- Added CLI tool with both local and Docker versions.
- GitHub workflow to auto-build and attach CLI `.exe` files on release.
