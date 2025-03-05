def pytest_addoption(parser):
    parser.addoption(
        "--max-threads",
        action="store",
        default="4",
        help="Set the number of max threads for the test"
    )

