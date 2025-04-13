module Somador8Bits(
   input wire [7:0] entrada,
   output reg [7:0] saida 
);

   always @(entrada) begin
      saida <= entrada + 1;
   end

endmodule


module Somador8Bitsteste;

  reg  [7:0] entrada;
  wire [7:0] saida;

  Somador8Bits dut (
      entrada,
      saida
  );

  initial begin
    entrada = 0;

    $display("Teste 1: Entrada = 1");
    entrada = 1;

    #1 $display("Saida = %d", saida);
    $display("Teste 2: Entrada = 2");
    entrada = 2;
  end

  initial begin
    $monitor("Tempo: %0d\tEntrada: %d\tSaida: %d\n", $time, entrada, saida);
  end

endmodule