### windows-only: [


# start delvewheel patch
def _delvewheel_patch_1_12_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'meshlib.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-meshlib-3.1.0.75')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-meshlib-3.1.0.75')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_12_0()
del _delvewheel_patch_1_12_0
# end delvewheel patch

# Fixes DLL loading paths.

def _init_patch():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    os.add_dll_directory(libs_dir)

_init_patch()
del _init_patch

### ]


### wheel-only: [

def _override_resources_dir():
    """
    override resources directory to the package's dir
    """
    import pathlib
    from . import mrmeshpy as mr

    mr.SystemPath.overrideDirectory(mr.SystemPath.Directory.Resources, pathlib.Path(__file__).parent.resolve())
    mr.SystemPath.overrideDirectory(mr.SystemPath.Directory.Fonts, pathlib.Path(__file__).parent.resolve())

_override_resources_dir()
del _override_resources_dir

### ]
