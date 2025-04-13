module CONTROL(
	 input wire [2:0] OPcode,
	 output reg PCWrite,
    output reg RegWrite,
    output reg Branch,
    output reg [2:0] ULAOp,
    output reg MemWrite,
    output reg MemRead,
    output reg RegMemWrite
);

	initial begin
		PCWrite = 1;
   end


	always @(opcode) begin
		case(opcode)
		3'b000: begin  // Soma
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'b00;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 1;
      end
      3'b001: begin  // Subtracao
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'b01;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 1;
      end
      3'b010: begin  // Multiplicacao SRL
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'b10;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 1;
      end
		3'b011: begin  // Multiplicacao SLL
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'b11;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 1;
      end
     3'b011: begin  // lw ou lwi
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'bxx;
        MemWrite = 0;
        MemRead = 1;
        RegMemWrite = 1;
        RegWrite = 0;
      end 
      3'b100: begin  // slt ou slti
        PCWrite = 0;
        Branch = 0;
        ULAOp = 2'b11;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 0;
      end
	  3'b101: begin  // sw ou swi
        PCWrite = 1;
        Branch = 0;
        ULAOp = 2'bxx;
        MemWrite = 1;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 0;
      end
		3'b111: begin  // beq ou bne
        PCWrite = 1;
        Branch = 1;
        ULAOp = 2'b11;
        MemWrite = 0;
        MemRead = 0;
        RegMemWrite = 0;
        RegWrite = 0;
      end
    endcase
  end
   endmodule



module CONTROLteste;//teste
	  reg [2:0] opcode;
	  wire PCWrite;
	  wire RegWrite;
	  wire Branch;
	  wire [1:0] ULAOp;
	  wire MemWrite;
	  wire MemRead;
	  wire RegMemWrite;

	  CONTROL CONTROLteste (
			opcode,
			PCWrite,
			RegWrite,
			Branch,
			ULAOp,
			MemWrite,
			MemRead,
			RegMemWrite
	  );
	  
	  initial begin
		 #1 $display("Teste 1: Verificação dos sinais de controle da instrução multiplicacao SRL ");
		 OPcode = 3'b010;

		 #1 $display("Teste 2: Verificação dos sinais de controle da instrução SLT");
		 OPcode = 3'b100;
	  end

	  initial begin
		 $monitor("Time = %d, OPcode = %d, PCWrite = %d, RegWrite = %d, Branch = %d, ULAOp = %d, MemWrite = %d, MemRead = %d, RegMemWrite = %d", $time, opcode, PCWrite, RegWrite, Send, Branch, ULAOp, MemWrite, MemRead, RegMemWrite);
	  end


endmodule
