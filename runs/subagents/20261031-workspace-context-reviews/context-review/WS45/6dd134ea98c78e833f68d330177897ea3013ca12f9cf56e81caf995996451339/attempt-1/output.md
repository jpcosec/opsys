## REFORMULACION

**Propósito:** verificar o completar en sldb la precondición de escritura de payload que fije el contrato WS12, distinguiendo before-image (`expected`/409), token publicado (`version`/`content_hash`) y precondición compartida aún no probada.

**Resultado:** inventario con path, símbolo y commit de la capacidad existente, más pruebas focalizadas por operación y escritor alcanzado.

**Repo dueño:** sldb. **Límites:** no mezcla UI, no fuerza CAS global ni algoritmo de hash, no depende de `source_mode` ni sustituye raw-source (WS20); reutiliza antes de implementar y solo completa lo faltante con tarea propia en sldb.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** contrato WS12 (`contratos/operaciones.md` y representación/operaciones/escritores), código existente en `src/sldb/api/documents/` y `src/sldb/cli/serve/`, pruebas actuales de `expected`, `version`/`content_hash` y comparación pública, y estado/commit del repo sldb. También las reglas comunes de alcance para store temporal real.

**Cambios previstos:** documento de inventario; pruebas focalizadas en `tests/`; código solo si al ejecutar falta capacidad, mediante tarea propia en sldb. No se prevén commits automáticos ni actas interrepo desde este nodo.

**Dependencias:** WS12 como productor del contrato; G_WRITE_CONTRACT por delta; G_SLDB_WRITE por recibo del delta concreto; G_PAYLOAD_PRECONDITION como salida propia; corpus/taller no aplica necesariamente a pruebas de API, que usan store temporal real.

**Validaciones futuras:** para cada operación y escritor alcanzado, comprobar que un estado previo obsoleto se rechaza sin cambios, uno vigente se aplica y el rechazo es observable por el llamante; verificar inventario contra contrato; repetir todo el contrato si hubo completado parcial.

## FUTURO

WS12 debe producir el contrato que fija representación, operaciones y escritores. El receptor humano P01 emite el acta G_SLDB_WRITE del delta concreto. La promoción y creación de tarea en sldb las decide el humano o el Executor por encargo. G_PAYLOAD_PRECONDITION quedará resuelto solo con evidencia verificable. WS21 permanece bloqueado por G_SOURCE y G_PAYLOAD_PRECONDITION hasta que corresponda.
