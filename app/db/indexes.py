from __future__ import annotations

import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


async def ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    books = db["books"]
    changes = db["changes"]
    locks = db["locks"]

    # Books indexes
    await books.create_index("upc", unique=True)
    await books.create_index("source_url", unique=True)
    await books.create_index("category")
    await books.create_index("rating")
    await books.create_index("price_incl_tax")
    await books.create_index("last_seen")
    await books.create_index([("category", 1), ("price_incl_tax", 1), ("rating", -1)])
    # hashed index on content_hash for quick change lookups
    await books.create_index([("content_hash", "hashed")])

    # Changes indexes
    await changes.create_index("book_upc")
    await changes.create_index([("timestamp", -1)])
    await changes.create_index("change_type")

    logger.info("MongoDB indexes ensured")

    # Locks TTL index
    try:
        await locks.create_index("expires_at", expireAfterSeconds=0)
    except Exception:
        # ignore if fails
        pass
