// top.v — conecta el diseño a los pines físicos de la Tang Nano 9K
// Escrito a mano. Digital NO toca este archivo.

module top (
    input  I0_1,   // switch: hay red
    input  I0_2,   // switch: batería cargada
    input  I0_3,   // switch: hay sol
    input  I0_4,   // switch: paro de emergencia
    output Q0_1,   // relé K1
    output Q0_2,   // relé K2
    output Q0_3,   // piloto batería baja
    output Q0_4,   // piloto casa energizada
    output Q0_5,   // piloto red
    output Q0_6,   // piloto sol
    output Q0_7    // piloto paro
);

    control_finca u1 (
        .I0_1(I0_1), .I0_2(I0_2), .I0_3(I0_3), .I0_4(I0_4),
        .Q0_1(Q0_1), .Q0_2(Q0_2), .Q0_3(Q0_3), .Q0_4(Q0_4),
        .Q0_5(Q0_5), .Q0_6(Q0_6), .Q0_7(Q0_7)
    );

endmodule
