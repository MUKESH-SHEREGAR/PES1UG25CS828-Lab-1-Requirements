# Lab 6: Code and Branch Coverage

This folder contains the Lab 6 credit card rewards application, two focused test suites, and the corresponding coverage evidence.

## Files

- `credit_card_rewards.py` — application module supplied with the assigned repository.
- `CodeCoverageTest_61_credit_card_rewards.py` — tests for line coverage.
- `BranchCoverageTest_61_credit_card_rewards.py` — tests for true and false outcomes across the decision branches.
- `code_coverage_output.txt` and `code_coverage_output.png` — line coverage run output.
- `branch_coverage_output.txt` and `branch_coverage_output.png` — branch coverage run output.

## Run

Install Python 3, `pytest`, and `coverage`, then run these commands from this folder:

```shell
coverage erase
coverage run -m pytest -q CodeCoverageTest_61_credit_card_rewards.py
coverage report -m credit_card_rewards.py

coverage erase
coverage run --branch -m pytest -q BranchCoverageTest_61_credit_card_rewards.py
coverage report -m credit_card_rewards.py
```

## Results

- Line coverage: **100%** (35 statements, 0 missed).
- Branch coverage: **100%** (26 branches, 0 partial branches).
- Test results: 6 line coverage tests and 28 branch coverage tests passed.

The two coverage suites are intentionally run separately so that each report shows the purpose of that set of tests.
