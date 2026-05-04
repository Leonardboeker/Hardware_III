# Agente 3 — Profundización técnica (España / Catalunya)

**Fecha de redacción:** 2026-05-04
**Ámbito:** especificaciones técnicas, normativa y procedimientos para tres métodos constructivos contrastados en el contexto regulatorio español y catalán: fábrica de ladrillo, impresión 3D en construcción y hormigón prefabricado.
**Idiomas:** castellano y catalán. Las citas a normas se reproducen en su versión oficial española siempre que existe.

---

## 1. Resumen ejecutivo

El marco normativo español aplicable a obra de edificación se articula en torno a tres pilares: el **Código Técnico de la Edificación (CTE)** —Real Decreto 314/2006 con sus modificaciones, vigente la versión consolidada de diciembre de 2019 con actualizaciones posteriores—, el **Código Estructural** aprobado por **Real Decreto 470/2021, de 29 de junio** (en vigor desde el 10 de noviembre de 2021, sustituye a la EHE-08 y la EAE) y el cuerpo de **normas UNE-EN** (Eurocódigos y normas armonizadas de producto) publicadas por **AENOR/UNE**. En Catalunya se superpone el **Decret 141/2012**, de 30 d'octubre, regulador de las condiciones mínimas de habitabilidad.

De los tres métodos analizados, dos están plenamente cubiertos por normativa específica (fábrica de ladrillo y hormigón prefabricado) y uno presenta un **vacío regulatorio explícito** (impresión 3D), tal como se documenta en la sección 6.

---

## 2. Tabla de restricciones técnicas por método

| Parámetro | Fábrica de ladrillo | Hormigón prefabricado | Impresión 3D |
|---|---|---|---|
| Norma estructural principal | CTE DB-SE-F (2019) + UNE-EN 1996-1-1:2011/A1:2013 (Eurocódigo 6) | RD 470/2021 Código Estructural + UNE-EN 13369:2024 | **Sin norma específica** (aplican CTE + UNE-EN ISO/ASTM 52900:2022 y 52939:2023 de manera supletoria) |
| Espesor mínimo de muro de carga | **115 mm** (DB-SE-F §5) | Variable por sistema; típicamente 80-200 mm en panel armado prefabricado | No regulado; los prototipos ejecutados (TOVA-IAAC, Be More 3D) emplean muros con cavidades de 200-400 mm |
| Esbeltez geométrica máxima | **hd/td ≤ 27** (DB-SE-F §5) | Definida proyecto a proyecto según UNE-EN 13369 §4.3 | Sin límite normado |
| Resistencia característica fk | Tabla 4.4 DB-SE-F: cálculo según K·fb^0,65·fm^0,25 con K=0,60 (macizo), 0,55 (perforado), 0,50 (aligerado), 0,40 (hueco) | fck ≥ 25 MPa habitual; clases C25/30 a C50/60 según Código Estructural | Sin valor característico homologado; ensayos caso por caso |
| Mortero/material de unión | UNE-EN 998-2:2018, clases CS I (0,4–2,5 MPa) a CS IV (≥ 6,0 MPa); designación M1 a M20 según resistencia | Hormigón estructural conforme UNE-EN 206 + Código Estructural, Anejo 14 (tolerancias) | Mezclas extrudibles base cemento, cal, yeso o tierra; sin norma de producto armonizada |
| Tolerancia plomada (desplome) | ± 2 cm por planta; ± 5 cm en altura total del edificio | Anejo 14 Código Estructural (más estricto que fábrica) | Tolerancias de capa: 1-3 mm habituales en boquilla, no normadas |
| Tolerancia planeidad | 5 mm en 1 m; 2 cm en 10 m | UNE-EN 13369 §4.3.1 Anexo D | No normada |
| Vida útil asignada (CTE / Código Estructural) | 50 años (edificios residenciales y administrativos) | 50 años; obras civiles especiales hasta 100 años (Código Estructural Tabla 5.1) | No asignada; los prototipos se documentan como demostradores |
| Resistencia al fuego típica (DB-SI) | EI 120 con LP 11,5 cm + enfoscado; EI 60 con LH-7 | REI 120 frecuente en panel ≥ 12 cm con recubrimiento ≥ 25 mm | Sin clasificación normalizada de muros impresos; ensayos puntuales |
| Densidad para cálculo de transporte | LH (hueco): 600-900 kg/m³; LP (perforado): 1.200-1.800 kg/m³; macizo: 1.800-2.200 kg/m³ | Hormigón normal: 2.400-2.500 kg/m³ | Mezclas tierra-cruda impresa (TOVA): aprox. 1.700-1.900 kg/m³; morteros impresos cementicios: 1.800-2.200 kg/m³ |
| Categoría de exposición | DB-HS1 + DB-SE-F §3.2 (clases MX1 a MX5 según humedad y heladas) | Código Estructural Art. 27: X0, XC1-4, XD1-3, XS1-3, XF1-4, XA1-3, XM1-3 | Pendiente de definir; cada prototipo se ensaya ad-hoc |
| Categoría de control en obra | I (autocontrol) o II (DB-SE-F §8) | Categoría 1, 2 o 3 según UNE-EN 13369 §6.3 | Sin esquema de control reconocido |

