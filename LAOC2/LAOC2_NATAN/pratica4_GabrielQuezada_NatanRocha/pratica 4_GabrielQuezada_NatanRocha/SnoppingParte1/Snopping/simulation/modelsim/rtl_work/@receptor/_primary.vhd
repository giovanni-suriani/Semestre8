library verilog;
use verilog.vl_types.all;
entity Receptor is
    port(
        i_Message       : in     vl_logic_vector(1 downto 0)
    );
end Receptor;
