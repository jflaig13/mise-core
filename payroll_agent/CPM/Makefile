.PHONY: up down logs test test-unit test-integration reset clean db-shell engine-shell help

# Default target
help:
	@echo "CPM Local Development - Available Commands"
	@echo "==========================================="
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - View logs (all services)"
	@echo "  make test            - Run all tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make reset           - Reset database (delete all data)"
	@echo "  make clean           - Remove all containers and volumes"
	@echo "  make db-shell        - Connect to PostgreSQL"
	@echo "  make engine-shell    - Connect to engine container"
	@echo ""

# Start all services
up:
	@echo "🚀 Starting CPM local stack..."
	docker-compose up --build -d
	@echo "✅ Services started"
	@echo "   Payroll Engine: http://localhost:8080"
	@echo "   Mock Transcriber: http://localhost:8081"
	@echo "   PostgreSQL: localhost:5432"

# Stop all services
down:
	@echo "🛑 Stopping services..."
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Run all tests
test: test-integration
	@echo "✅ All tests passed"

# Run integration tests
test-integration:
	@echo "🧪 Running integration tests..."
	cd local_dev && bash test_integration.sh

# Reset database (delete all data)
reset:
	@echo "⚠️  Resetting database..."
	docker-compose exec postgres psql -U payroll_user -d payroll -c "TRUNCATE TABLE shifts;"
	@echo "✅ Database reset complete"

# Remove all containers and volumes
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	@echo "✅ Cleanup complete"

# Connect to PostgreSQL
db-shell:
	@echo "📊 Connecting to PostgreSQL..."
	docker-compose exec postgres psql -U payroll_user -d payroll

# Connect to engine container
engine-shell:
	@echo "🔧 Connecting to payroll engine container..."
	docker-compose exec payroll_engine bash
