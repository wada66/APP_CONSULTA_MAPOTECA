import re
from flask import Flask, render_template, request, jsonify, current_app
from config import Config
from models import db
from sqlalchemy import or_, extract

# Importar todos os modelos (já definidos em models.py)
from models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Dicionário que mapeia schema para seus modelos
SCHEMA_MODELS = {
    'livros': {
        'principal': Livro,
        'setor': LivroSetor,
        'local': LivroLocal,
        'assunto': LivroAssunto,
        'autor': LivroAutorTabela,
        'executor': LivroExecutorTabela,
        'editor': LivroEditorTabela,
        'area': LivroAreaGeograficaLivro,
        'join_autor': LivroAutor,
        'join_executor': LivroExecutor,
        'join_editor': LivroEditor,
        'join_area': LivroAreaGeografica,
    },
    'mapas': {
        'principal': Mapa,
        'local': MapaLocal,
        'autor': MapaAutorTabela,
        'executor': MapaExecutorTabela,
        'area': MapaAreaGeograficaLivro,
        'join_autor': MapaAutor,
        'join_executor': MapaExecutor,
        'join_area': MapaAreaGeografica,
    },
    'projar': {
        'principal': Projar,
        'setor': ProjarSetor,
        'local': ProjarLocal,
        'assunto': ProjarAssunto,
        'autor': ProjarAutorTabela,
        'executor': ProjarExecutorTabela,
        'area': ProjarAreaGeograficaLivro,
        'join_autor': ProjarAutor,
        'join_executor': ProjarExecutor,
        'join_area': ProjarAreaGeografica,
        'join_assunto': ProjarAssuntoRel,
    },
    'projen': {
        'principal': Projen,
        'setor': ProjenSetor,
        'local': ProjenLocal,
        'assunto': ProjenAssunto,
        'autor': ProjenAutorTabela,
        'executor': ProjenExecutorTabela,
        'area': ProjenAreaGeograficaLivro,
        'join_autor': ProjenAutor,
        'join_executor': ProjenExecutor,
        'join_area': ProjenAreaGeografica,
        'join_assunto': ProjenAssuntoRel,
    }
}

def get_field_names(schema):
    """Retorna os nomes dos campos para cada schema"""
    if schema == 'livros':
        return {
            'pk': 'id_livro',
            'titulo': 'titulo_livro',
            'chamada': 'n_chamada_livro',
            'conteudo': 'conteudo_livro',
            'data': 'data_livro'
        }
    elif schema == 'mapas':
        return {
            'pk': 'id_mapa',
            'titulo': 'titulo_mapa',
            'chamada': 'n_chamada_mapa',
            'conteudo': 'conteudo_mapa',
            'data': 'data_mapa'
        }
    elif schema == 'projar':
        return {
            'pk': 'id_projar',
            'titulo': 'titulo_projar',
            'chamada': 'n_chamada_projar',
            'conteudo': 'conteudo_projar',
            'data': 'data_projar'
        }
    elif schema == 'projen':
        return {
            'pk': 'id_projen',
            'titulo': 'titulo_projen',
            'chamada': 'n_chamada_projen',
            'conteudo': 'conteudo_projen',
            'data': 'data_projen'
        }
    return {}

def criar_padrao_regex(palavra):
    """Gera padrão regex para busca case-insensitive com acentos."""
    padrao = ''
    for letra in palavra.lower():
        if letra == 'a': padrao += '[aáàãâä]'
        elif letra == 'e': padrao += '[eéèêë]'
        elif letra == 'i': padrao += '[iíìîï]'
        elif letra == 'o': padrao += '[oóòõôö]'
        elif letra == 'u': padrao += '[uúùûü]'
        elif letra == 'c': padrao += '[cç]'
        else: padrao += re.escape(letra)
    return padrao

@app.route('/')
def index():
    """Tela inicial com os 4 cards."""
    return render_template('index.html')

