CREATE TABLE IF NOT EXISTS films (
    tconst VARCHAR(20) PRIMARY KEY,
    titleType VARCHAR(50),
    primaryTitle VARCHAR(1000),
    originalTitle VARCHAR(1000),
    isAdult BOOLEAN,
    startYear INT,
    endYear INT,
    runtimeMinutes INT,
    genres VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS people (
    nconst VARCHAR(20) PRIMARY KEY,
    primaryName VARCHAR(255),
    birthYear INT,
    deathYear INT,
    primaryProfession VARCHAR(255),
    knownForTitles TEXT
);

CREATE TABLE IF NOT EXISTS people_films (
    nconst VARCHAR(20),
    tconst VARCHAR(20),
    category VARCHAR(100),
    job VARCHAR(255),
    characters TEXT,
    PRIMARY KEY (nconst, tconst),
    FOREIGN KEY (nconst) REFERENCES people(nconst),
    FOREIGN KEY (tconst) REFERENCES films(tconst)
);
