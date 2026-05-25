# funciones.py

# Imports necesarios
import pandas as pd
import matplotlib.pyplot as plt

# Función de gráficos de tarta para facilitar el análisis visual de los datos
def pie_chart_con_otros(df, columna, umbral=0.05, figsize=(10,10), colores=None):
    """
    Crea un gráfico de tarta para la columna especificada de un DataFrame.
    Los valores que representen menos del umbral se agrupan en 'Otros'.
    Los porcentajes se muestran en negro y las etiquetas en blanco.
    
    Parámetros:
    - df: DataFrame de pandas
    - columna: nombre de la columna categórica
    - umbral: porcentaje mínimo para que se muestre individualmente (por defecto 5%)
    - figsize: tamaño de la figura
    - colores: lista de colores para las porciones
    """
    
    # Contar valores
    conteo = df[columna].value_counts(normalize=True)
    
    # Separar los que superan el umbral
    principales = conteo[conteo >= umbral]
    otros = conteo[conteo < umbral].sum()
    
    if otros > 0:
        principales['Otros'] = otros
    
    # Función para mostrar porcentaje
    def func(pct, allvals):
        return f"{pct:.1f}%" if pct > 0 else ''
    
    # Crear gráfico
    plt.figure(figsize=figsize)
    wedges, textos, autotextos = plt.pie(
        principales.values, 
        labels=principales.index, 
        autopct=lambda pct: func(pct, principales.values),
        startangle=90, 
        colors=colores,
        explode=[0.05 if v == principales.max() else 0 for v in principales.values],
        wedgeprops={'edgecolor':'white'},  # borde blanco opcional
        pctdistance=0.85,  # distancia del porcentaje al centro
        labeldistance=1.05  # distancia de la etiqueta al centro
    )
    
    # Colores de textos
    for t in textos:      # etiquetas (labels) en blanco
        t.set_color('white')
        t.set_fontsize(10)
    for t in autotextos:  # porcentajes en negro
        t.set_color('black')
        t.set_fontsize(10)
    
    plt.title(f'{columna}')
    plt.axis('equal')
    plt.show()


# Función de gráfico de barras utilizada para facilitar el análisis de los datos
def bar_plot_top_n_auto(df, columna, top_n=10, figsize=(12,8), color='#66b3ff', label_col=None, scale='auto'):
    """
    Crea un gráfico de barras mostrando los top N valores de una columna.
    Funciona automáticamente con columnas categóricas o numéricas.
    
    Parámetros:
    - df: DataFrame de pandas
    - columna: nombre de la columna a graficar
    - top_n: número de valores principales a mostrar
    - figsize: tamaño del gráfico
    - color: color de las barras
    - label_col: columna opcional para usar como etiquetas de las barras (para numéricas)
    - scale: 'auto', 'K', 'M' para mostrar numéricas en miles o millones
    """
    
    is_numeric = pd.api.types.is_numeric_dtype(df[columna])
    
    if is_numeric:
        # Numérica: top N
        top_df = df.nlargest(top_n, columna)
        labels = top_df[label_col] if label_col else top_df.index.astype(str)
        values = top_df[columna].copy()
        
        # Escalar valores si son muy grandes
        scale_factor = 1
        scale_label = ''
        if scale == 'auto':
            max_val = values.max()
            if max_val > 1e6:
                scale_factor = 1e6
                scale_label = ' (Millones €)'
            elif max_val > 1e3:
                scale_factor = 1e3
                scale_label = ' (Miles €)'
        elif scale == 'M':
            scale_factor = 1e6
            scale_label = ' (Millones €)'
        elif scale == 'K':
            scale_factor = 1e3
            scale_label = ' (Miles €)'
        
        values_scaled = values / scale_factor
    else:
        # Categórica: contar frecuencias
        conteo = df[columna].value_counts().head(top_n)
        labels = conteo.index
        values_scaled = conteo.values
    
    plt.figure(figsize=figsize)
    bars = plt.bar(labels, values_scaled, color=color)

    # Mostrar los valores encima de cada barra
    for bar, val in zip(bars, values_scaled):
        yval = bar.get_height()
        if is_numeric:
            # Formato europeo: punto como separador de miles, sin decimales
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01*max(values_scaled),
                     f'{int(round(val)):,}', ha='center', va='bottom', fontsize=10)
        else:
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5,
                     f'{int(val):,}', ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha='right')
    plt.ylabel(columna + (scale_label if is_numeric else ''))
    plt.title(f'Top {top_n} {columna}')
    plt.tight_layout()
    plt.show()
