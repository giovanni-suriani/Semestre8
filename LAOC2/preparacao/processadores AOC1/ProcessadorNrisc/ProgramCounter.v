module ProgramCounter (
  input clk,
  input reset,
  input enable,
  output reg [7:0] address
);

  always @(posedge clk) begin
    if (reset)
      address <= 8'b00000000;
    else if (enable)
      address <= address + 1;
  end

endmodule

module testProgramCounter;
  reg clk;
  reg reset;
  reg enable;
  wire [7:0] address;

  ProgramCounter PC (
    .clk(clk),
    .reset(reset),
    .enable(enable),
    .address(address)
  );

  always begin
    #5 clk = ~clk;  // Inverte o sinal de clock a cada 5 unidades de tempo
  end

  initial begin
    clk = 0;
    reset = 1;
    enable = 0;
    #10 reset = 0;  // Desativa o sinal de reset após 10 unidades de tempo

    // Monitor para exibir o valor do PC
    $monitor("PC = %h", address);
    #50 enable = 1;  // Ativa o sinal de habilitação após 50 unidades de tempo
    #100 enable = 0;  // Desativa o sinal de habilitação após 100 unidades de tempo

    #10 $finish;  // Finaliza a simulação após 10 unidades de tempo adicionais
  end
endmodule