# Telegram Bot

Este projeto possui um bot do Telegram com opções de assinatura e um servidor FastAPI para gerenciamento de posts. Abaixo estão instruções de uso e descrição das funções principais.

## Requisitos

```bash
pip install -r requirements.txt
```

As variáveis podem ser definidas no ambiente ou em um arquivo `.env` na raiz do
projeto com o seguinte formato:

```
TELEGRAM_BOT_TOKEN=seu_token
MERCADO_PAGO_TOKEN=opcional
CRON_HOUR=9
```

Essas variáveis são:

- `TELEGRAM_BOT_TOKEN`: token do bot.
- Os canais público e privado são configurados pela API.
- `MERCADO_PAGO_TOKEN`: token do Mercado Pago (opcional).
- `CRON_HOUR`: horário (0-23) para os posts agendados (padrão 9).

## Iniciando os servidores

### Bot + Scheduler

Execute `main.py` para iniciar o bot e o agendador de posts:

```bash
python3 main.py
```

### API Web

Execute o servidor FastAPI com `uvicorn`:

```bash
uvicorn web.app:app --reload
```

A API fornece os seguintes endpoints:

- `POST /posts/public` — adiciona um post público (campo `text` e múltiplos arquivos `files`).
- `POST /posts/private` — adiciona um post privado (campo `text` e múltiplos arquivos `files`).
- `GET /posts/public` — lista posts públicos agendados.
- `GET /posts/private` — lista posts privados agendados.
- `POST /posts/public/{id}/send` — envia imediatamente o post público indicado.
- `POST /posts/private/{id}/send` — envia imediatamente o post privado indicado.
- `GET /stats` — exibe estatísticas de usuários e assinaturas.
- `GET /channels/available` — lista canais que o bot possui acesso.
- `GET /channels/config` — obtém os canais configurados.
- `POST /channels/config` — define o canal público e o privado.

Arquivos enviados são gravados na pasta `uploads` e podem ser acessados via `/uploads`.

### Interface Web

A pasta `web/static` contém páginas HTML simples para gerenciamento do bot.
Elas podem ser acessadas após iniciar a API:

- `index.html` — página inicial com links.
- `private_posts.html` — lista e cria posts para o canal privado.
- `public_posts.html` — lista e cria posts para o canal público.
- `channels.html` — configuração dos canais.
- `stats.html` — painel de estatísticas.

## Funções Principais

### `bot/bot.py`

- `start_bot()` — inicia o bot do Telegram.
- `start(update, context)` — envia a mensagem inicial de boas‑vindas.
- `mensal(update, context)` — informa o link de pagamento mensal.
- `vitalicio(update, context)` — informa o link de pagamento vitalício.

### `bot/scheduler.py`

- `start()` — inicia o agendador `APScheduler` para publicações diárias.

### `bot/poster.py`

- `send_public_post(session)` — envia um post para o canal público.
- `send_private_post(session)` — envia um post para o canal privado.

### `bot/subscriptions.py`

- `create_user(telegram_id, username)` — registra o usuário no banco.
- `activate_monthly(user)` — ativa o plano mensal.
- `activate_lifetime(user)` — ativa o plano vitalício.
- `check_expirations()` — verifica expirações de planos mensais.

### `bot/payments.py`

- `create_payment(amount, description)` — gera um link de pagamento fictício.

### `bot/database.py`

Contém os modelos SQLAlchemy (`User`, `PublicPost`, `PrivatePost`, `BotConfig`) e a função `get_session()` para obter uma sessão do banco.

## Executando testes

Não há testes automatizados, portanto basta seguir os passos de execução acima.

