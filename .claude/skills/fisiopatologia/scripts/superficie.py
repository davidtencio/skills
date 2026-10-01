"""Superficie de una proteína real (PDB/AlphaFold) cortada para mostrar el sitio de unión.

Dibuja los átomos como esferas (modelo de volumen) con proyección ortográfica y orden de
pintor. La cámara mira hacia el ligando desde fuera de la proteína y se eliminan los átomos
situados delante del ligando, de modo que el bolsillo queda a la vista como en un corte.
El resultado es un SVG autocontenido que se inserta como imagen.

Uso: python3 superficie.py archivo.pdb A DHT salida.svg
"""
import base64
import sys

import numpy as np

RADIOS = {"C": 1.7, "N": 1.55, "O": 1.52, "S": 1.8}


def leer_pdb(ruta, cadenas, ligando, cadena_ligando=None):
    """Átomos de proteína de `cadenas` (p. ej., "A" o "AB") y una copia del ligando.

    cadena_ligando: cadena de la copia del ligando que se muestra (por defecto, la primera de `cadenas`).
    """
    cadena_ligando = cadena_ligando or cadenas[0]
    proteina, lig = [], []
    for linea in open(ruta, encoding="utf-8", errors="ignore"):
        registro = linea[:6]
        if registro not in ("ATOM  ", "HETATM") or linea[16] not in (" ", "A"):
            continue
        xyz = [float(linea[30:38]), float(linea[38:46]), float(linea[46:54])]
        elemento = (linea[76:78].strip() or linea[12:14].strip())[:1].upper()
        if elemento == "H":
            continue
        residuo = (linea[21], linea[17:20], int(linea[22:26]), linea[12:16].strip())
        if registro == "ATOM  " and linea[21] in cadenas:
            proteina.append((xyz, elemento, residuo[:3], residuo[3]))
        elif registro == "HETATM" and linea[17:20].strip() == ligando and linea[21] == cadena_ligando:
            lig.append((xyz, elemento, residuo[:3], residuo[3]))
    if not proteina or (ligando and not lig):
        raise ValueError(f"No se encontraron las cadenas {cadenas} o el ligando {ligando} en {ruta}")
    return proteina, lig


def alinear(origen, destino, cadenas):
    """Rotación y traslación (Kabsch) que superpone los Cα de `origen` sobre los de `destino`."""
    def cas(ruta):
        return {(l[21], int(l[22:26])): [float(l[30:38]), float(l[38:46]), float(l[46:54])]
                for l in open(ruta, errors="ignore") if l.startswith("ATOM  ") and l[12:16] == " CA "
                and l[21] in cadenas and l[16] in (" ", "A")}
    a, b = cas(origen), cas(destino)
    comunes = sorted(set(a) & set(b))
    X, Y = np.array([a[k] for k in comunes]), np.array([b[k] for k in comunes])
    cx, cy = X.mean(0), Y.mean(0)
    U, _, Vt = np.linalg.svd((X - cx).T @ (Y - cy))
    d = np.sign(np.linalg.det(U @ Vt))
    R = U @ np.diag([1, 1, d]) @ Vt
    return lambda P: (np.asarray(P) - cx) @ R + cy


def _mezcla(c1, c2, t):
    a = np.array([int(c1[i:i + 2], 16) for i in (1, 3, 5)])
    b = np.array([int(c2[i:i + 2], 16) for i in (1, 3, 5)])
    r = (a * (1 - t) + b * t).round().astype(int)
    return "#" + "".join(f"{v:02X}" for v in r)


