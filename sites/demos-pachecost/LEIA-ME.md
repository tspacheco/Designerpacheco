# Demos dos clientes — como estão publicadas (desde 07/10/2026)

As demos já não vão dentro do zip do pachecost.com. Há dois projetos no Netlify:

1. **pachecost.com** (o de sempre): sobe-se à mão `pachecost-com-netlify.zip` (~8 MB, site da Pacheco Studios + regras). As regras mostram as demos sem mudar o endereço:
   - `pachecost.com/demo/<curto>/` e `demo.pachecost.com/<curto>/` → página do projeto das demos.
2. **pachecost-demos** (`https://pachecost-demos.netlify.app`): ligado ao GitHub, publica-se sozinho a cada push neste ramo. Configuração no Netlify: *Add new project → Import an existing project → GitHub → Designerpacheco*, ramo `claude/dez-negocios-dez-websites-7gevwu`, **Base directory** `sites/demos-pachecost` (o resto vem do `netlify.toml`: `python3 gerar.py --so-demos`, publica `_demos`). Nome do projeto: `pachecost-demos` (se o nome estiver ocupado, muda `DEMOS_URL` no `gerar.py` e gera de novo o zip do pachecost.com).

Juntar demos: acrescentar `("curto", "pasta-em-sites")` à lista `DEMOS` do `gerar.py` e fazer push. Não há limite de zip: cada demo pesa 1–4 MB e só se descarrega quando alguém a abre.

Gerar o zip do pachecost.com: `python3 gerar.py` (vai buscar o zip mais recente do ramo `claude/pacheco-studios-playbook-kztskg`). Testar as demos localmente: `python3 gerar.py --so-demos` e abrir `_demos/`.
