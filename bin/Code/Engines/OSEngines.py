# macOS stub for Windows-only OSEngines
def __getattr__(name):
    # Return a dummy function for any attribute
    return lambda *args, **kwargs: None
