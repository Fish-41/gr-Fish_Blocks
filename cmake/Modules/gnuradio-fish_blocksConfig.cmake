find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_FISH_BLOCKS gnuradio-fish_blocks)

FIND_PATH(
    GR_FISH_BLOCKS_INCLUDE_DIRS
    NAMES gnuradio/fish_blocks/api.h
    HINTS $ENV{FISH_BLOCKS_DIR}/include
        ${PC_FISH_BLOCKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_FISH_BLOCKS_LIBRARIES
    NAMES gnuradio-fish_blocks
    HINTS $ENV{FISH_BLOCKS_DIR}/lib
        ${PC_FISH_BLOCKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-fish_blocksTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_FISH_BLOCKS DEFAULT_MSG GR_FISH_BLOCKS_LIBRARIES GR_FISH_BLOCKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_FISH_BLOCKS_LIBRARIES GR_FISH_BLOCKS_INCLUDE_DIRS)
