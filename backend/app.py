# app.py - FastAPI Backend para Sistema de Biblioteca Escolar

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
import uvicorn

# Imports locais
from database import get_db, init_db
from models import Livro, LivroCreate, LivroUpdate, LivroResponse, EmprestimoRequest, StatusLivro
from models import validar_titulo_unico, validar_isbn_unico, pode_emprestar_livro, pode_devolver_livro
from pydantic import BaseModel

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Biblioteca Escolar",
    description="API para gerenciamento de livros e empréstimos de uma biblioteca escolar",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de resposta
class MessageResponse(BaseModel):
    message: str
    success: bool

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Inicializar banco de dados ao iniciar a aplicação"""
    init_db()

@app.get("/", response_model=MessageResponse)
async def root():
    """Endpoint raiz da API"""
    return MessageResponse(
        message="API da Biblioteca Escolar está funcionando!",
        success=True
    )

@app.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "biblioteca-api"
    }

# =================== ENDPOINTS DE LIVROS ===================

@app.get("/api/books", response_model=List[LivroResponse])
async def get_livros(
    search: Optional[str] = Query(None, description="Buscar por título, autor ou ISBN"),
    genero: Optional[str] = Query(None, description="Filtrar por gênero"),
    ano_min: Optional[int] = Query(None, description="Ano mínimo de publicação"),
    ano_max: Optional[int] = Query(None, description="Ano máximo de publicação"),
    status: Optional[StatusLivro] = Query(None, description="Status do livro"),
    db: Session = Depends(get_db)
):
    """
    Buscar livros com filtros avançados
    
    - **search**: Busca por título, autor ou ISBN (case-insensitive)
    - **genero**: Filtrar por gênero específico
    - **ano_min/ano_max**: Range de anos de publicação
    - **status**: Filtrar por status (disponivel, emprestado)
    """
    try:
        query = db.query(Livro)
        
        # Filtro de busca por texto
        if search:
            search_term = f"%{search.lower()}%"
            query = query.filter(
                (Livro.titulo.ilike(search_term)) |
                (Livro.autor.ilike(search_term)) |
                (Livro.isbn.ilike(search_term))
            )
        
        # Filtro por gênero
        if genero:
            query = query.filter(Livro.genero.ilike(f"%{genero}%"))
        
        # Filtro por ano
        if ano_min:
            query = query.filter(Livro.ano >= ano_min)
        if ano_max:
            query = query.filter(Livro.ano <= ano_max)
        
        # Filtro por status
        if status:
            query = query.filter(Livro.status == status)
        
        # Ordenar por título
        livros = query.order_by(Livro.titulo).all()
        
        return [LivroResponse.from_orm(livro) for livro in livros]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.get("/api/books/{livro_id}", response_model=LivroResponse)
async def get_livro_by_id(livro_id: int, db: Session = Depends(get_db)):
    """Buscar livro específico por ID"""
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        
        if not livro:
            raise HTTPException(
                status_code=404,
                detail=f"Livro com ID {livro_id} não encontrado"
            )
        
        return LivroResponse.from_orm(livro)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.post("/api/books", response_model=LivroResponse, status_code=201)
async def criar_livro(livro_data: LivroCreate, db: Session = Depends(get_db)):
    """
    Criar novo livro no acervo
    
    Validações incluem:
    - Título único no sistema
    - Campos obrigatórios
    - Formato de ano válido
    - ISBN único (se fornecido)
    """
    try:
        # Validar se título já existe
        if not validar_titulo_unico(db, livro_data.titulo):
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um livro com o título '{livro_data.titulo}'"
            )
        
        # Validar ISBN único (se fornecido)
        if livro_data.isbn and not validar_isbn_unico(db, livro_data.isbn):
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um livro com o ISBN '{livro_data.isbn}'"
            )
        
        # Criar novo livro
        novo_livro = Livro(
            titulo=livro_data.titulo.strip(),
            autor=livro_data.autor.strip(),
            ano=livro_data.ano,
            genero=livro_data.genero.strip(),
            isbn=livro_data.isbn.strip() if livro_data.isbn else None,
            status=StatusLivro.DISPONIVEL
        )
        
        db.add(novo_livro)
        db.commit()
        db.refresh(novo_livro)
        
        return LivroResponse.from_orm(novo_livro)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar livro: {str(e)}"
        )

@app.put("/api/books/{livro_id}", response_model=LivroResponse)
async def atualizar_livro(
    livro_id: int, 
    livro_data: LivroUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualizar informações de um livro existente
    
    Apenas campos fornecidos serão atualizados
    """
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        
        if not livro:
            raise HTTPException(
                status_code=404,
                detail=f"Livro com ID {livro_id} não encontrado"
            )
        
        # Validar título único (se fornecido e diferente do atual)
        if livro_data.titulo and livro_data.titulo.strip() != livro.titulo:
            if not validar_titulo_unico(db, livro_data.titulo, livro_id):
                raise HTTPException(
                    status_code=400,
                    detail=f"Já existe outro livro com o título '{livro_data.titulo}'"
                )
        
        # Validar ISBN único (se fornecido e diferente do atual)
        if livro_data.isbn and livro_data.isbn.strip() != livro.isbn:
            if not validar_isbn_unico(db, livro_data.isbn, livro_id):
                raise HTTPException(
                    status_code=400,
                    detail=f"Já existe outro livro com o ISBN '{livro_data.isbn}'"
                )
        
        # Atualizar campos fornecidos
        update_data = livro_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(livro, field, value)
        
        db.commit()
        db.refresh(livro)
        
        return LivroResponse.from_orm(livro)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar livro: {str(e)}"
        )

