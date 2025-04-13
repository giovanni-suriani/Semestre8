module ULA (
    input wire [7:0] A,
    input wire [7:0] B,
    output reg zero,
    output reg [7:0] result,
    input wire [2:0] ULAOp
);

  always @(A or B or ULAOp) begin
    case (ULAOp)
      3'b000:   result = A + B; // Soma (add, addi, sll, lw)
      3'b001:   result = A - B; // Subtracao (sub, subi)
		3'b010:   result = A >> B; // Multiplicacao (srl)
		3'b011:   result = A << B; // Multiplicacao (sll)
		3'b100:   result = A < B ? 1 : 0; // (slt, slti)
		3'b111:   zero = (result) == 0; // (beq, bne compara com saída 0)                
      default: result = 0;
    endcase

    if (result == 0) begin
      zero = 1;
    end else begin
      zero = 0;
    end
  end
endmodule

module ULAteste;

     reg [7:0] A;
     reg [7:0] B;
     wire zero;
     wire [7:0] result;
     reg [2:0] ULAOp;

		ULA ULA(A,B,zero,result,ULAOp); //instanciando ela dentro do modulo de teste
												 //, cada porta ligada à correspondente que queremos testar(só consegue mudar as entradas pra ver saídas)

	initial
		begin
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b000; $display("teste soma");
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b001; $display("teste subtração");
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b010; $display("teste multiplicacao srl");
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b011; $display("teste multiplicacao sll");
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b100; $display("teste slt");
		#1 A = 8'b00001010;	 B = 8'b00000001; ULAOp = 3'b111; $display("teste beq, bne");
		//outros testes com outras operações etc
		end
		
	initial
		begin
		$display("tempo A B zero result ULAOp"); //botar smp na mesma ordem
		$monitor ("time = %0d A = %0b B = %0b zero = %0b result = %0b ULAOp = %0b", 
					 $time, A, B, zero, result, ULAOp); //vai aparecer tempo la no modelsim passando
		end
endmodule
			




