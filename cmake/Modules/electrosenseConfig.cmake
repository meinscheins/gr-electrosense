if(NOT PKG_CONFIG_FOUND)
    INCLUDE(FindPkgConfig)
endif()
PKG_CHECK_MODULES(PC_ELECTROSENSE electrosense)

FIND_PATH(
    ELECTROSENSE_INCLUDE_DIRS
    NAMES electrosense/api.h
    HINTS $ENV{ELECTROSENSE_DIR}/include
        ${PC_ELECTROSENSE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ELECTROSENSE_LIBRARIES
    NAMES gnuradio-electrosense
    HINTS $ENV{ELECTROSENSE_DIR}/lib
        ${PC_ELECTROSENSE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/electrosenseTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ELECTROSENSE DEFAULT_MSG ELECTROSENSE_LIBRARIES ELECTROSENSE_INCLUDE_DIRS)
MARK_AS_ADVANCED(ELECTROSENSE_LIBRARIES ELECTROSENSE_INCLUDE_DIRS)
