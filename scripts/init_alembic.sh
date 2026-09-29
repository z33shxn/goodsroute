#!/bin/bash
# Initialize Alembic (run this after setting up the database)

echo "Initializing Alembic migrations..."

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

echo "Migration created. Review the migration file in alembic/versions/"
echo "Then run: alembic upgrade head"
