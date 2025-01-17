/*
 * Copyright 2021 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(rpi_gpufft.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(6a2bb30c8b08d5ddcd2421bbd76c5ad4)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <electrosense/rpi_gpufft.h>
// pydoc.h is automatically generated in the build directory
#include <rpi_gpufft_pydoc.h>

void bind_rpi_gpufft(py::module& m)
{

    using rpi_gpufft    = gr::electrosense::rpi_gpufft;


    py::class_<rpi_gpufft,
        std::shared_ptr<rpi_gpufft>>(m, "rpi_gpufft", D(rpi_gpufft))

        .def(py::init(&rpi_gpufft::make),
           py::arg("fft_size"),
           py::arg("forward"),
           py::arg("shift"),
           py::arg("njobs"),
           D(rpi_gpufft,make)
        )
        



        ;




}








