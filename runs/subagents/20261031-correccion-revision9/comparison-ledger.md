# Ledger de comparación final, revisión 9 del plan workspace

Firma: Claude Opus 5.5, coordinador, pane `w3Y:p1`, 2026-10-31. Asumo la aceptación de todas las filas.

## Supersesión de la atribución anterior

Las disposiciones escritas en la consolidación dicen «Borrador redactado por un agente Claude Sonnet y revisado por el coordinador». Esa frase fue falsa cuando se escribió: yo ordené al agente ponerla y no revisé cada disposición, solo las listas de ambigüedades. El fallo es mío, no del agente. Esos archivos se conservan sin editar; para ellos rige este ledger. No se retrofecha nada.

## Qué leí, exactamente

Para cada uno de los 73 nodos leí el scope y la acceptance completos de dag.yaml, output.md completo y disposition.md completo si existía, comparando reformulación y dry-run con el contrato. No leí input.md completo, ni los campos depends_on, requires y output_scope de cada nodo salvo donde el output los citaba. 34 nodos cambiaron tras la primera pasada y volví a leer su output final. La comparación fue lectura mía, sin herramienta de muestreo. Las disposiciones de esta tanda las redacté yo; las 39 anteriores las redactó el agente y yo las leí.

## Defectos que encontró la comparación

- WS12: la duración del timeout no decía quién la fija, y un revisor la atribuyó a WS34. Corregido en dag.yaml; attempt-1 sin crédito.
- WS12: el destino protoátomo de WS25.2 no estaba asumido. Corregido.
- WS42: la validación de materializaciones no tenía productor si faltaba. Corregido.
- WS19.1 y WS37: dry-run sin cambios futuros. Repetidos con instrucción explícita; intentos previos sin crédito.
- WS19, WS25.1, WS26.1 y WS27.2: reformulaban la revisión en vez del encargo. Repetidos.

Estos defectos no aparecían en las listas de ambigüedades.

## Instrucción de la última tanda

34 nodos corrieron con la instrucción de `final-instruction.txt`, que amplía el SYSTEM de context_review.py para pedir ejecución hipotética del nodo. Ese archivo no se modificó: se reemplazó ARGV en memoria y el argv queda en cada manifest o receipt. WS12, WS19.1 y WS37 tienen intentos fuera del runner, con receipt propio. WS33 reutilizó un intento previo porque su input coincide. Los otros 39 usan la instrucción original y sus dry-run sí describen el trabajo según lo que leí.

## Correcciones tras el Tester, 2026-10-31

El Tester adversarial encontró tres defectos en lo que yo había aceptado. Las disposiciones y manifiestos no se reescriben; rige lo siguiente.

- WS22: la disposición clasifica como «no es ambigüedad» que «comunes» significa no modificar el lector, y que abrir pills y átomos no pide renderer. El contrato no lo resuelve: lo reclasifico como detalle de promoción abierto.
- WS13.1: la disposición atribuye a la aceptación «rutas de lectura contrato WS11», que está en output_scope. La ruta de apertura sin ID queda como detalle de promoción abierto, no como «no es ambigüedad».
- WS12 y WS37 attempt-2: manifest.json es copia del attempt-1, por lo que dice attempt 1 y apunta a su input. Para esos intentos vale receipt.json; input.md es idéntico.

El Tester no pudo verificar que comparé los 73 nodos ni recomputar las 73 filas: eso sigue siendo atestación mía y hashes verificables por root.

## Filas

