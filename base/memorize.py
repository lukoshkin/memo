import random
import time

from pathlib import Path
from subprocess import run as shell


class PatientLearner:
    def __init__(self, infile, timeout, just_notify=True):
        self.time = timeout
        self.file = infile
        self.edit = False

        if just_notify: self._method = self._justNotify
        else: self._method = self._windowEdit

    def _justNotify(self, pair):
        # Ubuntu's Notify OSD and GNOME Shell
        # both ignore the timeout parameter.
        # Instead, we use '--hint=int:transient:1'
        # to remove the notification more quickly.
        shell([
            'notify-send',
            '--hint=int:transient:1',
            f'--icon={Path.cwd()}/logo.png',
            f'--expire-time={self.time*1000}',
            f'{pair}'])

    def _windowEdit(self, pair):
        out = shell([
            'zenity', '--title=Word-Translation',
            f'--timeout={self.time}', '--list', '--editable',
            '--hide-header', '--width=600', # '--height=100',
            '--column=0', f'{pair}'], capture_output=True)

        newpair = out.stdout.decode('utf-8').strip()

        if newpair and pair != newpair:
            self.read.remove(pair)
            self.read.append(newpair)
            print("Corrected successfully!")
            print(f'<{pair}> -> <{newpair}>')
            if not self.edit: self.edit = True

    def _genDict(self):
        with open(self.file, 'r') as fp:
            self.read = fp.read().splitlines()

        random.shuffle(self.read)
        for pair in self.read:
            yield pair

    def _isIdle(self):
        cmd = 'xset q | grep Monitor | grep -q On'
        EC = shell(cmd, shell=True).returncode

        idle = int(shell(
                ['xprintidle'], capture_output=True
                ).stdout.decode('utf-8').strip())

        if EC or idle > 6e5: return True
        return False

    def train(self, delay):
        try:
            gen = self._genDict()
            for pair in gen:
                self._method(pair)
                while self._isIdle(): time.sleep(delay)
                else: time.sleep(delay)
        except KeyboardInterrupt:
            if self.edit:
                with open(self.file, 'w') as fp:
                    for line in self.read: fp.write(f'{line}\n')

