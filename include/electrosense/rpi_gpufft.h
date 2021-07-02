/* -*- c++ -*- */
/*
 * Copyright 2021 gr-electrosense author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */


#ifndef INCLUDED_ELECTROSENSE_RPI_GPUFFT_H
#define INCLUDED_ELECTROSENSE_RPI_GPUFFT_H

#include <electrosense/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace electrosense {

    /*!
     * \brief <+description of block+>
     * \ingroup electrosense
     *
     */
    class ELECTROSENSE_API rpi_gpufft : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<rpi_gpufft> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of electrosense::rpi_gpufft.
       *
       * To avoid accidental use of raw pointers, electrosense::rpi_gpufft's
       * constructor is in a private implementation
       * class. electrosense::rpi_gpufft::make is the public interface for
       * creating new instances.
       */
      static sptr make(int fft_size, bool forward,
							  bool shift, int njobs);
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_RPI_GPUFFT_H */
