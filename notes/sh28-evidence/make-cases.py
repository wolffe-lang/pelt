"""Create sh28's oracle inputs; expectations are recorded, never inferred."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
CASES = {
 'last_arg': [': alpha', r'\k echo \e.\r'],
 'last_alias': [': alpha', r'\k echo \e_\r'],
 'last_repeat': [': older', ': newer', r'\k echo \e.\e.\r'],
 'last_quote': [": 'two words'", r'\k echo \e.\r'],
 'last_redir': [': value > output', r'\k echo \e.\r'],
 'last_single': ['true', r'\k echo \e.\r'],
 'last_oldest': [': oldest', r'\k echo \e.\e.\e.\r'],
 'last_numeric': [': first second third', r'\k echo \e1\e.\r'],
 'last_zero': [': first second', r'\k echo \e0\e.\r'],
 'last_midline': [': inserted', r'\k echo  tail\x01\ef \e.\r'],
 'last_interrupted': [': one', ': two', r'\k echo \e. \e.\r'],
 'yank_pop': [r'\k first\x15\x01second\x15echo \x19\ey\r'],
 'yank_pop_invalid': [r'\k echo hi\ey\r'],
 'transpose_chars': [r'\k echo ab\x14\r'],
 'transpose_chars_middle': [r'\k echo abcd\x02\x02\x14\r'],
 'transpose_words': [r'\k echo one two\et\r'],
 'upcase': [r'\k echo hello\eb\eu\r'],
 'downcase': [r'\k echo HELLO\eb\el\r'],
 'capitalize': [r'\k echo hELLO\eb\ec\r'],
 'undo': [r'\k echo base\x17new\x1f\r'],
 'undo_alias': [r'\k echo base\x17new\x18\x15\r'],
 'undo_twice': [r'\k echo base\x17new\x1f\x1f\r'],
 'revert': [': original', r'\k \x10 changed\er\r'],
 'history_first': ['echo oldest', 'echo newest', r'\k \e<\r'],
 'history_last': ['echo older', r'\k echo saved\x10\e>\r'],
 'comment': [r'\k echo forbidden\e#', 'echo survived'],
 'horizontal_space': [r'\k echo one   two\eb\e\\\r'],
 'character_search': [r'\k echo abcabc\x01\x1dbX\r'],
 'character_search_back': [r'\k echo abcabc\e\x1dbX\r'],
 'numeric_insert': [r'\k echo \e3x\r'],
 'numeric_motion': [r'\k echo abcd\e2\x02X\r'],
 'numeric_negative': [r'\k echo abcd\e-2\x02X\r'],
 'numeric_multi': [r'\k echo \e1\e2x\r'],
 'numeric_zero': [r'\k echo \e0x\r'],
 'abort_prefix': [r'\k echo good\x18\x07\r'],
 'abort_search': [': old', r'\k echo kept\x12old\x07\r'],
 'mark_exchange': [r'\k echo abcd\x00\x02\x02\x18\x18X\r'],
 'mark_exchange_twice': [r'\k echo abcd\x00\x02\x02\x18\x18\x18\x18X\r'],
 'search_abort': [r'\k echo kept\x1d\x07\r'],
 'vi_last_arg': [': one two', r'\k echo\e_\r'],
 'vi_last_quote': [": 'two words'", r'\k echo\e_\r'],
}
CASES.update({
 'quit_status': ["trap 'echo trapped' QUIT", 'false', r'\k echo forbidden\x1c', "printf 'status:%s\\n' $?:end"],
 'quit_remapped': ["stty quit '^E'", r'\k echo forbidden\x05', 'echo survived'],
 'vi_quit_insert': [r'\k echo forbidden\x1c', 'echo survived'],
 'vi_quit_command': [r'\k echo forbidden\e\x1c', 'echo survived'],
 'quit_search': [': old', 'false', r'\k \x12old\x1c', "printf 'status:%s\\n' $?:end"],
 'numeric_quoted': [r'\k echo \e3\x16x\r'],
 'transpose_negative': [r'\k echo one two three\e-\et!\r'],
 'mark_meta_space': [r'\k echo abcd\e \x02\x02\x18\x18X\r'],
 'mark_tracks_insert': [r'\k echo abcd\e \x01 \x18\x18X\r'],
 'abort_character_search_back': [r'\k echo kept\e\x1d\x07\r'],
 'yank_pop_wrap': [r'\k first\x15\x01second\x15echo \x19\ey\ey\r'],
 'quoted_last_arg': [r': one\ two', r'\k echo \e.\r'],
 'comment_toggle': [r'\k #echo accepted\e1\e#'],
 'last_reverse': [': older', ': newer', r'\k echo \e.\e.\e-\e.\r'],
 'undo_recalled': ['echo original', r'\k \x10\x17changed\x1f\x1f\r'],
 'case_upper_alias': [r'\k echo hello\eb\eU\r'],
 'kill_ring_ten': [r'\k ' + ''.join('k'+str(i)+r'\x15\x01' for i in range(12)) + r'echo \x19' + r'\ey'*9 + r'\r'],
 'pageup': ['echo oldest', 'echo newest', r'\k \e[5~\r'],
 'pagedown': ['echo prior', r'\k echo draft\x10\e[6~\r'],
 'undo_after_move': [r'\k echo abc\x02X\x1f\r'],
 'last_negative': [': one two three', r'\k echo \e-2\e.\r'],
 'case_negative': [r'\k echo hello\e-\eu!\r'],
 'numeric_delete': [r'\k echo abcde\e3\x7f\r'],
 'abort_numeric': [r'\k echo good\e3\x07!\r'],
 'kill_across_lines': [r'\k echo first\x01\ef\x06\x0b\r', r'\k echo second\x01\ef\x06\x0b\r', r'\k echo \x19\ey\r'],
})
for name, steps in CASES.items():
    if sys.argv[1:] and "sh28_"+name not in sys.argv[1:]:
        continue
    base = ROOT / 'tests/session' / ('sh28_' + name)
    base.with_suffix('.keys').write_text('\n'.join(['exec 2>&0'] + steps + ['exit']) + '\n')
    vi = name.startswith('vi_')
    base.with_suffix('.meta').write_text(
        'oracle=bash\ncompare=stdout\n' + ('args=-o vi\n' if vi else '') +
        'env=PS1=$\\s' + (' HISTSIZE=1' if name == 'last_oldest' else '') + '\npelt_args=-i -o friendly' + (' -o vi' if vi else '') + '\n' +
        'why=sh28 black-box bash 5.3.20-2, dash 0.5.13.4-1.1, fish 4.9.3-1; Arch image id 3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f digest sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785; measured twice by notes/sh28-evidence/record.py, see logs/record-terminal.log\n')
