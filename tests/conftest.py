import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--client",
        action="store",
        default="requests",
        choices=["requests", "httpx", "aiohttp"],
        help="Choose client type for tests",
    )


@pytest.fixture(scope="session")
def client_type(pytestconfig):
    return pytestconfig.getoption("client")
