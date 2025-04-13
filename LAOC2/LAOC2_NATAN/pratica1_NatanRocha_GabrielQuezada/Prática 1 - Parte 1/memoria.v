module memoria(SW, LEDG, LEDR, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, HEX6, HEX7);
    input [17:0] SW;
    output [0:6] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, HEX6, HEX7;
    output [7:0] LEDG;   // LEDs verdes
    output [17:0] LEDR;  // LEDs vermelhos
    wire [4:0] address;  // Endereço
    wire [7:0] data;     // Dados
    wire clock;          // Sinal de clock
    wire wren;           // Habilitador de escrita
    wire [7:0] out;      // Saída

    // Geração do sinal de clock
    assign clock = SW[17];
    assign LEDG[1:1] = clock;
    assign LEDG[0:0] = ~clock;

    // Controle de escrita na memória
    assign wren = SW[16];
    assign LEDR[0:0] = ~wren;
    assign LEDG[7:7] = wren;

    // Dados a serem escritos na memória (entrada)
    assign data = SW[13:6];

    // Endereço da posição de memória (saída)
    assign address = SW[4:0];

    // Instância do módulo de memória RAM
    ramlpm RAM(address, clock, data, wren, out);

    // Desativação dos displays 7 segmentos HEX2 e HEX3
    assign HEX2 = 7'b1111111;
    assign HEX3 = 7'b1111111;

    // Instâncias dos módulos de display 7 segmentos
    disp7seg dispSeg1(out[7:4], HEX1);      // Conteúdo da memória (saída)
    disp7seg dispSeg0(out[3:0], HEX0);
    disp7seg dispSeg5(address[4:4], HEX5);  // Endereço da posição de memória
    disp7seg dispSeg4(address[3:0], HEX4);
    disp7seg dispSeg7(data[7:4], HEX7);     // Dado inserido na memória (entrada)
    disp7seg dispSeg6(data[3:0], HEX6);

	 endmodule





