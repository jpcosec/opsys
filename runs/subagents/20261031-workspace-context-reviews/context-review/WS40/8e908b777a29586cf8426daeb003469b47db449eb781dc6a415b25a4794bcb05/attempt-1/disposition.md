# Disposición WS40, ronda 7

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: WS02/WS03 son ancestros transitivos: WS40→WS11→WS09→WS07→WS06→WS03 y WS02. alcance.md: «Una dependencia transitiva cuenta como prerrequisito aunque no figure en depends_on directo».
2. error_reviewer: Autor, email y configuración git son formato del entorno de prueba. context-review-guide.md: «nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
3. error_reviewer: El scope ya declara el root del entorno (graph_ui:.tmp/... o tmp_path) e incluye el tercer repo en el mismo corpus; su limpieza es detalle de prueba del TaskDoc.
4. error_reviewer: La aceptación exige «entorno aislado» y el scope declara la ubicación graph_ui:.tmp/...; si hace falta .gitignore es archivo concreto del TaskDoc: context-review-guide.md «nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
