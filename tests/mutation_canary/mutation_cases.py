import os
import time


def test_mutation_case():
    mutation = os.environ.get("HTG_MUTATION_CASE", "baseline")
    if mutation == "killable":
        assert 2 + 2 == 5
    if mutation == "crash":
        os._exit(70)
    if mutation == "timeout":
        time.sleep(5)
    assert True
