/* -*- c++ -*- */
/*
 * Copyright 2021 gr-electrosense author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H
#define INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H

#include <electrosense/rpi_gpufft.h>

extern "C" {
#include "gpu_fft.h"	
#include "mailbox.h"	
}

namespace gr {
  namespace electrosense {

    class rpi_gpufft_impl : public rpi_gpufft
    {
     private:
	 
		int d_fft_size;
		bool d_forward;
		bool d_shift;
		int d_njobs;
		int d_mb;
    	struct GPU_FFT_COMPLEX *d_base;
    	struct GPU_FFT *d_fft;



     public:
      rpi_gpufft_impl(int fft_size, bool forward,
							  bool shift, int njobs);
      ~rpi_gpufft_impl();

      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H */

