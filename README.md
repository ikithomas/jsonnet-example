
##### References
- jsonnet tutorial: https://jsonnet.org/learning/tutorial.html
- Repository: https://github.com/google/jsonnet

---

### Prerequisite
```bash
brew install jsonnet
```

### Setup
```bash
# create python venv
make venv

# activate venv
source venv/bin/activate

# install depeendencies
make setup

# run test and lint
make test && make lint
```

### Commands
```bash
# generate json from jsonnet file
jsonnet syntax.jsonnet

# run with external variables
jsonnet examples/external-variables/top-level-ext.jsonnet \
  --ext-str prefix="Happy Hour" \
  --ext-code brunch=true

# run with top level arguments
jsonnet examples/top-level-arguments/tla.jsonnet \
  --tla-str prefix="Happy Hour" \
  --tla-code brunch=true
```
