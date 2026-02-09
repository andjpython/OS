# Sistema de Ordens de Serviço (OS)

Backend Django REST Framework para gerenciamento completo de ordens de serviço, profissionais e ações técnicas.

## ✅ Status do Projeto

**TODOS OS REQUISITOS IMPLEMENTADOS E TESTADOS**

- ✅ Projeto Django configurado com 4 apps modulares
- ✅ Suporte para MySQL e SQLite
- ✅ 6 modelos implementados com relacionamentos
- ✅ API REST completa com DRF
- ✅ 15 testes unitários (100% aprovados)
- ✅ Regras de negócio implementadas
- ✅ Admin Django configurado
- ✅ Documentação completa

## 🏗️ Estrutura do Projeto

```
OS/
├── backend/                         # Projeto Django
│   ├── manage.py                    # CLI do Django
│   ├── requirements.txt             # Dependências Python
│   ├── .env.example                 # Exemplo de variáveis de ambiente
│   ├── .gitignore                   # Arquivos ignorados pelo Git
│   ├── README.md                    # Documentação do backend
│   ├── INICIO_RAPIDO.md            # Guia de início rápido
│   ├── exemplo_api.py              # Script de exemplo da API
│   │
│   ├── backend/                     # Configurações do projeto
│   │   ├── settings.py             # Configurações (MySQL/SQLite)
│   │   ├── urls.py                 # Rotas principais + API
│   │   └── wsgi.py                 # WSGI para deploy
│   │
│   ├── core/                        # App de domínios
│   │   ├── models.py               # StatusOS
│   │   ├── admin.py                # Admin do StatusOS
│   │   └── management/
│   │       └── commands/
│   │           └── seed_data.py    # Popular banco com dados
│   │
│   ├── pessoas/                     # App de profissionais
│   │   ├── models.py               # Profissional
│   │   ├── serializers.py          # ProfissionalSerializer
│   │   ├── views.py                # ProfissionalViewSet
│   │   ├── admin.py                # Admin
│   │   └── tests.py                # 4 testes
│   │
│   ├── ordens/                      # App de ordens de serviço
│   │   ├── models.py               # OrdemServico, OrdemServicoProfissional
│   │   ├── serializers.py          # Serializers
│   │   ├── views.py                # OrdemServicoViewSet + finalizar
│   │   ├── admin.py                # Admin
│   │   └── tests.py                # 5 testes
│   │
│   └── acoes/                       # App de ações técnicas
│       ├── models.py               # AcaoTecnica, FotoAcao
│       ├── serializers.py          # Serializers
│       ├── views.py                # ViewSets
│       ├── admin.py                # Admin
│       └── tests.py                # 6 testes
│
└── RESUMO_IMPLEMENTACAO.md         # Documentação completa da implementação
```

## 🗄️ Modelos de Dados

### StatusOS (core)
- `nome` - Nome do status (unique)
- `descricao` - Descrição do status

### Profissional (pessoas)
- `nome` - Nome do profissional
- `matricula` - Matrícula de 4 dígitos (unique, validado)
- `ativo` - Status ativo/inativo

### OrdemServico (ordens)
- `numero` - Número da OS (unique)
- `descricao` - Descrição da OS
- `status` - FK para StatusOS
- `data_abertura` - Data/hora de abertura (auto)
- `data_finalizacao` - Data/hora de finalização
- `tempo_total_minutos` - Tempo total calculado
- `profissionais` - Many-to-Many com Profissional

### AcaoTecnica (acoes)
- `ordem_servico` - FK para OrdemServico
- `profissional` - FK para Profissional
- `descricao` - Descrição da ação
- `data_hora` - Data/hora da ação (auto)

### FotoAcao (acoes)
- `acao` - FK para AcaoTecnica
- `arquivo` - Arquivo da foto (upload_to='acoes/')
- `criado_em` - Data/hora de criação (auto)

## 🔌 API REST Endpoints

### Ordens de Serviço
```
GET    /api/ordens/                    # Listar todas as OS
POST   /api/ordens/                    # Criar nova OS
GET    /api/ordens/{id}/               # Detalhes de uma OS
PUT    /api/ordens/{id}/               # Atualizar OS completa
PATCH  /api/ordens/{id}/               # Atualizar OS parcial
DELETE /api/ordens/{id}/               # Deletar OS
POST   /api/ordens/{id}/finalizar/     # Finalizar OS

# Filtros
GET    /api/ordens/?status_id={id}              # Filtrar por status
GET    /api/ordens/?profissional_id={id}        # Filtrar por profissional
```

