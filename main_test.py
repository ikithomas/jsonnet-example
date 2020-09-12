import subprocess
import json
import pytest


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

    def test_variables(self):
        j = to_json('examples/variables.jsonnet')
        mojito = j['Mojito']
        assert len(mojito['ingredients']) == 5
        assert mojito['ingredients'][3]['kind'] == 'Simple Syrup'
        assert mojito['ingredients'][3]['qty'] == 0.5

    def test_references(self):
        j = to_json('examples/references.jsonnet')
        fizz = j['Gin Fizz']
        assert fizz['served'] == 'Tall'

    def test_inner_reference(self):
        j = to_json('examples/inner-reference.jsonnet')
        assert j['Martini']['ingredients'][1]['qty'] == 1

    def test_arithmetic(self):
        j = to_json('examples/arithmetic.jsonnet')

        assert j['concat_array'] == [1, 2, 3, 4]
        assert j['concat_string'] == '1234'
        assert j['equality1'] == False
        assert j['equality2'] == True
        assert pytest.approx(j['ex1'], 0.01) == 1.66
        assert j['ex2'] == 3
        assert j['ex3'] == 1
        assert j['ex4'] == True
        assert j['obj'] == {
            'a': 1,
            'b': 3,
            'c': 4,
        }
        assert j['str1'] == 'The value of self.ex2 is 3.'
        assert j['str2'] == 'The value of self.ex2 is 3.'
        assert j['str3'] == 'ex1=1.67, ex2=3.00'
        assert j['str4'] == 'ex1=1.67, ex2=3.00'
        assert j['str5'] == 'ex1=1.67\nex2=3.00\n'

