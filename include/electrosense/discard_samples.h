/* -*- c++ -*- */
/*
 * Copyright 2021 gr-electrosense author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */


#ifndef INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H
#define INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H

#include <electrosense/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace electrosense {

    /*!
     * \brief <+description of block+>
     * \ingroup electrosense
     *
     */
    class ELECTROSENSE_API discard_samples : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<discard_samples> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of electrosense::discard_samples.
       *
       * To avoid accidental use of raw pointers, electrosense::discard_samples's
       * constructor is in a private implementation
       * class. electrosense::discard_samples::make is the public interface for
       * creating new instances.
       */
      static sptr make(double nsamples, double var, pmt::pmt_t tag_name, bool mode);

	  virtual void set_nsamples(double d_nsamples) = 0;
	  virtual void set_var(double d_var) = 0;
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H */
