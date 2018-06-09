class UncertaintyException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Number of deleted candies exceeds the desired maximun ratio (known vs. unknown ' \
                                 'candies)')


class WrappedChocolateException(UncertaintyException):
    def __init__(self):
        UncertaintyException.__init__(self)
