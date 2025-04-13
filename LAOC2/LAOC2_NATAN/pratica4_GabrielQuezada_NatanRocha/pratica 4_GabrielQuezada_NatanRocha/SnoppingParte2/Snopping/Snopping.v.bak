`include "Bus.v"
`include "Cache.v"
`include "Memory.v"

/*
    [12] => 0: Read, 1: Write
    [11:10] => 00: PO, 01: P1, 11: P3
    [9:7] => TAG
    [6:0] => DATA
  */
module Snopping (
    input wire i_Clock,
    input wire i_Start,
    input wire [12:0] i_Instruction
);

  wire [23:0] w_P0Out, w_P1Out, w_P3Out, w_MemOut, w_BusOut;

  Memory u_Memory (
      w_BusOut,
      w_MemOut
  );

  Cache #(0, "c0.mem") u_C0 (
      i_Clock,
      i_Start,
      i_Instruction,
      w_BusOut,
      w_P0Out
  );

  Cache #(1, "c1.mem") u_C1 (
      i_Clock,
      i_Start,
      i_Instruction,
      w_BusOut,
      w_P1Out
  );

  Cache #(3, "c3.mem") u_C3 (
      i_Clock,
      i_Start,
      i_Instruction,
      w_BusOut,
      w_P3Out
  );

  Bus u_Bus (
      w_P0Out,
      w_P1Out,
      w_P3Out,
      w_MemOut,
      w_BusOut
  );


endmodule
