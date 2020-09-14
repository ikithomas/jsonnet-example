local utils = import 'utils.libsonnet';
{
  Negroni: {
    ingredients: utils.equal_parts(
      6,
      [
        'Farmers Gin',
        'Sweet Red Vermouth',
        'Campari',
      ]
    ),
    garnish: 'Orange Peel',
    served: 'On The Rocks',
  },
}
