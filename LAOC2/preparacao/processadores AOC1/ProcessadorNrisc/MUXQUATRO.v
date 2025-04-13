module MultiplexadorQuatro(
   input wire [1:0] selecao,
   input wire [7:0] entrada1,
   input wire [7:0] entrada2,
	input wire [7:0] entrada3,
   input wire [7:0] entrada4,
   output reg saida 
);

   always @(selecao, entrada1, entrada2, entrada3, entrada4) begin
      case (selecao)
         2'b00: saida <= entrada1;
         2'b01: saida <= entrada2;
         2'b10: saida <= entrada3;
         2'b11: saida <= entrada4;
      endcase
   end

endmodule

module MultiplexadorQuatroteste;

  reg [1:0] selecao;
  reg [7:0] entrada1;
  reg [7:0] entrada2;
  reg [7:0] entrada3;
  reg [7:0] entrada4;
  wire [7:0] saida;

  MultiplexadorQuatro MultiplexadorQuatro(selecao, entrada1, entrada2, entrada3, entrada4, saida);

  initial 
	  begin
      #1 selecao=2'b00; entrada1=8'b00000000; entrada2=8'b00000001; entrada3=8'b00000010; entrada4=8'b10000000; $display("Teste MultiplexadorDois entrada 1");
		#1 selecao=2'b01; entrada1=8'b00000000; entrada2=8'b00000001; entrada3=8'b00000010; entrada4=8'b10000000; $display("Teste MultiplexadorDois entrada 2");
		#1 selecao=2'b10; entrada1=8'b00000000; entrada2=8'b00000001; entrada3=8'b00000010; entrada4=8'b10000000; $display("Teste MultiplexadorDois entrada 3");
		#1 selecao=2'b11; entrada1=8'b00000000; entrada2=8'b00000001; entrada3=8'b00000010; entrada4=8'b10000000; $display("Teste MultiplexadorDois entrada 4");
	  end

  initial 
	  begin
		$display("tempo selecao entrada1 entrada2 entrada3 entrada4 saida");
		$monitor("Tempo: %0d selecao: %0b entrada1: %0b entrada2: %0b entrada3: %0b entrada4: %0b saida: %0b\n", 
			      $time, selecao, entrada1, entrada2, entrada3, entrada4, saida);
	  end

endmodule