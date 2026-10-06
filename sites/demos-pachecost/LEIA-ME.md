# Demos em demo.pachecost.com

O pachecost.com e as demos vão num **único zip**: `pachecost-com-e-demos-netlify.zip`, que se sobe ao projeto Netlify do pachecost.com.
O `demo.pachecost.com` é um alias desse mesmo projeto, como o `ro.pachecost.com`.

`python3 sites/demos-pachecost/gerar.py` faz três coisas:
- vai buscar o `pacheco-studios-netlify.zip` mais recente ao ramo `claude/pacheco-studios-playbook-kztskg`;
- acrescenta as demos em `demo/<curto>/`;
- junta ao `_redirects` a regra `https://demo.pachecost.com/*  →  /demo/:splat  200!`.

**Sempre que o site principal mudar**, volta a correr o gerar.py e sobe o zip combinado. Se subires só o `pacheco-studios-netlify.zip`, as demos desaparecem.
Para acrescentar uma demo, junta-a à lista `DEMOS` e corre o gerar.py outra vez.
