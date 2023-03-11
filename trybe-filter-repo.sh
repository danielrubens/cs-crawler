### GIT FILTER-REPO ###

## NÃO EXECUTE ESSE SCRIPT DIRETAMENTE
## Esse script foi feito para uso do
## script 'trybe-publisher' fornecido 
## pela Trybe. 

[[ $# == 1 ]] && \
[[ $1 == "trybe-security-parameter" ]] && \
git filter-repo \
    --path .github \
    --path .vscode \
    --path .cspell.json \
    --path .markdownlint.json \
    --path trybe-filter-repo.sh \
    --path readme.md \
    --invert-paths --force --quiet
