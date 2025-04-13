module PortaAND(
   input wire entrada1,
   input wire entrada2,
   output reg saida 
);

   always @(entrada1, entrada2) begin
      saida <= entrada1 & entrada2;
   end

endmodule

module ANDTeste;
  reg  entrada1;
  reg  entrada2;
  wire saida;

  PortaAND dut (
      .saida(saida),
      .entrada1(entrada1),
      .entrada2(entrada2)
  );

  initial begin
    $display("Teste 1: entrada1=0, entrada2=0");
    entrada1 = 0;
    entrada2 = 0;

    #1 $display("Teste 2: entrada1=0, entrada2=1");
    entrada1 = 0;
    entrada2 = 1;

    #1 $display("Teste 3: entrada1=1, entrada2=0");
    entrada1 = 1;
    entrada2 = 0;

    #1 $display("Teste 4: entrada1=1, entrada2=1");
    entrada1 = 1;
    entrada2 = 1;
  end

  initial begin
    $monitor("Tempo :%0d\tEntrada 1: %b\tEntrada 2: %b\tSaida: %b\n", $time, entrada1, entrada2, saida);
  end

endmodule