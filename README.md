# Fase 2 – Mini-parser para lenguaje natural limitado

## Resumen Ejecutivo

Este proyecto implementa un parser descendente recursivo basado en gramática libre de contexto para analizar un subconjunto restringido del español que sigue el patrón Sujeto-Verbo-Objeto (SVO). El parser se compara con un modelo moderno de NLP basado en deep learning (spaCy), demostrando las ventajas y limitaciones de cada enfoque.

> **Nota:** Para información detallada sobre el diseño, análisis comparativo y conclusiones, consulta el informe académico completo (PDF).

## Gramática Libre de Contexto

### Especificación Formal (BNF)

```bnf
<oración>     ::= <sujeto> <predicado>
<sujeto>      ::= <artículo> <sustantivo> 
                | <artículo> <adjetivo> <sustantivo>
                | <artículo> <sustantivo> <adjetivo>
<predicado>   ::= <verbo> <complemento>
<complemento> ::= <artículo> <sustantivo>
                | <artículo> <adjetivo> <sustantivo>
                | <artículo> <sustantivo> <adjetivo>

<artículo>    ::= "el" | "la" | "un" | "una" | "los" | "las"
<sustantivo>  ::= "perro" | "perros" | "gato" | "gatos" | "niño" | "niña" 
                | "niños" | "niñas" | "casa" | "casas" | "libro" | "libros"
                | "árbol" | "árboles" | "computadora" | "carro" | "hueso"
<adjetivo>    ::= "grande" | "grandes" | "pequeño" | "pequeña" | "rojo" 
                | "roja" | "azul" | "hermoso" | "viejo" | "nuevo" | "nueva"
<verbo>       ::= "come" | "comen" | "lee" | "leen" | "ve" | "ven" 
                | "quiere" | "quieren" | "tiene" | "busca" | "buscan"
```

### Características

- **Tipo:** Gramática Libre de Contexto (CFG)
- **Patrón:** Sujeto-Verbo-Objeto (SVO)
- **Vocabulario:** ~72 palabras (artículos, sustantivos, adjetivos, verbos)
- **Flexibilidad:** Permite adjetivos antes o después del sustantivo
- **Restricciones:** 
  - Máximo un adjetivo por sintagma nominal
  - Artículo obligatorio en sujeto y complemento
  - Sin concordancia de número/género (simplificación intencional)

## Resultados

### Parser Manual

| Métrica | Resultado |
|---------|-----------|
| Oraciones válidas | 4/12 (33.3%) |
| Tiempo promedio | < 0.0001 ms/oración |
| Errores léxicos detectados | 5/8 casos inválidos |
| Errores sintácticos detectados | 3/8 casos inválidos |

**Casos válidos:**
- "el perro come un hueso"
- "la niña lee el libro"
- "un gato grande ve la casa"
- "el niño pequeño quiere un libro rojo"

### Comparación con spaCy

| Aspecto | Parser Manual | spaCy |
|---------|---------------|-------|
| Oraciones SVO detectadas | 4/12 (33.3%) | 7/12 (58.3%) |
| Velocidad | < 0.0001 ms/oración | 9.27 ms/oración |
| Ratio de velocidad | **~200x más rápido** | - |
| Vocabulario | ~72 palabras | Ilimitado |
| Validación estricta | Excelente | Moderada |

## Instalación

### Requisitos

- Python 3.8 o superior
- (Opcional) spaCy para comparación: `pip install spacy && python -m spacy download es_core_news_sm`

### Ejecución

```bash
# Parser básico (sin dependencias)
python mini_parser.py

# Comparación con spaCy (requiere spaCy instalado)
python comparacion_parsers.py

# Tests automatizados
python test_parser.py

# Visualizador de árboles
python visualizador_arbol.py

# Demo interactiva
python demo_interactiva.py
```

## Archivos del Proyecto

```
.
├── mini_parser.py              # Parser descendente recursivo
├── comparacion_parsers.py      # Comparación con spaCy
├── test_parser.py             # Suite de pruebas automatizadas
├── visualizador_arbol.py      # Visualización de árboles de derivación
├── demo_interactiva.py        # Interfaz interactiva
└── README.md                  # Este documento
```

## Solución de Problemas Rápida

- **"ModuleNotFoundError: No module named 'spacy'":** 
  ```bash
  pip install spacy && python -m spacy download es_core_news_sm
  ```

- **"python no se reconoce como comando" (Windows):** 
  Verifica que Python esté en PATH o reinstala Python marcando "Add Python to PATH"

---

**Versión:** 1.0 | **Fecha:** Noviembre 2025