| Nodo | Rol | Intento | input sha256 | output sha256 | disposition sha256 | Redactó disposición | Comparó y acepta | Fecha |
|---|---|---|---|---|---|---|---|---|
| ROOT | paquete | `attempt-1` | `c5aaff9d465b` | `772c2920f715` | `780876146777` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK01 | paquete | `attempt-1` | `bfd572f5bcb9` | `4ace9fef15ea` | `7b5add83f077` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK02 | paquete | `attempt-1` | `c959c5e03087` | `e0013ba91154` | `cd47d0481f5b` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK03 | paquete | `attempt-1` | `a19116153139` | `6917cba27ed4` | `99888776fd69` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK04 | paquete | `attempt-1` | `1a53e8c5e7c2` | `9c50f1c1908d` | `7f8aae2e5b4d` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK05 | paquete | `attempt-1` | `4189032376b6` | `698baebc9ddf` | `6a9d36c44946` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK06 | paquete | `attempt-1` | `2cd039f64078` | `112363b73159` | `1e5c317fe343` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK07 | paquete | `attempt-1` | `b020545f3c60` | `0c25f75c73eb` | `b278be574639` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| PK08 | paquete | `attempt-1` | `79062eb35828` | `554e79c90d95` | `0b183b8d011f` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS01 | delivery | `attempt-1` | `a6198b7f618f` | `575cf6c7ea8b` | `44fd899ef329` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS02 | delivery | `attempt-1` | `bcc8c8f56624` | `a0140dd47dd4` | `5d01cb44d7fb` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS03 | delivery | `attempt-1` | `cc1cf36ae00a` | `3bff9ddaf7a5` | `33b730be772e` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS04 | delivery | `attempt-1` | `f081be58d9fc` | `b0faf6df55d4` | `1270d04c8c1d` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS05 | delivery | `attempt-1` | `5725b504b36c` | `8b6adaeed604` | `34ce1eee68f1` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS06 | delivery | `attempt-1` | `23ed894e8fdd` | `5f56cef6ac5d` | `fa7190764232` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS07 | delivery | `attempt-1` | `0ef11a972e1f` | `feb20247f84c` | `f6d7187cb2e5` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS08 | delivery | `attempt-1` | `0a9ac8d60f47` | `debffb43342d` | `9c5b46be7b1f` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS09 | delivery | `attempt-1` | `80a4b9318f84` | `308dad31c295` | `fde014024cb9` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS10 | delivery | `attempt-1` | `2e0579620e35` | `8dbe0689c1d4` | `6247c8999694` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS11 | delivery | `attempt-1` | `a11aa22ba397` | `421130c772db` | `89d9a9f21b9b` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS12 | delivery | `attempt-2` | `bb6a2868ffb1` | `10e3788b3fe1` | `19160d358337` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS13 | aggregate | `attempt-1` | `3d32236a4e1b` | `f3a4a411c328` | `c1349c366723` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS13.1 | delivery | `attempt-1` | `7c6464a995c6` | `dacb5c8bb408` | `59caceee1364` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS13.2 | delivery | `attempt-1` | `4efd748bceb0` | `ed6fdefc3274` | `451bfa4b2864` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS13.3 | delivery | `attempt-1` | `da92d03c4e82` | `0762755d872e` | `9e0d95b24002` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS14 | delivery | `attempt-1` | `c40278dd8122` | `d2478951204e` | `634cf9beff2e` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS15 | aggregate | `attempt-1` | `add171863adf` | `c5054fd712f6` | `dc52de67f788` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS15.1 | delivery | `attempt-1` | `3a3237c3d267` | `bdbac1a135a2` | `eb2575c2a129` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS15.2 | delivery | `attempt-1` | `85d3a3feb97a` | `770a1f16b5e4` | `0a7ab8792df0` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS16 | delivery | `attempt-1` | `b69d8a3c008a` | `44814c07f217` | `51ede574959b` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS17 | delivery | `attempt-1` | `ff25e71599cd` | `c019290677ef` | `611d37f30cb6` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS18 | delivery | `attempt-1` | `be67fa9b84c4` | `e444fcf1fcbd` | `ce4a932c4281` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS19 | aggregate | `attempt-1` | `467436e7abcd` | `134f8fbc7f76` | `9fdcbf0cbbd6` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS19.1 | delivery | `attempt-1` | `731a0da19def` | `c19deffbcded` | `f5fd27159ebe` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS19.2 | delivery | `attempt-1` | `f53b343f25a4` | `4e599875d63f` | `9329779052f0` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS20 | delivery | `attempt-1` | `137e0949b280` | `ef1b17fe5769` | `83ffe0e10885` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS21 | delivery | `attempt-1` | `cf199d836027` | `ff0347a3ac2b` | `c819c21a4d41` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS22 | delivery | `attempt-1` | `d18f074b7e55` | `750b2bef5ad8` | `1b4f1545f125` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS23 | delivery | `attempt-1` | `360eccf15af7` | `2687d4967566` | `441ae25c807d` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS24 | delivery | `attempt-1` | `bf4ef16d66b5` | `e415993ffcd1` | `346e91d40441` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS25 | aggregate | `attempt-1` | `4ba06c4e6a0f` | `e0a5af134b42` | `b94add21ea47` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS25.1 | delivery | `attempt-1` | `a852ae61de64` | `e504d72e6f79` | `b3850e3a647a` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS25.2 | delivery | `attempt-1` | `6da3446aaf52` | `473276ce56d9` | `51790251a6ee` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS26 | aggregate | `attempt-1` | `d75c385db9e5` | `74adacb256e4` | `b7a0376a4a43` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS26.1 | delivery | `attempt-1` | `895446f37270` | `853dde107eb5` | `d6760388bb2b` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS26.2 | delivery | `attempt-1` | `0ff7ae18e2d9` | `3bb8296f682b` | `1d9ca920a70f` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS27 | aggregate | `attempt-1` | `e48374c6147d` | `6e1279be240d` | `8efdefb5dae8` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS27.1 | delivery | `attempt-1` | `1697ca0db4f4` | `7d7dce603347` | `72cde68714b8` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS27.2 | delivery | `attempt-1` | `27176daeeaf9` | `94b4e436231f` | `23a6395d8b2a` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS28 | delivery | `attempt-1` | `f85bf95493cc` | `537c391905f7` | `28a077a86b11` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS29 | delivery | `attempt-1` | `9aa87d2eabf7` | `c37a8e92ccc3` | `4416c02d34ed` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS30 | delivery | `attempt-1` | `019edfcd3bd6` | `d04630ef34ae` | `62bd7fbc22c7` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS31 | delivery | `attempt-1` | `4f80504cb14b` | `2b05c05022bb` | `02a683dfc2d3` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS32 | aggregate | `attempt-1` | `60c804b26019` | `d29468771d06` | `2ca1e86d6cf5` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS32.1 | delivery | `attempt-1` | `b88dfa4655e9` | `6c1f2bf79490` | `8d60dc897da2` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS32.2 | delivery | `attempt-1` | `b000cf1a12c1` | `f515732d89d2` | `44027c6a1c07` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS33 | aggregate | `attempt-1` | `1b03f9b321ff` | `4aa479e95544` | `6a28d4fadbca` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS33.1 | delivery | `attempt-1` | `dadf265d4cba` | `a84f8fa8add4` | `07bb51c67e79` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS33.2 | delivery | `attempt-1` | `3a9b09a0fa32` | `496f175b56d9` | `cf9182b3061c` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS34 | aggregate | `attempt-1` | `55b6e24348d4` | `e3f43d63ccc8` | `c8c743f9182b` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS34.1 | delivery | `attempt-1` | `442bba74d852` | `1b6be88b308c` | `48213222c2dd` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS34.2 | delivery | `attempt-1` | `81319b4927bc` | `79ae687e8cc0` | `58ec5ec68bd3` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS35 | delivery | `attempt-1` | `1ee9ece7e3b1` | `f7317d29632d` | `4efeec4f5054` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS36 | delivery | `attempt-1` | `9e1111fe7b32` | `2b851dbad39e` | `322312f377c3` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS37 | delivery | `attempt-2` | `3c322cc30808` | `cc1490defeb7` | `49b14d6b5c07` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS38 | delivery | `attempt-1` | `73622cfa01b3` | `52df21e43341` | `21d4ea18433b` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS39 | delivery | `attempt-1` | `eaaddc75ba42` | `99b537a79952` | `88124485e0de` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS40 | delivery | `attempt-1` | `c26ae332102d` | `5b62bb789cca` | `fbd74942729f` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS41 | delivery | `attempt-1` | `9d4c73d7d644` | `21a130f0e443` | `ea804a9ee40f` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS42 | delivery | `attempt-1` | `76e049bae76c` | `c0715b199f0c` | `0f7295795fe1` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS43 | delivery | `attempt-1` | `b95504ec7e04` | `fb2785ecb4d7` | `f3d4e98a6c77` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS44 | delivery | `attempt-1` | `a3a9ea212399` | `803d28941d6c` | `f650d4339484` | Claude Sonnet, agente preparatorio; atribución corregida aquí | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |
| WS45 | delivery | `attempt-1` | `32ee1060c471` | `f42df0ad98ab` | `75533c7a8842` | Claude Opus 5.5, coordinador | Claude Opus 5.5, coordinador: leído y comparado | 2026-10-31 |

