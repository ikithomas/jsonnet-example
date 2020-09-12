import subprocess
import json


def to_json(jsonnet_path):
    json_str = subprocess.run(
        ['jsonnet', jsonnet_path],
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True).stdout
    print(json_str)
    return json.loads(json_str)


class TestMain():
    def test_syntax(self):
        j = to_json('examples/syntax.jsonnet')
        dry_manahttan = j['cocktails']['Dry Manhattan']
        assert len(dry_manahttan['ingredients']) == 1
        assert dry_manahttan['ingredients'][0]['kind'] == 'Dry Red Vermouth'
        assert dry_manahttan['ingredients'][0]['qty'] == 1
        assert dry_manahttan['garnish'] == 'Lemon Slice'

    def test_variable(self):
        j = to_json('examples/variables.jsonnet')
        mojito = j['Mojito']
        assert len(mojito['ingredients']) == 5
        assert mojito['ingredients'][3]['kind'] == 'Simple Syrup'
        assert mojito['ingredients'][3]['qty'] == 0.5
