import os
import tempfile

__author__ = 'Peipei YI'


class Exp():
    """
    using this to unify runtime environment
    """
    def __init__(self, working_dir='working', task='pilot_'):
        if os.path.exists(working_dir):
            self.working_dir = working_dir
        else:
            self.working_dir = os.path.expanduser(os.path.join('~', working_dir, ''))
        self.temp_dir = os.path.join(tempfile.gettempdir(), task, '')
        if not os.path.isdir(self.temp_dir):
            os.mkdir(self.temp_dir)

    def __repr__(self):
        attr_list = filter(lambda attr_name: not attr_name.startswith('_'), dir(self))
        return '\n'.join(attr_name + '\t' + self.__dict__.get(attr_name) for attr_name in attr_list)

if __name__ == '__main__':
    exp = Exp()
    print exp.__repr__()
