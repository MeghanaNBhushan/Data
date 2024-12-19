import os


class Context:
    def __init__(self, root_dir, log_dir, continuous_output, credential_manager, encoding, env=None):
        self.root_dir = root_dir
        self.log_dir = log_dir
        self.continuous_output = continuous_output
        self.encoding = encoding
        self.credential_manager = credential_manager
        if env:
            self.env = env
        else:
            self.env = os.environ.copy()
        ## purge existing virtual env configuration
        if 'VIRTUAL_ENV' in self.env.keys():
            env_path_to_match = self.env.pop('VIRTUAL_ENV')
            if '_' in self.env.keys():
                self.env.pop('_')
            if 'PS1' in self.env.keys():
                self.env.pop('PS1')

            path_list = self.env.get('PATH').split(':')
            for idx, item in enumerate(path_list):
                if env_path_to_match in item:
                    path_list.pop(idx)
            self.env['PATH'] = ':'.join(path_list)

    def get_dir(self, path):
        if path:
            if os.path.isabs(path):
                result = path
            else:
                result = os.path.join(self.root_dir, path)
        else:
            result = self.root_dir

        return os.path.abspath(result)

    def clone(self):
        return Context(self.root_dir, self.log_dir, self.continuous_output, self.credential_manager, self.encoding, self.env)
