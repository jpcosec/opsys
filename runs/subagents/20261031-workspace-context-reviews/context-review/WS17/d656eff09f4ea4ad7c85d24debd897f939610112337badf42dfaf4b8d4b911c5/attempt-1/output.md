## REFORMULACION

WS17 debe producir plantillas Markdown authored de entradas e índices de navegación para el desk ejemplo, versionadas bajo `ejemplo/nav/` en el paquete del plan. El repo dueño es `deskops`. No es productor del corpus ni escribe repos reales: WS40 materializa estas fuentes bajo su root temporal. Límites: solo entradas/índices authored, sin copiar inventarios derivados ni duplicar el registry de deskops. La aceptación exige regenerar el corpus WS40 con las plantillas, recorrer links Markdown sin UI y comprobar que cada plantilla resuelve los roots/stores de los dos desks del manifiesto.

## AMBIGUEDADES

1. **No se define qué entradas/índices ni qué huecos de navegación cubrir.** Cita: «Escribir solo entradas/índices authored como plantillas versionadas bajo el paquete del plan» y «recorrer links Markdown sin UI». La aceptación solo comprueba que los links resuelven, no qué navegación debe existir; un conjunto mínimo pasaría. Obliga a inventar el contenido y la cobertura, salvo que se delegue explícitamente al TaskDoc.

2. **No se define cómo una plantilla referencia el root/store materializado.** Cita: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» y «el generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se fija si son rutas relativas al layout de WS40, marcadores sustituibles u otra convención. Obliga a inventar el mecanismo de vinculación; si no coincide con WS40, exigiría un cambio fuera de WS17.

## DRY-RUN

Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS17 y contratos vecinos WS11/WS40/WS30/WS43. Cambios previstos: crear plantillas Markdown bajo el `output_base` indicado, sin ejecutar. Dependencias: contrato de navegación WS11 y generador/manifiesto WS40 con los dos desks. Validaciones futuras: regenerar corpus con `ejemplo/nav/`, recorrer links sin UI, verificar resolución de roots/stores y ausencia de duplicación del registry; WS30 integra estas entradas.

## FUTURO

WS40 materializa las plantillas y emite el manifiesto con roots/stores. WS30 valida UF01 usando esas entradas. WS43 publica la navegación validada en el deskops real. La ubicación y las decisiones P09 quedan a cargo del humano y del contrato de navegación, no de este nodo.