def superficie_corte(ruta_pdb, cadena="A", ligando="DHT", ancho=420, alto=320, mostrar_ligando=True,
                     color="#7FC8A9", color_bolsillo="#F3E3A6", color_ligando="#E69F00", corte=1.0, margen=0.06,
                     cadena_ligando=None, marco=None, transformar=None, color_cadena2=None, radio_vista=None,
                     colores_cadena=None):
    """Devuelve (svg, (px, py), marco): dibujo, centro del ligando en la imagen y marco de la vista.

    cadena: una o varias cadenas ("AB") cuando el sitio de unión está entre dos subunidades.
    marco: el marco devuelto por otra llamada, para dibujar otra estructura desde el mismo ángulo
    (junto con `transformar = alinear(esta, aquella, cadenas)`).
    color_cadena2: color para las cadenas distintas de la del ligando (ayuda a ver la interfaz).
    colores_cadena: {cadena: color} para colorear cada cadena (p. ej., proteína y ADN) por separado.
    radio_vista: si se indica (Å), acerca la vista al bolsillo mostrando solo los átomos a esa distancia
    del ligando en el plano de la imagen.
    """
    proteina, lig = leer_pdb(ruta_pdb, cadena, ligando, cadena_ligando)
    P = np.array([a[0] for a in proteina])
    L = np.array([a[0] for a in lig])
    if transformar:
        P, L = transformar(P), transformar(L)
    centro_lig = L.mean(0)
    if marco:
        vista, ex, ey = marco["vista"], marco["ex"], marco["ey"]
        centro_lig = marco.get("centro", centro_lig)
    else:
        vista = centro_lig - P.mean(0)
        vista /= np.linalg.norm(vista)
        # Ejes de pantalla: el eje mayor de la proteína proyectada en horizontal
        proy = P - np.outer(P @ vista, vista)
        _, _, ejes = np.linalg.svd(proy - proy.mean(0), full_matrices=False)
        ex = ejes[0] - (ejes[0] @ vista) * vista
        ex /= np.linalg.norm(ex)
        ey = np.cross(vista, ex)
    cadena_principal = (cadena_ligando or cadena[0])

    def pantalla(X):
        return np.stack([(X - centro_lig) @ ex, -((X - centro_lig) @ ey), (X - centro_lig) @ vista], axis=1)

    sp, sl = pantalla(P), pantalla(L)
    radios = np.array([RADIOS.get(a[1], 1.7) for a in proteina])
    distancia = np.min(np.linalg.norm(P[:, None, :] - L[None, :, :], axis=2), axis=1)
    bolsillo = {a[2] for a, d in zip(proteina, distancia) if d < 4.5}
    visibles = sp[:, 2] < corte  # se eliminan los átomos delante del ligando
    if radio_vista:
        visibles &= np.hypot(sp[:, 0], sp[:, 1]) < radio_vista
    xs, ys = sp[visibles, 0], sp[visibles, 1]
    minx, maxx, miny, maxy = xs.min() - 2, xs.max() + 2, ys.min() - 2, ys.max() + 2
    escala = min(ancho * (1 - 2 * margen) / (maxx - minx), alto * (1 - 2 * margen) / (maxy - miny))
    ox = ancho / 2 - escala * (minx + maxx) / 2
    oy = alto / 2 - escala * (miny + maxy) / 2

    zmin, zmax = sp[visibles, 2].min(), corte
    gradientes, circulos = {}, []

    def gradiente(base):
        if base not in gradientes:
            gid = f"g{len(gradientes)}"
            gradientes[base] = (f'<radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.75">'
                                f'<stop offset="0" stop-color="{_mezcla(base, "#FFFFFF", 0.45)}"/>'
                                f'<stop offset="0.7" stop-color="{base}"/>'
                                f'<stop offset="1" stop-color="{_mezcla(base, "#000000", 0.35)}"/></radialGradient>', gid)
        return gradientes[base][1]

    elementos = []
    for i in np.where(visibles)[0]:
        x, y, z = sp[i]
        profundidad = (z - zmin) / max(zmax - zmin, 1e-6)
        nivel = round(profundidad * 7) / 7
        propio = (colores_cadena or {}).get(proteina[i][2][0])
        base = color_bolsillo if proteina[i][2] in bolsillo else (propio or (
            color_cadena2 if color_cadena2 and proteina[i][2][0] != cadena_principal else color))
        if z > corte - 1.6:  # cara de corte: más clara y plana
            base = _mezcla(base, "#FFFFFF", 0.35)
        base = _mezcla(base, "#1E3B33", 0.55 * (1 - nivel))
        elementos.append((z, x, y, radios[i], base))
    if mostrar_ligando:
        for (x, y, z), atomo in zip(sl, lig):
            base = "#D9483B" if atomo[1] == "O" else color_ligando
            elementos.append((z + 50, x, y, RADIOS.get(atomo[1], 1.7) * 0.95, base))
    for z, x, y, r, base in sorted(elementos, key=lambda e: e[0]):
        circulos.append(f'<circle cx="{ox + escala * x:.1f}" cy="{oy + escala * y:.1f}" r="{escala * r:.1f}" '
                        f'fill="url(#{gradiente(base)})"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}">'
           f'<defs>{"".join(g for g, _ in gradientes.values())}</defs>{"".join(circulos)}</svg>')
    return svg, (ox, oy), {"vista": vista, "ex": ex, "ey": ey, "centro": centro_lig}


