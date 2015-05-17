#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sat May 16 15:47:06 2015
##################################################

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import sys
import time

from distutils.version import StrictVersion
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.raw_samp_rate = raw_samp_rate = 2e6
        self.decimation = decimation = 8
        self.sym_rate = sym_rate = 2400
        self.samp_rate = samp_rate = raw_samp_rate/decimation
        self.half_dev = half_dev = 40e3
        self.freq_offset = freq_offset = 500
        self.bin_width = bin_width = 10e3

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(raw_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(450E6, 8E6), 0)
        self.uhd_usrp_source_0.set_gain(30, 0)
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, samp_rate, 10e3, 300, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(decimation, firdes.low_pass(
        	2, raw_samp_rate, 250e3, 50e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, "samples", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(False))
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate, -half_dev-bin_width/2+freq_offset, -half_dev+bin_width/2+freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate, +half_dev-bin_width/2+freq_offset, +half_dev+bin_width/2+freq_offset, 500, firdes.WIN_HAMMING, 6.76))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.low_pass_filter_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_valve_0, 0))
        self.connect((self.blks2_valve_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_null_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_raw_samp_rate(self):
        return self.raw_samp_rate

    def set_raw_samp_rate(self, raw_samp_rate):
        self.raw_samp_rate = raw_samp_rate
        self.set_samp_rate(self.raw_samp_rate/self.decimation)
        self.uhd_usrp_source_0.set_samp_rate(self.raw_samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(2, self.raw_samp_rate, 250e3, 50e3, firdes.WIN_HAMMING, 6.76))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_samp_rate(self.raw_samp_rate/self.decimation)

    def get_sym_rate(self):
        return self.sym_rate

    def set_sym_rate(self, sym_rate):
        self.sym_rate = sym_rate

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, +self.half_dev-self.bin_width/2+self.freq_offset, +self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.half_dev-self.bin_width/2+self.freq_offset, -self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 10e3, 300, firdes.WIN_HAMMING, 6.76))

    def get_half_dev(self):
        return self.half_dev

    def set_half_dev(self, half_dev):
        self.half_dev = half_dev
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, +self.half_dev-self.bin_width/2+self.freq_offset, +self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.half_dev-self.bin_width/2+self.freq_offset, -self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, +self.half_dev-self.bin_width/2+self.freq_offset, +self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.half_dev-self.bin_width/2+self.freq_offset, -self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))

    def get_bin_width(self):
        return self.bin_width

    def set_bin_width(self, bin_width):
        self.bin_width = bin_width
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, +self.half_dev-self.bin_width/2+self.freq_offset, +self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.half_dev-self.bin_width/2+self.freq_offset, -self.half_dev+self.bin_width/2+self.freq_offset, 500, firdes.WIN_HAMMING, 6.76))

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
