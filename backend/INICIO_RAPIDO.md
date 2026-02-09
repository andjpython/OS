# Início Rápido - Sistema de OS

## 🚀 Passos para iniciar o sistema

### 1. Instalar Dependências

```powershell
cd backend
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados (SQLite para desenvolvimento)

```powershell
$env:USE_SQLITE='1'
python manage.py migrate
```

### 3. Criar Superusuário (Admin)

```powershell
python manage.py createsuperuser
```

Preencha:
- Username: admin
- Email: admin@example.com
- Password: (sua senha)

### 4. Popular com Dados de Exemplo (Opcional)

```powershell
python manage.py seed_data
```

Este comando irá criar:
- 5 status de OS (Aberta, Em Andamento, etc.)
- 5 profissionais com matrículas
- 4 ordens de serviço
- 3 ações técnicas

### 5. Iniciar o Servidor

```powershell
python manage.py runserver
```

O servidor estará disponível em: http://localhost:8000

## 📍 URLs Importantes

- **Admin Django**: http://localhost:8000/admin
  - Login com o superusuário criado
  - Interface completa para gerenciar todos os dados

- **API REST**: http://localhost:8000/api/
  - Ordens: http://localhost:8000/api/ordens/
  - Ações: http://localhost:8000/api/acoes/
  - Profissionais: http://localhost:8000/api/profissionais/
  - Fotos: http://localhost:8000/api/fotos/

## 🧪 Executar Testes

```powershell
$env:USE_SQLITE='1'
python manage.py test ordens pessoas acoes
```

Resultado esperado: `Ran 15 tests in 0.0XXs - OK`

## 📝 Exemplos de Uso da API

### Criar Profissional

```bash
curl -X POST http://localhost:8000/api/profissionais/ \
  -H "Content-Type: application/json" \
  -d "{\"nome\": \"João Silva\", \"matricula\": \"1234\", \"ativo\": true}"
```

### Criar Ordem de Serviço

```bash
curl -X POST http://localhost:8000/api/ordens/ \
  -H "Content-Type: application/json" \
  -d "{\"numero\": \"OS-001\", \"descricao\": \"Instalação\", \"status\": 1, \"profissionais\": [1]}"
```

### Listar Ordens

```bash
curl http://localhost:8000/api/ordens/
```

### Filtrar por Status

```bash
curl http://localhost:8000/api/ordens/?status_id=1
```

### Finalizar OS

```bash
curl -X POST http://localhost:8000/api/ordens/1/finalizar/ \
  -H "Content-Type: application/json" \
  -d "{\"status_id\": 4}"
```

### Criar Ação Técnica

```bash
curl -X POST http://localhost:8000/api/acoes/ \
  -H "Content-Type: application/json" \
  -d "{\"ordem_servico\": 1, \"profissional\": 1, \"descricao\": \"Instalação concluída\"}"
```

## 🔧 Configuração MySQL (Produção)

### 1. Configurar Variáveis de Ambiente

Criar arquivo `.env` baseado no `.env.example`:

```env
# .env
MYSQL_DATABASE=os_db
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### 2. Criar Banco de Dados MySQL

```sql
CREATE DATABASE os_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Aplicar Migrations

```powershell
# Remover ou comentar USE_SQLITE
python manage.py migrate
```

## 🐛 Solução de Problemas

### Erro: "No module named django"
```powershell
pip install -r requirements.txt
```

### Erro: "django.db.utils.OperationalError"
- Verificar se o MySQL está rodando
- Verificar credenciais no `.env`
- Para desenvolvimento, use SQLite: `$env:USE_SQLITE='1'`

### Erro de Migrations
```powershell
# Resetar migrations (cuidado em produção!)
rm db.sqlite3
rm */migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

## 📚 Próximos Passos

1. Explorar o Admin Django em `/admin`
2. Testar os endpoints da API
3. Criar dados de teste com `seed_data`
4. Executar os testes unitários
5. Integrar com frontend (React, Vue, etc.)

## 🎯 Estrutura da API

```
/api/
├── ordens/
│   ├── GET, POST            → Listar/criar OS
│   ├── {id}/                → Detalhes/atualizar/deletar
│   └── {id}/finalizar/      → Finalizar OS
├── acoes/
│   ├── GET, POST            → Listar/criar ações
│   └── {id}/                → Detalhes
├── fotos/
│   ├── GET, POST            → Listar/adicionar fotos
│   └── {id}/                → Detalhes
└── profissionais/
    ├── GET, POST            → Listar/criar profissionais
    └── {id}/                → Detalhes
```

---

**Sistema pronto para uso! 🎉**
