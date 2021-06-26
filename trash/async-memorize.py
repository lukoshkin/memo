import sys
import random
import asyncio

from subprocess import run as shell


delay = 20
timeout = 10
infile = sys.argv[1]


with open(infile, 'r') as fp:
    read = fp.read().splitlines()

async def notify():
    correct = 0
    pair = random.choice(read)
    out = shell([
        'zenity', '--title=Word-Translation',
        f'--timeout={timeout}', '--list', '--editable',
        '--hide-header', '--width=600', # '--height=100',
        '--column=0', f'{pair}'], capture_output=True)

    newpair = out.stdout.decode('utf-8').strip()
    print('pair', f'<{pair}>', type(newpair))
    print('new pair', f'<{newpair}>', type(newpair))

    if newpair and pair != newpair:
        read.remove(pair)
        read.append(newpair)
        correct = 1
        print("Corrected successfully!")

    await asyncio.sleep(delay)
    return correct


correct = 0

try:
    while True: correct += asyncio.run(notify())
except KeyboardInterrupt:
    print(correct)
    if correct > 0:
        print("IF in TRY")
        with open(infile, 'r') as fp:
            for line in read:
                fp.write(line)