---

## 3. Inventario de normas UNE-EN y documentos CTE relevantes

### 3.1. Documentos Básicos del CTE (versión consolidada vigente)

- **DB-SE Seguridad Estructural** (texto consolidado con modificaciones hasta diciembre de 2019): bases generales aplicables a todas las estructuras de edificación, fija la vida útil nominal.
- **DB-SE-F Seguridad Estructural: Fábrica** (versión vigente con actualización publicada en diciembre de 2019). Capítulos 4 (resistencia), 5 (verificación: espesores, esbeltez, alturas) y 8 (control). PDF oficial en codigotecnico.org.
- **DB-SE-AE Acciones en la Edificación** (2009 con correcciones).
- **DB-SI Seguridad en caso de Incendio** (texto consolidado 2019): clasificación R / EI / REI; tablas para muros de fábrica en su Anejo F.
- **DB-HS Salubridad** (texto consolidado 2017-2019): HS1 protección frente a la humedad fija el grado de impermeabilidad de fachadas (tabla 2.5) y muros enterrados (tabla 2.1) en función de zona pluviométrica y exposición al viento.
- **DB-HE Ahorro de Energía** (actualización 2019, RD 732/2019). Define zonas climáticas; Catalunya combina **C1, C2, C3, D1, D2, D3 y E1** según altitud (Barcelona ciudad: C2; Lleida: D3; Girona: D2; alta montaña pirenaica: E1).

### 3.2. Eurocódigos en versión española (UNE-EN)

- **UNE-EN 1996-1-1:2011/A1:2013** — Eurocódigo 6: Proyecto de estructuras de fábrica. Reglas generales. Comité técnico CTN 140 de UNE.
- **UNE-EN 1996-1-2** — Estructuras de fábrica sometidas al fuego.
- **UNE-EN 1996-2:2011** — Diseño, selección de materiales y ejecución.
- **UNE-EN 1996-3** — Métodos simplificados para fábrica sin armar.
- **UNE-EN 1992-1-1** (Eurocódigo 2) — Proyecto de estructuras de hormigón. En España, su contenido sustantivo se ha trasladado al **Código Estructural (RD 470/2021)**.

### 3.3. Normas de producto y ejecución

- **UNE-EN 771-1:2011+A1:2016** — Especificaciones de piezas para fábrica. Parte 1: piezas de arcilla cocida. Define las clases **LD** (densidad aparente ≤ 1.000 kg/m³, fábricas revestidas) y **HD** (> 1.000 kg/m³, fábricas vistas o expuestas), y las categorías de resistencia **I** (probabilidad de no alcance < 5 %) y **II**.
- **UNE-EN 772-1, 772-3, 772-5, 772-7, 772-11, 772-13, 772-16, 772-19** — Métodos de ensayo de piezas para fábrica.
- **UNE-EN 998-2:2018** — Especificaciones de los morteros para albañilería. Parte 2: morteros para albañilería. Confirmada en 2023. Sustituye a UNE-EN 998-2:2012. Distingue morteros **diseñados** y **prescritos**, y clasifica por resistencia a compresión a 28 días (CS I a CS IV).
- **UNE-EN 13369:2024** — Reglas comunes para productos prefabricados de hormigón. Norma horizontal de la familia de prefabricados, base del marcado CE en sistema 2+. Comité CTN 127 con secretaría en ANDECE.
- **UNE-EN 206** — Hormigón. Especificación, prestaciones, producción y conformidad. Referencia obligada del Código Estructural.
- **UNE-EN 1090-2** — Ejecución de estructuras de acero (relevante para sistemas modulares mixtos prefabricados).

