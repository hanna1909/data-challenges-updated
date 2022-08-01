
# usage

``` bash
challengify ite .                                 # generate all challenges
challengify ite . -f                              # overwrite existing content
challengify ite . -f -c api_pred..api_advanced    # generate range of challenges

challengify ite . -vr -c api_pred                 # verbose dry run challenge version api
```

# content

the `Makefile` at the root of the project is the glovebox Makefile (glovebox does not check challenge sub directories)

challengify ite only generates
- content from `${source}` in `${destination}[${label}]/${project_name}`
- metadata in `${target}/${destination}[${label}]/${project_name}/.lewagon/challengify_generated.yml`

# `data-challenges` challenge validation

``` bash
make show_env
make list
make run_model
```
