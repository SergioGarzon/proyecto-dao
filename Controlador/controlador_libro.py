
from Entidades.libro import Libro
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import ConexionBD
from Persistencia.libro_dao import LibroDAO


class ControladorLibro:

    def consultar_libros(self):
        with ConexionBD().obtener_session() as session:
            dao = LibroDAO(session)
            libros = dao.listar_ordenados()
            return [self._a_fila(libro) for libro in libros]

    def buscar_libros(self, texto):
        with ConexionBD().obtener_session() as session:
            dao = LibroDAO(session)
            libros = dao.buscar(texto)
            return [self._a_fila(libro) for libro in libros]

    def insertar_libro(self, isbn, titulo, autor, editorial, anio):
        isbn, titulo, autor, editorial, anio = self._validar_datos(
            isbn, titulo, autor, editorial, anio
        )

        with ConexionBD().obtener_session() as session:
            dao = LibroDAO(session)

            if dao.buscar_por_isbn(isbn) is not None:
                raise ReglaNegocioError("Ya existe un libro con ese ISBN.")

            libro = Libro(
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                editorial=editorial,
                anio_publicacion=anio
            )

            dao.guardar(libro)

    def obtener_libro(self, codigo):
        with ConexionBD().obtener_session() as session:
            libro = LibroDAO(session).obtener(int(codigo))

            if libro is None:
                raise ReglaNegocioError("No se encontró el libro.")

            return self._a_fila(libro)

    def consultar_disponibilidad(self, codigo):
        # Cuántos ejemplares disponibles tiene el libro en cada sede activa
        try:
            codigo = int(codigo)
        except (ValueError, TypeError):
            raise ReglaNegocioError("Debe seleccionar un libro válido.")

        with ConexionBD().obtener_session() as session:
            libro = LibroDAO(session).obtener(codigo)

            if libro is None:
                raise ReglaNegocioError("No se encontró el libro.")

            return [
                (sede.nombre, disponibles, total)
                for sede, disponibles, total in libro.disponibilidad_por_sede()
            ]

    def modificar_libro(self, codigo, isbn, titulo, autor, editorial, anio):
        isbn, titulo, autor, editorial, anio = self._validar_datos(
            isbn, titulo, autor, editorial, anio
        )

        with ConexionBD().obtener_session() as session:
            dao = LibroDAO(session)
            libro = dao.obtener(int(codigo))

            if libro is None:
                raise ReglaNegocioError("No se encontró el libro.")

            existente = dao.buscar_por_isbn(isbn)

            if existente is not None and existente.codigo_libro != libro.codigo_libro:
                raise ReglaNegocioError("El ISBN ya pertenece a otro libro.")

            libro.isbn = isbn
            libro.titulo = titulo
            libro.autor = autor
            libro.editorial = editorial
            libro.anio_publicacion = anio

    def _validar_datos(self, isbn, titulo, autor, editorial, anio):
        isbn = isbn.strip()
        titulo = titulo.strip()
        autor = autor.strip()
        editorial = editorial.strip()
        anio = str(anio).strip()

        if not isbn or not titulo or not autor:
            raise ReglaNegocioError(
                "ISBN, título y autor son obligatorios."
            )

        if len(isbn) > 20 or len(titulo) > 150 or len(autor) > 100:
            raise ReglaNegocioError("Uno de los campos supera el largo permitido.")

        if len(editorial) > 100:
            raise ReglaNegocioError("La editorial es demasiado larga.")

        if anio:
            try:
                anio = int(anio)
            except ValueError:
                raise ReglaNegocioError("El año debe ser un número.")

            if anio <= 0:
                raise ReglaNegocioError("El año debe ser positivo.")
        else:
            anio = None

        return isbn, titulo, autor, editorial, anio

    def _a_fila(self, libro):
        return (
            libro.codigo_libro,
            libro.isbn,
            libro.titulo,
            libro.autor,
            libro.editorial or "",
            libro.anio_publicacion if libro.anio_publicacion is not None else ""
        )
