#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Electosense
# Author: Sreeraj Rajendran
# Description: Electrosense sensor code
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import electrosense
import osmosdr
import time
import pmt
import scanning  # embedded python module
import threading

from gnuradio import qtgui

class electrosense_hopping(gr.top_block, Qt.QWidget):

    def __init__(self, end_f=500e6, parameter_0=0, start_f=50e6):
        gr.top_block.__init__(self, "Electosense")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Electosense")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "electrosense_hopping")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.end_f = end_f
        self.parameter_0 = parameter_0
        self.start_f = start_f

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.prober = prober = 1
        self.hop_mode = hop_mode = 1
        self.variable_0 = variable_0 = 0
        self.tune_delay = tune_delay = 50e-3
        self.sensorid = sensorid = 123456
        self.rfgain = rfgain = 40
        self.ppm = ppm = 0
        self.navg_vectors = navg_vectors = 100
        self.fft_size = fft_size = 512
        self.cfreq = cfreq = scanning.step(start_f,end_f,samp_rate/1.5,prober,hop_mode,0.8,0.8)
        self.alpha = alpha = 0.75

        ##################################################
        # Blocks
        ##################################################
        self.vecprobe = blocks.probe_signal_vf(fft_size)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(alpha, fft_size)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(cfreq, 0)
        self.rtlsdr_source_0.set_freq_corr(ppm, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(rfgain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(250e3, 0)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_size,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-140, 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        def _prober_probe():
            while True:

                val = self.vecprobe.level()
                try:
                    self.set_prober(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1/(tune_delay+(1/samp_rate*fft_size*navg_vectors))))
        _prober_thread = threading.Thread(target=_prober_probe)
        _prober_thread.daemon = True
        _prober_thread.start()

        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, window.blackmanharris(fft_size), True, 1)
        self.electrosense_discard_samples_0 = electrosense.discard_samples(int(tune_delay * samp_rate), int(cfreq), pmt.intern("burst_len"), False)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, fft_size, 0)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*fft_size, navg_vectors)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.vecprobe, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.electrosense_discard_samples_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.electrosense_discard_samples_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "electrosense_hopping")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_end_f(self):
        return self.end_f

    def set_end_f(self, end_f):
        self.end_f = end_f
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_parameter_0(self):
        return self.parameter_0

    def set_parameter_0(self, parameter_0):
        self.parameter_0 = parameter_0

    def get_start_f(self):
        return self.start_f

    def set_start_f(self, start_f):
        self.start_f = start_f
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))
        self.electrosense_discard_samples_0.set_nsamples(int(self.tune_delay * self.samp_rate))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_prober(self):
        return self.prober

    def set_prober(self, prober):
        self.prober = prober
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_hop_mode(self):
        return self.hop_mode

    def set_hop_mode(self, hop_mode):
        self.hop_mode = hop_mode
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_variable_0(self):
        return self.variable_0

    def set_variable_0(self, variable_0):
        self.variable_0 = variable_0

    def get_tune_delay(self):
        return self.tune_delay

    def set_tune_delay(self, tune_delay):
        self.tune_delay = tune_delay
        self.electrosense_discard_samples_0.set_nsamples(int(self.tune_delay * self.samp_rate))

    def get_sensorid(self):
        return self.sensorid

    def set_sensorid(self, sensorid):
        self.sensorid = sensorid

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.rtlsdr_source_0.set_gain(self.rfgain, 0)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.rtlsdr_source_0.set_freq_corr(self.ppm, 0)

    def get_navg_vectors(self):
        return self.navg_vectors

    def set_navg_vectors(self, navg_vectors):
        self.navg_vectors = navg_vectors
        self.blocks_keep_one_in_n_0.set_n(self.navg_vectors)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self.electrosense_discard_samples_0.set_var(int(self.cfreq))
        self.rtlsdr_source_0.set_center_freq(self.cfreq, 0)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.single_pole_iir_filter_xx_0.set_taps(self.alpha)




def argument_parser():
    description = 'Electrosense sensor code'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--end-f", dest="end_f", type=eng_float, default="500.0M",
        help="Set End Frequency [default=%(default)r]")
    parser.add_argument(
        "--start-f", dest="start_f", type=eng_float, default="50.0M",
        help="Set Start frequency [default=%(default)r]")
    return parser


def main(top_block_cls=electrosense_hopping, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(end_f=options.end_f, start_f=options.start_f)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
