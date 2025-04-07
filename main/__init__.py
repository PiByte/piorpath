from importlib.metadata import PackageNotFoundError, version

__version__ = "1.0.0"
__author__ = "Payam Bijeh"

def _get_version():
    try:
        return version("piorpath")
    except PackageNotFoundError:
        return __version__
    except Exception as e:
        print(f"Version check warning: {str(e)}")
        return __version__

__version__ = _get_version()