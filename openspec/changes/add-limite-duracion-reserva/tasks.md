## 1. Análisis
- [ ] 1.1 Leer PLAN_INGENIERIA.md y openspec/specs/solicitud-reservas/spec.md
- [ ] 1.2 Confirmar dónde se aplican las validaciones (service.py) y el orden 401, 422, 404, 409

## 2. Implementación
- [ ] 2.1 En src/app/reservas/politicas.py: duración individual > 4 h lanza error de validación (422); exactamente 4 h es válido
- [ ] 2.2 En src/app/reservas/repository.py: consulta de reservas PENDIENTE/APROBADA del mismo usuario y espacio que terminan en el inicio o empiezan en el fin de la nueva
- [ ] 2.3 En src/app/reservas/politicas.py: sumar la cadena contigua; si supera 4 h, el servicio responde 409
- [ ] 2.4 Integrar en crear_solicitud_reserva dentro de la misma transacción, respetando el orden de validaciones

## 3. Pruebas nuevas (una por escenario)
- [ ] 3.1 4 horas exactas permitida
- [ ] 3.2 4 horas y 1 minuto: 422
- [ ] 3.3 2 h + 3 h contiguas del mismo usuario: segunda 409
- [ ] 3.4 2 h + 2 h contiguas del mismo usuario permitida
- [ ] 3.5 Mismas horas de otro usuario permitida
- [ ] 3.6 Reservas del mismo usuario separadas por un hueco permitida
- [ ] 3.7 Reserva CANCELADA o RECHAZADA no cuenta

## 4. Verificación
- [ ] 4.1 Ejecutar TODA la suite de pruebas existente con pytest y confirmar que pasa
