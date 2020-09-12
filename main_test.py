import subprocess
import json


def to_json(jsonnet_path):
    json_str = subprocess.run(
        ['jsonnet', jsonnet_path],
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True).stdout
    return json.loads(json_str)


class TestMain():
    def test_syntax(self):
        j = to_json('examples/syntax.jsonnet')
        assert j['cocktails']['Manhattan']['garnish'] == 'Maraschino Cherry'
