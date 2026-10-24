from src.app.nucleo.conexion import get_connection
from typing import Optional, List
from datetime import datetime, timedelta, timezone


def registrar_historial(reserva_id: int, estado_anterior: Optional[str], estado_nuevo: str,
                         cambiado_por: int, comentario: Optional[str], cambiado_en: Optional[str] = None, conn=None):
    c = conn or get_connection()
    should_close = conn is None
    try:
        cur = c.cursor()
        if cambiado_en is None:
            cambiado_en = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        cur.execute(
            "INSERT INTO HistorialReserva (reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario) VALUES (?, ?, ?, ?, ?, ?)",
            (reserva_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en, comentario),
        )
        c.commit() if should_close else None
        return cur.lastrowid
    finally:
        if should_close:
            c.close()


def obtener_historial_con_filtros(usuario: dict, reserva_id: Optional[int] = None,
                                   espacio_id: Optional[int] = None,
                                   estado: Optional[str] = None,
                                   desde: Optional[str] = None,
                                   hasta: Optional[str] = None, conn=None):
    c = conn or get_connection()
    should_close = conn is None
    try:
        cur = c.cursor()
        es_admin = usuario.get("rol") == "ADMINISTRADOR"
        usuario_id = usuario.get("id")
        
        # Para solicitante, nunca debe ver ajeno - incluso con filtros, debe restringirse a propias reservas
        if not es_admin:
            # Buscar reservas del usuario
            cur.execute("SELECT id FROM reservas WHERE usuario_id = ?", (usuario_id,))
            reservas_propias = set(r[0] for r in cur.fetchall())
            if not reservas_propias:
                return []
            # Si hay filtros de reserva_id que apuntan a ajenas, el solicitante no debe verlas
            if reserva_id is not None and reserva_id not in reservas_propias:
                return []
        
        query = """
            SELECT h.* FROM HistorialReserva h
            JOIN reservas r ON r.id = h.reserva_id
            WHERE 1=1
        """
        params = []
        
        if not es_admin:
            query += " AND r.usuario_id = ?"
            params.append(usuario_id)
        else:
            pass  # admin ve todo
        
        if reserva_id is not None:
            if not es_admin:
                # Ya verificamos arriba
                query += " AND h.reserva_id = ?"
                params.append(reserva_id)
            else:
                query += " AND h.reserva_id = ?"
                params.append(reserva_id)
        if espacio_id is not None:
            query += " AND r.espacio_id = ?"
            params.append(espacio_id)
        if estado is not None:
            query += " AND h.estado_nuevo = ?"
            params.append(estado)
        if desde:
            # desde fecha AAAA-MM-DD en hora de Bogotá, inclusiva - convertir a UTC para comparar
            # Bogotá es UTC-5 (aprox) - para fecha inicio del día en Bogotá, eso corresponde a inicio del día +5h en UTC? 
            # O más simplemente, para comparar con cambiado_en (UTC), debemos convertir el rango
            try:
                # Interpretar como inicio del día en Bogotá
                from zoneinfo import ZoneInfo
                tz_bogota = ZoneInfo("America/Bogota")
                desde_dt = datetime.strptime(desde, "%Y-%m-%d").replace(tzinfo=tz_bogota)
                desde_utc = desde_dt.astimezone(timezone.utc)
                query += " AND h.cambiado_en >= ?"
                params.append(desde_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
            except Exception:
                raise ValueError("Fecha inválida")
        if hasta:
            try:
                from zoneinfo import ZoneInfo
                tz_bogota = ZoneInfo("America/Bogota")
                hasta_dt = datetime.strptime(hasta, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=tz_bogota)
                hasta_utc = hasta_dt.astimezone(timezone.utc)
                query += " AND h.cambiado_en <= ?"
                params.append(hasta_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
            except Exception:
                raise ValueError("Fecha inválida")
        
        query += " ORDER BY h.cambiado_en DESC, h.id DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        result = []
        for row in rows:
            r = dict(row)
            # Asegurar formato UTC ISO 8601 con Z o +00:00
            cambiado_en = r.get("cambiado_en")
            if cambiado_en:
                # Si ya está en formato con Z o +00:00, mantenerlo; si es otro formato, intentar normalizar
                if 'T' in str(cambiado_en):
                    ce = str(cambiado_en)
                    if ce.endswith('Z'):
                        r["cambiado_en"] = ce
                    elif '+' in ce:
                        r["cambiado_en"] = ce
                    elif ce.count(':') >= 2:  # tiene tiempo sin zona
                        # asumir UTC
                        r["cambiado_en"] = ce.replace(' ', 'T') + 'Z' if 'T' not in ce else ce + 'Z'
                    else:
                        r["cambiado_en"] = ce
                else:
                    r["cambiado_en"] = cambiado_en
            result.append(r)
        return result
    finally:
        if should_close:
            c.close()
