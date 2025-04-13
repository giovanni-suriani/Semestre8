module ExtensorSinal(
   input wire [1:0] entrada,
   output reg [7:0] saida 
);

   always @(entrada) begin
      if (entrada[1] == 1) // Número negativo
         saida = {6'b11, entrada};
      else // Número positivo
         saida = {6'b00, entrada};
   end

endmodule

module ExtensorSinalteste;
		reg [1:0] entrada;
		wire [7:0] saida;
		
ExtensorSinal ExtensorSinal(entrada, saida);		

 initial 
	  begin
      #1 entrada=2'b10; $display("Teste extensor 1");
		#1 entrada=2'b11; $display("Teste extensor 2");
	  end
		
  initial 
	  begin
		$display("tempo entrada saida");
		$monitor("Tempo: %0d entrada: %0b saida: %0b\n", 
			      $time, entrada, saida);
	  end

		
endmodule