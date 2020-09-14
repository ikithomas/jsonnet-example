import subprocess
import json
import pytest


def to_json(jsonnet_path, *args):
    cmd = ['jsonnet', jsonnet_path]
    if args is not None:
        cmd.extend(args)

    json_str = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True
    ).stdout
    print(json_str)
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


class TestConditionals():
    @pytest.fixture
    def subject(self):
        return to_json('examples/conditionals.jsonnet')

    def test_first_ingrident(self, subject):
        assert subject['Virgin Mojito']['ingredients'][0]['qty'] == 6
        assert subject['Large Mojito']['ingredients'][0]['qty'] == 12

    def test_garnish(self, subject):
        assert subject['Virgin Mojito']['garnish'] is None
        assert subject['Large Mojito']['garnish'] == 'Lime wedge'


class TestComputedFields():
    @pytest.fixture
    def subject(self):
        return to_json('examples/computed-fields.jsonnet')

    def test_salted(self, subject):
        assert subject['Margarita']['garnish'] == 'Salt'

    def test_unsalted(self, subject):
        assert 'garnish' not in subject['Margarita Unsalted']


class TestComprehensions():
    @pytest.fixture
    def array(self):
        return to_json('examples/comprehensions.jsonnet')['array']

    @pytest.fixture
    def obj(self):
        return to_json('examples/comprehensions.jsonnet')['object']

    def test_array_comprehension(self, array):
        assert array['evens'] == [6, 8]
        assert array['odds'] == [5, 7]
        assert array['higher'] == [8, 9, 10, 11]
        assert array['lower'] == [2, 3, 4, 5]
        assert array['evens_and_odds'] == ['6-5', '6-7', '8-5', '8-7']

    def test_object_comprehension(self, obj):
        assert obj['evens'] == {
            'f6': True,
            'f8': True,
        }
        assert obj['mixture'] == {
           'a': 0,
           'b': 0,
           'c': 0,
           'f': 1,
           'g': 2
        }


class TestImports():
    @pytest.fixture
    def vodka_martini(self):
        return to_json('examples/imports/imports.jsonnet')['Vodka Martini']

    @pytest.fixture
    def manhattan(self):
        return to_json('examples/imports/imports.jsonnet')['Manhattan']

    def test_vodka_martini(self, vodka_martini):
        assert vodka_martini['garnish'] == 'Olive'
        assert vodka_martini['served'] == 'Straight Up'

    def test_manhattan(self, manhattan):
        assert manhattan['garnish'] == 'Maraschino Cherry'


class TestUtilsFunctions():
    @pytest.fixture
    def subject(self):
        return to_json('examples/utils-functions/negroni.jsonnet')['Negroni']

    def test_negroni(self, subject):
        assert subject['ingredients'][0]['qty'] == 2
        assert subject['ingredients'][1]['qty'] == 2
        assert subject['ingredients'][2]['qty'] == 2


class TestErrors():
    @pytest.fixture
    def subject(self):
        return to_json('examples/error.jsonnet')

    def test_error(self, subject):
        assert len(subject['equal_parts']) == 1


class TestExternalVariables():
    @pytest.fixture
    def subject(self):
        return to_json('examples/external-variables/top-level-ext.jsonnet',
                       '--ext-str', 'prefix=Happy Hour ',
                       '--ext-code', 'brunch=true')

    def test_external_variables(self, subject):
        assert subject['Happy Hour Bloody Mary']['served'] == 'Tall'


class TestTopLevelArguments():
    @pytest.fixture
    def subject(self):
        return to_json('examples/top-level-arguments/tla.jsonnet',
                       '--tla-str', 'prefix=Happy Hour ',
                       '--tla-code', 'brunch=true')

    def test_top_level_arguments(self, subject):
        assert subject['Happy Hour Bloody Mary']['served'] == 'Tall'


class TestObjectOrientedContrived():
    @pytest.fixture
    def processor(self):
        return to_json('examples/oo-contrived.jsonnet')['Processor']

    @pytest.fixture
    def computer(self):
        return to_json('examples/oo-contrived.jsonnet')['Computer']

    def test_computer(self, computer):
        assert computer['Processor']['model'] == 'intel i5 8400'
        assert computer['Processor']['num_of_core'] == 4
        assert computer['num_of_ram_slot'] == 2

    def test_processor(self, processor):
        assert processor['model'] == 'intel i7 9700k'
        assert processor['num_of_core'] == 4


class TestObjectOriented():
    @pytest.fixture
    def deluxe_sour(self):
        j = to_json('examples/object-oriented/sours-oo.jsonnet')
        return j['Deluxe Sour']

    def test_hidden_fields(self, deluxe_sour):
        assert 'citrus' not in deluxe_sour
        assert 'spirits' not in deluxe_sour

    def test_sweetener(self, deluxe_sour):
        assert deluxe_sour['ingredients'][2]['kind'] == 'Gomme Syrup'
        assert deluxe_sour['ingredients'][2]['qty'] == 0.5


