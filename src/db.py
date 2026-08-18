from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import clickhouse_connect
from dotenv import load_dotenv

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "clickhouse.toml"
EXAMPLE_CONFIG_PATH = PROJECT_ROOT / "config" / "clickhouse.example.toml"

load_dotenv(PROJECT_ROOT / ".env")


def get_config_path() -> Path:
    """Return the local configuration path, optionally overridden by an env var."""
    configured_path = os.getenv("B3_ECONOPHYSICS_CONFIG")
    return Path(configured_path).expanduser() if configured_path else DEFAULT_CONFIG_PATH


def load_clickhouse_config() -> dict[str, Any]:
    """
    Load ClickHouse configuration from the local configuration file.

    Copy ``config/clickhouse.example.toml`` to ``config/clickhouse.toml`` first,
    or point ``B3_ECONOPHYSICS_CONFIG`` to an alternative TOML file.
    """
    config_path = get_config_path()
    if not config_path.exists():
        raise FileNotFoundError(
            "ClickHouse config file not found: "
            f"{config_path}. Copy {EXAMPLE_CONFIG_PATH.name} to "
            "config/clickhouse.toml or set B3_ECONOPHYSICS_CONFIG."
        )

    with config_path.open("rb") as file:
        return tomllib.load(file)


def get_client():
    """
    Create a ClickHouse client using the local research configuration.

    Environment variables (``B3_CH_HOST``, ``B3_CH_PORT``,
    ``B3_CH_USERNAME``, ``B3_CH_PASSWORD`` and ``B3_CH_DATABASE``) take
    precedence over values in the local TOML configuration.
    """
    config = load_clickhouse_config()
    ch_config = config["clickhouse"]

    return clickhouse_connect.get_client(
        host=os.getenv("B3_CH_HOST", ch_config["host"]),
        port=int(os.getenv("B3_CH_PORT", str(ch_config["port"]))),
        username=os.getenv("B3_CH_USERNAME", ch_config["username"]),
        password=os.getenv("B3_CH_PASSWORD", ch_config["password"]),
        database=os.getenv("B3_CH_DATABASE", ch_config["database"]),
    )


def get_daily_table() -> str:
    """
    Return the configured daily candles table name.
    """
    config = load_clickhouse_config()
    return config["tables"]["daily"]


def query_df(sql: str):
    """
    Convenience wrapper to execute a SQL query and return a pandas DataFrame.
    """
    client = get_client()
    return client.query_df(sql)
