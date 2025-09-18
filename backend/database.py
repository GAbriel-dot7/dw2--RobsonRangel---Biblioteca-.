# database.py - Configuração do Banco de Dados SQLite

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
import sqlite3
import os
from typing import Generator

from models import Base

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./biblioteca.db"

# Criar engine SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Necessário para SQLite
    echo=False  # Mudar para True para ver logs SQL
)

# Configurar SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Event listener para habilitar foreign keys no SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Habilitar foreign keys e otimizações no SQLite"""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        
        # Habilitar foreign keys
        cursor.execute("PRAGMA foreign_keys=ON")
        
        # Otimizações de performance
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        cursor.execute("PRAGMA synchronous=NORMAL")  # Balanceamento performance/segurança
        cursor.execute("PRAGMA cache_size=1000")  # Cache de páginas
        cursor.execute("PRAGMA temp_store=MEMORY")  # Dados temporários em memória
        
        cursor.close()

def init_db():
    """Inicializar banco de dados - criar todas as tabelas"""
    try:
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Banco de dados inicializado com sucesso!")
        
        # Verificar se há dados e criar dados de exemplo se necessário
        db = SessionLocal()
        try:
            from models import Livro, StatusLivro
            from datetime import datetime, date
            
            # Contar livros existentes
            count = db.query(Livro).count()
            
            if count == 0:
                print("📚 Criando dados de exemplo...")
                criar_dados_exemplo(db)
                
        except Exception as e:
            print(f"⚠️ Erro ao criar dados de exemplo: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        raise

def criar_dados_exemplo(db: Session):
    """Criar dados de exemplo para teste"""
    from models import Livro, StatusLivro
    from datetime import datetime, date, timedelta
    
    livros_exemplo = [
        {
            "titulo": "O Pequeno Príncipe",
            "autor": "Antoine de Saint-Exupéry",
            "ano": 1943,
            "genero": "ficcao",
            "isbn": "978-8520925065",
            "capa_url": "https://images-na.ssl-images-amazon.com/images/I/71OZY035QKL.jpg",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "ano": 1899,
            "genero": "romance",
            "isbn": "978-8525406569",
            "status": StatusLivro.EMPRESTADO,
            "nome_usuario": "João Silva",
            "turma_usuario": "3º A",
            "data_emprestimo": date.today() - timedelta(days=10),
            "data_devolucao_prevista": date.today() + timedelta(days=5)
        },
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "ano": 1949,
            "genero": "ficcao",
            "isbn": "978-8535914849",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "O Cortiço",
            "autor": "Aluísio Azevedo",
            "ano": 1890,
            "genero": "romance",
            "isbn": "978-8525406576",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "A Revolução dos Bichos",
            "autor": "George Orwell",
            "ano": 1945,
            "genero": "ficcao",
            "isbn": "978-8535914856",
            "status": StatusLivro.EMPRESTADO,
            "nome_usuario": "Maria Santos",
            "turma_usuario": "2º B",
            "data_emprestimo": date.today() - timedelta(days=20),
            "data_devolucao_prevista": date.today() - timedelta(days=5)  # Em atraso
        },
        {
            "titulo": "Quincas Borba",
            "autor": "Machado de Assis",
            "ano": 1891,
            "genero": "romance",
            "isbn": "978-8525406583",
            "status": StatusLivro.MANUTENCAO
        },
        {
            "titulo": "O Hobbit",
            "autor": "J.R.R. Tolkien",
            "ano": 1937,
            "genero": "aventura",
            "isbn": "978-8595084759",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "Uma Breve História do Tempo",
            "autor": "Stephen Hawking",
            "ano": 1988,
            "genero": "ciencia",
            "isbn": "978-8580573466",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "O Código Da Vinci",
            "autor": "Dan Brown",
            "ano": 2003,
            "genero": "aventura",
            "isbn": "978-8575421376",
            "status": StatusLivro.DISPONIVEL
        },
        {
            "titulo": "Sapiens: Uma Breve História da Humanidade",
            "autor": "Yuval Noah Harari",
            "ano": 2011,
            "genero": "nao-ficcao",
            "isbn": "978-8525432186",
            "status": StatusLivro.EMPRESTADO,
            "nome_usuario": "Pedro Costa",
            "turma_usuario": "1º C",
            "data_emprestimo": date.today() - timedelta(days=5),
            "data_devolucao_prevista": date.today() + timedelta(days=10)
        }
    ]
    
    for livro_data in livros_exemplo:
        livro = Livro(
            titulo=livro_data["titulo"],
            autor=livro_data["autor"],
            ano=livro_data["ano"],
            genero=livro_data["genero"],
            isbn=livro_data.get("isbn"),
            capa_url=livro_data.get("capa_url"),
            status=livro_data["status"],
            nome_usuario=livro_data.get("nome_usuario"),
            turma_usuario=livro_data.get("turma_usuario"),
            data_emprestimo=livro_data.get("data_emprestimo"),
            data_devolucao_prevista=livro_data.get("data_devolucao_prevista"),
            data_cadastro=datetime.now()
        )
        db.add(livro)
    
    db.commit()
    print(f"✅ Criados {len(livros_exemplo)} livros de exemplo!")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados
    Usar como: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def reset_database():
    """Resetar banco de dados - CUIDADO: apaga todos os dados!"""
    try:
        # Remover arquivo do banco se existir
        if os.path.exists("biblioteca.db"):
            os.remove("biblioteca.db")
            print("🗑️ Banco de dados anterior removido")
        
        # Recriar banco
        init_db()
        print("✅ Banco de dados resetado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao resetar banco de dados: {e}")
        raise

