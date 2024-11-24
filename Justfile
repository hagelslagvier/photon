fix:
    find photon/ tests/ -name "*.py" -type f | xargs -I {} pyupgrade --py312-plus {}
    ruff check photon/ tests/ --fix --select I
    ruff format photon/ tests/


type-check:
    mypy photon/
    mypy tests/

test:
    pytest -s --cov=photon/ --cov-report=html:tests/coverage tests/

show-coverage:
    #!/usr/bin/env python3
    import pathlib
    import webbrowser

    report_path = f"file://{pathlib.Path.cwd()/'tests/coverage/index.html'}"
    webbrowser.open(report_path)

check:
    just fix
    just type-check
    just test

clean:
    find photon tests -type d -name ".*_cache" -exec rm -rf {} +
    find photon tests -type d -name "__pycache__" -exec rm -rf {} +
    find photon tests -type f \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} +
