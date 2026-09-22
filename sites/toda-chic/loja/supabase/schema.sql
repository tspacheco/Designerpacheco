-- TODA CHIC — base de dados da loja (Supabase / Postgres)
-- Correr uma vez no SQL Editor do projeto Supabase. Depois: seed.sql (gerado por seed.py).

create extension if not exists pgcrypto;

create table if not exists categorias (id text primary key, nome text not null, ordem int not null default 0, foto text, provisorio boolean default false);
create table if not exists estacoes (id text primary key, nome text not null, ordem int not null default 0, foto text, titulo text, frase text);

create table if not exists pecas (
  id text primary key,
  nome text not null,
  cat text not null,
  preco numeric(10,2),
  preco_antigo numeric(10,2),
  promo boolean generated always as (preco_antigo is not null and preco_antigo > preco) stored,
  tam text,
  tamanhos jsonb not null default '["Único"]',
  descricao text default '',
  estacao text default 'meia',
  nova boolean default false,
  sub text,
  fotos jsonb default '[]',
  ativo boolean default true,
  criada timestamptz default now()
);

create table if not exists cores (
  id bigserial primary key,
  peca_id text not null references pecas(id) on delete cascade,
  posicao int not null,
  nome text not null,
  hex text not null default '#CCCCCC',
  foto text,
  stock int not null default 0 check (stock >= 0),
  reservado int not null default 0 check (reservado >= 0),
  unique (peca_id, posicao)
);

create table if not exists encomendas (
  id bigserial primary key,
  token text not null unique default encode(gen_random_bytes(16), 'hex'),
  estado text not null default 'pendente' check (estado in ('pendente','paga','enviada','falhada','cancelada','expirada')),
  cliente jsonb not null,
  linhas jsonb not null,
  total numeric(10,2) not null,
  portes numeric(10,2) not null default 0,
  motivo text,
  stripe_session text,
  stripe_payment text,
  criada timestamptz default now(),
  atualizada timestamptz default now(),
  paga timestamptz,
  enviada timestamptz
);
create index if not exists encomendas_estado on encomendas(estado, criada desc);

-- catálogo público: o que a loja lê (stock já descontado das reservas)
create or replace view catalogo_publico as
select p.id, p.nome, p.cat, p.preco, p.preco_antigo, p.promo, p.tam, p.tamanhos, p.descricao as "desc", p.estacao, p.nova, p.sub, p.fotos,
  (select jsonb_agg(jsonb_build_object('nome', c.nome, 'hex', c.hex, 'foto', c.foto, 'stock', greatest(c.stock - c.reservado, 0)) order by c.posicao)
     from cores c where c.peca_id = p.id) as cores
from pecas p where p.ativo;

-- reservar stock ao criar a encomenda (atómico; falha se não houver stock)
create or replace function criar_encomenda(p_linhas jsonb, p_cliente jsonb)
returns encomendas language plpgsql security definer as $$
declare l jsonb; c cores%rowtype; p pecas%rowtype; total numeric := 0; linhas jsonb := '[]'; e encomendas%rowtype; qt int;
begin
  for l in select * from jsonb_array_elements(p_linhas) loop
    select * into p from pecas where id = l->>'peca' and ativo for update;
    if not found then raise exception 'Peça já não existe: %', l->>'peca'; end if;
    if p.preco is null then raise exception '% ainda não tem preço', p.nome; end if;
    select * into c from cores where peca_id = p.id and posicao = (l->>'cor')::int for update;
    if not found then raise exception 'Cor inválida'; end if;
    qt := greatest(1, least(9, coalesce((l->>'qt')::int, 1)));
    if c.stock - c.reservado < qt then raise exception 'Já não há stock suficiente de "%" em % (restam %)', p.nome, c.nome, greatest(c.stock - c.reservado, 0); end if;
    update cores set reservado = reservado + qt where id = c.id;
    linhas := linhas || jsonb_build_object('peca', p.id, 'nome', p.nome, 'cor', c.posicao, 'corNome', c.nome, 'tam', (l->>'tam')::int,
      'tamNome', coalesce(p.tamanhos->>((l->>'tam')::int), 'Único'), 'qt', qt, 'preco', p.preco, 'foto', c.foto);
    total := total + p.preco * qt;
  end loop;
  insert into encomendas (cliente, linhas, total) values (p_cliente, linhas, round(total, 2)) returning * into e;
  return e;
end $$;

-- pagamento confirmado (chamado pelo webhook da Stripe)
create or replace function marcar_paga(p_id bigint, p_payment text)
returns void language plpgsql security definer as $$
declare e encomendas%rowtype; l jsonb;
begin
  select * into e from encomendas where id = p_id for update;
  if not found or e.estado <> 'pendente' then return; end if;
  for l in select * from jsonb_array_elements(e.linhas) loop
    update cores set stock = greatest(stock - (l->>'qt')::int, 0), reservado = greatest(reservado - (l->>'qt')::int, 0)
      where peca_id = l->>'peca' and posicao = (l->>'cor')::int;
  end loop;
  update encomendas set estado = 'paga', paga = now(), atualizada = now(), stripe_payment = p_payment where id = p_id;
end $$;

-- libertar reservas (falha, cancelamento, expiração)
create or replace function libertar_encomenda(p_id bigint, p_estado text, p_motivo text default null)
returns void language plpgsql security definer as $$
declare e encomendas%rowtype; l jsonb;
begin
  select * into e from encomendas where id = p_id for update;
  if not found or e.estado <> 'pendente' then return; end if;
  for l in select * from jsonb_array_elements(e.linhas) loop
    update cores set reservado = greatest(reservado - (l->>'qt')::int, 0) where peca_id = l->>'peca' and posicao = (l->>'cor')::int;
  end loop;
  update encomendas set estado = p_estado, motivo = p_motivo, atualizada = now() where id = p_id;
end $$;

-- encomendas pendentes há mais de 60 minutos expiram (corre no pg_cron, de 5 em 5 minutos)
create or replace function expirar_reservas() returns int language plpgsql security definer as $$
declare n int := 0; r record;
begin
  for r in select id from encomendas where estado = 'pendente' and criada < now() - interval '60 minutes' loop
    perform libertar_encomenda(r.id, 'expirada', 'Expirou sem pagamento'); n := n + 1;
  end loop;
  return n;
end $$;
create extension if not exists pg_cron;
select cron.schedule('expirar-reservas', '*/5 * * * *', 'select expirar_reservas()');

-- segurança: nada é acessível com a chave anónima; só as funções (service role) tocam nas tabelas
alter table categorias enable row level security;
alter table estacoes enable row level security;
alter table pecas enable row level security;
alter table cores enable row level security;
alter table encomendas enable row level security;
-- (sem policies = sem acesso anónimo; as Edge Functions usam a service key)

-- fotos das peças novas
insert into storage.buckets (id, name, public) values ('produtos', 'produtos', true) on conflict do nothing;
