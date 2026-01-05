"""
Script de prueba para verificar la conversión de precios
"""

def limpiar_precio_europeo(precio_str):
    """Limpia un precio en formato europeo y lo convierte a float"""
    # Remover símbolo € y espacios
    precio_limpio = precio_str.replace('€', '').replace(' ', '').strip()

    # Si tiene coma, es formato europeo sin duda
    if ',' in precio_limpio:
        # Remover puntos (miles) y cambiar coma por punto (decimal)
        precio_limpio = precio_limpio.replace('.', '').replace(',', '.')
    # Si no tiene coma pero tiene puntos
    elif '.' in precio_limpio:
        # Múltiples puntos = separadores de miles europeos
        if precio_limpio.count('.') > 1:
            precio_limpio = precio_limpio.replace('.', '')
        else:
            # Un solo punto: verificar si es separador de miles o decimal
            partes = precio_limpio.split('.')
            # Si hay exactamente 3 dígitos después del punto y al menos 1 antes, probablemente es separador de miles europeo
            if len(partes) == 2 and len(partes[1]) == 3 and len(partes[0]) >= 1:
                # Es formato europeo: 1.000, 10.000, etc.
                precio_limpio = precio_limpio.replace('.', '')
            # Sino, es decimal (formato US o decimal europeo con 1-2 dígitos)

    return float(precio_limpio)


# Casos de prueba
casos_prueba = [
    ('300', 300.0),
    ('300,00', 300.0),
    ('300.00', 300.0),
    ('3.000,00', 3000.0),
    ('3.000,00 €', 3000.0),
    ('1.234.567,89', 1234567.89),
    ('1.234.567,89 €', 1234567.89),
    ('50,5', 50.5),
    ('1.000', 1000.0),
    ('1.000.000', 1000000.0),
]

print("=" * 60)
print("PRUEBAS DE CONVERSIÓN DE PRECIOS")
print("=" * 60)

errores = 0
for entrada, esperado in casos_prueba:
    try:
        resultado = limpiar_precio_europeo(entrada)
        estado = "✓" if abs(resultado - esperado) < 0.01 else "✗"
        if abs(resultado - esperado) >= 0.01:
            errores += 1
            print(f"{estado} '{entrada}' -> {resultado} (esperado: {esperado}) ¡ERROR!")
        else:
            print(f"{estado} '{entrada}' -> {resultado}")
    except Exception as e:
        errores += 1
        print(f"✗ '{entrada}' -> ERROR: {e}")

print("=" * 60)
if errores == 0:
    print("✓ TODAS LAS PRUEBAS PASARON")
else:
    print(f"✗ {errores} PRUEBAS FALLARON")
print("=" * 60)

