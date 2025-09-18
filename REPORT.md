# Relatório do Projeto Biblioteca

## 📊 Visão Geral do Projeto

Este projeto implementa um **Sistema de Biblioteca Escolar** completo, desenvolvido com arquitetura full-stack moderna, focado em simplicidade e funcionalidade para gestão de acervo escolar.

### 🎯 Objetivos Alcançados
- ✅ Sistema de cadastro e gerenciamento de livros
- ✅ Funcionalidades de empréstimo e devolução
- ✅ Interface web responsiva e intuitiva
- ✅ API RESTful completa com documentação automática
- ✅ Banco de dados SQLite com validações robustas
- ✅ Sistema de busca e filtros avançados

## 🏗️ Arquitetura e Tecnologias

### Frontend
- **HTML5**: Estrutura semântica com acessibilidade
- **CSS3**: Design responsivo com Grid/Flexbox e variáveis CSS
- **JavaScript ES6+**: Aplicação SPA com classe BibliotecaApp
- **Fetch API**: Comunicação assíncrona com backend

### Backend
- **FastAPI**: Framework moderno com documentação automática
- **SQLAlchemy**: ORM para abstração de banco de dados
- **Pydantic**: Validação de dados e serialização
- **SQLite**: Banco de dados leve e eficiente

### Estrutura de Pastas
```
📁 Biblioteca/
├── 📁 frontend/
│   ├── index.html      # Interface principal
│   ├── styles.css      # Estilos responsivos
│   └── scripts.js      # Lógica da aplicação
├── 📁 backend/
│   ├── app.py          # API FastAPI
│   ├── models.py       # Modelos SQLAlchemy/Pydantic
│   ├── database.py     # Configuração do banco
│   ├── seed.py         # População de dados
│   └── requirements.txt
└── REPORT.md
```

## 🔧 Decisões Técnicas

### 1. Modelo de Dados Simplificado
**Decisão**: Foco em campos essenciais para biblioteca escolar
```python
Livro:
- id (PK)
- titulo (único)
- autor
- ano
- genero
- isbn (opcional)
- status (disponivel/emprestado)
- data_emprestimo (quando aplicável)
```

**Justificativa**: Atende necessidades básicas sem complexidade desnecessária

### 2. Status Binário de Livros
**Decisão**: Apenas "disponível" e "emprestado"
**Justificativa**: Simplifica fluxo de trabalho em ambiente escolar

### 3. Frontend Vanilla JavaScript
**Decisão**: Não usar frameworks complexos
**Justificativa**: Facilita manutenção e aprendizado para ambiente educacional

### 4. SQLite como Banco
**Decisão**: Banco local em arquivo
**Justificativa**: Simplicidade de deploy e backup em ambiente escolar

## 📈 Funcionalidades Implementadas

### Core Features
1. **CRUD Completo de Livros**
   - Cadastro com validação de título único
   - Edição de informações
   - Exclusão (apenas se não emprestado)
   - Listagem com paginação

2. **Sistema de Empréstimos**
   - Empréstimo de livros disponíveis
   - Devolução com limpeza de dados
   - Controle de status automático

3. **Busca e Filtros**
   - Busca textual (título, autor, ISBN)
   - Filtros por gênero, ano, status
   - Combinação de múltiplos filtros

### Advanced Features
4. **Interface Responsiva**
   - Design mobile-first
   - Modais para formulários
   - Feedback visual (toasts)
   - Atalhos de teclado (Alt+N, Alt+E)

5. **API Documentada**
   - Swagger UI automático
   - Validação de entrada
   - Tratamento de erros
   - Health check endpoint

6. **Estatísticas**
   - Contadores de acervo
   - Gêneros mais populares
   - Percentuais de utilização

## 🎓 Aprendizados e Desafios

### Principais Aprendizados
1. **Integração Full-Stack**: Conexão eficiente entre frontend e backend via API REST
2. **Validação Robusta**: Implementação de validações tanto no frontend quanto backend
3. **UX Focada**: Interface intuitiva para usuários não-técnicos (bibliotecários, estudantes)
4. **Documentação Automática**: FastAPI facilita manutenção com docs geradas automaticamente

### Desafios Superados
1. **Validação de Unicidade**: Garantir títulos únicos sem conflitos em edições
2. **Estado Consistente**: Sincronização entre frontend e backend para status de livros
3. **Responsividade**: Layout adaptável para diferentes dispositivos escolares
4. **Tratamento de Erros**: Feedback claro para usuários sobre operações inválidas

### Melhorias Futuras
- 🔄 Sistema de usuários com autenticação
- 📅 Controle de prazos e multas por atraso
- 📊 Relatórios mais detalhados
- 🔍 Busca por código de barras
- 📱 Progressive Web App (PWA)

