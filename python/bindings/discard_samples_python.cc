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
/* BINDTOOL_HEADER_FILE(discard_samples.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(e4a9f8b46d39db132c623e951164ebba)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <electrosense/discard_samples.h>
// pydoc.h is automatically generated in the build directory
#include <discard_samples_pydoc.h>

void bind_discard_samples(py::module& m)
{

    using discard_samples    = gr::electrosense::discard_samples;


    py::class_<discard_samples,
        std::shared_ptr<discard_samples>>(m, "discard_samples", D(discard_samples))

        .def(py::init(&discard_samples::make),
           py::arg("nsamples"),
           py::arg("var"),
           py::arg("tag_name"),
           py::arg("mode"),
           D(discard_samples,make)
        )
        



        ;




}







