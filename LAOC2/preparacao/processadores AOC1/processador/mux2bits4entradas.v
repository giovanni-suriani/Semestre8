module mux2bits4entradas(var1, var2, var3, var4, sinal, saida);
input [1:0]sinal;
input[1:0] var1, var2, var3, var4;
output reg[1:0] saida;

always @(*) begin
case(sinal)
2'b00: begin saida = var1; end
2'b01: begin saida = var2; end
2'b10: begin saida = var3; end
2'b11: begin saida = var4; end
endcase
end

endmodule 

