{
  equal_parts(size, ingredients)::
    local qty = size / std.length(ingredients);
    [
      { kind: i, qty: qty } for i in ingredients
    ],
}
