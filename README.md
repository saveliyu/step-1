### Run Postgres
```bash
docker run --name pg \
  -v pg_data:/var/lib/postgresql \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -d \
  -p 15432:5432 \
  postgres
```

### Run Uvicorn
```bash
uvicorn app.main:app --port 8080 --reload
```