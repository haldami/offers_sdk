import json
import sys
from pathlib import Path
from unittest.mock import patch, AsyncMock

import pytest
from offers_sdk.cli import main as cli_main
from offers_sdk.models import Product
from offers_sdk.client import Client


@pytest.fixture
def products_file(tmp_path):
    """Create a temporary JSON file with products for testing."""
    data = [
        {"id": "11111111-1111-1111-1111-111111111111", "name": "Prod A", "description": "Test A"},
        {"id": "22222222-2222-2222-2222-222222222222", "name": "Prod B", "description": "Test B"},
    ]
    file_path = tmp_path / "products.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.fixture
def ids_file(tmp_path):
    """Create a temporary JSON file with UUIDs for testing."""
    data = [
        "11111111-1111-1111-1111-111111111111",
        "22222222-2222-2222-2222-222222222222",
    ]
    file_path = tmp_path / "ids.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.mark.parametrize(
    "cli_args,expected_calls",
    [
        (["--client-location", "dummy.json", "register",
          "--id", "11111111-1111-1111-1111-111111111111",
          "--name", "Prod A",
          "--description", "Test A"], 1),
        (["--client-location", "dummy.json", "register_batch", "--file", "products.json"], 2),
        (["--client-location", "dummy.json", "get_offers",
          "--id", "11111111-1111-1111-1111-111111111111"], 1),
        (["--client-location", "dummy.json", "get_offers_batch", "--file", "ids.json"], 2),
    ]
)
def test_cli_commands(cli_args, expected_calls, products_file, ids_file):
    """Test all CLI commands with mocked client methods."""

    # Patch Client.load_from_file to return a mocked client
    with patch.object(Client, "load_from_file") as mock_load:
        mock_client = AsyncMock(spec=Client)
        mock_load.return_value = mock_client

        # Adjust file paths in args if needed
        args = [a.replace("products.json", products_file).replace("ids.json", ids_file) for a in cli_args]

        # Patch sys.argv
        with patch.object(sys, "argv", ["offers-cli"] + args):
            cli_main()

        # Check number of calls based on CLI command
        if "register" in cli_args[2]:
            if "batch" in cli_args[2]:
                assert mock_client.register_product.call_count == expected_calls
            else:
                assert mock_client.register_product.call_count == 1
        elif "get_offers" in cli_args[2]:
            assert mock_client.get_offers.call_count == expected_calls
