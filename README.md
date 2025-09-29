# de-zoomcamp

Data Engineering A-Z Course

---

## PostgreSQL & pgAdmin Setup (Windows)

This guide helps you set up PostgreSQL and pgAdmin using Docker on Windows.

---

### 1. Run PostgreSQL in CMD (Single Container)

```powershell
docker run -it ^
  -e POSTGRES_USER=root ^
  -e POSTGRES_PASSWORD=root ^
  -e POSTGRES_DB=ny_taxi ^
  -v C:/Users/vikat/OneDrive/Desktop/NotionAi/de-zoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data ^
  -p 5432:5432 ^
  postgres:13
```

---

### 2. Run PostgreSQL and pgAdmin in a Docker Network

#### Step 1: Create a Docker Network

```powershell
docker network create pg_network
```

#### Step 2: Start PostgreSQL Container

```powershell
docker run -d ^
  --name postgres ^
  --network pg_network ^
  -e POSTGRES_USER=root ^
  -e POSTGRES_PASSWORD=root ^
  -e POSTGRES_DB=ny_taxi ^
  -v C:/Users/vikat/OneDrive/Desktop/NotionAi/de-zoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data ^
  -p 5432:5432 ^
  postgres:15
```

#### Step 3: Start pgAdmin Container

```powershell
docker run -d ^
  --name pgadmin ^
  --network pg_network ^
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com ^
  -e PGADMIN_DEFAULT_PASSWORD=admin ^
  -p 5050:80 ^
  dpage/pgadmin4
```

---

### 3. Build and Run ETL Container

#### Step 1: Build the Docker Image

```powershell
docker build -t etl_postgres:v001 .
```

#### Step 2: Run the ETL Container

```powershell
docker run -it --rm --network pg_network etl_postgres:v001 --username=root --password=root --host=postgres --port=5432 --database=ny_taxi
```

---

### Notes

- Replace file paths and credentials as needed for your environment.
- Access pgAdmin at [http://localhost:5050](http://localhost:5050).
- Use `postgres` as the hostname when connecting to PostgreSQL from pgAdmin or ETL container (since both are on the same Docker network).