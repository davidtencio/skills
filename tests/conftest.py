"""Utilidades comunes de los tests de las skills.

Las dos skills tienen módulos con el mismo nombre (componentes, recursos, pdf…), así que todo lo que importa
código de una skill se ejecuta en un proceso aparte (`ejecutar`), salvo los tests de piezas y de fuentes de
fisiopatologia, que importan solo módulos de esa skill.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS_DIR = RAIZ / ".claude" / "skills"
SKILLS_TODAS = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())
# Skills de láminas (mecanismo-accion, fisiopatologia): comparten módulos, biblioteca de ilustraciones y fuentes.
SKILLS = [s for s in SKILLS_TODAS if (SKILLS_DIR / s / "scripts" / "revisar_lamina.py").exists()]


def versionados(patron):
    """Archivos de git que cumplen el patrón (deja fuera los ejemplos sin seguimiento, p. ej. el material de entrega)."""
    salida = subprocess.run(["git", "ls-files", patron], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    return [RAIZ / linea for linea in salida.splitlines()]


def ejemplos():
    """Carpetas de ejemplo versionadas que tienen laminas.py, como (skill, carpeta)."""
    return [(ruta.parents[2].name, ruta.parent) for ruta in versionados(".claude/skills/*/ejemplos/*/laminas.py")]


def ejecutar(*args, timeout=600):
    """Ejecuta Python en un proceso aparte y devuelve el resultado completo."""
    return subprocess.run([sys.executable, *map(str, args)], cwd=RAIZ, capture_output=True, text=True, timeout=timeout)
