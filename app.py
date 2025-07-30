import streamlit as st
import pandas as pd
import numpy as np
import math

# Configuracion de la pagina
st.set_page_config(
    page_title="Analizador de Arboles de Decision",
    page_icon="🌳",
    layout="wide"
)

def calcular_entropia(datos, columna_clase):
    """
    Calcula la entropia de un conjunto de datos
    """
    if len(datos) == 0:
        return 0
    
    valores_clase = datos[columna_clase].value_counts()
    total = len(datos)
    entropia = 0
    
    for count in valores_clase:
        if count > 0:
            probabilidad = count / total
            entropia -= probabilidad * math.log2(probabilidad)
    
    return entropia

def calcular_ganancia(datos, atributo, columna_clase):
    """
    Calcula la ganancia de informacion de un atributo
    """
    entropia_total = calcular_entropia(datos, columna_clase)
    valores_atributo = datos[atributo].unique()
    total_instancias = len(datos)
    entropia_ponderada = 0
    
    # Mostrar detalles del calculo
    st.write(f"**Calculando ganancia para {atributo}:**")
    st.write(f"Entropia total: {entropia_total:.4f}")
    
    detalles = []
    for valor in valores_atributo:
        subset = datos[datos[atributo] == valor]
        peso = len(subset) / total_instancias
        entropia_subset = calcular_entropia(subset, columna_clase)
        entropia_ponderada += peso * entropia_subset
        
        detalles.append({
            'Valor': valor,
            'Instancias': len(subset),
            'Peso': f"{peso:.3f}",
            'Entropia': f"{entropia_subset:.4f}",
            'Contribucion': f"{peso * entropia_subset:.4f}"
        })
    
    df_detalles = pd.DataFrame(detalles)
    st.dataframe(df_detalles, use_container_width=True)
    
    ganancia = entropia_total - entropia_ponderada
    st.write(f"Entropia ponderada: {entropia_ponderada:.4f}")
    st.write(f"**Ganancia = {entropia_total:.4f} - {entropia_ponderada:.4f} = {ganancia:.4f}**")
    st.write("---")
    
    return ganancia

def generar_datos_aleatorios(config):
    """
    Genera datos aleatorios basado en configuracion
    """
    num_instancias = config['num_instancias']
    datos = {}
    
    for attr_config in config['atributos']:
        nombre = attr_config['nombre']
        
        if attr_config['tipo'] == 'Nominal':
            if attr_config['num_valores'] == 2:
                valores = ['Bajo', 'Normal']
            else:
                valores = ['Bajo', 'Normal', 'Alto']
            datos[nombre] = np.random.choice(valores, num_instancias)
            
        else:  # Numerico
            x1, x2 = attr_config['x1'], attr_config['x2']
            valores = []
            for _ in range(num_instancias):
                rand_val = np.random.uniform(x1-10, x2+10)
                if rand_val < x1:
                    valores.append(f"< {x1}")
                elif x1 <= rand_val <= x2:
                    valores.append(f"{x1} - {x2}")
                else:
                    valores.append(f"> {x2}")
            datos[nombre] = valores
    
    # Generar clase
    datos[config['nombre_clase']] = np.random.choice([0, 1], num_instancias)
    
    return pd.DataFrame(datos)

