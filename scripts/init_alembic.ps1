# Initialize Alembic (run this after setting up the database)

Write-Host "Initializing Alembic migrations..." -ForegroundColor Green

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

Write-Host "Migration created. Review the migration file in alembic/versions/" -ForegroundColor Yellow
Write-Host "Then run: alembic upgrade head" -ForegroundColor Yellow
