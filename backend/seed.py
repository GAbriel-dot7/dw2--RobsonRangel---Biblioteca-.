# seed.py - Script para popular banco de dados com dados iniciais

import sys
import os
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import Livro, StatusLivro

def criar_dados_completos():
    """Criar conjunto completo de dados para teste e demonstração"""
    
    # Inicializar banco se necessário
    init_db()
    
    db = SessionLocal()
    
    try:
        # Verificar se já há dados
        count = db.query(Livro).count()
        if count > 0:
            print(f"⚠️ Banco já possui {count} livros. Use --force para recriar.")
            return
        
        print("📚 Criando dados completos para a biblioteca...")
        
        # Lista abrangente de livros
        livros_seed = [
            # Literatura Clássica Brasileira
            {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "ano": 1899,
                "genero": "romance",
                "isbn": "978-8525406569",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "João Silva Santos",
                "turma_usuario": "3º A",
                "data_emprestimo": date.today() - timedelta(days=10),
                "data_devolucao_prevista": date.today() + timedelta(days=5)
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
                "titulo": "Quincas Borba",
                "autor": "Machado de Assis",
                "ano": 1891,
                "genero": "romance",
                "isbn": "978-8525406583",
                "status": StatusLivro.MANUTENCAO
            },
            {
                "titulo": "O Guarani",
                "autor": "José de Alencar",
                "ano": 1857,
                "genero": "romance",
                "isbn": "978-8525406590",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Iracema",
                "autor": "José de Alencar",
                "ano": 1865,
                "genero": "romance",
                "isbn": "978-8525406606",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Literatura Internacional
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
                "titulo": "1984",
                "autor": "George Orwell",
                "ano": 1949,
                "genero": "ficcao",
                "isbn": "978-8535914849",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "A Revolução dos Bichos",
                "autor": "George Orwell",
                "ano": 1945,
                "genero": "ficcao",
                "isbn": "978-8535914856",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "Maria Santos Costa",
                "turma_usuario": "2º B",
                "data_emprestimo": date.today() - timedelta(days=20),
                "data_devolucao_prevista": date.today() - timedelta(days=5)  # Em atraso
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
                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                "autor": "J.R.R. Tolkien",
                "ano": 1954,
                "genero": "aventura",
                "isbn": "978-8533613379",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "Pedro Costa Silva",
                "turma_usuario": "1º C",
                "data_emprestimo": date.today() - timedelta(days=5),
                "data_devolucao_prevista": date.today() + timedelta(days=10)
            },
            
            # Ficção Científica e Fantasia
            {
                "titulo": "Duna",
                "autor": "Frank Herbert",
                "ano": 1965,
                "genero": "ficcao",
                "isbn": "978-8576573344",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Fundação",
                "autor": "Isaac Asimov",
                "ano": 1951,
                "genero": "ficcao",
                "isbn": "978-8576573887",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Fahrenheit 451",
                "autor": "Ray Bradbury",
                "ano": 1953,
                "genero": "ficcao",
                "isbn": "978-8525052120",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Não-ficção e Ciência
            {
                "titulo": "Uma Breve História do Tempo",
                "autor": "Stephen Hawking",
                "ano": 1988,
                "genero": "ciencia",
                "isbn": "978-8580573466",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Sapiens: Uma Breve História da Humanidade",
                "autor": "Yuval Noah Harari",
                "ano": 2011,
                "genero": "nao-ficcao",
                "isbn": "978-8525432186",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "Ana Beatriz Oliveira",
                "turma_usuario": "3º C",
                "data_emprestimo": date.today() - timedelta(days=3),
                "data_devolucao_prevista": date.today() + timedelta(days=12)
            },
            {
                "titulo": "Homo Deus: Uma Breve História do Amanhã",
                "autor": "Yuval Noah Harari",
                "ano": 2015,
                "genero": "nao-ficcao",
                "isbn": "978-8535926438",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Gene Egoísta",
                "autor": "Richard Dawkins",
                "ano": 1976,
                "genero": "ciencia",
                "isbn": "978-8535925913",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Mistério e Suspense
            {
                "titulo": "O Código Da Vinci",
                "autor": "Dan Brown",
                "ano": 2003,
                "genero": "aventura",
                "isbn": "978-8575421376",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Anjos e Demônios",
                "autor": "Dan Brown",
                "ano": 2000,
                "genero": "aventura",
                "isbn": "978-8575421383",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Nome da Rosa",
                "autor": "Umberto Eco",
                "ano": 1980,
                "genero": "ficcao",
                "isbn": "978-8501061935",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Literatura Contemporânea
            {
                "titulo": "Cem Anos de Solidão",
                "autor": "Gabriel García Márquez",
                "ano": 1967,
                "genero": "ficcao",
                "isbn": "978-8501061942",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Alquimista",
                "autor": "Paulo Coelho",
                "ano": 1988,
                "genero": "ficcao",
                "isbn": "978-8573025378",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "Lucas Ferreira Lima",
                "turma_usuario": "2º A",
                "data_emprestimo": date.today() - timedelta(days=7),
                "data_devolucao_prevista": date.today() + timedelta(days=8)
            },
            {
                "titulo": "Veronika Decide Morrer",
                "autor": "Paulo Coelho",
                "ano": 1998,
                "genero": "ficcao",
                "isbn": "978-8573025385",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Biografia e História
            {
                "titulo": "Steve Jobs",
                "autor": "Walter Isaacson",
                "ano": 2011,
                "genero": "nao-ficcao",
                "isbn": "978-8535918244",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Einstein: Sua Vida, Seu Universo",
                "autor": "Walter Isaacson",
                "ano": 2007,
                "genero": "nao-ficcao",
                "isbn": "978-8535912279",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Literatura Jovem
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "autor": "J.K. Rowling",
                "ano": 1997,
                "genero": "aventura",
                "isbn": "978-8532512062",
                "status": StatusLivro.EMPRESTADO,
                "nome_usuario": "Beatriz Costa Santos",
                "turma_usuario": "1º B",
                "data_emprestimo": date.today() - timedelta(days=25),
                "data_devolucao_prevista": date.today() - timedelta(days=10)  # Em atraso
            },
            {
                "titulo": "Harry Potter e a Câmara Secreta",
                "autor": "J.K. Rowling",
                "ano": 1998,
                "genero": "aventura",
                "isbn": "978-8532512079",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Percy Jackson e o Ladrão de Raios",
                "autor": "Rick Riordan",
                "ano": 2005,
                "genero": "aventura",
                "isbn": "978-8580575237",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Autoajuda e Desenvolvimento
            {
                "titulo": "Como Fazer Amigos e Influenciar Pessoas",
                "autor": "Dale Carnegie",
                "ano": 1936,
                "genero": "nao-ficcao",
                "isbn": "978-8504014570",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Poder do Hábito",
                "autor": "Charles Duhigg",
                "ano": 2012,
                "genero": "nao-ficcao",
                "isbn": "978-8565765169",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Quadrinhos e Graphic Novels
            {
                "titulo": "Watchmen",
                "autor": "Alan Moore",
                "ano": 1986,
                "genero": "ficcao",
                "isbn": "978-8535909845",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Persépolis",
                "autor": "Marjane Satrapi",
                "ano": 2000,
                "genero": "nao-ficcao",
                "isbn": "978-8535909852",
                "status": StatusLivro.DISPONIVEL
            }
        ]
        
        # Inserir livros no banco
        livros_criados = 0
        for livro_data in livros_seed:
            try:
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
                livros_criados += 1
                
            except Exception as e:
                print(f"❌ Erro ao criar livro '{livro_data['titulo']}': {e}")
        
        # Commit das alterações
        db.commit()
        
        print(f"✅ {livros_criados} livros criados com sucesso!")
        
        # Mostrar estatísticas
        print("\n📊 Estatísticas do acervo:")
        print(f"   📚 Total: {db.query(Livro).count()}")
        print(f"   ✅ Disponíveis: {db.query(Livro).filter(Livro.status == StatusLivro.DISPONIVEL).count()}")
        print(f"   📖 Emprestados: {db.query(Livro).filter(Livro.status == StatusLivro.EMPRESTADO).count()}")
        print(f"   🔧 Em manutenção: {db.query(Livro).filter(Livro.status == StatusLivro.MANUTENCAO).count()}")
        
        # Mostrar livros em atraso
        from sqlalchemy import and_
        atrasos = db.query(Livro).filter(
            and_(
                Livro.status == StatusLivro.EMPRESTADO,
                Livro.data_devolucao_prevista < date.today()
            )
        ).count()
        print(f"   ⚠️ Em atraso: {atrasos}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar dados: {e}")
        raise
    finally:
        db.close()

def limpar_dados():
    """Limpar todos os dados do banco"""
    db = SessionLocal()
    try:
        count = db.query(Livro).count()
        if count == 0:
            print("ℹ️ Banco já está vazio.")
            return
        
        # Confirmar ação
        resposta = input(f"⚠️ Isso irá remover {count} livros. Confirma? (sim/não): ")
        if resposta.lower() not in ['sim', 's', 'yes', 'y']:
            print("❌ Operação cancelada.")
            return
        
        # Deletar todos os livros
        db.query(Livro).delete()
        db.commit()
        
        print(f"🗑️ {count} livros removidos com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao limpar dados: {e}")
        raise
    finally:
        db.close()

def mostrar_estatisticas():
    """Mostrar estatísticas atuais do banco"""
    db = SessionLocal()
    try:
        total = db.query(Livro).count()
        disponivel = db.query(Livro).filter(Livro.status == StatusLivro.DISPONIVEL).count()
        emprestado = db.query(Livro).filter(Livro.status == StatusLivro.EMPRESTADO).count()
        manutencao = db.query(Livro).filter(Livro.status == StatusLivro.MANUTENCAO).count()
        
        print("📊 ESTATÍSTICAS DA BIBLIOTECA")
        print("=" * 40)
        print(f"📚 Total de livros:     {total}")
        print(f"✅ Disponíveis:         {disponivel} ({disponivel/total*100:.1f}%)" if total > 0 else "✅ Disponíveis:         0")
        print(f"📖 Emprestados:         {emprestado} ({emprestado/total*100:.1f}%)" if total > 0 else "📖 Emprestados:         0")
        print(f"🔧 Em manutenção:       {manutencao} ({manutencao/total*100:.1f}%)" if total > 0 else "🔧 Em manutenção:       0")
        
        # Livros em atraso
        if emprestado > 0:
            from sqlalchemy import and_
            atrasos = db.query(Livro).filter(
                and_(
                    Livro.status == StatusLivro.EMPRESTADO,
                    Livro.data_devolucao_prevista < date.today()
                )
            ).count()
            print(f"⚠️ Em atraso:           {atrasos}")
        
        # Top gêneros
        from sqlalchemy import func
        top_generos = db.query(
            Livro.genero,
            func.count(Livro.id).label('count')
        ).group_by(Livro.genero).order_by(func.count(Livro.id).desc()).limit(3).all()
        
        if top_generos:
            print("\n🏆 GÊNEROS MAIS POPULARES:")
            for i, (genero, count) in enumerate(top_generos, 1):
                print(f"   {i}. {genero}: {count} livros")
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
    finally:
        db.close()

def main():
    """Função principal do script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Script para gerenciar dados da biblioteca")
    parser.add_argument("--seed", action="store_true", help="Criar dados de exemplo")
    parser.add_argument("--clear", action="store_true", help="Limpar todos os dados")
    parser.add_argument("--stats", action="store_true", help="Mostrar estatísticas")
    parser.add_argument("--force", action="store_true", help="Forçar recriação dos dados")
    
    args = parser.parse_args()
    
    if args.clear:
        limpar_dados()
    elif args.seed:
        if args.force:
            print("🔄 Forçando recriação dos dados...")
            limpar_dados()
        criar_dados_completos()
    elif args.stats:
        mostrar_estatisticas()
    else:
        print("🔧 Script de gerenciamento da biblioteca")
        print("Uso:")
        print("  python seed.py --seed     # Criar dados de exemplo")
        print("  python seed.py --clear    # Limpar todos os dados")
        print("  python seed.py --stats    # Mostrar estatísticas")
        print("  python seed.py --seed --force  # Recriar dados")

if __name__ == "__main__":
    main()
