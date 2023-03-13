module sub_block(
  input                         clk,   // 50 MHz clk
  input /* foo */               rstn,
  /* interface
  * network_if.IN   i0, i1,
  * network_if.OUT  o0, o1
  */
  fifo_if_.IN                   i0, i1,  // fifo in
  fifo_if_.OUT                  o0, o1,

  input custom_t                data_in,
  // output
  output reg[31:0] /*comment*/  reg32_out,
  output custom_t               data_out
);