def backup_database(backup_path: str = None):
    """Criar backup do banco de dados"""
    try:
        if backup_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"biblioteca_backup_{timestamp}.db"
        
        if os.path.exists("biblioteca.db"):
            import shutil
            shutil.copy2("biblioteca.db", backup_path)
            print(f"💾 Backup criado: {backup_path}")
            return backup_path
        else:
            print("⚠️ Banco de dados não encontrado para backup")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        raise

def get_db_stats():
    """Obter estatísticas do banco de dados"""
    try:
        db = SessionLocal()
        from models import Livro, StatusLivro
        
        stats = {
            "total_livros": db.query(Livro).count(),
            "por_status": {
                "disponivel": db.query(Livro).filter(Livro.status == StatusLivro.DISPONIVEL).count(),
                "emprestado": db.query(Livro).filter(Livro.status == StatusLivro.EMPRESTADO).count(),
                "manutencao": db.query(Livro).filter(Livro.status == StatusLivro.MANUTENCAO).count(),
            },
            "arquivo_db": {
                "existe": os.path.exists("biblioteca.db"),
                "tamanho_mb": round(os.path.getsize("biblioteca.db") / 1024 / 1024, 2) if os.path.exists("biblioteca.db") else 0
            }
        }
        
        db.close()
        return stats
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
        return None

def test_connection():
    """Testar conexão com o banco de dados"""
    try:
        db = SessionLocal()
        # Tentar executar uma query simples
        result = db.execute("SELECT 1").fetchone()
        db.close()
        
        if result:
            print("✅ Conexão com banco de dados OK!")
            return True
        else:
            print("❌ Falha na conexão com banco de dados")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

# Classe para gerenciamento de transações
class DatabaseManager:
    """Gerenciador de contexto para transações do banco"""
    
    def __init__(self):
        self.db = None
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()

# Utilitários para migrations simples
def add_column_if_not_exists(table_name: str, column_name: str, column_definition: str):
    """Adicionar coluna se não existir (migration simples)"""
    try:
        db = SessionLocal()
        
        # Verificar se coluna existe
        result = db.execute(f"PRAGMA table_info({table_name})").fetchall()
        columns = [col[1] for col in result]
        
        if column_name not in columns:
            db.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            db.commit()
            print(f"✅ Coluna {column_name} adicionada à tabela {table_name}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {e}")
        if db:
            db.rollback()
            db.close()

# Script principal para setup
if __name__ == "__main__":
    print("🔧 Configurando banco de dados...")
    
    # Testar conexão
    if test_connection():
        print("📊 Estatísticas do banco:")
        stats = get_db_stats()
        if stats:
            print(f"   - Total de livros: {stats['total_livros']}")
            print(f"   - Disponíveis: {stats['por_status']['disponivel']}")
            print(f"   - Emprestados: {stats['por_status']['emprestado']}")
            print(f"   - Em manutenção: {stats['por_status']['manutencao']}")
            print(f"   - Tamanho do arquivo: {stats['arquivo_db']['tamanho_mb']} MB")
    else:
        print("🔄 Inicializando banco de dados...")
        init_db()