@app.delete("/api/books/{livro_id}", response_model=MessageResponse)
async def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Remover livro do acervo
    
    Não permite remoção se livro estiver emprestado
    """
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        
        if not livro:
            raise HTTPException(
                status_code=404,
                detail=f"Livro com ID {livro_id} não encontrado"
            )
        
        # Verificar se livro está emprestado
        if livro.status == StatusLivro.EMPRESTADO:
            raise HTTPException(
                status_code=400,
                detail="Não é possível remover um livro que está emprestado"
            )
        
        db.delete(livro)
        db.commit()
        
        return MessageResponse(
            message=f"Livro '{livro.titulo}' removido com sucesso",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar livro: {str(e)}"
        )

# =================== ENDPOINTS DE EMPRÉSTIMO ===================

@app.post("/api/books/{livro_id}/emprestar", response_model=LivroResponse)
async def emprestar_livro(
    livro_id: int, 
    emprestimo_data: EmprestimoRequest, 
    db: Session = Depends(get_db)
):
    """
    Realizar empréstimo de um livro
    
    Validações:
    - Livro deve estar disponível
    - Define data de empréstimo
    """
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        
        if not livro:
            raise HTTPException(
                status_code=404,
                detail=f"Livro com ID {livro_id} não encontrado"
            )
        
        # Verificar se livro pode ser emprestado
        if not pode_emprestar_livro(livro):
            raise HTTPException(
                status_code=400,
                detail="Livro não está disponível para empréstimo"
            )
        
        # Atualizar informações do empréstimo
        livro.status = StatusLivro.EMPRESTADO
        livro.data_emprestimo = emprestimo_data.data_emprestimo or date.today()
        
        db.commit()
        db.refresh(livro)
        
        return LivroResponse.from_orm(livro)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar empréstimo: {str(e)}"
        )

@app.post("/api/books/{livro_id}/devolver", response_model=LivroResponse)
async def devolver_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Realizar devolução de um livro emprestado
    
    Validações:
    - Livro deve estar emprestado
    - Limpa dados do empréstimo
    """
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        
        if not livro:
            raise HTTPException(
                status_code=404,
                detail=f"Livro com ID {livro_id} não encontrado"
            )
        
        # Verificar se livro pode ser devolvido
        if not pode_devolver_livro(livro):
            raise HTTPException(
                status_code=400,
                detail="Livro não está emprestado no momento"
            )
        
        # Atualizar status do livro
        livro.status = StatusLivro.DISPONIVEL
        livro.data_emprestimo = None
        
        db.commit()
        db.refresh(livro)
        
        return LivroResponse.from_orm(livro)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar devolução: {str(e)}"
        )

# =================== ENDPOINTS DE ESTATÍSTICAS ===================

@app.get("/api/estatisticas")
async def estatisticas_biblioteca(db: Session = Depends(get_db)):
    """Estatísticas gerais da biblioteca"""
    try:
        total_livros = db.query(Livro).count()
        livros_disponiveis = db.query(Livro).filter(Livro.status == StatusLivro.DISPONIVEL).count()
        livros_emprestados = db.query(Livro).filter(Livro.status == StatusLivro.EMPRESTADO).count()
        
        # Gêneros mais populares
        from sqlalchemy import func
        generos_populares = db.query(
            Livro.genero,
            func.count(Livro.id).label('quantidade')
        ).group_by(Livro.genero).order_by(func.count(Livro.id).desc()).limit(5).all()
        
        return {
            "acervo": {
                "total": total_livros,
                "disponiveis": livros_disponiveis,
                "emprestados": livros_emprestados
            },
            "percentuais": {
                "disponibilidade": round((livros_disponiveis / total_livros * 100), 2) if total_livros > 0 else 0,
                "utilizacao": round((livros_emprestados / total_livros * 100), 2) if total_livros > 0 else 0
            },
            "generos_populares": [
                {"genero": genero, "quantidade": quantidade} 
                for genero, quantidade in generos_populares
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar estatísticas: {str(e)}"
        )

# =================== EXCEPTION HANDLERS ===================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler customizado para HTTPExceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler para exceções não tratadas"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

# =================== MAIN ===================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )
