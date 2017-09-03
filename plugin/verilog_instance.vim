if exists("g:loaded_verilog_instance") || &cp || v:version < 700
  finish
endif
let g:loaded_verilog_instance = 1

let s:plugin_dir_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:VerilogInstance(type,...) abort
  if a:0
    let [lnum1, lnum2] = [a:type, a:1]
  else
    let [lnum1, lnum2] = [line("'["), line("']")]
  endif
  let cmd = lnum1 . "norm! =="
  execute cmd
  let cmd = lnum1 . "," . lnum2 . "!" . " " . s:plugin_dir_path. "/verilog_instance.py"
  execute cmd
endfunction

command! -range VerilogInstance call s:VerilogInstance(<line1>,<line2>)
