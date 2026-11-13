import ast
import pandas as pd

def decodificar_nombre(nombre):
    if pd.isna(nombre):
        return nombre
    try:
        return str(nombre).encode().decode('unicode-escape')
    except Exception:
        return nombre

def procesar_tags(tags_str, df_tags_dict):
    if tags_str is None:
        return []
    
    try:
        if isinstance(tags_str, list):
            lista_tags = tags_str
        else:
            lista_tags = ast.literal_eval(str(tags_str))
            
        descripciones = []
        if isinstance(lista_tags, list):
            for t in lista_tags:
                if isinstance(t, dict):
                    tag_id = t.get('id')
                    if tag_id is not None:
                        desc = df_tags_dict.get(tag_id, f"Desconocido ({tag_id})")
                        descripciones.append(desc)
        return descripciones
    except Exception:
        return []


def extraer_posiciones(pos_str):
    inicio_x, inicio_y, fin_x, fin_y = None, None, None, None
    
    if pos_str is None:
        return pd.Series([inicio_x, inicio_y, fin_x, fin_y])
    
    try:
        # Si ya es una lista, la usamos directamente; si es un string, lo evaluamos
        if isinstance(pos_str, list):
            lista_pos = pos_str
        else:
            lista_pos = ast.literal_eval(str(pos_str))
            
        if isinstance(lista_pos, list):
            if len(lista_pos) >= 1 and isinstance(lista_pos[0], dict):
                inicio_x = lista_pos[0].get('x')
                inicio_y = lista_pos[0].get('y')
            if len(lista_pos) >= 2 and isinstance(lista_pos[1], dict):
                fin_x = lista_pos[1].get('x')
                fin_y = lista_pos[1].get('y')
    except Exception:
        pass
        
    return pd.Series([inicio_x, inicio_y, fin_x, fin_y])

def extraer_pais_nacimiento(area_str):
    if pd.isna(area_str):
        return ""
    try:
        if isinstance(area_str, str) and area_str.startswith('{'):
            d = ast.literal_eval(area_str)
            return d.get('name', '')
        return area_str
    except Exception:
        return ""

def extraer_nombre_area(area_val):
    if pd.isna(area_val):
        return ""
    # Si ya es un diccionario de Python
    if isinstance(area_val, dict):
        return str(area_val.get('name', ''))
    # Si es un string que parece un diccionario o JSON
    if isinstance(area_val, str):
        area_val_str = area_val.strip()
        if area_val_str.startswith('{') and area_val_str.endswith('}'):
            try:
                # Intentamos evaluar el diccionario
                d = ast.literal_eval(area_val_str)
                if isinstance(d, dict):
                    return str(d.get('name', ''))
            except Exception:
                pass
        return area_val_str
    return ""
