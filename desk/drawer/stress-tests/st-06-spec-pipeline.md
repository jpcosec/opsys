# ST-06: Spec pipeline stress

**Basado en:** UC-06

## Script

```bash
# 1. Build spec
deskops spec build my-spec-id

# 2. Ver spec disponible
deskops spec list

# 3. Ver detalle del spec
deskops spec show my-spec-id

# 4. Iterar: cambiar spec, rebuild
# (editar spec manualmente)
deskops spec build my-spec-id

# 5. Spec que no existe
deskops spec build nonexistent-spec

# 6. Spec inválido (formato roto)
deskops spec build broken-spec
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `spec build` exitoso | ¿Imprime dónde quedó el artifact? ¿El path es absoluto o relativo? |
| `spec list` | ¿Los specs tienen descripción o solo ID? ¿Agrupa por tipo? |
| `spec show` | ¿Muestra los campos del spec? ¿Los templates? ¿O es críptico? |
| Re-build con cambios | ¿El artifact se regenera limpio? ¿O deja basura del build anterior? |
| Spec inexistente | ¿El error dice "spec 'nonexistent-spec' not found" o "KeyError"? |
| Spec inválido | ¿El error señala exactamente qué está mal (línea, campo)? |

## Modos de fracaso

- `spec build` no dice dónde escribió el artifact — el usuario tiene que adivinar
- Re-build es sucio: archivos viejos que ya no deberían existir siguen ahí
- No hay `spec build --watch` — el usuario tiene que rebuildear manualmente en cada cambio
- Specs rotos dan un traceback de Python en vez de "error en spec: campo X faltante"
- `spec list` y `spec build` usan nombres distintos para el mismo spec
- Build exitoso produce un artifact vacío o con contenido placeholder
