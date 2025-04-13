module Memory (
    input [23:0] i_Bus,
    output reg [23:0] o_Bus
);

  /*
    [22-21] => 0 -> RM, 1 -> WM, 2   -> Invalidate
    [20-18] => TAG
    [17-11] => DATA
    [10] => WB?
    [9-7] => TAG
    [6-0] => DATA
  */
  reg [9:0] r_Memory[0:3];
  initial $readmemb("mem.mem", r_Memory);

  integer i = 0;
  always @(i_Bus) begin
    o_Bus = 0;

    if (i_Bus[10]) begin
      for (i = 0; i < 4; i = i + 1) begin
        if (r_Memory[i][9:7] == i_Bus[9:7]) begin
          r_Memory[i] = {i_Bus[9:7], i_Bus[6:0]};
        end
      end
    end else if (i_Bus[22:21] == 0) begin 
      // Read Miss
      for (i = 0; i < 4; i = i + 1) begin
        if (r_Memory[i][9:7] == i_Bus[20:18]) begin
          o_Bus = {i_Bus[22:21], i_Bus[20:18], r_Memory[i][6:0], 1'b0, i_Bus[9:7], r_Memory[i][6:0]};
        end
      end
    end
  end

endmodule
