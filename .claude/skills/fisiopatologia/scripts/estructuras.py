"""Estructuras químicas 2D exactas con RDKit (pip install rdkit).

Las moléculas se definen por SMILES (p. ej., obtenidos de PubChem) y se verifican por
su fórmula molecular antes de dibujarlas.
"""
import base64

from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.rdMolDescriptors import CalcMolFormula


def molecula(smiles, formula_esperada=None):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"SMILES no válido: {smiles}")
    if formula_esperada and CalcMolFormula(mol) != formula_esperada:
        raise ValueError(f"Fórmula {CalcMolFormula(mol)} distinta de la esperada {formula_esperada}")
    rdDepictor.SetPreferCoordGen(True)
    rdDepictor.Compute2DCoords(mol)
    return mol


def formula(mol):
    """Fórmula molecular con subíndices Unicode (C₁₉H₃₀O₂)."""
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return CalcMolFormula(mol).translate(sub)


def estructura(mol, x, y, w, h, grosor=2.2, fuente=0.75, rotar=0, monocromo=None, estereo=False):
    """Devuelve un <image> SVG con la estructura dibujada en la caja (x, y, w, h).

    monocromo: color hexadecimal para todo el dibujo (p. ej., en láminas para proyectar);
    por defecto se usan los colores convencionales por elemento (O rojo, N azul, Cl verde).
    estereo: si es False (por defecto) se omiten cuñas e hidrógenos estereoquímicos para que el
    esqueleto se lea mejor en láminas didácticas.
    """
    if not estereo:
        mol = Chem.Mol(mol)
        Chem.RemoveStereochemistry(mol)
    escala = 3
    dibujo = rdMolDraw2D.MolDraw2DSVG(int(w * escala), int(h * escala))
    op = dibujo.drawOptions()
    op.clearBackground = False
    op.bondLineWidth = grosor * escala / 2
    op.baseFontSize = fuente
    op.padding = 0.08
    op.rotate = rotar
    op.additionalAtomLabelPadding = 0.1
    if monocromo:
        r, g, b = (int(monocromo[i:i + 2], 16) / 255 for i in (1, 3, 5))
        op.updateAtomPalette({n: (r, g, b) for n in range(1, 119)})
    dibujo.DrawMolecule(mol)
    dibujo.FinishDrawing()
    datos = base64.b64encode(dibujo.GetDrawingText().encode()).decode()
    return (f'<image href="data:image/svg+xml;base64,{datos}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>')
