module ProcessadorNrisc(clk);
	input clk;
	wire [7:0] data1;
	wire [7:0] instrucaoLida;
	wire [7:0] saidaExtensor;
	wire [7:0] dadosLidos;
	wire [7:0] result;
	wire [7:0] saidaPC;
	wire [7:0] saidaSomador1;
	wire [7:0] saidaSomador2;
	wire [7:0] readData1;
	wire [7:0] readData2;
	wire [7:0] saidaMux1;
	wire [7:0] saidaMux2;
	wire [7:0] saidaMux3;
	wire [7:0] saidaMux4;
	wire [7:0] saidaMuxQuatro1;
	wire [7:0] instrucaoLida;
	
	REGISTRADORES REGISTRADORES (instrucaoLida[3:2],instrucaoLida[1:0],instrucaoLida[3:2],writeData, writeEnable,readData1,readData2,memRead,raRead,);
	ULA ULA (saidaMux2[7:0],saidaMuxQuatro1[7:0],zero,result,ULAOp);
	MultiplexadorDois MultiplexadorDois1(selecao,data1[7:0],8'b00000000,saidaMux1);
	MultiplexadorDois MultiplexadorDois2(selecao,dadosLidos[7:0],result[7:0],saidaMux2); 
	MultiplexadorDois MultiplexadorDois3(selecao,8'b00000000,8'b00000001,saidaMux3); 
	MultiplexadorDois MultiplexadorDois4(selecao,saidaSomador1[7:0],saidaSomador2[7:0],saidaMux4); //alter
	MultiplexadorQuatro MultiplexadorQuatro(selecao,readData2[7:0],saidaExtensor[7:0],8'b00000000,entrada4,saidaMuxQuatro1);
	Memory Memory(clock,result[7:0],readData1[7:0],dadosLidos,MemRead,MemWrite);
	INSTRUCAO INSTRUCAO(clock,saidaPC[7:0],instrucaoLida);
	ExtensorSinal ExtensorSinal(instrucaoLida[7:0],saidaExtensor);
   Somador8Bits Somador8Bits(saidaPC[7:0],saidaSomador1);
   Somador8BitsDuas Somador8BitsDuas(readData2[7:0],saidaSomador1[7:0],saidaSomador2);
	PortaAND PortaAND(entrada1,saidaMux3[7:0],saida);
	CONTROL(OPcode,PCWrite,RegWrite,Branch,ULAOp,MemWrite,MemRead,RegMemWrite);
	ProgramCounter (clk,reset,enable,saidaPC);
endmodule

module ProcessadorNriscTeste 

	ProcessadorNrisc ProcessadorNrisc(clk)
	
	initial
	begin	  
    for(i=0;i<=65535;i=i+1)
      Memoria.mem[i]=0;//Inicializa a mem�ria com 0
    
    $readmemh("testevibn",ProcessadorNrisc.INSTRUCAO.data); //Leitura do arquivo
 
    CLK = 0;
	end
	
	reg clk
		initial
		  begin
			 counter = 1;
			 forever
			 begin       
				 #1;	
				 CLK = ~CLK;
			
			 end
	  end
		
	 initial
		begin
		$display("tempo A B zero result ULAOp"); 
		$monitor ("time = %0d A = %0b B = %0b zero = %0b result = %0b ULAOp = %0b", 
					 $time, ProcessadorNrisc.REGISTRADORES.readData1, B, zero, result, ULAOp); //pegar a msm ideia do exemplo
	 end
	 
	 
	always@(posedge (CLK == 0))
	begin
		counter = counter + 1;
	end
endmodule