### 3.4. Marco regulatorio catalán

- **Decret 141/2012, de 30 d'octubre** (entrada en vigor 3 de noviembre de 2012), pel qual es regulen les condicions mínimes d'habitabilitat dels habitatges i la cèdula d'habitabilitat. Cuatro anejos: I obra nueva, II usado, III dotacional público, IV intervención en edificios existentes. Criterios de interpretación elaborados con COAC y Agència de l'Habitatge.
- **Plecs de Condicions Tècniques Generals** del COAC y del ITeC, integrados en la base **BEDEC** (banco de precios y pliegos), referencia habitual en proyecto y obra en Catalunya. Disponible en itec.cat/banc-preus-bedec/.
- Fichas constructivas BEDEC para envans i parets d'obra ceràmica, panells de formigó prefabricat i pericons prefabricats.

### 3.5. Normas internacionales sobre fabricación aditiva (relevantes por defecto a la impresión 3D)

- **UNE-EN ISO/ASTM 52900:2022** — Fabricación aditiva. Principios generales, fundamentos y vocabulario (versión española de ISO/ASTM 52900:2021).
- **UNE-EN ISO/ASTM 52910:2020** — Requisitos, pautas y recomendaciones para diseño con fabricación aditiva.
- **ISO/ASTM 52939:2023** — Fabricación aditiva para construcción. Principios de cualificación. Elementos estructurales y de infraestructura. **No transpuesta aún como UNE en España a la fecha de este informe.**

---

## 4. Fábrica de ladrillo — síntesis técnica

El cálculo y la ejecución de muros de fábrica en España siguen una doble vía: el **CTE DB-SE-F** (texto íntegramente nacional pero compatible con Eurocódigo) y la **UNE-EN 1996-1-1:2011/A1:2013** con su Anejo Nacional. Las restricciones geométricas básicas del DB-SE-F §5 son:

- Espesor mínimo de muro de carga: **115 mm**.
- Esbeltez geométrica máxima `hd/td ≤ 27` (siendo hd la altura de cálculo y td el espesor eficaz).
- Para muros arriostrados solo en cabeza y base (caso 1): `hd = h`. Si se arriostra mediante forjados de hormigón armado con entrega de al menos `2t/3` y 85 mm, y la excentricidad de compresión en cabeza es menor de `0,25·t` (caso 2): `hd = 0,75·h`.

La resistencia característica a compresión de la fábrica se obtiene de la tabla 4.4 del DB-SE-F o, en general, de la expresión `fk = K·fb^0,65·fm^0,25` (Anejo C), donde fb es la resistencia normalizada de la pieza, fm la del mortero y K vale 0,60 para piezas macizas, 0,55 para perforadas, 0,50 para aligeradas y 0,40 para huecas. Las **categorías de control en obra** son I (autocontrol con ensayos) y II.

**Productos:** las piezas siguen UNE-EN 771-1:2011+A1:2016 con clasificación LD/HD y categorías I/II por resistencia. El mortero, UNE-EN 998-2:2018 (CS I a CS IV; designación M1 a M20).

**Tolerancias de ejecución:** desplome ±2 cm por planta y ±5 cm sobre altura total; planeidad 5 mm/m y 2 cm/10 m; espesor de muro simple ±2,5 cm.

**DB-HS1 (humedad):** la hoja principal de fachada de fábrica debe ser perforada o maciza si no hay revestimiento exterior, o de bloque cerámico/hormigón/piedra natural ≥ 12 cm; el grado de impermeabilidad mínimo se obtiene de la tabla 2.5 según pluviometría y viento.

**DB-SI:** un muro de LP de 11,5 cm con enfoscado alcanza **EI 120**; un muro de LH-7 con revestimiento llega a **EI 60**.

