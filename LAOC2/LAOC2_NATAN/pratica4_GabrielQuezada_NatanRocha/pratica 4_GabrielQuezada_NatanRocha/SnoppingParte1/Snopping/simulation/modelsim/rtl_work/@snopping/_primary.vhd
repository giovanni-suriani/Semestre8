library verilog;
use verilog.vl_types.all;
entity Snopping is
    port(
        i_Start         : in     vl_logic;
        i_Clock         : in     vl_logic;
        i_Operation     : in     vl_logic_vector(1 downto 0)
    );
end Snopping;
