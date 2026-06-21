from __future__ import print_function

from .debug import err
from . import zenv, blorb, ops, term

def run_game(
        args,
        callback_output=lambda x:0,
):
    path = args.STORY_FILE_OR_URL
    try:
        with open(path, 'rb') as f:
            mem = f.read()
    except IOError as e:
        err('could not load file:', e)

    vm_type = b'ZCOD'

    if blorb.is_blorb(mem):
        codeChunk = blorb.get_code_chunk(mem)
        if not codeChunk:
            err('no runnable game code found in blorb file')
        mem = codeChunk.data
        vm_type = codeChunk.name

    if vm_type == b'ZCOD':
        run_zmach(mem, args, callback_output, callback_input)
    else:
        err('unknown game vm type: {}'.format(repr(vm_type)))


def run_zmach(mem, args, callback_output, callback_input):
    env = zenv.Env(mem, args)
    if env.hdr.version not in [1,2,3,4,5,7,8]:
        err('unsupported z-machine version: '+str(env.hdr.version))

    term.init()
    env.screen.first_draw()
    ops.setup_opcodes(env)
    try:
        while True:
            zenv.step(env)
            callback_output(env.screen.get_output())
    except KeyboardInterrupt:
        pass

