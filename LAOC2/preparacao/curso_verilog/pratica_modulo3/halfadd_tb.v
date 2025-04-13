`timescale 1ns / 1ps
`include "halfadd.v"


module halfadd_tb;

  // Declare testbench signals
  reg a, b;
  wire sum, carry;

  // Instantiate the module under test (MUT)

  halfadd u_halfadd (
      .a    (a),
      .b    (b),
      .sum  (sum),
      .carry(carry)
  );


  // Run simulation
  initial begin
    // Initialize GTKWave VCD dump
    $dumpfile("wave.vcd");   // Name of the VCD file to generate
    $dumpvars(0, halfadd_tb); // Dump all variables in this module

    // Apply test inputs
    a = 0; b = 0; #10;
    a = 0; b = 1; #10;
    a = 1; b = 0; #10;
    a = 1; b = 1; #10;

    $finish;
  end

endmodule
