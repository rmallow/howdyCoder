class multiBase:
    """
    For use in multiple inheritance, consumes args and kwargs
    Call object.__init__ without arguments
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
