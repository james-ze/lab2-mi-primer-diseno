#!/usr/bin/env python3
"""Dibuja la forma de onda de un archivo VCD generado por una simulación.

Uso:
    python3 plot_vcd.py tb.vcd onda_simulacion.png

Lee el VCD, saca las señales de un bit y las dibuja como pulsos digitales.
Pensado para la bitácora: queda más legible que una captura de GTKWave.
"""
import re
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Orden en que quiero ver las señales. Las que no estén en la lista van al final.
ORDEN = ["I0_1", "I0_2", "I0_3", "I0_4",
         "Q0_1", "Q0_2", "Q0_3", "Q0_4", "Q0_5", "Q0_6", "Q0_7"]

AZUL, ROJO, GRIS, FONDO = "#1f4fa8", "#b23c17", "#777777", "#fdecea"


def leer_vcd(ruta):
    """Devuelve (escala_en_texto, {nombre: [(tiempo, valor), ...]})."""
    texto = open(ruta, encoding="utf-8", errors="ignore").read()

    # La escala de tiempo, por ejemplo "1ns"
    m = re.search(r"\$timescale\s+(.*?)\s+\$end", texto, re.S)
    escala = m.group(1).strip() if m else "1ns"

    # Cada senal declarada: $var wire 1 ! Q0_7 $end
    # El simbolo corto (!) es el identificador que se usa despues en los cambios.
    simbolo_de = {}
    for tipo, ancho, simbolo, nombre in re.findall(
            r"\$var\s+(\w+)\s+(\d+)\s+(\S+)\s+(\S+)[^$]*\$end", texto):
        if ancho == "1" and nombre not in simbolo_de:
            simbolo_de[nombre] = simbolo

    # Los cambios de valor vienen despues de $enddefinitions
    cuerpo = texto.split("$enddefinitions $end", 1)[-1]

    cambios = {s: [] for s in simbolo_de.values()}
    t = 0
    for linea in cuerpo.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        if linea.startswith("#"):
            t = int(linea[1:])
        elif linea[0] in "01xzXZ" and len(linea) > 1:
            valor, simbolo = linea[0], linea[1:]
            if simbolo in cambios:
                cambios[simbolo].append((t, valor))

    return escala, {n: cambios[s] for n, s in simbolo_de.items()}


def escalonar(eventos, t_final):
    """Convierte una lista de (tiempo, valor) en puntos para dibujar escalones."""
    xs, ys = [], []
    valor = 0
    t_prev = 0
    for t, v in eventos:
        nuevo = 0 if v in "0" else (1 if v in "1" else 0)
        xs += [t_prev, t]
        ys += [valor, valor]
        valor = nuevo
        t_prev = t
    xs += [t_prev, t_final]
    ys += [valor, valor]
    return xs, ys


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "tb.vcd"
    salida = sys.argv[2] if len(sys.argv) > 2 else "onda_simulacion.png"

    escala, senales = leer_vcd(entrada)

    # El testbench usa `timescale 1us/1ns`, asi que el VCD viene en ns.
    # Pasamos a microsegundos para que el eje sea legible.
    factor, unidad = (1000.0, "us") if "ns" in escala else (1.0, escala)
    senales = {n: [(t / factor, v) for t, v in ev] for n, ev in senales.items()}

    # Cada vector de prueba dura 10 unidades de la escala del testbench (#10)
    t_final = max((e[-1][0] for e in senales.values() if e), default=0)
    # El primer vector arranca en t=0 y el ultimo en t_max, o sea que entre
    # los 16 vectores hay 15 intervalos. De ahi sale la duracion de cada uno.
    paso = t_final / 15 if t_final else 1
    t_final = 16 * paso  # el ultimo vector tambien dura un paso completo

    # Solo los puertos del modulo. Las senales internas (nP, Q0_4_temp)
    # quedan fuera para que la figura sea legible.
    nombres = [n for n in ORDEN if n in senales]

    fig, ax = plt.subplots(figsize=(15, 7.2))
    alto, sep = 0.62, 1.0

    # Franja de fondo donde el paro esta accionado
    if "I0_4" in senales:
        xs, ys = escalonar(senales["I0_4"], t_final)
        inicio = None
        for x, y in zip(xs, ys):
            if y == 1 and inicio is None:
                inicio = x
            elif y == 0 and inicio is not None:
                ax.add_patch(Rectangle((inicio, -len(nombres) * sep - 0.3),
                                       x - inicio, len(nombres) * sep + 0.9,
                                       fc=FONDO, ec="none", zorder=0))
                inicio = None
        if inicio is not None:
            ax.add_patch(Rectangle((inicio, -len(nombres) * sep - 0.3),
                                   t_final - inicio, len(nombres) * sep + 0.9,
                                   fc=FONDO, ec="none", zorder=0))

    # Separadores de cada vector de prueba
    for k in range(17):
        ax.axvline(k * paso, color="#dddddd", lw=0.8, zorder=1)
    for k in range(16):
        ax.text(( k + 0.5) * paso, 0.55, str(k), ha="center", va="bottom",
                fontsize=7, color=GRIS, zorder=3)
    ax.text(-paso * 0.35, 0.55, "vector", ha="right", va="bottom",
            fontsize=7.5, color=GRIS, style="italic")

    for idx, nombre in enumerate(nombres):
        base = -idx * sep
        color = AZUL if nombre.startswith("I") else ROJO
        xs, ys = escalonar(senales[nombre], t_final)
        ax.step(xs, [base + y * alto for y in ys], where="post",
                color=color, lw=1.9, zorder=4)
        ax.axhline(base, color="#eeeeee", lw=0.6, zorder=1)
        ax.text(-paso * 0.35, base + alto / 2, nombre, ha="right", va="center",
                fontsize=10.5, weight="bold", color=color, zorder=4)

    ax.set_xlim(-paso * 2.1, t_final)
    ax.set_ylim(-len(nombres) * sep + 0.1, 1.5)
    ax.set_yticks([])
    ax.set_xlabel(f"tiempo ({unidad})", fontsize=10)
    ax.set_xticks([k * paso for k in range(0, 17, 2)])
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)

    ax.set_title("Simulación funcional del control de la finca\n"
                 "16 vectores de prueba, todas las combinaciones de las 4 entradas",
                 fontsize=13, weight="bold", pad=16)
    ax.text(t_final * 0.5, 1.25,
            "franja rosada: paro de emergencia accionado (I0_4 = 1). "
            "Q0_1 y Q0_2 quedan en cero sin importar las demás entradas.",
            ha="center", va="center", fontsize=9.5, color=GRIS)

    plt.tight_layout()
    plt.savefig(salida, dpi=150, bbox_inches="tight")
    plt.savefig(salida.rsplit(".", 1)[0] + ".svg", bbox_inches="tight")
    print("escrito", salida)


if __name__ == "__main__":
    main()