### Ações Técnicas
```
GET    /api/acoes/                     # Listar ações
POST   /api/acoes/                     # Criar ação
GET    /api/acoes/{id}/                # Detalhes da ação
PUT    /api/acoes/{id}/                # Atualizar ação
DELETE /api/acoes/{id}/                # Deletar ação
```

### Fotos
```
GET    /api/fotos/                     # Listar fotos
POST   /api/fotos/                     # Upload de foto
GET    /api/fotos/{id}/                # Detalhes da foto
DELETE /api/fotos/{id}/                # Deletar foto
```

### Profissionais
```
GET    /api/profissionais/             # Listar profissionais
POST   /api/profissionais/             # Criar profissional
GET    /api/profissionais/{id}/        # Detalhes do profissional
PUT    /api/profissionais/{id}/        # Atualizar profissional
DELETE /api/profissionais/{id}/        # Deletar profissional

# Filtros
GET    /api/profissionais/?matricula={matricula}   # Buscar por matrícula
```

## 🎯 Regras de Negócio Implementadas

1. **Validação de Matrícula**
   - Deve ter exatamente 4 dígitos
   - Deve ser única no sistema
   - Validação em nível de modelo e serializer

2. **Finalização de Ordem de Serviço**
   - Registra automaticamente `data_finalizacao`
   - Calcula `tempo_total_minutos` (data_finalizacao - data_abertura)
   - Atualiza o status da OS
   - Impede finalização duplicada

3. **Ações Técnicas**
   - Profissional deve estar associado à OS
   - Validação em nível de modelo (clean) e serializer
   - Data/hora registrada automaticamente

## 🚀 Início Rápido

### 1. Instalar e Configurar

```powershell
cd backend
pip install -r requirements.txt
$env:USE_SQLITE='1'
python manage.py migrate
python manage.py createsuperuser
```

### 2. Popular com Dados de Exemplo

```powershell
python manage.py seed_data
```

### 3. Iniciar o Servidor

```powershell
python manage.py runserver
```

Acesse:
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api/

## 🧪 Testes

```powershell
$env:USE_SQLITE='1'
python manage.py test ordens pessoas acoes
```

**Resultado:** 15 testes, 100% aprovados

### Cobertura de Testes
- ✅ Criação de modelos
- ✅ Validações de campos
- ✅ Regras de negócio
- ✅ Finalização de OS e cálculo de tempo
- ✅ Associação de profissionais
- ✅ Validações de ações técnicas

## 📦 Dependências

- **Django 6.0.2** - Framework web
- **Django REST Framework 3.16.1** - API REST
- **PyMySQL 1.1.2** - Driver MySQL para Python

## 🔧 Configuração

### Desenvolvimento (SQLite)
```powershell
$env:USE_SQLITE='1'
```

### Produção (MySQL)
```env
MYSQL_DATABASE=os_db
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

## 📚 Documentação Adicional

- **INICIO_RAPIDO.md** - Guia passo a passo para iniciar
- **RESUMO_IMPLEMENTACAO.md** - Detalhes completos da implementação
- **backend/README.md** - Documentação técnica do backend
- **exemplo_api.py** - Script Python com exemplos de uso da API

## ✨ Recursos Extras

- ✅ Django Admin configurado para todos os modelos
- ✅ Inlines para relacionamentos (profissionais, fotos)
- ✅ Filtros e buscas no admin
- ✅ Comando de management para popular banco
- ✅ Upload de arquivos (fotos)
- ✅ Otimizações de query (select_related, prefetch_related)
- ✅ .gitignore configurado
- ✅ .env.example documentado

## 🎓 Próximos Passos Sugeridos

1. **Frontend**: Desenvolver interface React/Vue para consumir a API
2. **Autenticação**: Adicionar JWT/Token authentication
3. **Permissões**: Implementar controle de acesso por role
4. **Notificações**: Sistema de notificações para OS
5. **Relatórios**: Gerar relatórios em PDF/Excel
6. **WebSocket**: Atualizações em tempo real
7. **Docker**: Containerizar a aplicação
8. **CI/CD**: Pipeline de deploy automatizado

## 📄 Licença

Este projeto foi desenvolvido como sistema de gerenciamento de ordens de serviço.

---

**Desenvolvido com Django + DRF** 🚀
# OS
# OS
