# seed.py - Script para popular banco de dados com dados iniciais

import sys
import os
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import Livro, StatusLivro

# seed.py - Script para popular banco de dados com dados iniciais

import sys
import os
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import Livro, StatusLivro, validar_titulo_unico, validar_isbn_unico

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
        
        # Lista abrangente de livros para biblioteca escolar (35 livros total)
        livros_seed = [
            # Literatura Clássica Brasileira
            {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "ano": 1899,
                "genero": "Romance",
                "isbn": "978-8525406569",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=10)
            },
            {
                "titulo": "O Cortiço",
                "autor": "Aluísio Azevedo",
                "ano": 1890,
                "genero": "Romance",
                "isbn": "978-8525406576",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Iracema",
                "autor": "José de Alencar",
                "ano": 1865,
                "genero": "Romance",
                "isbn": "978-8525406606",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Ateneu",
                "autor": "Raul Pompéia",
                "ano": 1888,
                "genero": "Romance",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Senhora",
                "autor": "José de Alencar",
                "ano": 1875,
                "genero": "Romance",
                "isbn": "978-8520923580",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=6)
            },
            {
                "titulo": "O Guarani",
                "autor": "José de Alencar",
                "ano": 1857,
                "genero": "Romance",
                "isbn": "978-8525406590",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Memórias Póstumas de Brás Cubas",
                "autor": "Machado de Assis",
                "ano": 1881,
                "genero": "Romance",
                "isbn": "978-8520923597",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Literatura Internacional Clássica
            {
                "titulo": "O Pequeno Príncipe",
                "autor": "Antoine de Saint-Exupéry",
                "ano": 1943,
                "genero": "Ficção",
                "isbn": "978-8520925065",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "ano": 1949,
                "genero": "Ficção Científica",
                "isbn": "978-8535914849",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "A Revolução dos Bichos",
                "autor": "George Orwell",
                "ano": 1945,
                "genero": "Fábula",
                "isbn": "978-8535914856",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=20)
            },
            {
                "titulo": "Dom Quixote",
                "autor": "Miguel de Cervantes",
                "ano": 1605,
                "genero": "Romance",
                "isbn": "978-8525432124",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Conde de Monte Cristo",
                "autor": "Alexandre Dumas",
                "ano": 1844,
                "genero": "Aventura",
                "isbn": "978-8520923603",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=4)
            },
            {
                "titulo": "Os Três Mosqueteiros",
                "autor": "Alexandre Dumas",
                "ano": 1844,
                "genero": "Aventura",
                "isbn": "978-8520923610",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Orgulho e Preconceito",
                "autor": "Jane Austen",
                "ano": 1813,
                "genero": "Romance",
                "isbn": "978-8535926445",
                "status": StatusLivro.DISPONIVEL
            },
            
            # Fantasia e Aventura
            {
                "titulo": "O Hobbit",
                "autor": "J.R.R. Tolkien",
                "ano": 1937,
                "genero": "Fantasia",
                "isbn": "978-8595084759",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "autor": "J.K. Rowling",
                "ano": 1997,
                "genero": "Fantasia",
                "isbn": "978-8532512062",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=25)
            },
            {
                "titulo": "Harry Potter e a Câmara Secreta",
                "autor": "J.K. Rowling",
                "ano": 1998,
                "genero": "Fantasia",
                "isbn": "978-8532512079",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Harry Potter e o Prisioneiro de Azkaban",
                "autor": "J.K. Rowling",
                "ano": 1999,
                "genero": "Fantasia",
                "isbn": "978-8532512086",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=12)
            },
            {
                "titulo": "As Crônicas de Nárnia: O Leão, a Feiticeira e o Guarda-Roupa",
                "autor": "C.S. Lewis",
                "ano": 1950,
                "genero": "Fantasia",
                "isbn": "978-8578274550",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Percy Jackson e o Ladrão de Raios",
                "autor": "Rick Riordan",
                "ano": 2005,
                "genero": "Aventura",
                "isbn": "978-8580575237",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=5)
            },
            {
                "titulo": "Percy Jackson e o Mar de Monstros",
                "autor": "Rick Riordan",
                "ano": 2006,
                "genero": "Aventura",
                "isbn": "978-8580575244",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                "autor": "J.R.R. Tolkien",
                "ano": 1954,
                "genero": "Fantasia",
                "isbn": "978-8533615653",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=8)
            },
            
            # Ciência e Não-ficção
            {
                "titulo": "Uma Breve História do Tempo",
                "autor": "Stephen Hawking",
                "ano": 1988,
                "genero": "Ciência",
                "isbn": "978-8580573466",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Sapiens: Uma Breve História da Humanidade",
                "autor": "Yuval Noah Harari",
                "ano": 2011,
                "genero": "História",
                "isbn": "978-8525432186",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=3)
            },
            {
                "titulo": "O Mundo de Sofia",
                "autor": "Jostein Gaarder",
                "ano": 1991,
                "genero": "Filosofia",
                "isbn": "978-8535906770",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Cosmos",
                "autor": "Carl Sagan",
                "ano": 1980,
                "genero": "Ciência",
                "isbn": "978-8535925920",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Homo Deus: Uma Breve História do Amanhã",
                "autor": "Yuval Noah Harari",
                "ano": 2015,
                "genero": "História",
                "isbn": "978-8535926438",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=9)
            },
            
            # Literatura Contemporânea
            {
                "titulo": "O Alquimista",
                "autor": "Paulo Coelho",
                "ano": 1988,
                "genero": "Ficção",
                "isbn": "978-8573025378",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=7)
            },
            {
                "titulo": "Cem Anos de Solidão",
                "autor": "Gabriel García Márquez",
                "ano": 1967,
                "genero": "Realismo Mágico",
                "isbn": "978-8501061942",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Capitães da Areia",
                "autor": "Jorge Amado",
                "ano": 1937,
                "genero": "Romance",
                "isbn": "978-8535918632",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=14)
            },
            {
                "titulo": "A Hora da Estrela",
                "autor": "Clarice Lispector",
                "ano": 1977,
                "genero": "Romance",
                "isbn": "978-8520925959",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "O Nome da Rosa",
                "autor": "Umberto Eco",
                "ano": 1980,
                "genero": "Mistério",
                "isbn": "978-8501061935",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Veronika Decide Morrer",
                "autor": "Paulo Coelho",
                "ano": 1998,
                "genero": "Ficção",
                "isbn": "978-8573025385",
                "status": StatusLivro.DISPONIVEL
            },
            {
                "titulo": "Dona Flor e Seus Dois Maridos",
                "autor": "Jorge Amado",
                "ano": 1966,
                "genero": "Romance",
                "isbn": "978-8535918649",
                "status": StatusLivro.EMPRESTADO,
                "data_emprestimo": date.today() - timedelta(days=2)
            },
            {
                "titulo": "Gabriela, Cravo e Canela",
                "autor": "Jorge Amado",
                "ano": 1958,
                "genero": "Romance",
                "isbn": "978-8535918656",
                "status": StatusLivro.DISPONIVEL
            }
        ]
        
        # Inserir livros no banco com validações
        livros_criados = 0
        livros_ignorados = 0
        
        for livro_data in livros_seed:
            try:
                # Verificar se título já existe
                if not validar_titulo_unico(db, livro_data["titulo"]):
                    print(f"⚠️ Livro '{livro_data['titulo']}' já existe - ignorando")
                    livros_ignorados += 1
                    continue
                
                # Verificar ISBN se fornecido
                if livro_data.get("isbn") and not validar_isbn_unico(db, livro_data["isbn"]):
                    print(f"⚠️ ISBN '{livro_data['isbn']}' já existe - ignorando")
                    livros_ignorados += 1
                    continue
                
                livro = Livro(
                    titulo=livro_data["titulo"],
                    autor=livro_data["autor"],
                    ano=livro_data["ano"],
                    genero=livro_data["genero"],
                    isbn=livro_data.get("isbn"),
                    status=livro_data["status"],
                    data_emprestimo=livro_data.get("data_emprestimo")
                )
                
                db.add(livro)
                livros_criados += 1
                
                # Status visual
                status_icon = "📚" if livro_data["status"] == StatusLivro.DISPONIVEL else "📖"
                print(f"✅ {status_icon} {livro_data['titulo']} - {livro_data['autor']} ({livro_data['ano']})")
                
            except Exception as e:
                print(f"❌ Erro ao criar livro '{livro_data['titulo']}': {e}")
        
        # Commit das alterações
        db.commit()
        
        print(f"\n🎉 {livros_criados} livros criados com sucesso!")
        if livros_ignorados > 0:
            print(f"⚠️ {livros_ignorados} livros ignorados (já existem)")
        
        # Mostrar estatísticas finais
        print("\n📊 Estatísticas do acervo:")
        total = db.query(Livro).count()
        disponivel = db.query(Livro).filter(Livro.status == StatusLivro.DISPONIVEL).count()
        emprestado = db.query(Livro).filter(Livro.status == StatusLivro.EMPRESTADO).count()
        
        print(f"   � Total: {total}")
        print(f"   ✅ Disponíveis: {disponivel} ({disponivel/total*100:.1f}%)" if total > 0 else "   ✅ Disponíveis: 0")
        print(f"   📖 Emprestados: {emprestado} ({emprestado/total*100:.1f}%)" if total > 0 else "   📖 Emprestados: 0")
        
        print("\n✨ Seed concluído!")
        
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
        
        print("📊 ESTATÍSTICAS DA BIBLIOTECA")
        print("=" * 40)
        print(f"📚 Total de livros:     {total}")
        print(f"✅ Disponíveis:         {disponivel} ({disponivel/total*100:.1f}%)" if total > 0 else "✅ Disponíveis:         0")
        print(f"📖 Emprestados:         {emprestado} ({emprestado/total*100:.1f}%)" if total > 0 else "📖 Emprestados:         0")
        
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