## Adenda 2026-10-31, tras la revisión root de d9877e86

Firma: Claude Opus 5.5, coordinador. Lo anterior se conserva; donde difiera, rige esta adenda.

- **Conteo.** Este ledger dijo 39 y 34 revisiones. Según el recuento root sobre argv, fueron 40 con SYSTEM original y 33 con SYSTEM ampliado. La afirmación anterior era incorrecta.
- **Recibos.** Dije que los intentos manuales de WS12 y WS37 valían por su `receipt.json`. Eso sobrestimaba: omiten technical_failure, output_sha256, pid y otros campos, y hacían fallar `attempts()`. Quedan como evidencia histórica declarada, con recibo incompleto, sin rellenar y sin crédito operativo.
- **WS35.** La disposición `WS35/1ee9ece.../attempt-1/disposition.md` clasificó como «no es ambigüedad» qué hace la vista con mensajes sin intento, y yo la acepté al leerla. Fue extrapolación: el scope distingue mensajes por API de resultados vinculados por WS33.1. Clasificación vigente: decisión de presentación pendiente al promover. Productor: TaskDoc de WS35, que fija mostrar o excluir esos mensajes y su aceptación antes de ejecutar. No cambia contrato ni pide decisión de producto hoy.
- **WS33, WS13 y WS15.** Las acepté como fieles aunque su dry-run no recorría hijos. Ese juicio fue insuficiente y se reemplaza con los intentos nuevos.

