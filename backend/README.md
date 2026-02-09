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

### Produção (MySQL)

```bash
# Configurar variáveis de ambiente
set MYSQL_DATABASE=os_db
set MYSQL_USER=root
set MYSQL_PASSWORD=senha
set MYSQL_HOST=localhost
set MYSQL_PORT=3306

# Aplicar migrations
python manage.py migrate
```

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
