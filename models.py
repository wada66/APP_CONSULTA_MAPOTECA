from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ------------------------------------------------------------
# Schema livros
# ------------------------------------------------------------
class LivroSetor(db.Model):
    __tablename__ = 'setor'
    __table_args__ = {'schema': 'livros'}
    id_setor = db.Column(db.Integer, primary_key=True)
    nome_setor = db.Column(db.String(200))
    livros = db.relationship('Livro', backref='setor_obj', foreign_keys='Livro.id_setor')

class LivroLocal(db.Model):
    __tablename__ = 'local'
    __table_args__ = {'schema': 'livros'}
    id_local = db.Column(db.Integer, primary_key=True)
    nome_local = db.Column(db.String(40))
    livros = db.relationship('Livro', backref='local_obj', foreign_keys='Livro.id_local')

class LivroAssunto(db.Model):
    __tablename__ = 'assunto'
    __table_args__ = {'schema': 'livros'}
    id_assunto = db.Column(db.Integer, primary_key=True)
    nome_assunto = db.Column(db.String(300))
    livros = db.relationship('Livro', backref='assunto_obj', foreign_keys='Livro.id_assunto')

class Livro(db.Model):
    __tablename__ = 'livro'
    __table_args__ = {'schema': 'livros'}
    id_livro = db.Column(db.Integer, primary_key=True)
    tipo_livro = db.Column(db.String(1))
    idioma_livro = db.Column(db.String(10))
    titulo_livro = db.Column(db.String(500))
    edicao_livro = db.Column(db.String(13))
    n_chamada_livro = db.Column(db.String(40))
    data_livro = db.Column(db.Date)
    colacao_paginas_livro = db.Column(db.String(20))
    colacao_volume_tomo_livro = db.Column(db.String(30))
    serie_livro = db.Column(db.String(100))
    conteudo_livro = db.Column(db.String(1000))
    notas_gerais_livro = db.Column(db.String(1000))
    outros_formatos_disponiveis_livro = db.Column(db.String(40))
    aquisicao_livro = db.Column(db.String(60))
    fonte_livro = db.Column(db.String(300))
    id_setor = db.Column(db.Integer, db.ForeignKey('livros.setor.id_setor'))
    id_local = db.Column(db.Integer, db.ForeignKey('livros.local.id_local'))
    id_assunto = db.Column(db.Integer, db.ForeignKey('livros.assunto.id_assunto'))

    # Relacionamentos N:N
    autores = db.relationship('LivroAutor', backref='livro', lazy='dynamic')
    executores = db.relationship('LivroExecutor', backref='livro', lazy='dynamic')
    editores = db.relationship('LivroEditor', backref='livro', lazy='dynamic')
    areas = db.relationship('LivroAreaGeografica', backref='livro', lazy='dynamic')

class LivroAutorTabela(db.Model):
    __tablename__ = 'autor'
    __table_args__ = {'schema': 'livros'}
    id_autor = db.Column(db.Integer, primary_key=True)
    nome_autor = db.Column(db.String(200))
    tipo_autor = db.Column(db.String(40))

class LivroExecutorTabela(db.Model):
    __tablename__ = 'executor'
    __table_args__ = {'schema': 'livros'}
    id_executor = db.Column(db.Integer, primary_key=True)
    nome_executor = db.Column(db.String(200))

class LivroEditorTabela(db.Model):
    __tablename__ = 'editor'
    __table_args__ = {'schema': 'livros'}
    id_editor = db.Column(db.Integer, primary_key=True)
    nome_editor = db.Column(db.String(200))

class LivroAreaGeograficaLivro(db.Model):
    __tablename__ = 'area_geografica'
    __table_args__ = {'schema': 'livros'}
    id_area_geografica = db.Column(db.Integer, primary_key=True)
    nome_area_geografica = db.Column(db.String(40))