## 🧪 Como Testar o Sistema

### 📋 Pré-requisitos

#### 1. Instalar Python e Dependências
```bash
# Navegar para a pasta backend
cd backend

# Instalar dependências
pip install -r requirements.txt
```

### 🚀 Iniciando o Sistema

#### 1. Iniciar o Backend (API FastAPI)
```bash
cd backend
python app.py
```

A API estará disponível em:
- **Aplicação**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### 2. Abrir o Frontend
Abra o arquivo `frontend/index.html` diretamente no navegador ou use um servidor web local.

### 🧪 Testando Funcionalidades

#### Via Interface Web (Frontend)

1. **Adicionar Livros**
   - Clique em "Adicionar Livro" 
   - Preencha: Título, Autor, Ano, Gênero, ISBN (opcional)
   - Título deve ser único no sistema

2. **Buscar e Filtrar**
   - Use a barra de pesquisa para buscar por título, autor ou ISBN
   - Filtre por gênero, ano ou status
   - Use paginação para navegar pelos resultados

3. **Emprestar Livros**
   - Clique em "Emprestar" em um livro disponível
   - Livro muda status para "Emprestado"

4. **Devolver Livros**
   - Clique em "Devolver" em um livro emprestado
   - Livro volta ao status "Disponível"

5. **Editar/Excluir**
   - Use os botões "Editar" e "Excluir" nos cards dos livros
   - Livros emprestados não podem ser excluídos

#### Via API (Para Testes Avançados)

Acesse http://localhost:8000/docs para testar todos os endpoints interativamente:

**Endpoints Principais:**
- `GET /api/books` - Listar livros com filtros
- `POST /api/books` - Criar novo livro
- `GET /api/books/{id}` - Buscar livro por ID
- `PUT /api/books/{id}` - Atualizar livro
- `DELETE /api/books/{id}` - Excluir livro
- `POST /api/books/{id}/emprestar` - Emprestar livro
- `POST /api/books/{id}/devolver` - Devolver livro
- `GET /api/estatisticas` - Estatísticas da biblioteca

### 📊 Banco de Dados

#### Visualizar Dados
O sistema usa SQLite. Arquivo: `backend/biblioteca.db`

Ferramentas recomendadas:
- DB Browser for SQLite
- VS Code com extensão SQLite

#### Popular com Dados de Exemplo
```bash
cd backend
python seed.py
```

### 🔧 Estrutura dos Dados

#### Modelo de Livro (Simplificado)
```json
{
    "id": 1,
    "titulo": "Dom Casmurro",           
    "autor": "Machado de Assis",
    "ano": 1899,
    "genero": "Romance",
    "isbn": "978-85-359-0277-5",        
    "status": "disponivel",             
    "data_emprestimo": "2024-01-15"     
}
```

#### Status Possíveis
- **disponivel**: Livro pode ser emprestado
- **emprestado**: Livro está com usuário

### ⚠️ Validações Implementadas

1. **Título Único**: Não permite dois livros com mesmo título
2. **ISBN Único**: Se fornecido, deve ser único
3. **Campos Obrigatórios**: Título, autor, ano, gênero
4. **Regras de Empréstimo**: 
   - Só empresta livros disponíveis
   - Só devolve livros emprestados
   - Não pode excluir livros emprestados

### 🎯 Casos de Teste Sugeridos

1. **Teste de Validação**
   - Tente criar livro com título duplicado
   - Tente criar livro sem campos obrigatórios

2. **Teste de Fluxo de Empréstimo**
   - Empreste um livro → verifique mudança de status
   - Tente emprestar livro já emprestado
   - Devolva o livro → verifique mudança de status

3. **Teste de Filtros**
   - Busque por diferentes termos
   - Filtre por gênero específico
   - Combine múltiplos filtros

4. **Teste de Performance**
   - Adicione muitos livros via seed.py
   - Teste paginação e filtros com volume alto de dados

## 📋 Conclusão

O Sistema de Biblioteca Escolar foi desenvolvido com sucesso, atendendo aos requisitos de:
- ✅ **Funcionalidade**: CRUD completo e empréstimos
- ✅ **Usabilidade**: Interface intuitiva para ambiente escolar
- ✅ **Manutenibilidade**: Código limpo e bem documentado
- ✅ **Escalabilidade**: Arquitetura preparada para evoluções

O projeto demonstra aplicação prática de conceitos modernos de desenvolvimento web, com foco em simplicidade e eficiência para o contexto educacional.

---

💡 **Dica**: Use o endpoint `/docs` para testar a API de forma interativa e ver a documentação automática gerada pelo FastAPI!
