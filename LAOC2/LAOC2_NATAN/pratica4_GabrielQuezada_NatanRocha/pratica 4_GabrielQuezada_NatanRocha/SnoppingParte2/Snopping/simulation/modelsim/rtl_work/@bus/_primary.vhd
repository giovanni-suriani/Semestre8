library verilog;
use verilog.vl_types.all;
entity \Bus\ is
    port(
        i_P0            : in     vl_logic_vector(23 downto 0);
        i_P1            : in     vl_logic_vector(23 downto 0);
        i_P3            : in     vl_logic_vector(23 downto 0);
        i_Mem           : in     vl_logic_vector(23 downto 0);
        o_PO            : out    vl_logic_vector(23 downto 0)
    );
end \Bus\;
