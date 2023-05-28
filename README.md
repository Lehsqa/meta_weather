# Getting Started with Meta Weather DRF app

## Running

1) ### `docker-compose up -d --build`
2) ### `docker-compose up`

## Available Path

### `http://localhost:8000/admin` - admin panel (user: admin; password: root) for searching DB's

### `http://localhost:8000/api/weather` - request for getting weather view set

### `http://localhost:8000/api/parsing-tasks` - request for getting parsing tasks view set

### `http://localhost:8000/api/update-weather/` - request for manual updating the weather DB

### `http://localhost:8000/api/update-weather-time/?time={hours}:{minutes}` - request for updating time for scheduler job
