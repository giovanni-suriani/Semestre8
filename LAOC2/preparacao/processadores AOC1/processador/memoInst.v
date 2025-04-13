module memoInst (leEndereco,instrucao,clock,reset);
input clock,reset;
input [7:0] leEndereco;
output [7:0] instrucao; 
reg [30:0] RF [7:0]; 
reg [7:0]intermediario; //onde salva a instrucao

always begin @(posedge clock) 
	if (reset)
		case(leEndereco)
			8'b00000000: intermediario = 8'b11101111; //set $s1, 7 # $s1 = 7
			8'b00000001: intermediario = 8'b00010101; //add $s1, $s1 #s1 = 14
			8'b00000010: intermediario = 8'b11110100; //set $s2, 4 # $s2 = 4
			8'b00000011: intermediario = 8'b00010110; //add $s1, $s2 #s1 = 14 #18
			8'b00000100: intermediario = 8'b01011111; //sw $s1, 3($sp)
			8'b00000101: intermediario = 8'b11110000; //set  $s2, 0;
			8'b00000110: intermediario = 8'b01101110; //sw $s2, 2($sp)
			8'b00000111: intermediario = 8'b11101101; //set $s1, 5
			8'b00001000: intermediario = 8'b01011101;//sw $s1, 1($sp)
			8'b00001001: intermediario = 8'b00000100; //beq $s1, $zero
			8'b00001010: intermediario = 8'b10101110; //lw $s2, 2($sp)
			8'b00001011: intermediario = 8'b00011001;//add $s2, $s1 
			8'b00001100: intermediario = 8'b01101110; //sw $s2, 2($sp)
			8'b00001101: intermediario = 8'b10011101; //lw $s1, 1($sp)
			8'b00001110: intermediario = 8'b00100101; //subi $s1, 1
			8'b00001111: intermediario = 8'b01011101; //sw $s1, 1($sp)
			8'b00010000: intermediario = 8'b10101111; //lw $s2, 3($sp)
			8'b00010001: intermediario = 8'b11001001; //j 
			8'b00010010: intermediario = 8'b00110000; //halt
			//8'b00010011: intermediario = 8'b;
			default: intermediario = 8'b00110000; //halt
			endcase
	end
assign instrucao = intermediario;

endmodule

