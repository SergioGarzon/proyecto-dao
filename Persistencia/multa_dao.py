from Entidades.multa import Multa
from Persistencia.base_dao import BaseDAO


class MultaDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Multa)

    def listar_filtradas(self, pendientes=None, legajo_dni=None):
        # pendientes: True = sin pagar, False = pagadas, None = todas
        consulta = self.session.query(Multa)
        if pendientes is True:
            consulta = consulta.filter(Multa.fecha_pago.is_(None))
        elif pendientes is False:
            consulta = consulta.filter(Multa.fecha_pago.isnot(None))
        if legajo_dni is not None:
            consulta = consulta.filter(Multa.legajo_dni == legajo_dni)
        return consulta.order_by(Multa.fecha_generacion.desc(), Multa.id_multa.desc()).all()

    def pendientes_de_socio(self, legajo_dni):
        return self.listar_filtradas(pendientes=True, legajo_dni=legajo_dni)
