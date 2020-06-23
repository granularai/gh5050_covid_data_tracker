
class PluginBaseError(Exception):
    """Raised when a plugin cannot be used"""

    def __init__(self, plugin_name):
        message = f"Unable to use {plugin_name}"
        super().__init__(message)

    def __repr__(self):
        return self.message


class PluginAttributeMissingError(PluginBaseError):
    """Raised when a plugin is missing a required attribute"""
    def __init__(self, plugin_name, required):
        message = (f"Cannot instantiate class {plugin_name} "
                   f"without {required} attribute defined")
        super().__init__(message)


class PluginValidationError(PluginBaseError):
    """Raised when a plugin is missing a required attribute"""
    def __init__(self, plugin_name):
        message = f"Cannot validate class {plugin_name} results"
        super().__init__(message)


class UserDefinedValidationFailed(PluginValidationError):
    """Raised when a plugin is missing a required attribute"""
    def __init__(self, plugin_name):
        message = f"{plugin_name} validation rules defined by user failed"
        super().__init__(message)


class EmptySexTable(PluginValidationError):
    """Raised when a plugin is missing a required attribute"""
    def __init__(self, plugin_name):
        message = f"No data retrieved for {plugin_name}"
        super().__init__(message)
