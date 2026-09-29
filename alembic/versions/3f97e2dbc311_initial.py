"""initial (fully rerunnable + works with dirty DB)

Revision ID: 3f97e2dbc311
Revises:
Create Date: 2026-02-14
"""

from alembic import op
import sqlalchemy as sa

revision = "3f97e2dbc311"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # PostGIS (safe to run repeatedly)
    bind.execute(sa.text("CREATE EXTENSION IF NOT EXISTS postgis;"))

    # 1) Enum: create only if missing (MATCHES your API: active/sold/hidden)
    bind.execute(sa.text("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'listingstatus') THEN
            CREATE TYPE listingstatus AS ENUM ('active', 'sold', 'hidden');
        END IF;
    END$$;
    """))

    # 2) Tables (create if missing)

    bind.execute(sa.text("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        username VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    """))

    # IMPORTANT: geometry (not geography) to avoid ST_AsEWKB(geography) error
    bind.execute(sa.text("""
    CREATE TABLE IF NOT EXISTS stores (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location geometry(POINT,4326) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    """))

    # IMPORTANT: add description + updated_at (your API/model expects these)
    bind.execute(sa.text("""
    CREATE TABLE IF NOT EXISTS listings (
        id SERIAL PRIMARY KEY,
        store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        status listingstatus NOT NULL DEFAULT 'active',
        price NUMERIC(12,2),
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ
    );
    """))

    # 3) Indexes
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_users_username ON users(username);"))

    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_stores_name ON stores(name);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_stores_location ON stores USING gist(location);"))

    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_listings_id ON listings(id);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_listings_title ON listings(title);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_listings_category ON listings(category);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_listings_status ON listings(status);"))
    bind.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_listings_store_id ON listings(store_id);"))


def downgrade() -> None:
    bind = op.get_bind()

    bind.execute(sa.text("DROP INDEX IF EXISTS ix_listings_store_id;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_listings_status;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_listings_category;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_listings_title;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_listings_id;"))

    bind.execute(sa.text("DROP INDEX IF EXISTS idx_stores_location;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_stores_name;"))

    bind.execute(sa.text("DROP INDEX IF EXISTS ix_users_username;"))
    bind.execute(sa.text("DROP INDEX IF EXISTS ix_users_email;"))

    bind.execute(sa.text("DROP TABLE IF EXISTS listings;"))
    bind.execute(sa.text("DROP TABLE IF EXISTS stores;"))
    bind.execute(sa.text("DROP TABLE IF EXISTS users;"))

    bind.execute(sa.text("DROP TYPE IF EXISTS listingstatus;"))