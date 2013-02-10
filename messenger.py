import settings

def respect_debug(print_func):
    def wrapper(self, *args, **kwargs):
        if settings.DEBUG == False:
            return
        return print_func(self, *args, **kwargs)

    return wrapper

class Messenger:

    INDENTATION_BULLETS = {
        0: '*',
        1: '->',
        2: '+',
    }

    def __init__(self):
        self.indentation_spaces = 4
        self.level = 0

    def bullet_symbol(self, relative_level=0):
        level = self.level + relative_level
        return self.INDENTATION_BULLETS.get(level, '-')

    @respect_debug
    def print_task(self, message):
        self.level -= 1
        print '%s %s..' % (self.INDENTATION_BULLETS[0], message)
        self.level += 1

    @respect_debug
    def print_task_error(self, message):
        self.level -= 1
        print '! [ERROR] %s' % message
        self.level += 1

    @respect_debug
    def print_subtask(self, message, relative_level=0):
        self.level += 1
        print '%s%s %s' % (
            ' ' * self.indentation_spaces * (self.level + relative_level),
            self.bullet_symbol(relative_level),
            message
        )
        self.level -= 1

    @respect_debug
    def print_subtask_error(self, message, relative_level=0):
        self.level += 1
        print '%s! [ERROR] %s' % (
            ' ' * self.indentation_spaces * (self.level + relative_level),
            message
        )
        self.level -= 1

messenger = Messenger()
