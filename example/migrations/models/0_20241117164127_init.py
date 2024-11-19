from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permission" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "companies" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "company_id" UUID NOT NULL REFERENCES "companies" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts_permission" (
    "accounts_id" UUID NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE,
    "permission_id" UUID NOT NULL REFERENCES "permission" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_accounts_pe_account_b6a87f" ON "accounts_permission" ("accounts_id", "permission_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
