module MultiplexadorDois(
   input wire selecao,
   input wire [7:0] entrada1,
   input wire [7:0] entrada2,
   output reg [7:0] saida 
);

   always @(selecao, entrada1, entrada2) begin
      case (selecao)
         1'b0: saida <= entrada1;
         1'b1: saida <= entrada2;
      endcase
   end

endmodule


module MultiplexadorDoisteste;

  reg selecao;
  reg [7:0] entrada1;
  reg [7:0] entrada2;
  wire [7:0] saida;

  MultiplexadorDois MultiplexadorDois(selecao, entrada1, entrada2, saida);

  initial 
	  begin
      #1 selecao=1'b0; entrada1=8'b00000001; entrada2=8'b00000010; $display("Teste MultiplexadorDois entrada 1");
		#1 selecao=1'b1; entrada1=8'b00000001; entrada2=8'b00000010; $display("Teste MultiplexadorDois entrada 2");
	  end

  initial 
	  begin
		$display("tempo selecao entrada1 entrada2 saida");
		$monitor("Tempo: %0d selecao: %0b entrada1: %0b entrada2: %0b saida: %0b\n", 
			      $time, selecao, entrada1, entrada2, saida);
	  end

endmodule