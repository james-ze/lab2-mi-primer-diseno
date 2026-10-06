# Evidencia de simulación

## Qué hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `tb.vcd` | volcado de todas las señales en el tiempo, generado por la simulación |
| `onda_simulacion.png` | captura de la forma de onda vista en GTKWave |

## Cómo se generó

```bash
cd ../diseno
iverilog -o tb.vvp control_finca_tb.v control_finca.v
vvp tb.vvp
gtkwave tb.vcd
```

Salida de la simulación:

```
VCD info: dumpfile tb.vcd opened for output.
All tests passed.
```

## Qué prueba el testbench

Recorre las **16 combinaciones posibles** de las 4 entradas, que son todas (2⁴ = 16). Para cada una espera 10 µs a que el circuito se estabilice y compara las siete salidas contra los valores de la tabla de verdad. Si una sola no coincide, imprime cuál falló y detiene la simulación.

Con 4 entradas la prueba exhaustiva es posible. Con 16 entradas serían 65.536 combinaciones y con 32 más de cuatro mil millones, así que en diseños grandes se prueban casos representativos.

## Verificación cruzada

El mismo diseño se verificó con **dos simuladores independientes**:

| Herramienta | Qué simula | Resultado |
|---|---|---|
| Digital (hneemann) | el circuito de compuertas dibujado | tabla de verdad: `passed` |
| Icarus Verilog | el archivo `control_finca.v` exportado | `All tests passed.` |

Son programas distintos, escritos por equipos distintos, que parten de representaciones distintas del mismo diseño. Que coincidan en las 16 filas es lo que da confianza en el resultado.

## Prueba de que la prueba funciona

Se alteró deliberadamente un valor esperado en la tabla de verdad y se volvió a correr la simulación. La prueba **falló**, como debía.

Esto importa porque una prueba que pasa siempre, incluso con datos incorrectos, no está verificando nada. Comprobar que la prueba sabe fallar es parte de confiar en ella.

## Qué se observa en la forma de onda

1. **Dominio del paro.** En la mitad derecha de la gráfica, `I0_4` se mantiene en alto durante ocho tramos. Ahí `Q0_1` y `Q0_2` quedan en cero y no se mueven aunque las otras tres entradas sigan cambiando. Es la verificación visual de que el paro domina sobre el resto de la lógica.

2. **Los pilotos siguen informando.** `Q0_5`, `Q0_6` y `Q0_7` siguen a sus entradas incluso con el paro accionado. Fue una decisión de diseño: el sistema se detiene, pero el operario debe poder ver qué está pasando.

3. **Respaldo ante corte de red.** En los tramos donde `I0_1` cae a cero con `I0_2` en uno, `Q0_1` y `Q0_2` se mantienen altos. La casa sigue energizada desde las baterías.

4. **Sin transitorios.** Las salidas cambian en el mismo instante que las entradas, sin estados intermedios. Confirma que el diseño es puramente combinacional, sin memoria.

## Nota sobre el archivo VCD

Un `.vcd` es texto plano. Contiene un encabezado que declara las señales y después una lista de instantes con los cambios. Solo registra **cambios**, no el valor en cada momento, por eso pesa tan poco. La forma de onda no está guardada como imagen: la dibuja el visor a partir de esa lista de eventos.

El testbench exportado por Digital no incluye las líneas `$dumpfile` y `$dumpvars`, así que hubo que agregarlas a mano para que la simulación dejara este archivo.
