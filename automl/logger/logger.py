from filepath import log_dir


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def write_log(msg):
        try:
            msg_n = "%s\n" % msg
            with open('%s/log.txt' % log_dir, 'a+') as log_file:
                log_file.write(msg_n)
        except FileNotFoundError as e:
            print(e)