@app.route('/listar')
def listar():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return "Schema inválido", 400

    models = SCHEMA_MODELS[schema]
    Principal = models['principal']
    field_names = get_field_names(schema)

    # Carregar dados para os selects (se existirem)
    locais = models['local'].query.order_by(models['local'].nome_local).all() if 'local' in models else []
    setores = models['setor'].query.order_by(models['setor'].nome_setor).all() if 'setor' in models else []
    assuntos = models['assunto'].query.order_by(models['assunto'].nome_assunto).all() if 'assunto' in models else []
    autores = models['autor'].query.order_by(models['autor'].nome_autor).all() if 'autor' in models else []
    executores = models['executor'].query.order_by(models['executor'].nome_executor).all() if 'executor' in models else []
    editores = models['editor'].query.order_by(models['editor'].nome_editor).all() if 'editor' in models else []
    areas = models['area'].query.order_by(models['area'].nome_area_geografica).all() if 'area' in models else []

    # Verificar se há filtros
    has_filters = any([
        request.args.get('id'),
        request.args.get('n_chamada'),
        request.args.get('titulo'),
        request.args.get('autor'),
        request.args.get('local_id'),
        request.args.get('setor_id'),
        request.args.get('assunto_id'),
        request.args.get('mes'),
        request.args.get('ano'),
        request.args.get('conteudo'),
        request.args.get('executor'),
        request.args.get('editor'),
        request.args.get('area_id'),
        request.args.get('escala'),
        request.args.get('projecao'),
        request.args.get('outras_versoes'),
    ])

    filtros = {}
    if has_filters:
        query = Principal.query

        # Filtros comuns (presentes em todos os schemas)
        if 'id' in request.args and request.args['id']:
            try:
                id_val = int(request.args['id'])
                query = query.filter(getattr(Principal, field_names['pk']) == id_val)
                filtros['id'] = request.args['id']
            except:
                pass

        if 'n_chamada' in request.args and request.args['n_chamada']:
            query = query.filter(getattr(Principal, field_names['chamada']).like(f"%{request.args['n_chamada']}%"))
            filtros['n_chamada'] = request.args['n_chamada']

        if 'titulo' in request.args and request.args['titulo']:
            termo = request.args['titulo'].strip()
            if termo:
                palavras = termo.split()
                condicoes = []
                for palavra in palavras:
                    if len(palavra) >= 2:
                        padrao = criar_padrao_regex(palavra)
                        try:
                            condicoes.append(getattr(Principal, field_names['titulo']).op('~*')(padrao))
                        except:
                            condicoes.append(getattr(Principal, field_names['titulo']).ilike(f"%{palavra}%"))
                    else:
                        condicoes.append(getattr(Principal, field_names['titulo']).ilike(f"%{palavra}%"))
                if condicoes:
                    query = query.filter(*condicoes)
                filtros['titulo'] = termo

        if 'data' in request.args and request.args['data']:
            try:
                from datetime import datetime
                data_str = request.args['data']
                # Verifica se está no formato correto YYYY-MM-DD
                data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
                query = query.filter(getattr(Principal, field_names['data']) == data_obj)
                filtros['data'] = data_str
            except (ValueError, AttributeError):
                # Se não conseguir converter, ignora o filtro de data
                pass

        if 'conteudo' in request.args and request.args['conteudo']:
            termo = request.args['conteudo'].strip()
            if termo:
                palavras = termo.split()
                condicoes = []
                for palavra in palavras:
                    if len(palavra) >= 2:
                        padrao = criar_padrao_regex(palavra)
                        try:
                            condicoes.append(getattr(Principal, field_names['conteudo']).op('~*')(padrao))
                        except:
                            condicoes.append(getattr(Principal, field_names['conteudo']).ilike(f"%{palavra}%"))
                    else:
                        condicoes.append(getattr(Principal, field_names['conteudo']).ilike(f"%{palavra}%"))
                if condicoes:
                    query = query.filter(*condicoes)
                filtros['conteudo'] = termo

        # Filtros específicos por schema
        if schema == 'livros':
            # Autor
            if 'autor' in request.args and request.args['autor']:
                termo = request.args['autor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['autor'].nome_autor.op('~*')(padrao))
                            except:
                                condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_autor'].id_livro).join(
                            models['autor'], models['join_autor'].id_autor == models['autor'].id_autor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_livro.in_(subq))
                    filtros['autor'] = termo

            # Local
            if 'local_id' in request.args and request.args['local_id']:
                try:
                    query = query.filter(Principal.id_local == int(request.args['local_id']))
                    filtros['local_id'] = request.args['local_id']
                except: pass

            # Setor
            if 'setor_id' in request.args and request.args['setor_id']:
                try:
                    query = query.filter(Principal.id_setor == int(request.args['setor_id']))
                    filtros['setor_id'] = request.args['setor_id']
                except: pass

            # Assunto (FK)
            if 'assunto_id' in request.args and request.args['assunto_id']:
                try:
                    query = query.filter(Principal.id_assunto == int(request.args['assunto_id']))
                    filtros['assunto_id'] = request.args['assunto_id']
                except: pass

            # Executor
            if 'executor' in request.args and request.args['executor']:
                termo = request.args['executor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['executor'].nome_executor.op('~*')(padrao))
                            except:
                                condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_executor'].id_livro).join(
                            models['executor'], models['join_executor'].id_executor == models['executor'].id_executor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_livro.in_(subq))
                    filtros['executor'] = termo

            # Editor
            if 'editor' in request.args and request.args['editor']:
                termo = request.args['editor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['editor'].nome_editor.op('~*')(padrao))
                            except:
                                condicoes.append(models['editor'].nome_editor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['editor'].nome_editor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_editor'].id_livro).join(
                            models['editor'], models['join_editor'].id_editor == models['editor'].id_editor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_livro.in_(subq))
                    filtros['editor'] = termo

            # Área geográfica
            if 'area_id' in request.args and request.args['area_id']:
                try:
                    subq = db.session.query(models['join_area'].id_livro).filter(
                        models['join_area'].id_area_geografica == int(request.args['area_id'])
                    )
                    query = query.filter(Principal.id_livro.in_(subq))
                    filtros['area_id'] = request.args['area_id']
                except: pass

        elif schema == 'mapas':
            # Autor
            if 'autor' in request.args and request.args['autor']:
                termo = request.args['autor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['autor'].nome_autor.op('~*')(padrao))
                            except:
                                condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_autor'].mapa_id).join(
                            models['autor'], models['join_autor'].autor_id == models['autor'].id_autor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_mapa.in_(subq))
                    filtros['autor'] = termo

            # Local
            if 'local_id' in request.args and request.args['local_id']:
                try:
                    query = query.filter(Principal.local_id == int(request.args['local_id']))
                    filtros['local_id'] = request.args['local_id']
                except: pass

            # Executor
            if 'executor' in request.args and request.args['executor']:
                termo = request.args['executor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['executor'].nome_executor.op('~*')(padrao))
                            except:
                                condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_executor'].mapa_id).join(
                            models['executor'], models['join_executor'].executor_id == models['executor'].id_executor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_mapa.in_(subq))
                    filtros['executor'] = termo

            # Área geográfica
            if 'area_id' in request.args and request.args['area_id']:
                try:
                    subq = db.session.query(models['join_area'].mapa_id).filter(
                        models['join_area'].area_geografica_id == int(request.args['area_id'])
                    )
                    query = query.filter(Principal.id_mapa.in_(subq))
                    filtros['area_id'] = request.args['area_id']
                except: pass

            # Campos específicos de mapa
            if 'escala' in request.args and request.args['escala']:
                query = query.filter(Principal.escala_mapa.ilike(f"%{request.args['escala']}%"))
                filtros['escala'] = request.args['escala']
            if 'projecao' in request.args and request.args['projecao']:
                query = query.filter(Principal.projecao_mapa.ilike(f"%{request.args['projecao']}%"))
                filtros['projecao'] = request.args['projecao']
            if 'articulacao' in request.args and request.args['articulacao']:
                query = query.filter(Principal.articulacao_mapa.ilike(f"%{request.args['articulacao']}%"))
                filtros['articulacao'] = request.args['articulacao']
            if 'setor_mapa' in request.args and request.args['setor_mapa']:
                query = query.filter(Principal.setor_mapa.ilike(f"%{request.args['setor_mapa']}%"))
                filtros['setor_mapa'] = request.args['setor_mapa']
            if 'assunto_mapa' in request.args and request.args['assunto_mapa']:
                query = query.filter(Principal.assunto_mapa.ilike(f"%{request.args['assunto_mapa']}%"))
                filtros['assunto_mapa'] = request.args['assunto_mapa']

        elif schema == 'projar':
            # Autor
            if 'autor' in request.args and request.args['autor']:
                termo = request.args['autor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['autor'].nome_autor.op('~*')(padrao))
                            except:
                                condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_autor'].projar_id).join(
                            models['autor'], models['join_autor'].autor_id == models['autor'].id_autor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_projar.in_(subq))
                    filtros['autor'] = termo

            # Executor
            if 'executor' in request.args and request.args['executor']:
                termo = request.args['executor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['executor'].nome_executor.op('~*')(padrao))
                            except:
                                condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_executor'].projar_id).join(
                            models['executor'], models['join_executor'].executor_id == models['executor'].id_executor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_projar.in_(subq))
                    filtros['executor'] = termo

            # Local
            if 'local_id' in request.args and request.args['local_id']:
                try:
                    query = query.filter(Principal.local_id == int(request.args['local_id']))
                    filtros['local_id'] = request.args['local_id']
                except: pass

            # Setor
            if 'setor_id' in request.args and request.args['setor_id']:
                try:
                    query = query.filter(Principal.setor_id == int(request.args['setor_id']))
                    filtros['setor_id'] = request.args['setor_id']
                except: pass

            # Assunto (via tabela de junção)
            if 'assunto_id' in request.args and request.args['assunto_id']:
                try:
                    subq = db.session.query(models['join_assunto'].projar_id).filter(
                        models['join_assunto'].assunto_id == int(request.args['assunto_id'])
                    )
                    query = query.filter(Principal.id_projar.in_(subq))
                    filtros['assunto_id'] = request.args['assunto_id']
                except: pass

            # Área geográfica
            if 'area_id' in request.args and request.args['area_id']:
                try:
                    subq = db.session.query(models['join_area'].projar_id).filter(
                        models['join_area'].area_geografica_id == int(request.args['area_id'])
                    )
                    query = query.filter(Principal.id_projar.in_(subq))
                    filtros['area_id'] = request.args['area_id']
                except: pass

            # Campos específicos
            if 'escala' in request.args and request.args['escala']:
                query = query.filter(Principal.escala_projar.ilike(f"%{request.args['escala']}%"))
                filtros['escala'] = request.args['escala']
            if 'outras_versoes' in request.args and request.args['outras_versoes']:
                query = query.filter(Principal.outras_versoes_projar.ilike(f"%{request.args['outras_versoes']}%"))
                filtros['outras_versoes'] = request.args['outras_versoes']

        elif schema == 'projen':
            # Autor
            if 'autor' in request.args and request.args['autor']:
                termo = request.args['autor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['autor'].nome_autor.op('~*')(padrao))
                            except:
                                condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['autor'].nome_autor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_autor'].projen_id).join(
                            models['autor'], models['join_autor'].autor_id == models['autor'].id_autor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_projen.in_(subq))
                    filtros['autor'] = termo

            # Executor
            if 'executor' in request.args and request.args['executor']:
                termo = request.args['executor'].strip()
                if termo:
                    palavras = termo.split()
                    condicoes = []
                    for palavra in palavras:
                        if len(palavra) >= 2:
                            padrao = criar_padrao_regex(palavra)
                            try:
                                condicoes.append(models['executor'].nome_executor.op('~*')(padrao))
                            except:
                                condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                        else:
                            condicoes.append(models['executor'].nome_executor.ilike(f"%{palavra}%"))
                    if condicoes:
                        subq = db.session.query(models['join_executor'].projen_id).join(
                            models['executor'], models['join_executor'].executor_id == models['executor'].id_executor
                        ).filter(*condicoes)
                        query = query.filter(Principal.id_projen.in_(subq))
                    filtros['executor'] = termo

            # Local
            if 'local_id' in request.args and request.args['local_id']:
                try:
                    query = query.filter(Principal.local_id == int(request.args['local_id']))
                    filtros['local_id'] = request.args['local_id']
                except: pass

            # Setor
            if 'setor_id' in request.args and request.args['setor_id']:
                try:
                    query = query.filter(Principal.setor_id == int(request.args['setor_id']))
                    filtros['setor_id'] = request.args['setor_id']
                except: pass

            # Assunto (via tabela de junção)
            if 'assunto_id' in request.args and request.args['assunto_id']:
                try:
                    subq = db.session.query(models['join_assunto'].projen_id).filter(
                        models['join_assunto'].assunto_id == int(request.args['assunto_id'])
                    )
                    query = query.filter(Principal.id_projen.in_(subq))
                    filtros['assunto_id'] = request.args['assunto_id']
                except: pass

            # Área geográfica
            if 'area_id' in request.args and request.args['area_id']:
                try:
                    subq = db.session.query(models['join_area'].projen_id).filter(
                        models['join_area'].area_geografica_id == int(request.args['area_id'])
                    )
                    query = query.filter(Principal.id_projen.in_(subq))
                    filtros['area_id'] = request.args['area_id']
                except: pass

        # Ordenação e execução da query
        order_field = getattr(Principal, field_names['pk'])
        itens = query.order_by(order_field.desc()).all()
    else:
        itens = []

    # Passar os dados para o template
    return render_template('listar.html',
                           schema=schema,
                           itens=itens,
                           locais=locais,
                           setores=setores,
                           assuntos=assuntos,
                           autores=autores,
                           executores=executores,
                           editores=editores,
                           areas=areas,
                           filtros=filtros,
                           has_filters=has_filters)

# APIs auxiliares (se necessário)
@app.route('/api/autores')
def api_autores():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Autor = SCHEMA_MODELS[schema].get('autor')
    if not Autor:
        return jsonify([])
    autores = Autor.query.order_by(Autor.nome_autor).all()
    return jsonify([{'id': a.id_autor, 'nome': a.nome_autor, 'tipo': getattr(a, 'tipo_autor', '')} for a in autores])

@app.route('/api/executores')
def api_executores():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Executor = SCHEMA_MODELS[schema].get('executor')
    if not Executor:
        return jsonify([])
    executores = Executor.query.order_by(Executor.nome_executor).all()
    return jsonify([{'id': e.id_executor, 'nome': e.nome_executor} for e in executores])

@app.route('/api/editores')
def api_editores():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Editor = SCHEMA_MODELS[schema].get('editor')
    if not Editor:
        return jsonify([])
    editores = Editor.query.order_by(Editor.nome_editor).all()
    return jsonify([{'id': e.id_editor, 'nome': e.nome_editor} for e in editores])

@app.route('/api/locais')
def api_locais():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Local = SCHEMA_MODELS[schema].get('local')
    if not Local:
        return jsonify([])
    locais = Local.query.order_by(Local.nome_local).all()
    return jsonify([{'id': l.id_local, 'nome': l.nome_local} for l in locais])

@app.route('/api/setores')
def api_setores():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Setor = SCHEMA_MODELS[schema].get('setor')
    if not Setor:
        return jsonify([])
    setores = Setor.query.order_by(Setor.nome_setor).all()
    return jsonify([{'id': s.id_setor, 'nome': s.nome_setor} for s in setores])

@app.route('/api/assuntos')
def api_assuntos():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Assunto = SCHEMA_MODELS[schema].get('assunto')
    if not Assunto:
        return jsonify([])
    assuntos = Assunto.query.order_by(Assunto.nome_assunto).all()
    return jsonify([{'id': a.id_assunto, 'nome': a.nome_assunto} for a in assuntos])

@app.route('/api/areas')
def api_areas():
    schema = request.args.get('schema', 'livros')
    if schema not in SCHEMA_MODELS:
        return jsonify([])
    Area = SCHEMA_MODELS[schema].get('area')
    if not Area:
        return jsonify([])
    areas = Area.query.order_by(Area.nome_area_geografica).all()
    return jsonify([{'id': a.id_area_geografica, 'nome': a.nome_area_geografica} for a in areas])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)