class LivroAutor(db.Model):
    __tablename__ = 'livro_autor'
    __table_args__ = {'schema': 'livros'}
    id_livro_autor = db.Column(db.Integer, primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.livro.id_livro'))
    id_autor = db.Column(db.Integer, db.ForeignKey('livros.autor.id_autor'))
    autor = db.relationship('LivroAutorTabela', backref='livros_autores')

class LivroExecutor(db.Model):
    __tablename__ = 'livro_executor'
    __table_args__ = {'schema': 'livros'}
    id_livro_executor = db.Column(db.Integer, primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.livro.id_livro'))
    id_executor = db.Column(db.Integer, db.ForeignKey('livros.executor.id_executor'))
    executor = db.relationship('LivroExecutorTabela', backref='livros_executores')

class LivroEditor(db.Model):
    __tablename__ = 'livro_editor'
    __table_args__ = {'schema': 'livros'}
    id_livro_editor = db.Column(db.Integer, primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.livro.id_livro'))
    id_editor = db.Column(db.Integer, db.ForeignKey('livros.editor.id_editor'))
    editor = db.relationship('LivroEditorTabela', backref='livros_editores')

class LivroAreaGeografica(db.Model):
    __tablename__ = 'livro_area_geografica'
    __table_args__ = {'schema': 'livros'}
    id_livro_area_geografica = db.Column(db.Integer, primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.livro.id_livro'))
    id_area_geografica = db.Column(db.Integer, db.ForeignKey('livros.area_geografica.id_area_geografica'))
    area = db.relationship('LivroAreaGeograficaLivro', backref='livros_areas')

# ------------------------------------------------------------
# Schema mapas
# ------------------------------------------------------------
class MapaLocal(db.Model):
    __tablename__ = 'local'
    __table_args__ = {'schema': 'mapas'}
    id_local = db.Column(db.Integer, primary_key=True)
    nome_local = db.Column(db.String(40))
    mapas = db.relationship('Mapa', backref='local_obj', foreign_keys='Mapa.local_id')

class MapaAutorTabela(db.Model):
    __tablename__ = 'autor'
    __table_args__ = {'schema': 'mapas'}
    id_autor = db.Column(db.Integer, primary_key=True)
    nome_autor = db.Column(db.String(200))
    tipo_autor = db.Column(db.String(40))

class MapaExecutorTabela(db.Model):
    __tablename__ = 'executor'
    __table_args__ = {'schema': 'mapas'}
    id_executor = db.Column(db.Integer, primary_key=True)
    nome_executor = db.Column(db.String(200))

class MapaAreaGeograficaLivro(db.Model):
    __tablename__ = 'area_geografica'
    __table_args__ = {'schema': 'mapas'}
    id_area_geografica = db.Column(db.Integer, primary_key=True)
    nome_area_geografica = db.Column(db.String(40))

class Mapa(db.Model):
    __tablename__ = 'mapa'
    __table_args__ = {'schema': 'mapas'}
    id_mapa = db.Column(db.Integer, primary_key=True)
    n_chamada_mapa = db.Column(db.String(40))
    titulo_mapa = db.Column(db.String(500))
    escala_mapa = db.Column(db.String(40))
    articulacao_mapa = db.Column(db.String(40))
    projecao_mapa = db.Column(db.String(3))
    latitude_mapa = db.Column(db.String(40))
    longitude_mapa = db.Column(db.String(40))
    local_id = db.Column(db.Integer, db.ForeignKey('mapas.local.id_local'))
    data_mapa = db.Column(db.Date)
    colacao_mapa = db.Column(db.String(25))
    conteudo_mapa = db.Column(db.String(1000))
    nota_geral_mapa = db.Column(db.String(1000))
    aquisicao_mapa = db.Column(db.String(100))
    elaboracao_mapa = db.Column(db.String(300))
    assunto_mapa = db.Column(db.String(10000))
    fonte_mapa = db.Column(db.String(200))
    setor_mapa = db.Column(db.String(7))

    # Relacionamentos N:N
    autores = db.relationship('MapaAutor', backref='mapa', lazy='dynamic')
    executores = db.relationship('MapaExecutor', backref='mapa', lazy='dynamic')
    areas = db.relationship('MapaAreaGeografica', backref='mapa', lazy='dynamic')

class MapaAutor(db.Model):
    __tablename__ = 'mapa_autor'
    __table_args__ = {'schema': 'mapas'}
    id_mapa_autor = db.Column(db.Integer, primary_key=True)
    mapa_id = db.Column(db.Integer, db.ForeignKey('mapas.mapa.id_mapa'))
    autor_id = db.Column(db.Integer, db.ForeignKey('mapas.autor.id_autor'))
    autor = db.relationship('MapaAutorTabela', backref='mapas_autores')

class MapaExecutor(db.Model):
    __tablename__ = 'mapa_executor'
    __table_args__ = {'schema': 'mapas'}
    id_mapa_executor = db.Column(db.Integer, primary_key=True)
    mapa_id = db.Column(db.Integer, db.ForeignKey('mapas.mapa.id_mapa'))
    executor_id = db.Column(db.Integer, db.ForeignKey('mapas.executor.id_executor'))
    executor = db.relationship('MapaExecutorTabela', backref='mapas_executores')

class MapaAreaGeografica(db.Model):
    __tablename__ = 'mapa_area_geografica'
    __table_args__ = {'schema': 'mapas'}
    id_mapa_area_geografica = db.Column(db.Integer, primary_key=True)
    mapa_id = db.Column(db.Integer, db.ForeignKey('mapas.mapa.id_mapa'))
    area_geografica_id = db.Column(db.Integer, db.ForeignKey('mapas.area_geografica.id_area_geografica'))
    area = db.relationship('MapaAreaGeograficaLivro', backref='mapas_areas')

# ------------------------------------------------------------
# Schema projar
# ------------------------------------------------------------
class ProjarSetor(db.Model):
    __tablename__ = 'setor'
    __table_args__ = {'schema': 'projar'}
    id_setor = db.Column(db.Integer, primary_key=True)
    nome_setor = db.Column(db.String(150))
    projars = db.relationship('Projar', backref='setor_obj', foreign_keys='Projar.setor_id')

class ProjarLocal(db.Model):
    __tablename__ = 'local'
    __table_args__ = {'schema': 'projar'}
    id_local = db.Column(db.Integer, primary_key=True)
    nome_local = db.Column(db.String(150))
    projars = db.relationship('Projar', backref='local_obj', foreign_keys='Projar.local_id')

class ProjarAssunto(db.Model):
    __tablename__ = 'assunto'
    __table_args__ = {'schema': 'projar'}
    id_assunto = db.Column(db.Integer, primary_key=True)
    nome_assunto = db.Column(db.String(300))

class ProjarAutorTabela(db.Model):
    __tablename__ = 'autor'
    __table_args__ = {'schema': 'projar'}
    id_autor = db.Column(db.Integer, primary_key=True)
    nome_autor = db.Column(db.String(200))
    tipo_autor = db.Column(db.String(30))

class ProjarExecutorTabela(db.Model):
    __tablename__ = 'executor'
    __table_args__ = {'schema': 'projar'}
    id_executor = db.Column(db.Integer, primary_key=True)
    nome_executor = db.Column(db.String(200))
    tipo_executor = db.Column(db.String(40))

class ProjarAreaGeograficaLivro(db.Model):
    __tablename__ = 'area_geografica'
    __table_args__ = {'schema': 'projar'}
    id_area_geografica = db.Column(db.Integer, primary_key=True)
    nome_area_geografica = db.Column(db.String(150))

class Projar(db.Model):
    __tablename__ = 'projar'
    __table_args__ = {'schema': 'projar'}
    id_projar = db.Column(db.Integer, primary_key=True)
    n_chamada_projar = db.Column(db.String(10))
    titulo_projar = db.Column(db.String(500))
    local_id = db.Column(db.Integer, db.ForeignKey('projar.local.id_local'))
    data_projar = db.Column(db.Date)
    colacao_projar = db.Column(db.String(20))
    conteudo_projar = db.Column(db.String(1000))
    notas_gerais_projar = db.Column(db.String(1000))
    setor_id = db.Column(db.Integer, db.ForeignKey('projar.setor.id_setor'))
    fonte_projar = db.Column(db.String(200))
    escala_projar = db.Column(db.String(20))
    outras_versoes_projar = db.Column(db.String(96))

    # Relacionamentos N:N
    autores = db.relationship('ProjarAutor', backref='projar', lazy='dynamic')
    executores = db.relationship('ProjarExecutor', backref='projar', lazy='dynamic')
    areas = db.relationship('ProjarAreaGeografica', backref='projar', lazy='dynamic')
    assuntos = db.relationship('ProjarAssuntoRel', backref='projar', lazy='dynamic')

class ProjarAutor(db.Model):
    __tablename__ = 'projar_autor'
    __table_args__ = {'schema': 'projar'}
    id_projar_autor = db.Column(db.Integer, primary_key=True)
    projar_id = db.Column(db.Integer, db.ForeignKey('projar.projar.id_projar'))
    autor_id = db.Column(db.Integer, db.ForeignKey('projar.autor.id_autor'))
    autor = db.relationship('ProjarAutorTabela', backref='projar_autores')

class ProjarExecutor(db.Model):
    __tablename__ = 'projar_executor'
    __table_args__ = {'schema': 'projar'}
    id_projar_executor = db.Column(db.Integer, primary_key=True)
    projar_id = db.Column(db.Integer, db.ForeignKey('projar.projar.id_projar'))
    executor_id = db.Column(db.Integer, db.ForeignKey('projar.executor.id_executor'))
    executor = db.relationship('ProjarExecutorTabela', backref='projar_executores')

class ProjarAreaGeografica(db.Model):
    __tablename__ = 'projar_area_geografica'
    __table_args__ = {'schema': 'projar'}
    id_projar_area_geografica = db.Column(db.Integer, primary_key=True)
    projar_id = db.Column(db.Integer, db.ForeignKey('projar.projar.id_projar'))
    area_geografica_id = db.Column(db.Integer, db.ForeignKey('projar.area_geografica.id_area_geografica'))
    area = db.relationship('ProjarAreaGeograficaLivro', backref='projar_areas')

class ProjarAssuntoRel(db.Model):
    __tablename__ = 'projar_assunto'
    __table_args__ = {'schema': 'projar'}
    id_projar_assunto = db.Column(db.Integer, primary_key=True)
    projar_id = db.Column(db.Integer, db.ForeignKey('projar.projar.id_projar'))
    assunto_id = db.Column(db.Integer, db.ForeignKey('projar.assunto.id_assunto'))
    assunto = db.relationship('ProjarAssunto', backref='projar_assuntos')

# ------------------------------------------------------------
# Schema projen
# ------------------------------------------------------------
class ProjenSetor(db.Model):
    __tablename__ = 'setor'
    __table_args__ = {'schema': 'projen'}
    id_setor = db.Column(db.Integer, primary_key=True)
    nome_setor = db.Column(db.String(150))
    projens = db.relationship('Projen', backref='setor_obj', foreign_keys='Projen.setor_id')

class ProjenLocal(db.Model):
    __tablename__ = 'local'
    __table_args__ = {'schema': 'projen'}
    id_local = db.Column(db.Integer, primary_key=True)
    nome_local = db.Column(db.String(150))
    projens = db.relationship('Projen', backref='local_obj', foreign_keys='Projen.local_id')

class ProjenAssunto(db.Model):
    __tablename__ = 'assunto'
    __table_args__ = {'schema': 'projen'}
    id_assunto = db.Column(db.Integer, primary_key=True)
    nome_assunto = db.Column(db.String(300))

class ProjenAutorTabela(db.Model):
    __tablename__ = 'autor'
    __table_args__ = {'schema': 'projen'}
    id_autor = db.Column(db.Integer, primary_key=True)
    nome_autor = db.Column(db.String(200))
    tipo_autor = db.Column(db.String(12))

class ProjenExecutorTabela(db.Model):
    __tablename__ = 'executor'
    __table_args__ = {'schema': 'projen'}
    id_executor = db.Column(db.Integer, primary_key=True)
    nome_executor = db.Column(db.String(200))

class ProjenAreaGeograficaLivro(db.Model):
    __tablename__ = 'area_geografica'
    __table_args__ = {'schema': 'projen'}
    id_area_geografica = db.Column(db.Integer, primary_key=True)
    nome_area_geografica = db.Column(db.String(150))

class Projen(db.Model):
    __tablename__ = 'projen'
    __table_args__ = {'schema': 'projen'}
    id_projen = db.Column(db.Integer, primary_key=True)
    n_chamada_projen = db.Column(db.String(10))
    titulo_projen = db.Column(db.String(500))
    local_id = db.Column(db.Integer, db.ForeignKey('projen.local.id_local'))
    data_projen = db.Column(db.Date)
    colacao_pag_projen = db.Column(db.String(20))
    colacao_volume_tomo_projen = db.Column(db.String(20))
    conteudo_projen = db.Column(db.String(1000))
    notas_gerais_projen = db.Column(db.String(500))
    setor_id = db.Column(db.Integer, db.ForeignKey('projen.setor.id_setor'))
    fonte_projen = db.Column(db.String(200))

    # Relacionamentos N:N
    autores = db.relationship('ProjenAutor', backref='projen', lazy='dynamic')
    executores = db.relationship('ProjenExecutor', backref='projen', lazy='dynamic')
    areas = db.relationship('ProjenAreaGeografica', backref='projen', lazy='dynamic')
    assuntos = db.relationship('ProjenAssuntoRel', backref='projen', lazy='dynamic')

class ProjenAutor(db.Model):
    __tablename__ = 'projen_autor'
    __table_args__ = {'schema': 'projen'}
    id_projen_autor = db.Column(db.Integer, primary_key=True)
    projen_id = db.Column(db.Integer, db.ForeignKey('projen.projen.id_projen'))
    autor_id = db.Column(db.Integer, db.ForeignKey('projen.autor.id_autor'))
    autor = db.relationship('ProjenAutorTabela', backref='projen_autores')

class ProjenExecutor(db.Model):
    __tablename__ = 'projen_executor'
    __table_args__ = {'schema': 'projen'}
    id_projen_executor = db.Column(db.Integer, primary_key=True)
    projen_id = db.Column(db.Integer, db.ForeignKey('projen.projen.id_projen'))
    executor_id = db.Column(db.Integer, db.ForeignKey('projen.executor.id_executor'))
    executor = db.relationship('ProjenExecutorTabela', backref='projen_executores')

class ProjenAreaGeografica(db.Model):
    __tablename__ = 'projen_area_geografica'
    __table_args__ = {'schema': 'projen'}
    id_projen_area_geografica = db.Column(db.Integer, primary_key=True)
    projen_id = db.Column(db.Integer, db.ForeignKey('projen.projen.id_projen'))
    area_geografica_id = db.Column(db.Integer, db.ForeignKey('projen.area_geografica.id_area_geografica'))
    area = db.relationship('ProjenAreaGeograficaLivro', backref='projen_areas')

class ProjenAssuntoRel(db.Model):
    __tablename__ = 'projen_assunto'
    __table_args__ = {'schema': 'projen'}
    id_projen_assunto = db.Column(db.Integer, primary_key=True)
    projen_id = db.Column(db.Integer, db.ForeignKey('projen.projen.id_projen'))
    assunto_id = db.Column(db.Integer, db.ForeignKey('projen.assunto.id_assunto'))
    assunto = db.relationship('ProjenAssunto', backref='projen_assuntos')