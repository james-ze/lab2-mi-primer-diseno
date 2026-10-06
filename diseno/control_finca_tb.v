//  A testbench for control_finca_tb
`timescale 1us/1ns

module control_finca_tb;
    reg I0_2;
    reg I0_3;
    reg I0_4;
    reg I0_1;
    wire Q0_1;
    wire Q0_2;
    wire Q0_4;
    wire Q0_3;
    wire Q0_5;
    wire Q0_6;
    wire Q0_7;

  control_finca control_finca0 (
    .I0_2(I0_2),
    .I0_3(I0_3),
    .I0_4(I0_4),
    .I0_1(I0_1),
    .Q0_1(Q0_1),
    .Q0_2(Q0_2),
    .Q0_4(Q0_4),
    .Q0_3(Q0_3),
    .Q0_5(Q0_5),
    .Q0_6(Q0_6),
    .Q0_7(Q0_7)
  );

    reg [10:0] patterns[0:15];
    integer i;

    initial begin
      patterns[0] = 11'b0_0_0_0_0_0_0_0_1_0_0;
      patterns[1] = 11'b0_0_0_1_0_0_1_1_1_1_0;
      patterns[2] = 11'b0_0_1_0_0_0_0_1_0_1_1;
      patterns[3] = 11'b0_0_1_1_0_0_1_1_0_1_0;
      patterns[4] = 11'b0_1_0_0_0_1_0_0_1_0_0;
      patterns[5] = 11'b0_1_0_1_0_1_1_1_1_1_0;
      patterns[6] = 11'b0_1_1_0_0_1_0_1_0_1_1;
      patterns[7] = 11'b0_1_1_1_0_1_1_1_0_1_1;
      patterns[8] = 11'b1_0_0_0_1_0_0_0_1_0_0;
      patterns[9] = 11'b1_0_0_1_1_0_1_0_1_0_0;
      patterns[10] = 11'b1_0_1_0_1_0_0_0_0_0_0;
      patterns[11] = 11'b1_0_1_1_1_0_1_0_0_0_0;
      patterns[12] = 11'b1_1_0_0_1_1_0_0_1_0_0;
      patterns[13] = 11'b1_1_0_1_1_1_1_0_1_0_0;
      patterns[14] = 11'b1_1_1_0_1_1_0_0_0_0_0;
      patterns[15] = 11'b1_1_1_1_1_1_1_0_0_0_0;

      for (i = 0; i < 16; i = i + 1)
      begin
        I0_4 = patterns[i][10];
        I0_3 = patterns[i][9];
        I0_2 = patterns[i][8];
        I0_1 = patterns[i][7];
        #10;
        if (patterns[i][6] !== 1'hx)
        begin
          if (Q0_7 !== patterns[i][6])
          begin
            $display("%d:Q0_7: (assertion error). Expected %h, found %h", i, patterns[i][6], Q0_7);
            $finish;
          end
        end
        if (patterns[i][5] !== 1'hx)
        begin
          if (Q0_6 !== patterns[i][5])
          begin
            $display("%d:Q0_6: (assertion error). Expected %h, found %h", i, patterns[i][5], Q0_6);
            $finish;
          end
        end
        if (patterns[i][4] !== 1'hx)
        begin
          if (Q0_5 !== patterns[i][4])
          begin
            $display("%d:Q0_5: (assertion error). Expected %h, found %h", i, patterns[i][4], Q0_5);
            $finish;
          end
        end
        if (patterns[i][3] !== 1'hx)
        begin
          if (Q0_4 !== patterns[i][3])
          begin
            $display("%d:Q0_4: (assertion error). Expected %h, found %h", i, patterns[i][3], Q0_4);
            $finish;
          end
        end
        if (patterns[i][2] !== 1'hx)
        begin
          if (Q0_3 !== patterns[i][2])
          begin
            $display("%d:Q0_3: (assertion error). Expected %h, found %h", i, patterns[i][2], Q0_3);
            $finish;
          end
        end
        if (patterns[i][1] !== 1'hx)
        begin
          if (Q0_2 !== patterns[i][1])
          begin
            $display("%d:Q0_2: (assertion error). Expected %h, found %h", i, patterns[i][1], Q0_2);
            $finish;
          end
        end
        if (patterns[i][0] !== 1'hx)
        begin
          if (Q0_1 !== patterns[i][0])
          begin
            $display("%d:Q0_1: (assertion error). Expected %h, found %h", i, patterns[i][0], Q0_1);
            $finish;
          end
        end
      end

      $display("All tests passed.");
    end
    endmodule
