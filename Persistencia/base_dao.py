class BaseDAO:
    """Operaciones comunes. La sesión la abre el controlador y la pasa al crear el DAO."""

    def __init__(self, session, modelo):
        self.session = session
        self.modelo = modelo

    def obtener(self, id_entidad):
        return self.session.get(self.modelo, id_entidad)

    def listar(self):
        return self.session.query(self.modelo).all()

    def guardar(self, entidad):
        self.session.add(entidad)
