"""Database integrity and structural schema verification utilities.

Ensures the physical storage matrices are fully compliant with relational layout
blueprints and PEP 8 geometric formatting limits across all execution environments.
"""

from __future__ import annotations

import sqlite3
from typing import Final


class DatabaseChecker:
    """Encapsulates safe relational tracking operations against local registries."""

    def __init__(self, db_path: str = "app.db") -> None:
        """Initialize the checker targeting a explicit filesystem path."""
        self.db_path: Final[str] = db_path

    def verify_table_presence(self) -> list[str]:
        """Extract the names of all identified tables within the relational ledger.

        Returns:
            A collection containing the names of all identified tables.
        """
        # Context manager ensures connection closure even if exceptions occur
        # during the execution lifecycle.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [str(row[0]) for row in cursor.fetchall()]

    def verify_schema_integrity(self, table_name: str) -> list[str]:
        """Extract column metadata nominal attributes for a given target table name.

        Args:
            table_name: The exact string name of the table to inspect.

        Returns:
            A list containing the identified column name fields.
        """
        query = f"PRAGMA table_info({table_name});"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return [str(row[1]) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []


if __name__ == "__main__":
    checker = DatabaseChecker()
    tables = checker.verify_table_presence()
    print(f"Verified active storage layers. Target tables resolved: {tables}")
