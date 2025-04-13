module EmissorTestbench;

  localparam RM = 2'b00;  // read miss
  localparam RH = 2'b01;  // read hit
  localparam WM = 2'b10;  // write miss
  localparam WH = 2'b11;  // write hit

  reg r_Clock = 1'b0;
  reg [1:0] r_Operation;

  Emissor u_Emissor (
      .i_Clock(r_Clock),
      .i_Operation(r_Operation)
  );

  always #5 r_Clock = ~r_Clock;

  initial
    $monitor(
        "r_Message = %2d, r_Signal = %2d, r_State = %2d",
        u_Emissor.r_Message,
        u_Emissor.r_Signal,
        u_Emissor.r_State
    );

  initial begin
    @(negedge r_Clock);
    $display("Test 1: read miss");
    r_Operation = RM;

    @(negedge r_Clock);
    $display("Test 2: read hit");
    r_Operation = RH;

    @(negedge r_Clock);
    $display("Test 3: read miss");
    r_Operation = RM;

    @(negedge r_Clock);
    $display("Test 4: write hit");
    r_Operation = WH;

    @(negedge r_Clock);
    $display("Test 5: write miss");
    r_Operation = WM;

    #100;
    $finish();
  end

endmodule

