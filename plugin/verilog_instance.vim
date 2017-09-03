if exists("g:loaded_verilog_instance") || &cp || v:version < 700
  finish
endif
let g:loaded_verilog_instance = 1

let s:plugin_dir_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:VerilogInstance() range
  let cmd=a:firstline . "," . a:lastline . "!" . " " . s:plugin_dir_path. "/verilog_instance.py"
  execute cmd
  let cmd=a:firstline . "," . a:lastline . "norm! =="
  execute cmd
endfunction

command! -range VerilogInstance call s:VerilogInstance()
