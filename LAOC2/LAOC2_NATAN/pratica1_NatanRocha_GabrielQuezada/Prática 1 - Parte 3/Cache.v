module Cache (clock, address, wren, data, q, RAM, qRAM, hit, state, reset, mem_access_done, lru0, lru1, lru2, lru3, d0, d1, d2, d3);
	input clock, wren, reset;
	input [7:0] data;
	input [7:0] qRAM;
	input [4:0] address;

	output reg [7:0] q;
	output reg [13:0] RAM;
	output reg hit;
	
	output reg mem_access_done;

	// Estados de processamento da Cache:
	// 1 -> HIT
	// 2 -> MISS
	// 3 -> Atualiza LRU
	output reg [2:0] state;
   
	// Variáveis para salvar o valor do LRU de todas as posições da cache
	output reg [1:0] lru0;
	output reg [1:0] lru1;
	output reg [1:0] lru2;
	output reg [1:0] lru3;
	
	// Variáveis para salvar o valor do Dirty de todas as posições da cache
	output reg d0;
	output reg d1;
	output reg d2;
	output reg d3;

	
	// Cria a cache totalmente associativa por conjunto de 2 vias -> 8 enderecos na cache ao todo e 17 bits para cada endereco:
	// [7:0]   => Dados armazenados
	// [12:8]  => Tag do endereco
	// [14:13] => Bit de controle LRU (3 = mais antigo, 0 = mais recente)
	// [15:15] => Bit de controle Dirty
	// [16:16] => Bit de controle Valid
	reg [16:0] cache [1:0][3:0];

	
	// Criar um reg para salvar o index da cache caso ocorra um hit
	reg [1:0] indexCache;
	
	// Salva o index em que está o bloco que será retirado da cache
	reg [1:0] exit_index;
	
	// Criar uma variavel para iterar nas posicoes da Cache
	integer index = 0;

	// Inicializando os valores da cache
	initial begin
	
		  cache[0][0][16:0] <= 17'b10001010000000110; /* Válido 1, Dirty 0, LRU 0, Tag 20, Valor 6*/
        cache[0][1][16:0] <= 17'b10011011000000010; /* Válido 1, Dirty 0, LRU 1, Tag 22, Valor 2*/
        cache[0][2][16:0] <= 17'b00111100100000110; /* Válido 0, Dirty 0, LRU 3, Tag 25, Valor 6*/
        cache[0][3][16:0] <= 17'b10101010100000100; /* Válido 1, Dirty 0, LRU 2, Tag 21, Valor 4*/

        cache[1][0][16:0] <= 17'b00000101000000100; /* Válido 0, Dirty 0, LRU 0, Tag 10, Valor 4*/
        cache[1][1][16:0] <= 17'b10011011100000110; /* Válido 1, Dirty 0, LRU 1, Tag 23, Valor 2*/
        cache[1][2][16:0] <= 17'b10110010000000100; /* Válido 1, Dirty 0, LRU 3, Tag 4, Valor 4*/
        cache[1][3][16:0] <= 17'b00100001100000010; /* Válido 0, Dirty 0, LRU 2, Tag 3, Valor 2*/
		
		// Dirty
        d0 <= cache[0][0][15];
        d1 <= cache[0][1][15];
        d2 <= cache[0][2][15];
        d3 <= cache[0][3][15];
        
        // LRU
        lru0 <= cache[0][0][14:13];
        lru1 <= cache[0][1][14:13];
        lru2 <= cache[0][2][14:13];
        lru3 <= cache[0][3][14:13];

        hit <= 1'b0;
        state <= 3'd0;
		  
	end
	
	always @ (posedge clock) begin
        
        // Resetando o valor de hit
        hit <= 1'b0;
        
        // Percorrendo a Cache para definir se ocorreu um hit ou miss
        for (index = 0; index < 4; index = index + 1) begin
            if (cache[0][index][12:8] == address[4:0] && cache[0][index][16]) begin
                hit <= 1'b1;
                indexCache = index;
            end
            else if (cache[1][index][12:8] == address[4:0] && cache[1][index][16]) begin
                hit <= 1'b1;
                indexCache = index + 4; // Offset para segunda via
            end
        end
        
        if (hit) begin
            state <= 3'd1;
        end
        else begin
            state <= 3'd2;
        end
		
		case (state)
			 
			3'd1: // hit
			begin
				
				// hit -> escrita
				if (wren) begin
               cache[indexCache[1]][indexCache[0]][7:0] <= data; // Escreve o dado

               cache[indexCache[1]][indexCache[0]][15] <= 1'b1;  // Atualiza o dirty

					q <= data;							  // Coloca o dado escrito na saída da cache
					state <= 3'd3; 					  // Atualiza LRU
					
					//Atualiza Dirty
               d0 <= cache[0][0][15];
					d1 <= cache[1][0][15];
               d2 <= cache[1][2][15];
               d3 <= cache[1][3][15];
				end
				
				// hit -> leitura
				else begin
               q <= cache[indexCache[1]][indexCache[0]][7:0];    // Coloca o dado lido na saída da cache
					state <= 3'd3;                  // Atuliza LRU
				end
				
			end
			
			3'd2: // miss
			begin
				
				// Selecionar bloco com menor LRU para ser retirado da Cache
				exit_index <= 0;
				for (index = 0; index < 4; index = index + 1) begin
               if (cache[indexCache[1]][indexCache[0]][14:13] == 0) begin

						exit_index <= index;
					end
				end
				
				// Write-Back
            if (cache[exit_index[1]][exit_index[0]][15] == 1) begin

					
					// Salvando endereco a ser acessado na RAM
               RAM[13:9] <= cache[exit_index[1]][exit_index[0]][12:8];

					
					// Ativa escrita na RAM
					RAM[8] <= 1'b1;
					
					// Passa os dados da cache para serem escritos na RAM
					RAM[7:0] <= cache[exit_index[1]][exit_index[0]][7:0];
					
					// qRAM deve conter o dado presente no bloco que está saindo da cache
					
				end
				
				// Acessar Memória
				mem_access_done <= 1'b0;
				
				// Salvando endereco a ser acessado na RAM
				RAM[13:9] <= address[4:0];

				// Desativa escrita na RAM
				RAM[8] <= 1'b0;
				
				// qRAM deve conter o dado presente no bloco que está sendo movido para a cache
				
				// Finalizar Acesso à Memória
				mem_access_done <= 1'b1;
				
				// Após o acesso a memória a posição acessada terá seu dado salvo em qRAM
				// Possibilitando agora a transferência desse valor para a cache
				
				// Atualiza a cache
				if (mem_access_done) begin
					cache[exit_index[1]][exit_index[0]][12:8] <= address[4:0];   // Tag
               cache[exit_index[1]][exit_index[0]][7:0] <= qRAM;             // Dados
               cache[exit_index[1]][exit_index[0]][16] <= 1'b1;              // Valid
               cache[exit_index[1]][exit_index[0]][15] <= 1'b0;              // Dirty
				end
				
			end
			
			3'd3: // Atualiza LRU
			begin
				
				// Posição Acessada - LRU 0
				// Todas as posições da cache atualizam LRU
            if (cache[indexCache[1]][indexCache[0]][14:13] == 2'b00) begin
					
					// Atualiza a Posição Acessada
               cache[indexCache[1]][indexCache[0]][14:13] <= 3;

					
					// Atualiza Demais Posições
					for (index = 0; index < 4; index = index + 1) begin
						if(index != indexCache) begin
                  cache[indexCache[1]][index][14:13] <= cache[indexCache[1]][index][14:13] - 1;
						end
					end
					
				end
				
				// Posição Acessada - LRU 1
				// Somente a posição acessada e as posições que possuem LRU > 1 atualizam LRU
            else if (cache[indexCache[1]][indexCache[0]][14:13] == 2'b01) begin

				
					// Atualiza a Posição Acessada
               cache[indexCache[1]][indexCache[0]][14:13] <= 2'b11; // Define o LRU para 3

					
					// Atualiza Demais Posições
					for (index = 0; index < 4; index = index + 1) begin
               if(index != indexCache[0] && cache[indexCache[1]][index][14:13] > 1) begin

               cache[indexCache[1]][index][14:13] <= cache[indexCache[1]][index][14:13] - 1;

						end
					end
					
				end
				
				// Posição Acessada - LRU 2
				// Somente a posição acessada e as posições que possuem LRU > 2 atualizam LRU
            else if (cache[indexCache[1]][indexCache[0]][14:13] == 2'b10) begin

				
					// Atualiza a Posição Acessada
               cache[indexCache[1]][indexCache[0]][14:13] <= 2'b11;

					
					// Atualiza Demais Posições
					for (index = 0; index < 4; index = index + 1) begin
               if (index != indexCache[0] && cache[indexCache[1]][index][14:13] > 2) begin

               cache[indexCache[1]][index][14:13] <= cache[indexCache[1]][index][14:13] - 1;

						end
					end
					
				end
				
				// Posição Acessada - LRU 3
				// Nesse caso não é necessário alterar a LRU de nenhuma posição da cache
            lru0 <= cache[0][0][14:13];
            lru1 <= cache[1][0][14:13];
            lru2 <= cache[1][2][14:13];
            lru3 <= cache[1][3][14:13];


				
			end
			
		endcase
		
	end
	
endmodule
