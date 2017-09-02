function! VerilogInstance() range
  let cmd=a:firstline . "," . a:lastline . "!" . "verilog_instance.py"
  execute cmd
  let cmd=a:firstline . "," . a:lastline . "norm =="
  execute cmd
endfunction
