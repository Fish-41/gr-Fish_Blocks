# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT Fish_Blocks_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT Fish_Blocks_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND Fish_Blocks_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(Fish_Blocks
   ../../..
   gr::Fish_Blocks
   "${Fish_Blocks_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET Fish_Blocks_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:Fish_Blocks_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/Fish_Blocks/
)

install(TARGETS Fish_Blocks_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/Fish_Blocks COMPONENT pythonapi)
