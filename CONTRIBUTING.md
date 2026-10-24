# Validate seed format contracts

The `main` branch publishes the `micharisma-seeds/v1` schemas and portable validation tools. The fictional league data and game simulations remain on the `pseudo` branch. Existing JSON files under `sports/`, `locations/`, `quests/`, and `ratings/` use the legacy format and are outside this validator's scope.

Create a Python environment and run the checks from this repository:

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
.venv/bin/python -m unittest discover -s tools -p 'test_*.py'
.venv/bin/python tools/validate_seeds.py
```

The tests must report eight tests and `OK`. The default validator checks one example manifest and the sequence registry in `tools/fixtures/`; it must report zero failures. Either check returns nonzero on failure. The fixtures demonstrate syntax and are not a sports dataset. GitHub Actions runs these same checks.

To check another bundle, pass its manifest files or directory as positional arguments and supply its registry path with `--registry`. All relationships use semantic entity codes, never database IDs. YAML and JSON share the same format. Do not use ERB, custom YAML tags, aliases, duplicate mapping keys, or multiple YAML documents.

The [published schemas](schemas/README.md) check envelopes, entity types, field names and types, and code syntax. They do not resolve references, infer memberships, validate basketball statistics, or define seed replay behavior. Those checks belong to the application and dataset-specific tests.
