library verilog;
use verilog.vl_types.all;
entity Memory is
    port(
        clock           : in     vl_logic;
        address         : in     vl_logic_vector(3 downto 0);
        writeData       : in     vl_logic_vector(7 downto 0);
        dataOut         : out    vl_logic_vector(7 downto 0);
        MemRead         : in     vl_logic;
        MemWrite        : in     vl_logic
    );
end Memory;
