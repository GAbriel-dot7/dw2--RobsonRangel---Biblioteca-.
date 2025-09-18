# models.py - Modelos SQLAlchemy para Sistema de Biblioteca Escolar

from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

# Base do SQLAlchemy
Base = declarative_base()

# Enum para status do livro
class StatusLivro(str, Enum):
    DISPONIVEL = "disponivel"
    EMPRESTADO = "emprestado"

# =================== MODELO SQLALCHEMY ===================

class Livro(Base):
    """
    Tabela de livros da biblioteca
    
    Campos obrigatórios: titulo, autor, ano, genero, status
    Campos opcionais: isbn, data_emprestimo
    """
    __tablename__ = "livros"
    
    # Campo chave primária
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Campos obrigatórios
    titulo = Column(String(200), nullable=False, index=True)
    autor = Column(String(100), nullable=False, index=True)
    ano = Column(Integer, nullable=False)
    genero = Column(String(50), nullable=False, index=True)
    status = Column(SQLEnum(StatusLivro), default=StatusLivro.DISPONIVEL, nullable=False, index=True)
    
    # Campos opcionais
    isbn = Column(String(20), nullable=True, unique=True, index=True)
    data_emprestimo = Column(Date, nullable=True)
    
    # Constraints de unicidade
    __table_args__ = (
        UniqueConstraint('titulo', name='uq_livro_titulo'),
    )
    
    def __repr__(self):
        return f"<Livro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', status='{self.status}')>"
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano})"

# =================== MODELOS PYDANTIC PARA API ===================

class LivroBase(BaseModel):
    """Modelo base com validações"""
    titulo: str = Field(..., min_length=1, max_length=200, description="Título do livro")
    autor: str = Field(..., min_length=1, max_length=100, description="Autor do livro")
    ano: int = Field(..., ge=1800, le=2025, description="Ano de publicação")
    genero: str = Field(..., min_length=1, max_length=50, description="Gênero do livro")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN do livro (opcional)")
    
    @validator('titulo', 'autor', 'genero')
    def validar_campos_texto(cls, v):
        """Validar campos de texto não podem estar vazios"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Campo não pode estar vazio')
        return v
    
    @validator('ano')
    def validar_ano(cls, v):
        """Validar se ano está em range válido"""
        if v < 1800 or v > 2025:
            raise ValueError('Ano deve estar entre 1800 e 2025')
        return v
    
    @validator('isbn')
    def validar_isbn(cls, v):
        """Validar formato básico do ISBN"""
        if v is not None:
            v = v.strip().replace('-', '').replace(' ', '')
            if v and not v.isdigit():
                raise ValueError('ISBN deve conter apenas números')
            if v and len(v) not in [10, 13]:
                raise ValueError('ISBN deve ter 10 ou 13 dígitos')
        return v

class LivroCreate(LivroBase):
    """Modelo para criação de novo livro"""
    pass

class LivroUpdate(BaseModel):
    """Modelo para atualização de livro (todos campos opcionais)"""
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    autor: Optional[str] = Field(None, min_length=1, max_length=100)
    ano: Optional[int] = Field(None, ge=1800, le=2025)
    genero: Optional[str] = Field(None, min_length=1, max_length=50)
    isbn: Optional[str] = Field(None, max_length=20)
    status: Optional[StatusLivro] = None
    data_emprestimo: Optional[date] = None
    
    @validator('titulo', 'autor', 'genero')
    def validar_campos_texto(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Campo não pode estar vazio')
        return v
    
    @validator('ano')
    def validar_ano(cls, v):
        if v is not None and (v < 1800 or v > 2025):
            raise ValueError('Ano deve estar entre 1800 e 2025')
        return v
    
    @validator('isbn')
    def validar_isbn(cls, v):
        if v is not None:
            v = v.strip().replace('-', '').replace(' ', '')
            if v and not v.isdigit():
                raise ValueError('ISBN deve conter apenas números')
            if v and len(v) not in [10, 13]:
                raise ValueError('ISBN deve ter 10 ou 13 dígitos')
        return v

class LivroResponse(LivroBase):
    """Modelo de resposta da API"""
    id: int
    status: StatusLivro
    data_emprestimo: Optional[date] = None
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj):
        """Converter objeto SQLAlchemy para Pydantic"""
        return cls(
            id=obj.id,
            titulo=obj.titulo,
            autor=obj.autor,
            ano=obj.ano,
            genero=obj.genero,
            isbn=obj.isbn,
            status=obj.status,
            data_emprestimo=obj.data_emprestimo
        )

class EmprestimoRequest(BaseModel):
    """Modelo para realizar empréstimo"""
    data_emprestimo: Optional[date] = Field(None, description="Data do empréstimo (padrão: hoje)")
    
    @validator('data_emprestimo')
    def validar_data_emprestimo(cls, v):
        """Data de empréstimo não pode ser futura"""
        if v is not None and v > date.today():
            raise ValueError('Data de empréstimo não pode ser futura')
        return v

# =================== FUNÇÕES UTILITÁRIAS ===================

def validar_titulo_unico(db_session, titulo: str, livro_id: Optional[int] = None) -> bool:
    """Verificar se título é único no banco de dados"""
    query = db_session.query(Livro).filter(Livro.titulo.ilike(titulo.strip()))
    if livro_id:
        query = query.filter(Livro.id != livro_id)
    return query.first() is None

def validar_isbn_unico(db_session, isbn: str, livro_id: Optional[int] = None) -> bool:
    """Verificar se ISBN é único no banco de dados"""
    if not isbn:
        return True
    
    query = db_session.query(Livro).filter(Livro.isbn == isbn.strip())
    if livro_id:
        query = query.filter(Livro.id != livro_id)
    return query.first() is None

def pode_emprestar_livro(livro: Livro) -> bool:
    """Verificar se livro pode ser emprestado"""
    return livro.status == StatusLivro.DISPONIVEL

def pode_devolver_livro(livro: Livro) -> bool:
    """Verificar se livro pode ser devolvido"""
    return livro.status == StatusLivro.EMPRESTADO
