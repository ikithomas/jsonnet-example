import subprocess
import json
import pytest


def to_json(jsonnet_path):
    json_str = subprocess.run(
        ['jsonnet', jsonnet_path],
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True).stdout
    # print(json_str)
    return json.loads(json_str)


class TestSyntax():
    @pytest.fixture
    def subject(self):
        j = to_json('examples/syntax.jsonnet')
        dry_manahttan = j['cocktails']['Dry Manhattan']
        return dry_manahttan

    def test_ingredients(self, subject):
        assert len(subject['ingredients']) == 1
        assert subject['ingredients'][0]['kind'] == 'Dry Red Vermouth'
        assert subject['ingredients'][0]['qty'] == 1

    def test_garnish(self, subject):
        assert subject['garnish'] == 'Lemon Slice'


class TestVariables():
    @pytest.fixture
    def subject(self):
        j = to_json('examples/variables.jsonnet')
        return j['Mojito']

    def test_ingredients(self, subject):
        assert len(subject['ingredients']) == 5
        assert subject['ingredients'][3]['kind'] == 'Simple Syrup'
        assert subject['ingredients'][3]['qty'] == 0.5


class TestReferences():
    @pytest.fixture
    def subject(self):
        j = to_json('examples/references.jsonnet')
        return j['Gin Fizz']

    def test_served(self, subject):
        assert subject['served'] == 'Tall'


class TestInnerReference():
    @pytest.fixture
    def subject(self):
        return to_json('examples/inner-reference.jsonnet')

    def test_subject(self, subject):
        assert subject['Martini']['ingredients'][1]['qty'] == 1


class TestArithmetic():
    @pytest.fixture
    def subject(self):
        return to_json('examples/arithmetic.jsonnet')

    def test_concat_array(self, subject):
        assert subject['concat_array'] == [1, 2, 3, 4]

    def test_concat_string(self, subject):
        assert subject['concat_string'] == '1234'

    def test_equality1(self, subject):
        assert not subject['equality1']

    def test_equality2(self, subject):
        assert subject['equality2']

    def test_ex(self, subject):
        assert pytest.approx(subject['ex1'], 0.01) == 1.66
        assert subject['ex2'] == 3
        assert subject['ex3'] == 1
        assert subject['ex4']

    def test_obj(self, subject):
        assert subject['obj'] == {
            'a': 1,
            'b': 3,
            'c': 4,
        }

    def test_obj_member(self, subject):
        assert subject['obj_member']

    def test_str(self, subject):
        assert subject['str1'] == 'The value of self.ex2 is 3.'
        assert subject['str2'] == 'The value of self.ex2 is 3.'
        assert subject['str3'] == 'ex1=1.67, ex2=3.00'
        assert subject['str4'] == 'ex1=1.67, ex2=3.00'
        assert subject['str5'] == 'ex1=1.67\nex2=3.00\n'


class TestFunctions():
    @pytest.fixture
    def subject(self):
        return to_json('examples/functions.jsonnet')

    def test_first_class_function(self, subject):
        assert subject['first_class_function'] == 25

    def test_inline_function(self, subject):
        assert pytest.approx(subject['inline_function'], 0.01) == 79.54

    def test_multiline_function(self, subject):
        assert pytest.approx(subject['multiline_function'], 0.01) == 160.6

    def test_named_params(self, subject):
        assert subject['named_params'] == 6

    def test_call_method(self, subject):
        assert subject['call_method'] == 'Meow! foo'

    def test_standard_lib(self, subject):
        assert subject['standard_lib'] == 'foo bar'

    def test_len(self, subject):
        assert subject['len'] == [5, 3]


class TestObjectConstructor():
    @pytest.fixture
    def subject(self):
        return to_json('examples/object-constructor.jsonnet')

    def test_object_constructor(self, subject):
        assert subject['Pisco Sour'] == {
            'garnish': 'Angostura bitters',
            'ingredients': [
                {'kind': 'Machu Pisco', 'qty': 2},
                {'kind': 'Egg white', 'qty': 1},
                {'kind': 'Lemon Juice', 'qty': 1},
                {'kind': 'Simple Syrup', 'qty': 1},
            ],
            'served': 'Straight Up'
        }
