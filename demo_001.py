"""
Simple Demo for GCI reference markings

Roger D. Serwy

"""
from pylab import *
from numpy import *
ion()


## quick interface to APLAWDW
import corpus_loader

# Replace with path to full APLAWD database
aplawd = corpus_loader.APLAWD('./mini_aplawd')  

markings = corpus_loader.APLAWD_Markings('./aplawd_gci')

a = aplawd.load(2)  # can be 0, 1, or 2 if using mini_aplawd
gci_ref = markings.load(a.name)


fig = figure(1)
clf()

ax = subplot(311)
t = arange(len(a.s)) / a.fs
plot(t, a.s, alpha=0.5)
ylabel('speech')
title('APLAWD waveform: %s' % a.name)

subplot(312, sharex=ax)
t = arange(len(a.d)) / a.fs

plot(t, a.d, alpha=0.5,
     label='DEGG')

plot(t[gci_ref], 0*gci_ref, 'o', ms=5, alpha=0.5,
     label='reference markings')

legend(loc='lower right', fancybox=True, framealpha=0.5)
ylabel('DEGG')

subplot(313, sharex=ax)
t = arange(len(a.e)) / a.fs
plot(t, a.e, alpha=0.5)
ylabel('EGG')
xlabel('time (s)')

tight_layout()

show(block=True)
