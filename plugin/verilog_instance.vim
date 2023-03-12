" Create Verilog port instantiation from port declaration
" Maintainer:   Antoine Madec <http://github.com/antoinemadec/>

if exists("g:loaded_verilog_instance") || &cp
  finish
endif
let g:loaded_verilog_instance = 1

let s:plugin_dir_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

if !get(g:, 'verilog_instance_skip_last_coma')
  let g:verilog_instance_skip_last_coma = 0
endif

if !get(g:, 'verilog_instance_keep_comments')
  let g:verilog_instance_keep_comments = 0
endif

if !get(g:, 'verilog_instance_keep_empty_lines')
  let g:verilog_instance_keep_empty_lines = 0
endif

function! s:VerilogInstance(type,...) abort
  if a:0
    let [lnum1, lnum2] = [a:type, a:1]
  else
    let [lnum1, lnum2] = [line("'["), line("']")]
  endif
  let cmd = lnum1 . "norm! =="
  execute cmd
  let cmd = lnum1 . "," . lnum2 . "!" . " " . s:plugin_dir_path . "/verilog_instance.py " . g:verilog_instance_skip_last_coma . g:verilog_instance_keep_comments . g:verilog_instance_keep_empty_lines
  execute cmd
endfunction

xnoremap <silent> <Plug>VerilogInstance     :<C-U>call <SID>VerilogInstance(line("'<"),line("'>"))<CR>
nnoremap <silent> <Plug>VerilogInstance     :<C-U>set opfunc=<SID>VerilogInstance<CR>g@
nnoremap <silent> <Plug>VerilogInstanceLine :<C-U>set opfunc=<SID>VerilogInstance<Bar>exe 'norm! 'v:count1.'g@_'<CR>
command! -range VerilogInstance call s:VerilogInstance(<line1>,<line2>)

if !hasmapto('<Plug>VerilogInstance') && maparg('gb','n') ==# ''
  xmap gb  <Plug>VerilogInstance
  nmap gb  <Plug>VerilogInstance
  nmap gbb <Plug>VerilogInstanceLine
endif