def superficie_complejo(ruta_pdb, grupos, ancho=420, alto=320, margen=0.06):
    """Complejo proteína-proteína (p. ej., antígeno y fragmento Fab) sin corte.

    grupos: [("C", "#7FC8A9"), ("AB", "#E9A6C0")] — cadenas y color de cada grupo. La vista se
    orienta para que la interfaz entre el primer y el segundo grupo quede de perfil (en horizontal).
    """
    atomos = []
    for cadenas, color in grupos:
        prot, _ = leer_pdb(ruta_pdb, cadenas, None)
        atomos += [(np.array(a[0]), RADIOS.get(a[1], 1.7), color) for a in prot]
    X = np.array([a[0] for a in atomos])
    c1 = np.mean([a[0] for a in atomos if a[2] == grupos[0][1]], axis=0)
    c2 = np.mean([a[0] for a in atomos if a[2] == grupos[1][1]], axis=0)
    ex = (c2 - c1) / np.linalg.norm(c2 - c1)
    _, _, ejes = np.linalg.svd(X - X.mean(0), full_matrices=False)
    vista = ejes[2] - (ejes[2] @ ex) * ex
    vista /= np.linalg.norm(vista)
    ey = np.cross(vista, ex)
    centro = X.mean(0)
    sp = np.stack([(X - centro) @ ex, -((X - centro) @ ey), (X - centro) @ vista], axis=1)
    minx, maxx, miny, maxy = sp[:, 0].min() - 2, sp[:, 0].max() + 2, sp[:, 1].min() - 2, sp[:, 1].max() + 2
    escala = min(ancho * (1 - 2 * margen) / (maxx - minx), alto * (1 - 2 * margen) / (maxy - miny))
    ox, oy = ancho / 2 - escala * (minx + maxx) / 2, alto / 2 - escala * (miny + maxy) / 2
    zmin, zmax = sp[:, 2].min(), sp[:, 2].max()
    gradientes, circulos = {}, []
    for i in np.argsort(sp[:, 2]):
        x, y, z = sp[i]
        nivel = round((z - zmin) / max(zmax - zmin, 1e-6) * 7) / 7
        base = _mezcla(atomos[i][2], "#1E3B33", 0.5 * (1 - nivel))
        if base not in gradientes:
            gid = f"c{len(gradientes)}"
            gradientes[base] = (f'<radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.75">'
                                f'<stop offset="0" stop-color="{_mezcla(base, "#FFFFFF", 0.45)}"/>'
                                f'<stop offset="0.7" stop-color="{base}"/>'
                                f'<stop offset="1" stop-color="{_mezcla(base, "#000000", 0.35)}"/></radialGradient>', gid)
        circulos.append(f'<circle cx="{ox + escala * x:.1f}" cy="{oy + escala * y:.1f}" r="{escala * atomos[i][1]:.1f}" '
                        f'fill="url(#{gradientes[base][1]})"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}">'
            f'<defs>{"".join(g for g, _ in gradientes.values())}</defs>{"".join(circulos)}</svg>')


def como_imagen(svg, x, y, w, h):
    datos = base64.b64encode(svg.encode()).decode()
    return (f'<image href="data:image/svg+xml;base64,{datos}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>')


if __name__ == "__main__":
    ruta, cadena, lig, salida = sys.argv[1:5]
    svg, centro, _ = superficie_corte(ruta, cadena, lig)
    open(salida, "w").write(svg)
    print(salida, "centro del ligando:", centro)
