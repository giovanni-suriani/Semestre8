`include "Snopping.v"

module SnoppingTestbench;

  reg r_Clock = 0;
  reg r_Start = 0;
  reg [12:0] r_Instruction;

  reg [12:0] r_Instructions[0:8];
  integer k = 0;
  initial begin
    r_Instructions[0] = 13'b0001000000000;  // P0: READ 120
    r_Instructions[1] = 13'b1001001010000;  // P0: WRITE 120 <- 80
    r_Instructions[2] = 13'b1111001010000;  // P3: WRITE 120 <- 80
    r_Instructions[3] = 13'b0010100000000;  // P1: READ 110
    r_Instructions[4] = 13'b1110100011110;  // P3: WRITE 110 <- 30
    r_Instructions[5] = 13'b0110100000000;  // P3: READ 110
    r_Instructions[6] = 13'b1000010110000;  // P0: WRITE 108 <- 48
    r_Instructions[7] = 13'b1111101001110;  // P3: WRITE 130 <- 78
  end

  Snopping u_Snopping (
      r_Clock,
      r_Start,
      r_Instruction
  );

  always #5 r_Clock = ~r_Clock;

  integer i = 0;
  task automatic display();
    begin

      $display("C0 CONTENTS:");
      for (i = 0; i < 4; i = i + 1) begin
        $display("B%0d: S %2d T %2d V %2d", i, u_Snopping.u_C0.r_Memory[i][11:10],
                 u_Snopping.u_C0.r_Memory[i][9:7], u_Snopping.u_C0.r_Memory[i][6:0]);
      end
      $display("\n");

      $display("C1 CONTENTS:");
      for (i = 0; i < 4; i = i + 1) begin
        $display("B%0d: S %2d T %2d V %2d", i, u_Snopping.u_C1.r_Memory[i][11:10],
                 u_Snopping.u_C1.r_Memory[i][9:7], u_Snopping.u_C1.r_Memory[i][6:0]);
      end
      $display("\n");

      $display("C3 CONTENTS:");
      for (i = 0; i < 4; i = i + 1) begin
        $display("B%0d: S %2d T %2d V %2d", i, u_Snopping.u_C3.r_Memory[i][11:10],
                 u_Snopping.u_C3.r_Memory[i][9:7], u_Snopping.u_C3.r_Memory[i][6:0]);
      end
      $display("\n");

      $display("MEM CONTENTS:");
      for (i = 0; i < 4; i = i + 1) begin
        $display("T %2d V %2d", u_Snopping.u_Memory.r_Memory[i][9:7],
                 u_Snopping.u_Memory.r_Memory[i][6:0]);
      end

    end
  endtask


  initial begin
    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");

    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");

    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");

    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");
    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");
    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");
    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $display("--------------------------------------");
    @(negedge r_Clock);
    r_Instruction = r_Instructions[k];
    k = k + 1;
    r_Start = 1;
    @(negedge r_Clock);
    r_Start = 0;
    #40;
    display();

    $finish();
  end

  initial begin
    $dumpfile("test.vcd");
    $dumpvars(0, SnoppingTestbench);
  end


endmodule
