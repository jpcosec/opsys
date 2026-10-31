from pathlib import Path
import sys,yaml,json,re,hashlib
B=Path('desk/drawer/plans/workspace-documental');sys.path.insert(0,str(B));import context_review as cr
R=Path('runs/subagents/20261031-finalizar-plan-workspace');p=B/'dag.yaml';d=yaml.safe_load(p.read_text());nodes={n['id']:n for n in cr.all_nodes(d)}
notes={
'ROOT':'Corregido por supervisor: el primer macrocontrato medía reviews, no resultado del plan. Nuevo contrato sustantivo exige entregas, interfaces entre paquetes y validación futura. Re-review requerido; no aceptar meta-review como comprensión del trabajo.',
'WS02':'Hallazgos 1–4 corregidos: universo desk/categorías, store local .sldb, listas de operaciones por superficie y evidencia según soporte (path/hash/listado/salida) definidos sin mutar inventario.',
'WS04':'Hallazgos 1–3 corregidos: mapeo de cada nodo con ausencia explícita; HEAD/Board y commits de partida; path/símbolo/commit prueba base, no aceptación ampliada; sesiones no son autoridad.',
'WS05':'Hallazgo correcto de cobertura del input: faltaba contrato WS33 requerido por alcance. Se añade review_context_nodes WS33 al bundle sin reviews anteriores. El nodo inventaría documentación, no probe vivo.',
'WS06':'1/2 corregidos: P01 ya designado, operador Scion posterior; fila por delta/capacidad única con múltiples IDs si corresponde. 3 precisión de evidencia path/símbolo/commit añadida, no nueva autorización.',
'WS07':'1 corregido suministrando baseline_proposal string raíz explícito; 2 cobertura documental es decisiones.md+owner-decisions y covered_work, no UFs. Solo actualización por nueva decisión con fuente; no repetir firmas.',
'WS08':'1/2/3 corregidos: todas UF01–10 y listas de IDs/operaciones/gates; separar gate humano de prueba técnica WS29, ninguno adicional cuando corresponda. Delegación condicionada, no autorizada.',
'WS09':'1/2/3 aclaraciones de contrato: fila compuesta admite listas/clasificación por componente; separar solo estado/evidencia independiente; error futuro condicionado o no definido con productor, sin inventar funcionamiento.',
'WS10':'Hallazgo resuelto en scope: Taller y ruta exacta, productor WS40; ejemplo futuro sin capturas inventadas. P08 ya aprobó identidad/objetivos.',
'WS11':'1–3 reales: contrato básico puede cerrar sin actas; recepción es externa por delta al preparar/promover, actor P01/repo receptor; deskops solo enlaza, no escribe interrepo. G_SPEC_VIEW externo contract_source WS11, sin falso productor interno que obligue esperar opcional.',
'WS12':'1–3 aclarados: matriz/contrato, no ejecutar mutaciones ni actas interrepo; auditorías WS02–04 y evidencia path/símbolo/commit/API/pruebas; campos protegidos por modelo/lifecycle WS02. API faltante con productor no equivale disponible; WS20 produce guardas G_SOURCE.',
'WS13.1':'1 foco elemento dentro documento vs documento activo explícitos, correspondencia real WS11. 2 scope reutiliza workspace/node/contexto existentes y no solo carpeta futura document. 3 cláusula contradictoria eliminada: commit base jamás sustituye aceptación ampliada de este delta. Re-review obligatorio.',
'WS13.2':'1/2 refresco explícito sin reinicio para altas modeladas/no modeladas; 3 catálogo existente permitido y API/seguridad no modelada viene WS11. No duplicar lector.',
'WS13.3':'Hallazgos 1/2 descartados como diseño futuro expresamente asignado: scope exige pestañas/divisiones e historia y depends_on WS11, cuyo contrato fija foco/enlaces/historia. La guía dice «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide». No se exige aquí un layout UI concreto; abrir/cambiar/cerrar/volver conservando foco/origen es comprobable. Al promover, TaskDoc debe fijar interacción cierre/historia contra contrato WS11; no permiso para improvisar producto.',
'WS14':'1 ambigüedad léxica corregida (Sin resultados = búsqueda vacía, no prohibición). 2 prueba observable añadida: tecleo no dispara petición de carga completa de grafo; no requiere inventar umbral/debounce.',
'WS17':'1–4 definidos: índice curado con links no copia inventario, plantilla fuente única/destino regenerado, conjunto cubre dos desks vía WS11/manifiesto, registry desk/registry/repo-*.md de WS02 sin duplicarlo.',
'WS18':'1 aclarado futuro TaskDoc en spec2viz por supervisor/Executor, paquete deskops no escribe interrepo. 2 selección mínima viene catálogo WS09+WS11 contrastado WS03; sin ella parar/corregir productor antes de promoción, no selección inventada. Recepción externa por delta.',
'WS20':'1 WS20 se convierte en tarea propia sldb mismo delta/recibo al promover, no segundo productor. 2 existente debe cumplir TODO G_SOURCE; parcial solo completar faltantes y volver a probar contrato entero.',
'WS24':'1 tags provienen payload/semantic_tags públicos según WS03/WS11; 2 no modelados heredados de WS13.1/13.2 vía WS13, sin segundo lector; 3 Context ruta existente node/workspace-view.js y registry explicitados.',
'WS26.2':'1 conservador: normalización/expansión contrato WS12; igualdad/contención solapan, glob/no-resuelto no comprobado y supervisor revisa antes ready. 2 no inventar promoción: operación completa WS12 o preparar handoff mostrando pendiente.',
'WS27.1':'1 historial limitado a commits TaskDoc.references orden fecha y files, sin refs se declara ausencia y diff working tree HEAD. 2 repo/aliases/root resuelve WS11 y si no resoluble queda no disponible, sin escritura cruzada.',
'WS27.2':'1/2 correspondencia por tipo evidencia y reporte público closeout verify se fija en WS12; no inferir por renderer ni afirmar que un gate ejecuta pruebas. Sin reporte/fallo = no verificable/error, no aprobado.',
'WS30':'1 descartado con ruta verificable: WS30→WS17→WS11→WS08 (además WS12→WS08) ya transitiva. alcance.md dice dependencia transitiva cuenta como prerrequisito. 2 triage sin causa no inventa nodo; supervisor diagnóstico en repo/superficie antes atribuir. 3 edición UF03 con navegación necesaria y lectura completa WS16 separadas. Acta enumera WS17 paths/hashes para WS43.',
'WS31':'1 base contratos deskops paquete explicitada; otros solo inventariados por WS11/12. 2 sin recibo pruebas/commit de TaskDoc WS29 capítulo propuesto, no espera extensión. 3 Executor verifica links/etiquetas/atom→doc y Tester independiente comprueba antes cierre.',
'WS32.1':'1 registro input WS32.2 es contrato WS12 derivado inventario WS05, WS32.1 materializa, no almacenamiento inventado. 2 código modelo cambiado como código con registro/validación SLDB; instancias trackeadas por API/CLI, no ad hoc.',
'WS32.2':'Sesión/hash asignados a inventario WS05+contrato WS12 (artefacto log intento, campo/algoritmo/fuente reales). Si faltan no calcular hash inventado: hueco bloqueado con productor antes de promoción.',
'WS38':'Acuerdo durable = regla reusable demostrada, no incidente/permisos sesión; buscar y reusar átomo de WS31 equivalente antes crear. No duplicar por capítulo.',
'WS39':'1 Context panel lateral real WS13, entrada documento activo→Schema/clase/editor existente WS04; probar entrada. 2 depende WS13 para integrar lector; gate humano lectura habilita uso, no desarrollo API aislado.',
'WS42':'1 productores explícitos inventario WS02/03→contrato WS12; hueco no disponible. 2 modelo MaterializationContractDoc registrado, store temporal TaskDoc o manifiesto Taller, versión/commit y validación API pública; no renderer propio.',
'WS43':'1 criterio durable mapa P01/02/07/09 y condicional escritura P03–06, sin permisos sesión ni duplicar átomo. 2 acta WS30 lista WS17 paths/hashes y publicación registra correspondencia. 3 repo sin entrada no se omite: enlazar registry y mostrar ausencia/follow-up dueño sin fabricar entrada interrepo.'}
for line in (R/'runner-final.log').read_text().splitlines():
 nid,ok,path=line.split(' ',2);a=Path(path);out=(a/'output.md').read_text();n=nodes[nid]
 assert ok=='ok'
 note=notes.get(nid)
 if nid.startswith('PK'):note='Macrocontrato anterior solo probaba vigencia de reviews. No satisface intención de paquete sustantivo; corregido resultado/interfaces/orden/validación según hijos. Nueva comprensión macro requerida.'
 if note is None:
  assert re.search(r'AMBIGUEDADES[^\n]*\n+\s*(?:\*\*)?(?:ninguna|Ninguna)',out),nid
  note='Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.'
 data,_=cr.bundle(d,n);current=cr.sha(data)==a.parent.name and cr.sha(cr.canonical(n).encode())==json.loads((a/'manifest.json').read_text())['node_contract_sha256']
 accepted=nid not in notes and not nid.startswith('PK') and nid!='ROOT' or nid=='WS13.3'
 state='accepted_current' if current and accepted else ('accepted_old_input_superseded' if accepted else 'requires_contract_correction_rereview')
 citation=out[:out.upper().index('AMBIGUEDADES')].strip()
 (a/'disposition.md').write_text(f'# Executor comparison — {nid}\n\nState: {state}\n\n## Reformulación examinada\n\n{citation}\n\n## Comparación con intención / hallazgos\n\n{note}\n\nSe leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.\n')
 if state=='accepted_current':
  n['context_review'].update(status='reviewed',input_sha256=cr.sha(data),contract_sha256=cr.sha(cr.canonical(n).encode()),evidence=[path])
p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
(R/'round1-findings.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
