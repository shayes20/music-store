# flask-app1

## Configuration

Configuration can be done two places:

1. `.env` (for local deployment)
2. `ansible/inventory/hosts.yml` (for ansible deployments)

| Field                                      | Description                                                                         |
| ------------------------------------------ | ----------------------------------------------------------------------------------- |
| `SITE_NAME` or `web_app_title`             | The name of the site deployed, this will be the title that appears on deployed site |
| `web_app_name`                             | This the name that will be used internally: name of service, directory name, ...    |
| `WEB_APP_PORT` or `web_app_port`           | Port that the web app is listening on                                               |
| `WEB_APP_HOST` or `web_app_host`           | Host that the web app is listening on                                               |
| `POSTGRES_HOST` or `postgres_host`         | Port that Postgres is listening on                                                  |
| `POSTGRES_PORT` or `postgres_port`         | Host that Postgres is listening on                                                  |
| `POSTGRES_USER` or `postgres_user`         | Postgres user that web_app authenticates to                                         |
| `POSTGRES_PASSWORD` or `postgres_password` | Password of postgres user                                                           |
| `POSTGRES_DB` or `postgres_db`             | Postgres database webapp uses                                                       |

## Deployment

### Local

#### Postgres

Local postgres deployments relies on user docker and docker-compose, you can use the following commands.

**Start Postgres**

```bash
docker compose up -d
```

**Stop Postgres**

```bash
docker compose down
```

#### Flask App

Local flask app deployment relies on using just using python and pip

**Start Flask App**

```bash
pip install -r requirements.txt
python main.py
```



