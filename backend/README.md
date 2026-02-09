# Backend - Sistema de Ordens de Serviço

Backend Django REST Framework para gerenciamento de ordens de serviço.

## Estrutura

- **core**: Modelos de domínio (StatusOS)
- **ordens**: Ordens de serviço e profissionais associados
- **acoes**: Ações técnicas e fotos
- **pessoas**: Cadastro de profissionais

## Configuração

### Desenvolvimento (SQLite)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar para usar SQLite
set USE_SQLITE=1

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

### Deploy no Render (PostgreSQL)

1. Crie um banco **PostgreSQL** no Render e copie a `DATABASE_URL`.
2. Crie um **Web Service** apontando para o repositório e defina a pasta `backend` como root.
3. Configure as variáveis de ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `DEBUG=0`
   - `ALLOWED_HOSTS` (ex: `seu-app.onrender.com`)
4. Comandos do serviço:
   - **Build**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start**: `gunicorn backend.wsgi:application`

## API Endpoints

- `GET/POST /api/ordens/` - Listar/criar ordens de serviço
- `GET/PUT/PATCH/DELETE /api/ordens/{id}/` - Detalhes da OS
- `POST /api/ordens/{id}/finalizar/` - Finalizar OS
- `GET/POST /api/acoes/` - Listar/criar ações técnicas
- `GET/POST /api/fotos/` - Listar/adicionar fotos
- `GET/POST /api/profissionais/` - Listar/criar profissionais

### Filtros

- `GET /api/ordens/?status_id={id}` - Filtrar por status
- `GET /api/ordens/?profissional_id={id}` - Filtrar por profissional
- `GET /api/profissionais/?matricula={matricula}` - Buscar por matrícula

## Regras de Negócio

1. **Matrícula**: 4 dígitos únicos
2. **Finalização de OS**: Calcula automaticamente `tempo_total_minutos` e atualiza status
3. **Ações Técnicas**: Profissional deve estar associado à OS
