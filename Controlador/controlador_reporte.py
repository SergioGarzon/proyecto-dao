"""Reportes del sistema.

Cada reporte devuelve un dict con la misma forma, así una sola ventana puede mostrarlos a todos:
    titulo:   texto del encabezado
    resumen:  líneas de texto con los totales
    columnas: títulos de la tabla
    filas:    tuplas de la tabla
    grafico:  {"tipo": "barras_horizontales" | "barras_apiladas" | "lineas",
               "titulo", "etiquetas", "series": {nombre: [valores]}, "eje_x", "eje_y", "anotaciones" (opcional)}
"""
from datetime import date, timedelta

from Entidades.enums import MotivoMulta
from Entidades.estado_remito import Danado, Extraviado, Recibido
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import ConexionBD
from Persistencia.reporte_dao import ReporteDAO

DIAS_PERIODO_POR_DEFECTO = 180
RUTAS_EN_GRAFICO = 10
SOCIOS_CON_MAS_DEUDA = 5


def formatear_monto(monto):
    # 5300.0 -> "$5.300,00"
    return "$" + f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class ControladorReporte:

    # Texto del combo de la pantalla -> nombre del método que arma el reporte
    REPORTES = {
        "Movimiento de ejemplares entre sedes": "movimiento_entre_sedes",
        "Tasa de envíos exitosos e incidencias": "envios_e_incidencias",
        "Libros más pedidos entre sedes": "libros_mas_pedidos",
        "Préstamos vencidos y multas": "vencidos_y_multas",
    }

    def generar(self, nombre, desde=None, hasta=None, limite=10, hoy=None):
        if nombre not in self.REPORTES:
            raise ReglaNegocioError("Debe elegir un reporte de la lista.")
        desde, hasta = self.validar_periodo(desde, hasta, hoy)
        metodo = getattr(self, self.REPORTES[nombre])
        if nombre == "Libros más pedidos entre sedes":
            return metodo(desde, hasta, self._validar_limite(limite))
        if nombre == "Préstamos vencidos y multas":
            return metodo(desde, hasta, hoy or date.today())
        return metodo(desde, hasta)

    def validar_periodo(self, desde, hasta, hoy=None):
        """Acepta fechas AAAA-MM-DD (texto o date). Sin fechas, toma los últimos 6 meses."""
        hoy = hoy or date.today()
        hasta = self._leer_fecha(hasta, "Hasta") if hasta else hoy
        desde = self._leer_fecha(desde, "Desde") if desde else hasta - timedelta(days=DIAS_PERIODO_POR_DEFECTO)
        if desde > hasta:
            raise ReglaNegocioError("La fecha Desde no puede ser posterior a la fecha Hasta.")
        return desde, hasta

    # Reporte 1
    def movimiento_entre_sedes(self, desde, hasta):
        with ConexionBD().obtener_session() as session:
            dao = ReporteDAO(session)
            envios = dao.envios_por_ruta(desde, hasta)
            tiempos = {(origen, destino): horas for origen, destino, horas in dao.transito_promedio_por_ruta(desde, hasta)}

        filas = []
        for origen, destino, cantidad, recibidos in envios:
            horas = tiempos.get((origen, destino))
            filas.append((origen, destino, cantidad, recibidos, f"{horas:.1f}" if horas is not None else "-"))

        total_envios = sum(fila[2] for fila in filas)
        total_recibidos = sum(fila[3] for fila in filas)
        resumen = [f"Período: {self._periodo(desde, hasta)}",
                   f"Envíos: {total_envios} en {len(filas)} rutas. Recibidos: {total_recibidos}."]
        if tiempos:
            # Promedio general ponderado por la cantidad de recibidos de cada ruta
            pesos = {(fila[0], fila[1]): fila[3] for fila in filas}
            total_pesos = sum(pesos.get(ruta, 0) for ruta in tiempos)
            if total_pesos:
                promedio = sum(horas * pesos.get(ruta, 0) for ruta, horas in tiempos.items()) / total_pesos
                resumen.append(f"Tiempo promedio de tránsito: {promedio:.1f} h ({promedio / 24:.1f} días).")
            ruta_lenta, horas_lenta = max(tiempos.items(), key=lambda item: item[1])
            resumen.append(f"Ruta más lenta: {ruta_lenta[0]} → {ruta_lenta[1]} ({horas_lenta:.1f} h).")

        principales = filas[:RUTAS_EN_GRAFICO]
        return {
            "titulo": "Movimiento de ejemplares entre sedes",
            "resumen": resumen,
            "columnas": ("Sede origen", "Sede destino", "Envíos", "Recibidos", "Horas promedio"),
            "filas": filas,
            "grafico": {
                "tipo": "barras_horizontales",
                "titulo": f"Las {len(principales)} rutas con más envíos",
                "etiquetas": [f"{fila[0]} → {fila[1]}" for fila in principales],
                "series": {"Envíos": [fila[2] for fila in principales]},
                "anotaciones": [f"{fila[4]} h" for fila in principales],
                "eje_x": "Cantidad de envíos",
            },
        }

    # Reporte 2
    def envios_e_incidencias(self, desde, hasta):
        with ConexionBD().obtener_session() as session:
            datos = ReporteDAO(session).remitos_finalizados_por_sede(desde, hasta)

        estados = (Recibido.nombre, Danado.nombre, Extraviado.nombre)
        por_sede = {}
        for sede, estado, cantidad in datos:
            por_sede.setdefault(sede, dict.fromkeys(estados, 0))[estado] = cantidad

        filas = []
        for sede, conteo in por_sede.items():
            total = sum(conteo.values())
            filas.append((sede, total, conteo[Recibido.nombre], conteo[Danado.nombre], conteo[Extraviado.nombre],
                          f"{conteo[Recibido.nombre] / total * 100:.1f}%"))

        total = sum(fila[1] for fila in filas)
        exitosos = sum(fila[2] for fila in filas)
        incidencias = total - exitosos
        resumen = [f"Período: {self._periodo(desde, hasta)}"]
        if total:
            resumen += [f"Remitos finalizados: {total}. Exitosos: {exitosos} ({exitosos / total * 100:.1f}%).",
                        f"Incidencias: {incidencias} ({incidencias / total * 100:.1f}%): "
                        f"{sum(fila[3] for fila in filas)} dañados y {sum(fila[4] for fila in filas)} extraviados."]
        else:
            resumen.append("No hay remitos finalizados en el período.")

        def porcentajes(indice):
            return [fila[indice] / fila[1] * 100 for fila in filas]

        return {
            "titulo": "Tasa de envíos exitosos e incidencias",
            "resumen": resumen,
            "columnas": ("Sede origen", "Finalizados", "Recibidos", "Dañados", "Extraviados", "Éxito"),
            "filas": filas,
            "grafico": {
                "tipo": "barras_apiladas",
                "titulo": "Resultado de los envíos por sede de origen (%)",
                "etiquetas": [fila[0] for fila in filas],
                "series": {"Recibido": porcentajes(2), "Dañado": porcentajes(3), "Extraviado": porcentajes(4)},
                "eje_y": "% de remitos",
            },
        }

    # Reporte 3
    def libros_mas_pedidos(self, desde, hasta, limite=10):
        with ConexionBD().obtener_session() as session:
            datos = ReporteDAO(session).libros_mas_pedidos_intersedes(desde, hasta, limite)

        filas = [(posicion, titulo, autor, cantidad)
                 for posicion, (titulo, autor, cantidad) in enumerate(datos, start=1)]
        resumen = [f"Período: {self._periodo(desde, hasta)}"]
        if filas:
            resumen.append(f"El más pedido: \"{filas[0][1]}\" ({filas[0][3]} pedidos entre sedes).")
        else:
            resumen.append("No hubo préstamos interbibliotecarios en el período.")

        return {
            "titulo": f"Top {limite} de libros más pedidos entre sedes",
            "resumen": resumen,
            "columnas": ("Puesto", "Título", "Autor", "Pedidos"),
            "filas": filas,
            "grafico": {
                "tipo": "barras_horizontales",
                "titulo": "Pedidos en préstamos interbibliotecarios",
                "etiquetas": [fila[1] for fila in filas],
                "series": {"Pedidos": [fila[3] for fila in filas]},
                "eje_x": "Cantidad de pedidos",
            },
        }

    # Reporte 4
    def vencidos_y_multas(self, desde, hasta, hoy=None):
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            dao = ReporteDAO(session)
            multas = dao.multas_por_mes_y_motivo(desde, hasta)
            vencidos = dao.prestamos_vencidos(hoy)
            deudores = dao.socios_con_mas_deuda(SOCIOS_CON_MAS_DEUDA)

        motivos = list(MotivoMulta)
        por_mes = {}
        for mes, motivo, _, monto, pagado in multas:
            datos_mes = por_mes.setdefault(mes, {"montos": dict.fromkeys(motivos, 0.0), "pagado": 0.0})
            datos_mes["montos"][motivo] = monto
            datos_mes["pagado"] += pagado

        filas = []
        for mes, datos_mes in por_mes.items():
            total = sum(datos_mes["montos"].values())
            filas.append((self._mes(mes), *(formatear_monto(datos_mes["montos"][motivo]) for motivo in motivos),
                          formatear_monto(total), formatear_monto(datos_mes["pagado"]),
                          formatear_monto(total - datos_mes["pagado"])))

        total_generado = sum(sum(d["montos"].values()) for d in por_mes.values())
        total_pagado = sum(d["pagado"] for d in por_mes.values())
        resumen = [f"Período: {self._periodo(desde, hasta)}",
                   f"Multas generadas: {formatear_monto(total_generado)}. Cobrado: {formatear_monto(total_pagado)}. "
                   f"Pendiente: {formatear_monto(total_generado - total_pagado)}."]
        if vencidos:
            atraso = sum((hoy - vencimiento).days for _, _, vencimiento in vencidos) / len(vencidos)
            resumen.append(f"Préstamos vencidos hoy: {len(vencidos)}, con {atraso:.0f} días de atraso promedio.")
        else:
            resumen.append("No hay préstamos vencidos.")
        if deudores:
            resumen.append("Socios con más deuda: " + "; ".join(
                f"{nombre} ({legajo}) {formatear_monto(total)}" for legajo, nombre, total in deudores) + ".")

        meses = list(por_mes)
        return {
            "titulo": "Préstamos vencidos y multas acumuladas",
            "resumen": resumen,
            "columnas": ("Mes", *(motivo.value for motivo in motivos), "Total", "Cobrado", "Pendiente"),
            "filas": filas,
            "grafico": {
                "tipo": "lineas",
                "titulo": "Monto de multas generadas por mes",
                "etiquetas": [self._mes(mes) for mes in meses],
                "series": {motivo.value: [por_mes[mes]["montos"][motivo] for mes in meses] for motivo in motivos},
                "eje_y": "Monto ($)",
            },
        }

    # Auxiliares
    def _leer_fecha(self, valor, campo):
        if isinstance(valor, date):
            return valor
        try:
            return date.fromisoformat(str(valor).strip())
        except ValueError:
            raise ReglaNegocioError(f"La fecha {campo} debe tener el formato AAAA-MM-DD.")

    def _validar_limite(self, limite):
        try:
            limite = int(limite)
        except (TypeError, ValueError):
            raise ReglaNegocioError("El Top N debe ser un número.")
        if not 1 <= limite <= 50:
            raise ReglaNegocioError("El Top N debe estar entre 1 y 50.")
        return limite

    def _periodo(self, desde, hasta):
        return f"{desde.isoformat()} a {hasta.isoformat()}"

    def _mes(self, mes):
        # "2026-06" -> "06/2026"
        anio, numero = mes.split("-")
        return f"{numero}/{anio}"
