library verilog;
use verilog.vl_types.all;
entity Memory is
    port(
        i_Bus           : in     vl_logic_vector(23 downto 0);
        o_Bus           : out    vl_logic_vector(23 downto 0)
    );
end Memory;
