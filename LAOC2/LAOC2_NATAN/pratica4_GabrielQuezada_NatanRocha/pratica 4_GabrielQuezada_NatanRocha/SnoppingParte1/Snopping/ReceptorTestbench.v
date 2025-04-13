module ReceptorTestbench;

  localparam READ_MISS = 2'b00;  // 0
  localparam INVALIDATE = 2'b01;  // 1
  localparam WRITE_MISS = 2'b10;  // 2
  localparam NOTHING = 0;

  reg r_Clock = 1'b0;
  reg [1:0] r_Operation;

  Receptor u_Receptor (
      .i_Clock(r_Clock),
      .i_Operation(r_Operation)
  );

  always #5 r_Clock = ~r_Clock;

  initial $monitor("r_Signal = %2d, r_State = %2d", u_Receptor.r_Signal, u_Receptor.r_State);

  initial begin
    @(negedge r_Clock);
    $display("Test 1: READ_MISS");
    r_Operation = READ_MISS;

    @(negedge r_Clock);
    $display("Test 2: INVALIDATE");
    r_Operation = INVALIDATE;

    #100;
    $finish();
  end

endmodule

