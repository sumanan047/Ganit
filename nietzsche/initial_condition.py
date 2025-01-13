class InitialConditions:
    def __init__(self, domain,
                 mode="constant",
                 value = None,
                 funcion = None):
        self.domain = domain
        self.mode = mode
        self.value = value
        self.funcion = funcion
        self.ic_arr = None

    def set(self):
        """
        Description
        ===========
        Set the initial condition based on the specified mode.

        Arguments
        =========
        None

        Keyword arguments
        =================
        None

        Returns
        =======
        None

        Raises
        ======
        ValueError -- If an invalid mode is specified or if the required value or function is not set.
        """
        
        if self.mode == "constant":
            if self.value is None:
                raise ValueError("Value must be set for constant mode")
            self.ic_arr = np.full(self.domain.shape, self.value)
        elif self.mode == "function":
            if self.funcion is None:
                raise ValueError("Function must be set for function mode")
            self.ic_arr = self.funcion(self.domain)
        else:
            raise ValueError("Invalid mode. Choose between constant, function")
        return None