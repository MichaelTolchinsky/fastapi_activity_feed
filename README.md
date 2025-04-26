# Activity Feed Backend

This project is a small **FastAPI**-based backend system designed for learning and practicing backend skills
It simulates a **mini LinkedIn-style Activity Feed** system.

---

## ⚡ Technologies Used

- Python 3.11
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis (with `redis.asyncio`)
- Kafka (with `aiokafka`)
- Docker & Docker Compose

---

## 🚀 Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/activity-feed-fastapi.git
cd activity-feed-fastapi
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=activity_feed
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/activity_feed

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_TTL=60 # seconds

# Kafka
KAFKA_HOST=kafka
KAFKA_PORT=9092
```

### 3. Start Dependencies with Docker

```bash
docker-compose up -d
```

The API Swagger will be available at: http://localhost:8000/docs