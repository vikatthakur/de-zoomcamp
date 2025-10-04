# de-zoomcamp

Data Engineering A-Z Course

---

## PostgreSQL & pgAdmin Setup (Windows & Linux)

This guide helps you set up PostgreSQL and pgAdmin using Docker or Docker Compose.

---

### 1. Run PostgreSQL in CMD (Single Container)

```bash
docker run -it \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

---

### 2. Run PostgreSQL and pgAdmin in a Docker Network (Manual)

#### Step 1: Create a Docker Network

```bash
docker network create pg_network
```

#### Step 2: Start PostgreSQL Container

```bash
docker run -d \
  --name postgres \
  --network pg_network \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

#### Step 3: Start pgAdmin Container

```bash
docker run -d \
  --name pgadmin \
  --network pg_network \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin \
  -p 5050:80 \
  dpage/pgadmin4
```

---

### 3. Run PostgreSQL and pgAdmin with Docker Compose (Automated)

Create a `docker-compose.yaml` file with the following content:

```yaml
version: '3.8'

services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    ports:
      - "5432:5432"
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data"
    networks:
      - pg_network

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_PASSWORD=admin
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
    ports:
      - "5050:80"
    networks:
      - pg_network

networks:
  pg_network:
    driver: bridge

```

Start both services:

```bash
docker compose up -d
```

---

### 4. Build and Run ETL Container

#### Step 1: Build the Docker Image

```bash
docker build -t etl_postgres:v001 .
```

#### Step 2: Run the ETL Container

#### Step 2: Run the ETL Container

If running containers manually (not using Docker Compose):

```bash
docker run -it --rm \
  --network pg_network \
  etl_postgres:v001 \
  --username=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --url=${url} \
  --table=yellow_taxi_trips \
  --database=ny_taxi
```

If running with Docker Compose (the network name changes to `de-zoomcamp_pg_network`):

```bash
docker run -it --rm \
  --network de-zoomcamp_pg_network \
  etl_postgres:v001 \
  --username=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --url=${url} \
  --table=yellow_taxi_trips \
  --database=ny_taxi
```

---

### Data Sources

- NYC Yellow Taxi Trip Record Data: [https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

---

### Miscellaneous

#### Hosting Local Files for Docker Using Python HTTP Server

You can use Python's built-in HTTP server to host files locally and make them accessible to Docker containers.

**Start the HTTP server:**
```bash
python -m http.server [port_number]
```
Replace `[port_number]` with your desired port (e.g., `8080`).

**Accessing files from Docker:**

When passing a URL to a Docker container, use the following format:
```
url=http://host.docker.internal:8080/data/taxi_zone_lookup.parquet/part-00000-b43637e3-5efb-4d5c-bf79-518195ea32fd-c000.snappy.parquet
```
- `host.docker.internal` resolves automatically to the host machine's localhost from within Docker containers.
- Ensure your file is located in the correct directory served by the HTTP server.

This approach allows your Docker containers to download files from your local machine as if they were hosted externally.

### Notes

- Replace file paths and credentials as needed for your environment.
- Access pgAdmin at [http://localhost:5050](http://localhost:5050).
- Use `postgres` as the hostname when connecting to PostgreSQL from pgAdmin or ETL container (since both are on the same Docker network or Compose network).
- For Docker Compose, the default network allows containers to communicate using service names (`pgdatabase`, `pgadmin`).