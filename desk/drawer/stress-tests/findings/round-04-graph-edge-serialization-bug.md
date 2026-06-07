# Round 04 — Graph: edge serialization bug

**Source:** ST-graph-deep

## CRITICAL: KG JSON edges are empty

Los 68 edges en `kg.json` existen como entradas de diccionario pero **todos tienen `role: None` y `target: None`**. El grafo serializado en KG JSON no puede ser recorrido — `graph neighbors` no encuentra edges porque los edges existen pero están vacíos.

## NetworkX snapshot tiene los datos correctos

El archivo `knowledge_graph.nx.json` tiene 82 links con `role: "references"`, `source_kind`, `confidence`, y `provenance` completos. **Los datos existen upstream** pero la serialización a KG JSON los pierde.

## Node count drift

- kg.json: 257 nodos
- nx.json: 260 nodos
Probablemente el NX snapshot es de un build anterior.

## Self-reflection no está en el pipeline

`find_missing_snapshot_targets` en `self_reflection.py` nunca se llama durante `graph build`. El módulo de self-reflection existe pero no está conectado.

## Code duplication

`find_missing_snapshot_targets` aparece tanto en `checks.py` como en `self_reflection.py` con la misma firma.

## Graph build performance

0.455 segundos. Rápido para el tamaño actual (257 nodos).

## __init__.py delgado

`deskops/graph/__init__.py` solo exporta `DocGraphNode` y `extract_doc_nodes` de los ~10 símbolos públicos del subpackage.