**Densidades** para cálculo de cargas y transporte: LH ≈ 600-900 kg/m³; LP ≈ 1.200-1.800 kg/m³; ladrillo macizo ≈ 1.800-2.200 kg/m³.

**Procedimientos de ejecución:** los manuales de **Hispalyt** (Asociación Española de Fabricantes de Ladrillos y Tejas de Arcilla Cocida), elaborados con el IETcc-CSIC, son la referencia operativa del sector. Existen siete cuadernos sobre componentes, recepción, herramientas, fábricas de pequeño formato para revestir, fábricas de gran formato, fachadas con ladrillo cara vista y soluciones para cumplir el CTE.

---

## 5. Hormigón prefabricado — síntesis técnica

El **Real Decreto 470/2021, de 29 de junio**, aprueba el **Código Estructural**, en vigor desde el 10 de noviembre de 2021. Sustituye a la EHE-08 (RD 1247/2008) y a la EAE (RD 751/2011). Regula estructuras de hormigón, acero y mixtas, tanto en edificación como en obra civil, incluyendo prefabricados.

**Clases de exposición** (Art. 27 Código Estructural): X0 (interior seco), XC1-XC4 (carbonatación), XD1-XD3 (cloruros no marinos), XS1-XS3 (marinos), XF1-XF4 (heladicidad), XA1-XA3 (química), XM1-XM3 (abrasión). En Catalunya costera (Barcelona, Tarragona) la combinación habitual es XC4 + XS1 + XF1.

**Vida útil nominal:** 50 años en edificación residencial y administrativa; 100 años en obras singulares. Los recubrimientos mínimos se ajustan a clase de exposición y vida útil (Anejo correspondiente del Código Estructural y guía MITMA de abril de 2022).

**Norma horizontal de producto:** **UNE-EN 13369:2024** establece reglas comunes (geometría, propiedades del hormigón, durabilidad, evaluación y verificación de la constancia de prestaciones AVCP en sistema 2+, marcado CE). Sobre ella se apilan normas verticales para placas alveolares (UNE-EN 1168), elementos lineales (UNE-EN 13225), paneles de fachada (UNE-EN 14992), forjados nervados, cerramientos, etc.

**Tolerancias geométricas:** Anejo 14 del Código Estructural y §4.3 de UNE-EN 13369; significativamente más estrictas que en fábrica (planeidad típica < 5 mm en panel y plomada < L/500).

**Sistemas constructivos representativos en Catalunya:**
- **Hormipresa** (Pla de Santa Maria, Tarragona, 50 años de actividad). Sistema **Arctic Wall**, primer sistema industrializado de hormigón certificado **Passivhaus**, y **HybridWall** (panel de hormigón blanco + madera técnica estructural).
- **Prefabricats Planas**, **WES Panel**, **AM Prefabricadas**, **The Concrete Home (TCH)** y **Moodul** son referentes industriales catalanes/españoles con módulos en hormigón armado.

**Densidades de transporte:** hormigón normal 2.400-2.500 kg/m³; hormigón ligero 1.600-2.000 kg/m³.

**Procedimientos:** la UNE-EN 13369 exige Categoría 1, 2 o 3 de control (§6.3). El **CTN 127 de UNE**, con secretaría en **ANDECE** (Asociación Nacional de la Industria del Prefabricado de Hormigón), publica resúmenes anuales de avances normativos.

---

## 6. Impresión 3D — vacío regulatorio en España (sección dedicada)

**El hallazgo central de esta investigación es la ausencia de un Documento Básico del CTE, una norma UNE-EN específica de cálculo, o un Documento de Idoneidad Técnica nacional que cubra la impresión 3D como sistema constructivo estructural.** No existe una vía reglamentaria directa para considerar un muro impreso como muro de carga en un proyecto firmado bajo CTE. Los proyectos ejecutados en España (TOVA-IAAC, Be More 3D, demostradores 3DCONS) operan como **demostradores experimentales**, no como obra residencial entregada con licencia de primera ocupación bajo el régimen ordinario de CTE.

### 6.1. Normas aplicables por defecto (no específicas)

