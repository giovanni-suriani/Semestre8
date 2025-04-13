module Somador8BitsDuas(
   input wire [7:0] entrada1,
   input wire [7:0] entrada2,
   output reg [7:0] saida 
);

   always @(entrada1, entrada2) begin
      saida <= entrada1 + entrada2;
   end

endmodule

module Somador8BitsDuasteste;

  reg  [7:0] entrada1;
  reg [7:0] entrada2;
  wire [7:0] saida;

  Somador8BitsDuas Somador8BitsDuas(entrada1, entrada2, saida);

  initial 
	  begin
      #1 entrada1=2; entrada2=3; $display("Teste somador 2 entradas");
	  end

  initial 
	  begin
		$display("tempo entrada1 entrada2 saida");
		$monitor("Tempo: %0d\tEntrada1: %d\tEntrada2: %d\tSaida: %d\n", 
			      $time, entrada1, entrada2, saida);
	  end

endmodule