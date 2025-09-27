# de-zoomcamp
Data Engineering A-Z Course

dpage/pgadmin4
# Run Postgres in CMD on Windows

```powershell
docker run -it \ 
  -e POSTGRES_USER="root" \ 
  -e POSTGRES_PASSWORD="root" \ 
  -e POSTGRES_DB="ny_taxi" \ 
  -v C:/Users/vikat/OneDrive/Desktop/NotionAi/de-zoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data \ 
  -p 5432:5432 \ 
  postgres:13
```

## Run Postgres and pgAdmin in the same Docker network

### 1. Create the network
```powershell
docker network create pg_network
```

### 2. Run the Postgres container
```powershell
docker run -d \ 
  --name postgres \ 
  --network pg_network \ 
  -e POSTGRES_USER=root \ 
  -e POSTGRES_PASSWORD=root \ 
  -e POSTGRES_DB=ny_taxi \ 
  -v C:/Users/vikat/OneDrive/Desktop/NotionAi/de-zoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data \ 
  -p 5432:5432 \ 
  postgres:15
```

### 3. Run the pgAdmin container
```powershell
docker run -d \ 
  --name pgadmin \ 
  --network pg_network \ 
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \ 
  -e PGADMIN_DEFAULT_PASSWORD=admin \ 
  -p 5050:80 \ 
  dpage/pgadmin4
```

