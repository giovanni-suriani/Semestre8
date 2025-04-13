module Bus (
    input  wire [23:0] i_P0,
    input  wire [23:0] i_P1,
    input  wire [23:0] i_P3,
    input  wire [23:0] i_Mem,
    output reg  [23:0] o_PO
);

  /*
    [22-21] => 0 -> RM, 1 -> WM, 2   -> Invalidate
    [20-18] => TAG
    [17-11] => DATA
    [10] => WB?
    [9-7] => TAG
    [6-0] => DATA
  */
  always @(*)
    if (i_P0 != 0) begin
      o_PO = i_P0;
    end else if (i_P1 != 0) begin
      o_PO = i_P1;
    end else if (i_P3 != 0) begin
      o_PO = i_P3;
    end else if(i_Mem != 0) begin
      o_PO = i_Mem;
    end


endmodule