- **UNE-EN ISO/ASTM 52900:2022** — Vocabulario y principios generales de fabricación aditiva. Aplica a cualquier proceso aditivo, no solo construcción.
- **UNE-EN ISO/ASTM 52910:2020** — Recomendaciones de diseño para fabricación aditiva.
- **ISO/ASTM 52939:2023** — Principios de cualificación de elementos estructurales y de infraestructura mediante fabricación aditiva. **Pendiente de adopción como UNE.**
- **CTE DB-SE, DB-HS, DB-HE, DB-SI** aplican como obligación general, pero ninguna sección recoge soluciones impresas en 3D.
- **Marcado CE** debería tramitarse vía Evaluación Técnica Europea (ETE) puntual cuando no existe norma armonizada de producto.

### 6.2. Iniciativas y proyectos institucionales españoles

- **Proyecto 3DCONS** (CDTI, programa estratégico CIEN, FEDER): consorcio liderado por **Vías y Construcciones (Grupo ACS)** con LafargeHolcim, Saint-Gobain Placo, CYPE, Geocisa, Proingesa, Atanga; colaboración del **IETcc-CSIC**, Fundación CIM-UPC, Universidad de Burgos, **CARTIF** y UPM. Tres líneas de trabajo: materiales para impresión 3D (yeso, cal, cemento y mixtos); sistemas robóticos; nuevos procesos integrando BIM, escaneo 3D y termografía. Hito clave: primer sistema mundial de impresión directa de fachada nueva sobre superficie existente.
- **Proyecto Print'n Build** y **CON3D** (CDTI, completado en marzo de 2015): proceso automatizado de generación de estructuras por fabricación aditiva.
- **TOVA — IAAC Valldaura Labs** (Barcelona, 2022): primer edificio impreso en España con tierra cruda local (mezcla de tierra, áloe, clara de huevo, enzimas). Superficie 9 m², 7 semanas de impresión con impresora Crane WASP. Fundación de geopolímero, cubierta de madera. Premio New European Bauhaus 2023, categoría circularidad. **No es vivienda con cédula de habitabilidad.**
- **Be More 3D — UPV Valencia**: primera vivienda completa impresa in situ con hormigón en España (24 m², campus de Vera). Promueve un programa de 7 viviendas en Cuenca para repoblamiento rural.

### 6.3. Posicionamiento institucional

