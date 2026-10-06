# Lab 2 — Mi primer diseño

Red de control para una finca que conmuta entre la red eléctrica y un banco de baterías cargado por paneles solares, con paro de emergencia.

**Curso:** Electrónica Digital 1 · Universidad Nacional de Colombia
**Tarjeta:** Sipeed Tang Nano 9K (Gowin GW1NR-9)

**Integrantes:**
- James Yefrei Velasquez Boyaca (jvelasquezbo@unal.edu.co)
- Juan Esteban Castañeda Cristancho (jcastanedacr@unal.edu.co)
- Andres Alejandro González Vargas (agonzalesva@unal.edu.co)

---

## El problema

Una casa de finca puede alimentarse de dos fuentes: la red eléctrica o un inversor conectado a un banco de baterías que se carga con paneles solares. El sistema debe decidir automáticamente de cuál de las dos come la casa, avisar el estado de cada sensor, y detenerse de forma segura cuando se acciona el paro de emergencia.

## Entradas y salidas

| Entrada | Significado |
|---|---|
| `I0_1` | hay red eléctrica |
| `I0_2` | batería cargada (sensor con histéresis) |
| `I0_3` | hay radiación solar |
| `I0_4` | paro de emergencia accionado |

| Salida | Significado |
|---|---|
| `Q0_1` | relé K1, conmutador de fuente: 0 = red, 1 = inversor |
| `Q0_2` | relé K2, energiza la casa |
| `Q0_3` | piloto: batería descargada |
| `Q0_4` | piloto: casa energizada |
| `Q0_5` | piloto: hay red |
| `Q0_6` | piloto: hay sol |
| `Q0_7` | piloto: paro accionado |

## Criterio de diseño

Se eligió **prioridad solar**: la casa pasa a las baterías solo si están cargadas y además hay sol o se fue la red. Si la batería está baja, nunca conmuta, para no descargarla por debajo del umbral.

```
nP   = ~I0_4
Q0_1 = nP & I0_2 & (I0_3 | ~I0_1)
Q0_2 = nP & (I0_1 | I0_2)
Q0_3 = ~I0_2
Q0_4 = Q0_2
Q0_5 = I0_1
Q0_6 = I0_3
Q0_7 = I0_4
```

**Falla segura:** el paro entra negado en las dos ecuaciones de potencia, así que domina sobre todo lo demás. En el montaje, K1 en reposo conecta la red a través de su contacto NC, de modo que una falla del control deja la casa alimentada.

## Estructura del repositorio

```
diseno/          circuito de contactos, circuito de compuertas, Verilog del diseño y testbench
implementacion/  top.v, top.cst y el bitstream generado
simulacion/      forma de onda y evidencia de las pruebas
docs/            figuras del montaje y fotos del protoboard
```

## Cómo reproducir

### Simulación (no necesita la tarjeta)

```bash
cd diseno
iverilog -o tb.vvp control_finca_tb.v control_finca.v
vvp tb.vvp
```

Salida esperada: `All tests passed.`

El testbench recorre las 16 combinaciones posibles de las 4 entradas, o sea una prueba exhaustiva.

### Síntesis y carga en la Tang Nano 9K

Requiere el OSS CAD Suite, porque el flujo de Gowin necesita `nextpnr-himbaechel` y `gowin_pack`.

```bash
source ~/Descargas/oss-cad-suite/environment
yosys -p "read_verilog implementacion/top.v diseno/control_finca.v; synth_gowin -top top -json implementacion/build/top.json"
nextpnr-himbaechel --json implementacion/build/top.json \
    --write implementacion/build/top_pnr.json \
    --device GW1NR-LV9QN88PC6/I5 --vopt family=GW1N-9C \
    --vopt cst=implementacion/top.cst
gowin_pack -d GW1N-9C -o implementacion/build/top.fs implementacion/build/top_pnr.json
openFPGALoader -b tangnano9k implementacion/build/top.fs
```

## Asignación de pines

| Señal | Pin | Señal | Pin |
|---|---|---|---|
| `I0_1` | 25 | `Q0_1` | 39 |
| `I0_2` | 26 | `Q0_2` | 28 |
| `I0_3` | 27 | `Q0_3` | 29 |
| `I0_4` | 36 | `Q0_4` | 30 |
| | | `Q0_5` | 33 |
| | | `Q0_6` | 34 |
| | | `Q0_7` | 35 |

Las cuatro entradas se ubicaron en pines verificados como LVCMOS33. Los LEDs integrados de la tarjeta (10, 11, 13, 14, 15, 16) están en el banco de 1.8 V y son activos en bajo, por eso no se usaron.

## Montaje

- **Entradas:** 3V3 → interruptor → 1 kΩ → nodo → pin, con 10 kΩ del nodo a GND. El pull-down evita que el pin quede flotante con el interruptor abierto.
- **Pilotos:** pin → 330 Ω → LED → GND.
- **Relés:** pin → 1 kΩ → base 2N2222A; emisor a GND; colector a la bobina; el otro extremo de la bobina a +5 V; diodo 1N4004 en paralelo con la bobina, cátodo hacia +5 V.
- GND del protoboard unido al GND de la tarjeta.

## Verificación

| Herramienta | Resultado |
|---|---|
| Digital (simulador propio) | tabla de verdad de 16 filas: `passed` |
| Icarus Verilog | `All tests passed.` |
| Yosys | 3 celdas LUT4, 0 memorias, 0 procesos, 0 problemas |
| openFPGALoader | `CRC check: Success` |
| Montaje físico | respuesta correcta de los siete indicadores y conmutación audible de los relés |

Que dos simuladores independientes, escritos por equipos distintos, coincidan en las 16 filas es lo que da confianza en el diseño.

## Notas y limitaciones

1. El circuito del dominio físico, hecho con relés, **no es sintetizable**. Digital lo rechaza porque en Verilog una señal necesita un solo origen, mientras que dos contactos unidos forman un nodo con varios. El paso de contactos a compuertas es un trabajo de diseño, no una conversión automática.

2. `Q0_4` se definió como contacto auxiliar de K2. En el diseño HDL es una copia de `Q0_2`, así que confirma que la orden se dio, no que el relé cerró. Para el comportamiento real tendría que ser una entrada leída desde el contacto auxiliar.

3. El diseño es puramente combinacional. La transferencia entre fuentes ocurre con la casa conectada. En una instalación real se añadiría un retardo y un enclavamiento entre fuentes.

4. El entorno del curso está configurado para Lattice ECP5 (`nextpnr-ecp5`, `ecppack`, archivos `.lpf`). La Tang Nano es Gowin y requiere otra cadena, por eso se instaló el OSS CAD Suite.