def crear_formulario_manual(config):
    """
    Crea formulario para entrada manual de datos
    """
    st.write("### ✏️ Entrada Manual de Datos")
    
    num_instancias = config['num_instancias']
    
    # Crear formulario
    with st.form("formulario_datos"):
        st.write(f"Ingresa los datos para {num_instancias} instancias:")
        
        # Inicializar diccionario para almacenar datos
        datos_formulario = {}
        
        # Inicializar listas para cada atributo
        for attr_config in config['atributos']:
            datos_formulario[attr_config['nombre']] = []
        datos_formulario[config['nombre_clase']] = []
        
        # Crear headers
        cols = st.columns(len(config['atributos']) + 1)
        for i, attr_config in enumerate(config['atributos']):
            cols[i].write(f"**{attr_config['nombre']}**")
        cols[-1].write(f"**{config['nombre_clase']}**")
        
        # Filas de datos
        for fila in range(num_instancias):
            cols = st.columns(len(config['atributos']) + 1)
            
            for i, attr_config in enumerate(config['atributos']):
                nombre_attr = attr_config['nombre']
                
                if attr_config['tipo'] == 'Nominal':
                    if attr_config['num_valores'] == 2:
                        opciones = ['Bajo', 'Normal']
                    else:
                        opciones = ['Bajo', 'Normal', 'Alto']
                    
                    valor = cols[i].selectbox(
                        f"Fila {fila+1}",
                        opciones,
                        key=f"{nombre_attr}_{fila}",
                        label_visibility="collapsed"
                    )
                    datos_formulario[nombre_attr].append(valor)
                    
                else:  # Numerico
                    x1, x2 = attr_config['x1'], attr_config['x2']
                    opciones = [f"< {x1}", f"{x1} - {x2}", f"> {x2}"]
                    
                    valor = cols[i].selectbox(
                        f"Fila {fila+1}",
                        opciones,
                        key=f"{nombre_attr}_{fila}",
                        label_visibility="collapsed"
                    )
                    datos_formulario[nombre_attr].append(valor)
            
            # Columna clase
            valor_clase = cols[-1].selectbox(
                f"Fila {fila+1}",
                [0, 1],
                format_func=lambda x: "No" if x == 0 else "Si",
                key=f"clase_{fila}",
                label_visibility="collapsed"
            )
            datos_formulario[config['nombre_clase']].append(valor_clase)
        
        # Botón de envío del formulario
        submitted = st.form_submit_button("💾 Guardar Datos")
        
        if submitted:
            return pd.DataFrame(datos_formulario)
    
    return None

def crear_csv_ejemplo(config):
    """
    Crea un CSV de ejemplo basado en la configuracion de atributos
    """
    datos_ejemplo = {}
    
    # Crear datos de ejemplo
    for attr_config in config['atributos']:
        nombre = attr_config['nombre']
        
        if attr_config['tipo'] == 'Nominal':
            if attr_config['num_valores'] == 2:
                datos_ejemplo[nombre] = ['Bajo', 'Normal', 'Bajo']
            else:
                datos_ejemplo[nombre] = ['Bajo', 'Normal', 'Alto']
        else:  # Numerico
            x1, x2 = attr_config['x1'], attr_config['x2']
            datos_ejemplo[nombre] = [f"< {x1}", f"{x1} - {x2}", f"> {x2}"]
    
    # Agregar clase
    datos_ejemplo[config['nombre_clase']] = [0, 1, 0]
    
    df_ejemplo = pd.DataFrame(datos_ejemplo)
    return df_ejemplo

