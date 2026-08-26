# CareerMatch

An explainable Python job-matching dashboard using token vectors and cosine similarity.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-unittest-18794e)
![License](https://img.shields.io/badge/license-MIT-blue)

## Highlights

- Modern local browser dashboard with interactive navigation.
- Synthetic demonstration data included under `mockdata/`.
- Dependency-free Python runtime based on the standard library.
- Command-line mode for automation and technical demonstrations.
- Automated tests and GitHub Actions workflow.

## Quick start

```bash
python matcher.py
```

The browser opens automatically. Use the sidebar to access Dashboard, Data,
Reports and Settings. Stop the local server with `Ctrl+C`.

## Tests

```bash
python -m unittest discover -v
```

## Project-specific usage

# Explainable Job Match Engine

Run: `python matcher.py` to open the visual dashboard. Edit the profile and calculate the ranking.
CLI mode: `python matcher.py --cli` or pass two custom paths. Produces ranked `matches.json` with scores and matched keywords.
Tests: `python -m unittest test_matcher.py`.


## Portfolio note

This is a portfolio prototype built with synthetic data. Production deployment
would require authentication, authorization, secrets management, observability,
database migrations and a supported application server.

## License

MIT
