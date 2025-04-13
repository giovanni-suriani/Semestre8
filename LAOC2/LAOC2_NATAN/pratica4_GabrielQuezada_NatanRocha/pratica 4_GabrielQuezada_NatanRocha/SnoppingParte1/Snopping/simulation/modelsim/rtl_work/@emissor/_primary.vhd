library verilog;
use verilog.vl_types.all;
entity Emissor is
    port(
        i_Clock         : in     vl_logic;
        i_Start         : in     vl_logic;
        i_Operation     : in     vl_logic_vector(1 downto 0);
        o_Message       : out    vl_logic_vector(1 downto 0)
    );
end Emissor;