def main():
    st.title("🌳 Analizador de Arboles de Decision")
    st.markdown("Calculo de Entropia General y Ganancia de Informacion")
    st.markdown("---")
    
    # Sidebar para configuracion
    st.sidebar.header("Configuracion de Datos")
    
    modo = st.sidebar.selectbox(
        "Selecciona el modo:",
        ["Carga desde Excel", "Generacion Manual"]
    )
    
    datos = None
    columna_clase = None
    
    if modo == "Carga desde Excel":
        st.subheader("📁 Carga desde Excel")
        archivo = st.file_uploader("Sube tu archivo Excel", type=['xlsx', 'xls'])
        
        if archivo is not None:
            try:
                datos = pd.read_excel(archivo)
                st.success("Archivo cargado exitosamente!")
                
                # Permitir seleccionar columna clase
                st.write("### Seleccionar Columna Clase")
                columna_clase = st.selectbox(
                    "Selecciona cual columna representa la clase:",
                    datos.columns.tolist()
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
    
    elif modo == "Generacion Manual":
        st.subheader("✏️ Configuracion Manual")
        
        # Configuracion basica
        num_atributos = st.sidebar.slider("Numero de atributos:", 3, 5, 3)
        num_instancias = st.sidebar.slider("Numero de instancias:", 5, 20, 10)
        
        # Nombre de la clase
        nombre_clase = st.sidebar.text_input("Nombre de la columna clase:", value="Clase")
        
        # Configurar cada atributo
        config_atributos = []
        
        st.sidebar.subheader("Configuracion de Atributos")
        
        for i in range(num_atributos):
            with st.sidebar.expander(f"Atributo {i+1}"):
                
                # Nombre del atributo
                nombre_attr = st.text_input(
                    f"Nombre del Atributo {i+1}:",
                    value=f"Atributo_{i+1}",
                    key=f"nombre_{i}"
                )
                
                tipo = st.selectbox(
                    f"Tipo:",
                    ["Nominal", "Numerico"],
                    key=f"tipo_{i}"
                )
                
                if tipo == "Nominal":
                    num_valores = st.selectbox(
                        "Numero de valores:",
                        [2, 3],
                        key=f"valores_{i}"
                    )
                    config_atributos.append({
                        'nombre': nombre_attr,
                        'tipo': 'Nominal',
                        'num_valores': num_valores
                    })
                else:
                    x1 = st.number_input(f"Valor X1:", value=25, key=f"x1_{i}")
                    x2 = st.number_input(f"Valor X2:", value=32, key=f"x2_{i}")
                    config_atributos.append({
                        'nombre': nombre_attr,
                        'tipo': 'Numerico',
                        'x1': x1,
                        'x2': x2
                    })
        
        # Tipo de llenado
        tipo_llenado = st.selectbox(
            "Tipo de llenado de datos:",
            ["Manual", "Aleatorio", "Importar Archivo"]
        )
        
        config = {
            'num_instancias': num_instancias,
            'atributos': config_atributos,
            'nombre_clase': nombre_clase
        }
        
        if tipo_llenado == "Aleatorio":
            if st.button("🎲 Generar Datos Aleatorios"):
                datos = generar_datos_aleatorios(config)
                st.session_state['datos_generados'] = datos
                columna_clase = nombre_clase
            
            if 'datos_generados' in st.session_state:
                datos = st.session_state['datos_generados']
                columna_clase = nombre_clase
        
        elif tipo_llenado == "Manual":
            datos_manual = crear_formulario_manual(config)
            if datos_manual is not None:
                datos = datos_manual
                st.session_state['datos_generados'] = datos
                columna_clase = nombre_clase
            elif 'datos_generados' in st.session_state:
                datos = st.session_state['datos_generados']
                columna_clase = nombre_clase
        
        elif tipo_llenado == "Importar Archivo":
            st.write("### 📁 Importar Datos desde Archivo")
            
            archivo_importado = st.file_uploader(
                "Sube tu archivo con los datos:",
                type=['csv', 'xlsx', 'xls'],
                help="El archivo debe tener las columnas que coincidan con los atributos configurados"
            )
            
            if archivo_importado is not None:
                try:
                    # Leer el archivo segun su extension
                    if archivo_importado.name.endswith('.csv'):
                        datos_importados = pd.read_csv(archivo_importado)
                        st.info("📄 Archivo CSV cargado")
                    else:
                        datos_importados = pd.read_excel(archivo_importado)
                        st.info("📊 Archivo Excel cargado")
                    
                    st.write("**Datos importados:**")
                    st.dataframe(datos_importados.head())
                    
                    # Verificar que las columnas coincidan
                    columnas_esperadas = [attr['nombre'] for attr in config_atributos] + [nombre_clase]
                    columnas_archivo = datos_importados.columns.tolist()
                    
                    st.write("**Verificacion de columnas:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Columnas esperadas:**")
                        for col in columnas_esperadas:
                            st.write(f"- {col}")
                    
                    with col2:
                        st.write("**Columnas en archivo:**")
                        for col in columnas_archivo:
                            if col in columnas_esperadas:
                                st.write(f"✅ {col}")
                            else:
                                st.write(f"❌ {col}")
                    
                    # Botones para descargar archivos de ejemplo
                    st.write("**¿No tienes un archivo?**")
                    df_ejemplo = crear_csv_ejemplo(config)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_ejemplo = df_ejemplo.to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar CSV de Ejemplo",
                            data=csv_ejemplo,
                            file_name="ejemplo_datos.csv",
                            mime="text/csv",
                            help="Descarga este archivo CSV como plantilla"
                        )
                    
                    with col2:
                        # Crear Excel de ejemplo
                        import io
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df_ejemplo.to_excel(writer, index=False, sheet_name='Datos')
                        
                        st.download_button(
                            label="📥 Descargar Excel de Ejemplo",
                            data=buffer.getvalue(),
                            file_name="ejemplo_datos.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Descarga este archivo Excel como plantilla"
                        )
                    
                    with st.expander("Ver estructura del archivo de ejemplo"):
                        st.dataframe(df_ejemplo)

                    # Verificar si todas las columnas necesarias están presentes
                    columnas_faltantes = set(columnas_esperadas) - set(columnas_archivo)
                    columnas_extra = set(columnas_archivo) - set(columnas_esperadas)
                    
                    if columnas_faltantes:
                        st.error(f"Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
                    elif columnas_extra:
                        st.warning(f"El archivo tiene columnas extra que seran ignoradas: {', '.join(columnas_extra)}")
                        # Seleccionar solo las columnas necesarias
                        datos = datos_importados[columnas_esperadas].copy()
                        st.session_state['datos_generados'] = datos
                        columna_clase = nombre_clase
                        st.success("¡Datos importados exitosamente!")
                    else:
                        # Todas las columnas coinciden perfectamente
                        datos = datos_importados.copy()
                        st.session_state['datos_generados'] = datos
                        columna_clase = nombre_clase
                        st.success("¡Datos importados exitosamente!")
                    
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")
                    st.info("Asegurate de que el archivo sea valido (CSV o Excel) con las columnas correctas")
    
    # Analisis principal
    if datos is not None and columna_clase is not None:
        st.subheader("📋 Tabla de Datos")
        st.dataframe(datos, use_container_width=True)
        
        # Obtener atributos
        atributos = [col for col in datos.columns if col != columna_clase]
        
        st.markdown("---")
        st.subheader("🧮 Calculos de Entropia y Ganancia")
        
        # Calcular entropia general
        entropia_general = calcular_entropia(datos, columna_clase)
        
        st.write("### 📊 Entropia General del Conjunto")
        valores_clase = datos[columna_clase].value_counts()
        total = len(datos)
        
        st.write("Distribucion de clases:")
        for clase, count in valores_clase.items():
            prob = count / total
            st.write(f"- {clase}: {count} instancias (probabilidad: {prob:.3f})")
        
        st.write(f"**Entropia General = {entropia_general:.4f}**")
        st.write("---")
        
        # Calcular ganancia para cada atributo
        st.write("### 📈 Ganancia de Informacion por Atributo")
        
        ganancias = {}
        for atributo in atributos:
            ganancia = calcular_ganancia(datos, atributo, columna_clase)
            ganancias[atributo] = ganancia
        
        # Determinar nodo raiz
        nodo_raiz = max(ganancias, key=ganancias.get)
        ganancia_maxima = ganancias[nodo_raiz]
        
        # Mostrar resultados finales
        st.subheader("🎯 Resultados Finales")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Entropia General", f"{entropia_general:.4f}")
        
        with col2:
            st.metric("Nodo Raiz", nodo_raiz)
        
        with col3:
            st.metric("Ganancia Maxima", f"{ganancia_maxima:.4f}")
        
        # Tabla resumen de ganancias
        st.write("### 📊 Resumen de Ganancias")
        
        df_resumen = pd.DataFrame([
            {"Atributo": attr, "Ganancia": f"{ganancia:.4f}", "Relevancia": "🥇 NODO RAIZ" if attr == nodo_raiz else ""}
            for attr, ganancia in sorted(ganancias.items(), key=lambda x: x[1], reverse=True)
        ])
        
        st.dataframe(df_resumen, use_container_width=True)
        
        # Explicacion final
        st.write("### 💡 Interpretacion")
        st.success(f"**El atributo '{nodo_raiz}' debe ser seleccionado como NODO RAIZ** porque tiene la mayor ganancia de informacion ({ganancia_maxima:.4f})")
        
        st.write("**Orden de relevancia para construccion del arbol:**")
        for i, (attr, ganancia) in enumerate(sorted(ganancias.items(), key=lambda x: x[1], reverse=True), 1):
            if i == 1:
                st.write(f"{i}. **{attr}** (Ganancia: {ganancia:.4f}) - 🌳 **NODO RAIZ**")
            else:
                st.write(f"{i}. **{attr}** (Ganancia: {ganancia:.4f})")

if __name__ == "__main__":
    main()
