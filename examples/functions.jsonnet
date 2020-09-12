// Define a local function.
// Default arguments are like Python:
local lbs_to_kg(lbs) = lbs / 2.2;

// Define a local multiline function.
local kg_to_lbs(kg) =
  kg * 2.2;

local area(x, y) = x * y;

local cat = {
  // A method
  meow(name): 'Meow! %s' % name,
};

{
  // Functions are first class citizens.
  first_class_function:
    (function(x) x * x)(5),

  inline_function: lbs_to_kg(175),

  multiline_function: kg_to_lbs(73),

  // Like python, parameters can be named at call time.
  // This allows changing their order
  named_params: area(y=3, x=2),

  // object.my_method returns the function,
  // which is then called like any other.
  call_method: cat.meow('foo'),

  standard_lib: std.join(' ', std.split('foo/bar', '/')),
  len: [
    std.length('hello'),
    std.length([1, 2, 3]),
  ],
}