No se ha localizado un informe técnico oficial publicado por el **CGATE** (Consejo General de la Arquitectura Técnica) ni por el **COAC** (Col·legi d'Arquitectes de Catalunya) que fije postura sobre la admisibilidad de la impresión 3D como sistema estructural en proyecto firmado. El IETcc-CSIC (Instituto Eduardo Torroja) participa en 3DCONS como agente de I+D, no como entidad de homologación.

### 6.4. Implicación práctica

Cualquier obra impresa en 3D que pretenda licenciarse hoy en España debe: (a) demostrar prestaciones equivalentes a las exigidas por el CTE mediante ensayos específicos sobre cada partida; (b) tramitar marcado CE vía ETE cuando proceda; (c) en estructura, verificar el cumplimiento del Código Estructural por equivalencia mediante ensayos de hormigón impreso (no asimilable directamente a hormigón vibrado UNE-EN 206). En la práctica, los demostradores se acogen a **ámbitos no residenciales** o a **programas piloto de innovación** (FEDER, Next Generation, regulación local específica) para sortear la indeterminación normativa.

---

## 7. Síntesis técnica comparada

Los tres métodos analizados se sitúan en estadios regulatorios muy distintos. La **fábrica de ladrillo** dispone del marco más maduro: el CTE DB-SE-F y la UNE-EN 1996 cubren cálculo, ejecución y control, mientras la UNE-EN 771-1 y la UNE-EN 998-2 garantizan trazabilidad de productos. Hispalyt y el IETcc-CSIC suministran manuales operativos contrastados, y las tolerancias y procedimientos están perfectamente documentados en los Plecs de Condicions del COAC y en BEDEC. En Catalunya, la combinación de DB-HE 2019 (zona C2 en Barcelona, D3 en Lleida) y Decret 141/2012 obliga, en obra nueva, a paramentos exteriores con fachada ventilada, cámara y aislamiento; el muro de fábrica simple ya no satisface por sí solo las transmitancias máximas y se complementa con SATE, trasdosados o doble hoja con cámara. Esto desplaza los **espesores totales de fachada** habituales a 30-40 cm.

El **hormigón prefabricado** tiene cobertura normativa completa desde 2021. El Código Estructural (RD 470/2021) sustituye y unifica EHE-08 y EAE; la UNE-EN 13369:2024 da reglas comunes a la familia entera de productos prefabricados, con marcado CE en sistema 2+ obligatorio. Los fabricantes catalanes (Hormipresa, Prefabricats Planas, WES Panel) ofrecen sistemas certificados que cumplen Passivhaus (Arctic Wall) e integran la doble lógica estructural y arquitectónica. El control en fábrica permite tolerancias mucho más estrictas que en obra húmeda. Las clases de exposición XC4 + XS1 + XF1 dominan la franja litoral catalana y exigen recubrimientos mayores y dosificaciones específicas según el Anejo del Código Estructural y la guía MITMA de abril de 2022.

La **impresión 3D**, en cambio, opera en un espacio normativo que solo contiene normas marco internacionales (UNE-EN ISO/ASTM 52900:2022, 52910:2020, ISO/ASTM 52939:2023 aún no UNE) y la obligación general del CTE. **No existe Documento Básico, no existe norma UNE-EN específica de cálculo de muros impresos, no existe Documento de Idoneidad Técnica nacional para sistemas impresos**, y los proyectos ejecutados (TOVA-IAAC, Be More 3D, 3DCONS) son demostradores y no obra residencial bajo régimen ordinario. La trayectoria institucional (CDTI, IETcc-CSIC, IAAC, UPV, ANDECE, AENOR) muestra un campo en construcción acelerada pero todavía pre-normativo. Esto tiene tres consecuencias prácticas para una propuesta hoy en España: (i) las verificaciones estructurales se asumen caso por caso mediante ensayos específicos; (ii) los plazos de licencia y la responsabilidad civil se complican; (iii) los proyectos viables se concentran en piezas no estructurales (mobiliario urbano, fachadas no portantes, prototipado) o en demostradores con cobertura de I+D.

En síntesis: para una intervención reproducible y con licencia ordinaria en Catalunya, fábrica y prefabricado son las opciones plenamente reglamentadas; la impresión 3D ofrece libertad geométrica pero exige un esfuerzo adicional muy importante de justificación técnica y administrativa, y depende de la maduración (previsiblemente en los próximos 3-5 años) de la familia ISO/ASTM 52939 y de su transposición como UNE, así como de la incorporación al CTE de soluciones reconocidas mediante Documentos Reconocidos del Registro General del CTE.

---

## 8. Fuentes y referencias

### CTE — codigotecnico.org
- Documentos CTE — codigotecnico.org/DocumentosCTE/DocumentosCTE.html
- DB-SE Seguridad Estructural — codigotecnico.org/DocumentosCTE/SeguridadEstructural.html
- DB-SE-F — codigotecnico.org/pdf/Documentos/SE/DBSE-F.pdf
- DB-HE — codigotecnico.org/pdf/Documentos/HE/DcmHE.pdf
- DB-HS — codigotecnico.org/pdf/Documentos/HS/DBHS.pdf
- Guía aplicación DB-HE 2019 — codigotecnico.org/pdf/GuiasyOtros/Guia_aplicacion_DBHE2019.pdf
- Registro General de Documentos Reconocidos — codigotecnico.org/RegistroCTE/DocumentosReconocidos.html

### Código Estructural — Ministerio de Transportes y Movilidad Sostenible
- Real Decreto 470/2021 (BOE) — boe.es/buscar/doc.php?id=BOE-A-2021-13681
- Página oficial — transportes.gob.es/ministerio/normativa-y-estudios-tecnicos/reglamentacion-vigente-sobre-seguridad-estructural/codigo-estructural
- Guía determinación recubrimientos abril 2022 — transportes.gob.es/recursos_mfom/comodin/recursos/guia_para_la_determinacion_de_recubrimientos_abril_2022.pdf

### Normas UNE / AENOR
- UNE-EN 1996-1-1:2011 — une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0046870
- UNE-EN 1996-2:2011 — tienda.aenor.com/p/norma-une-en-1996-2-2011-n0048628
- UNE-EN 771-1:2011+A1:2016 — une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0057657
- UNE-EN 998-2:2018 — une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0060256
- UNE-EN 13369:2024 — tienda.aenor.com/Paginas/Noticias/une-en-133692024,-reglas-comunes-para-prefabricados-de-hormigon.aspx
- UNE-EN ISO/ASTM 52900:2022 — une.org/encuentra-tu-norma/busca-tu-norma/norma?c=norma-une-en-iso-astm-52900-2022-n0069563
- CTN 136 Materiales cerámicos — revista.une.org/20/ctn-136-materiales-ceramicos-de-arcilla-cocida-para-la-const.html
- CTN 127 Prefabricados — revista.une.org/11/ctn-127-prefabricados-de-cemento-y-hormigon.html

### IETcc-CSIC, Hispalyt, ANDECE, ITeC, COAC
- Proyecto 3DCONS — ietcc.csic.es/projects/proyecto-3dcons-nuevos-procesos-de-construccion-mediante-impresion-3d/
- Print'n Build — ietcc.csic.es/projects/desarrollo-de-un-prototipo-para-impresion-3d-de-construcciones-a-gran-escala-printnbuild/
- Hispalyt publicaciones — hispalyt.es/es/documentacion-tecnica/publicaciones
- Manual de Ejecución Hispalyt — activatie.org/publicacion?451
- ANDECE biblioteca EHE-08 — andece.org/wp-content/uploads/2019/09/Biblioteca-de-consultas-EHE08.pdf
- ANDECE avances normativos 2023 — andece.org/resumen-de-los-avances-normativos-de-los-prefabricados-de-hormigon-en-2023/
- ITeC BEDEC — itec.cat/banc-preus-bedec/
- COAC Plecs de Condicions Tècniques Generals — arquitectes.cat/ca/plecs-de-condicions-tecniques-generals
- COAC zonas climáticas Catalunya — arquitectes.cat/ca/system/files/oct/he_1_zones_clim.pdf

### Decret 141/2012 — Catalunya
- Texto oficial Portal Jurídic — portaljuridic.gencat.cat/ca/document-del-pjur/?documentId=619728
- Criterios de interpretación — habitatge.gencat.cat/ca/ambits/cedules-habitabilitat/decret-141-2012/
- CIDO Diputació Barcelona — cido.diba.cat/legislacio/1628095

### Industria y proyectos de impresión 3D en España
- IAAC TOVA — iaac.net/projects/tova/ y iaac.net/project/3dpa-prototype-2022/
- Be More 3D UPV — upv.es/noticias-upv/noticia-10298-be-more-3d-es.html
- Hormipresa Arctic Wall — hormipresa.com/vivienda/en/arctic-wall/ y hormipresa.com/vivienda/hybridwall/
- Prefabricats Planas — prefabricatsplanas.com/es/
- Estrategia española impresión 3D construcción — imprimalia3d.com/noticias/2015/04/22/004660/repaso-estrategia-espa-ola-impresi-n-3d-construcci-n
- 3DModular normativas industrializada — 3dmodular.com/normativas-construccion-industrializada/
- Aceroplatea actividades normalización fabricación aditiva — aceroplatea.es/assets/uploads/documents/doc_6880877fbf283.pdf

### Resistencia al fuego y tolerancias
- VerificaciónCTE DB-SI — verificacioncte.es/blog/resistencia-fuego-db-si
- Documentación Enginyers BCN protección pasiva — documentacio.enginyersbcn.cat/storage/app/uploads/public/624/c76/9ad/624c769adfe6e984252162.pdf
- Anejo 14 Código Estructural — cdn.mitma.gob.es/portal-web-drupal/CPH/codigo_estructural/anejo_14._tolerancias_en_elementos_de_hormigon.pdf
- COAATG manual proceso ejecución fábrica — doc.coaatg.org/Doc/documentos/MANUAL%20DE%20PROCESO%20DE%20EJECUCI%C3%93N/FICHAS/3.2.1.doc

---

*Documento elaborado por el Agente 3 — Profundización técnica. Contenido íntegramente en castellano y catalán. Sin código.*
