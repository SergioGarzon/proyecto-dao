
from sqlalchemy import or_

from Entidades.libro import Libro
from Persistencia.base_dao import BaseDAO


class LibroDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Libro)

    def listar_ordenados(self):
        return (self.session.query(Libro)
                .order_by(Libro.titulo)
                .all())

    def buscar(self, texto):
        texto = texto.strip()

        if not texto:
            return self.listar_ordenados()

        return (self.session.query(Libro)
                .filter(or_(
                    Libro.titulo.ilike(f"%{texto}%"),
                    Libro.autor.ilike(f"%{texto}%"),
                    Libro.isbn == texto
                ))
                .order_by(Libro.titulo)
                .all())

    def buscar_por_isbn(self, isbn):
        return (self.session.query(Libro)
                .filter_by(isbn=isbn)
                .first())
