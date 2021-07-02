/* -*- c++ -*- */
/*
 * Copyright 2021 gr-electrosense author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "rpi_gpufft_impl.h"

namespace gr {
	namespace electrosense {

		rpi_gpufft::sptr
			rpi_gpufft::make(int fft_size, bool forward,
					bool shift, int njobs)
			{
				return gnuradio::get_initial_sptr
					(new rpi_gpufft_impl(fft_size, forward,
										 shift, njobs));
			}

		/*
		 * The private constructor
		 */
		rpi_gpufft_impl::rpi_gpufft_impl(int fft_size, bool forward,
				bool shift, int njobs)
			: gr::sync_block("rpi_gpufft",
					gr::io_signature::make(1, 1, fft_size * sizeof(gr_complex)),
					gr::io_signature::make(1, 1, fft_size * sizeof(gr_complex))),
			d_fft_size(fft_size),
			d_forward(forward),
			d_shift(shift),
			d_njobs(njobs)
		{
			int v, log2_N, dir, ret;

			if(forward)
			{
				dir = GPU_FFT_FWD;
			}
			else
			{
				dir = GPU_FFT_REV;
			}

			log2_N = 8;
			for(v=8; v<=22; v++)
			{
				if((1<<v) == d_fft_size)
				{
					log2_N = v;
					break;
				}
			}
			d_mb = mbox_open();
			ret = gpu_fft_prepare(d_mb, log2_N, dir, d_njobs, &d_fft);
			set_output_multiple(njobs);

		}

		/*
		 * Our virtual destructor.
		 */
		rpi_gpufft_impl::~rpi_gpufft_impl()
		{
			gpu_fft_release(d_fft); 
		}

		int
			rpi_gpufft_impl::work(int noutput_items,
					gr_vector_const_void_star &input_items,
					gr_vector_void_star &output_items)
			{
				const gr_complex *in = (const gr_complex *) input_items[0];
				gr_complex *out = (gr_complex *) output_items[0];

				int i,j,count;
				unsigned int len = (unsigned int)(ceil(d_fft_size/2.0));

				count=0;

				while(count<=noutput_items)
				{
					for (j=0; j<d_njobs; j++) {
						d_base = d_fft->in + j*d_fft->step; 
						for (i=0; i<d_fft_size; i++) 
						{
							d_base[i].re = in[i].real();
							d_base[i].im = in[i].imag();
						}
						in += d_fft_size;
					}

					gpu_fft_execute(d_fft); 

					for (j=0; j<d_njobs; j++) {
						d_base = d_fft->out + j*d_fft->step; 

						if(d_shift)
						{
							for (i=0; i<d_fft_size; i++) {
								out[i].real(d_base[(len+i)%d_fft_size].re) ;
								out[i].imag(d_base[(len+i)%d_fft_size].im) ;
							}
						}
						else
						{
							for (i=0; i<d_fft_size; i++) {
								out[i].real(d_base[i].re) ;
								out[i].imag(d_base[i].im) ;
							}
						}

						out += d_fft_size;
					}


					count += d_njobs;
				}


				return noutput_items;
			}

	} /* namespace electrosense */
} /* namespace gr */

