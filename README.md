# 🌳 Analizador de Arboles de Decision

## 📖 Descripcion de la Aplicacion

Esta aplicacion web desarrollada en Python con Streamlit permite realizar analisis estadistico de arboles de decision mediante el calculo de entropia general y ganancia de informacion. Su objetivo principal es determinar cual atributo debe ser seleccionado como nodo raiz en la construccion de un arbol de decision.

### ¿Que hace la aplicacion?

La aplicacion analiza conjuntos de datos para:

1. **Calcular la entropia general** del conjunto completo de datos
2. **Determinar la ganancia de informacion** de cada atributo individual
3. **Identificar el nodo raiz optimo** (atributo con mayor ganancia)
4. **Mostrar el orden de relevancia** de todos los atributos

### Modos de Operacion

#### 1. Carga desde Excel
- Permite subir archivos Excel (.xlsx, .xls) con datos existentes
- El usuario selecciona cual columna representa la clase
- Analiza automaticamente todos los atributos restantes

#### 2. Generacion Manual
Ofrece tres opciones para crear datos:

**Manual**: Formulario interactivo donde el usuario ingresa cada valor
**Aleatorio**: Genera datos automaticamente segun configuracion
**Importar Archivo**: Carga datos desde CSV o Excel con validacion

### Configuracion de Atributos

**Atributos Nominales:**
- 2 valores: Bajo, Normal
- 3 valores: Bajo, Normal, Alto

**Atributos Numericos:**
- Define valores X1 y X2
- Clasifica automaticamente como: < X1, X1-X2, > X2

**Clase:**
- Valores binarios: 0 (Negativo) o 1 (Positivo)

### Resultados del Analisis

La aplicacion muestra:
- Tabla completa de datos analizados
- Entropia general del conjunto
- Calculo detallado de ganancia por atributo
- Identificacion del nodo raiz recomendado
- Orden de relevancia para construccion del arbol

---

## 🔧 Funciones del Codigo

### \`calcular_entropia(datos, columna_clase)\`
**Proposito**: Calcula la entropia de un conjunto de datos basado en la distribucion de clases.
- Recibe un DataFrame y el nombre de la columna clase
- Aplica la formula: Entropia(S) = -Σ(pi * log2(pi))
- Retorna el valor de entropia como float

### \`calcular_ganancia(datos, atributo, columna_clase)\`
**Proposito**: Calcula la ganancia de informacion de un atributo especifico.
- Calcula la entropia total del conjunto
- Para cada valor del atributo, calcula la entropia del subconjunto
- Aplica la formula: Ganancia(S,A) = Entropia(S) - Σ((|Sv|/|S|) * Entropia(Sv))
- Muestra calculos detallados en pantalla
- Retorna la ganancia de informacion como float

### \`generar_datos_aleatorios(config)\`
**Proposito**: Genera un conjunto de datos aleatorio basado en configuracion.
- Recibe diccionario con configuracion de atributos
- Para atributos nominales: selecciona aleatoriamente entre valores permitidos
- Para atributos numericos: genera valores y los clasifica en rangos
- Para la clase: asigna aleatoriamente 0 o 1
- Retorna DataFrame con datos generados

### \`crear_formulario_manual(config)\`
**Proposito**: Crea interfaz interactiva para entrada manual de datos.
- Genera formulario dinamico basado en configuracion de atributos
- Crea selectboxes para cada celda de datos
- Incluye validacion y boton de envio
- Retorna DataFrame con datos ingresados o None si no se envio

### \`crear_csv_ejemplo(config)\`
**Proposito**: Genera archivo de ejemplo basado en configuracion de atributos.
- Crea DataFrame con 3 filas de datos de ejemplo
- Respeta la configuracion de tipos de atributos
- Sirve como plantilla para usuarios
- Retorna DataFrame de ejemplo

### \`main()\`
**Proposito**: Funcion principal que controla toda la aplicacion.
- Configura la interfaz de Streamlit
- Maneja la navegacion entre modos
- Coordina la carga y procesamiento de datos
- Ejecuta los calculos de entropia y ganancia
- Muestra los resultados finales

---

## 🚀 Instalacion y Configuracion Local

### 1. Crear Entorno Virtual

**En Windows:**
\`\`\`bash
python -m venv venv
venv\\Scripts\\activate
\`\`\`

**En macOS/Linux:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 2. Instalar Dependencias

Una vez activado el entorno virtual:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Ejecutar la Aplicacion

\`\`\`bash
streamlit run app.py
\`\`\`

### 4. Acceder a la Aplicacion

La aplicacion se abrira automaticamente en tu navegador en:
\`\`\`
http://localhost:8501
\`\`\`

### Dependencias Incluidas

- **streamlit**: Framework para la aplicacion web
- **pandas**: Manipulacion y analisis de datos
- **numpy**: Calculos matematicos y arrays
- **openpyxl**: Lectura de archivos Excel

### Desactivar Entorno Virtual

Cuando termines de usar la aplicacion:

\`\`\`bash
deactivate
\`\`\`

---

**Desarrollado para analisis estadistico de arboles de decision**
