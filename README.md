# Fase 2 – Mini-parser para lenguaje natural limitado

## Resumen Ejecutivo

Este proyecto implementa un parser descendente recursivo basado en gramática libre de contexto para analizar un subconjunto restringido del español que sigue el patrón Sujeto-Verbo-Objeto (SVO). El parser se compara con un modelo moderno de NLP basado en deep learning (spaCy), demostrando las ventajas y limitaciones de cada enfoque.

> **Nota:** Para información detallada sobre el diseño, análisis comparativo y conclusiones, consultar detalles en el informe enviado.

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

### Requisitos del Sistema

**Mínimos (Solo Parser):**
- Python 3.8 o superior
- Sin dependencias externas
- ~1 MB de espacio en disco

**Completos (Con Comparación spaCy):**
- Python 3.8 o superior
- pip (gestor de paquetes)
- spaCy 3.x
- Modelo es_core_news_sm (~13 MB)
- ~50 MB de espacio en disco total

### Paso 1: Verificar Python

Verifica si Python está instalado:

```bash
# Windows
python --version

# Linux/Mac
python3 --version
```

**Resultado esperado:** `Python 3.8.x` o superior.

Si no está instalado:
- **Windows/Mac:** Descarga desde https://www.python.org/downloads/
- **Linux:** Instala con el gestor de paquetes de tu sistema
  ```bash
  # Ubuntu/Debian
  sudo apt install python3
  
  # Fedora/RHEL
  sudo dnf install python3
  ```

**Nota importante para Windows:** Durante la instalación, marca la casilla **"Add Python to PATH"**.

### Paso 2: Verificar pip

Verifica si pip está disponible:

```bash
# Windows
python -m pip --version

# Linux/Mac
python3 -m pip --version
```

Si pip no está instalado:

```bash
# Windows
python -m ensurepip --upgrade

# Linux (Ubuntu/Debian)
sudo apt install python3-pip

# Linux (Fedora/RHEL)
sudo dnf install python3-pip

# Mac
python3 -m ensurepip --upgrade
```

### Paso 3: Instalar Dependencias (Opcional)

**Nota:** El parser principal (`mini_parser.py`) funciona sin dependencias externas. Solo necesitas instalar spaCy si quieres ejecutar `comparacion_parsers.py`.

#### Instalar spaCy

```bash
# Windows
python -m pip install spacy

# Linux/Mac
python3 -m pip install spacy

# Si tienes problemas de permisos, usa --user
python -m pip install --user spacy      # Windows
python3 -m pip install --user spacy    # Linux/Mac
```

#### Descargar Modelo en Español

```bash
# Windows
python -m spacy download es_core_news_sm

# Linux/Mac
python3 -m spacy download es_core_news_sm

# Con --user si es necesario
python -m spacy download --user es_core_news_sm      # Windows
python3 -m spacy download --user es_core_news_sm    # Linux/Mac
```

### Paso 4: Verificar Instalación

Ejecuta los tests para verificar que todo funciona:

```bash
# Windows
python test_parser.py

# Linux/Mac
python3 test_parser.py
```

**Resultado esperado:**
```
✓ TODOS LOS TESTS PASARON
Tests ejecutados: 24
Tests exitosos: 24
```

### Paso 5: Ejecutar el Proyecto

#### Parser Manual Básico (Sin dependencias)

```bash
# Windows
python mini_parser.py

# Linux/Mac
python3 mini_parser.py
```

#### Comparación con spaCy (Requiere spaCy instalado)

```bash
# Windows
python comparacion_parsers.py

# Linux/Mac
python3 comparacion_parsers.py
```

#### Visualizador de Árboles

```bash
# Windows
python visualizador_arbol.py

# Linux/Mac
python3 visualizador_arbol.py
```

#### Demo Interactiva

```bash
# Windows
python demo_interactiva.py

# Linux/Mac
python3 demo_interactiva.py
```

#### Tests Automatizados

```bash
# Windows
python test_parser.py

# Linux/Mac
python3 test_parser.py
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

## Solución de Problemas (en caso existan)

### "python no se reconoce como comando" (Windows)

**Problema:** Python no está en el PATH del sistema.

**Solución:**
1. Verifica que Python esté instalado: busca "Python" en el menú de inicio
2. Si está instalado pero no funciona en la terminal:
   - Reinstala Python desde https://www.python.org/downloads/
   - Durante la instalación, **marca la casilla "Add Python to PATH"**
3. Alternativa: Usa `py` en lugar de `python`:
   ```bash
   py --version
   py -m pip install spacy
   ```

### "ModuleNotFoundError: No module named 'spacy'"

**Problema:** spaCy no está instalado.

**Solución:**
```bash
# Windows
python -m pip install spacy

# Linux/Mac
python3 -m pip install spacy

# Si tienes problemas de permisos
python -m pip install --user spacy      # Windows
python3 -m pip install --user spacy    # Linux/Mac
```

### "Can't find model 'es_core_news_sm'"

**Problema:** El modelo de spaCy en español no está descargado.

**Solución:**
```bash
# Windows
python -m spacy download es_core_news_sm

# Linux/Mac
python3 -m spacy download es_core_news_sm

# Con --user si es necesario
python -m spacy download --user es_core_news_sm      # Windows
python3 -m spacy download --user es_core_news_sm    # Linux/Mac
```

### "Permission denied" (Linux/Mac)

**Problema:** No tienes permisos para instalar paquetes globalmente.

**Solución:** Usa la flag `--user` para instalar en el directorio del usuario:
```bash
python3 -m pip install --user spacy
python3 -m spacy download --user es_core_news_sm
```

### "pip no se reconoce como comando"

**Problema:** pip no está instalado o no está en PATH.

**Solución:**
```bash
# Windows
python -m ensurepip --upgrade

# Linux (Ubuntu/Debian)
sudo apt install python3-pip

# Linux (Fedora/RHEL)
sudo dnf install python3-pip
```