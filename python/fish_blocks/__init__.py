#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio FISH_BLOCKS module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the fish_blocks namespace
try:
    # this might fail if the module is python-only
    from .fish_blocks_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .vector_sink import vector_sink
from .comp_weight import comp_weight
from .lcmv_weights import lcmv_weights
#
