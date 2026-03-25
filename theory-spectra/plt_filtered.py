# Siebe Vanlommel
import numpy as np, glob
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

#ref = 560.0 #estimate
ref = (571.329 - 7.3) # 23Na in NaNO3 (PBE+pcSseg-3) is -7.3 ppm

Na_freq = 132.49 # MHz, of spectrometer
def get_spectrum(mainpath, sigma=0):
    sum_spec = None
    freq = None
    files = sorted(glob.glob(mainpath))
    #print(files)
    for f in files:
        d = np.loadtxt(f)
        freq = d[:,0]
        spec = d[:,1] #real part of signal
        if sum_spec is None:
            sum_spec = np.zeros_like(spec)
        sum_spec += spec
    sum_spec /= np.trapz(sum_spec)
    final_filter = gaussian_filter1d(sum_spec, sigma=sigma)
    freq = -1*freq/132.49 + ref
    return freq, final_filter, sum_spec

fig, ax = plt.subplots(1,1)

ax.set_title('gaussian filter sigma = 10 ppm')
freq0,spec0_f,spec0 = get_spectrum("isotropic/high-xNa/*/output.txt", sigma=10)
freq1,spec1_f,spec1 = get_spectrum("isotropic/low-xNa/*/output.txt", sigma=10)
ax.plot(freq0, spec0_f, c='gold', label='iso (a0b0, CS), $x_{Na} = 0.267$', linestyle='--')
ax.plot(freq1, spec1_f, c='tab:blue', label='iso (a0b0, CS), $x_{Na} = 0.004$', linestyle='--')

np.savetxt("summed_spectra/iso_highNa_filter.dat", np.column_stack((freq0,spec0_f)), fmt="%.6f", delimiter="\t", header="iso shift (ppm)\t Re signal (arb u)\t")
np.savetxt("summed_spectra/iso_lowNa_filter.dat", np.column_stack((freq1,spec1_f)), fmt="%.6f", delimiter="\t", header="iso shift (ppm)\t Re signal (arb u)\t")
np.savetxt("summed_spectra/iso_highNa_raw.dat", np.column_stack((freq0,spec0)), fmt="%.6f", delimiter="\t", header="iso shift (ppm)\t Re signal (arb u)\t")
np.savetxt("summed_spectra/iso_lowNa_raw.dat", np.column_stack((freq1,spec1)), fmt="%.6f", delimiter="\t", header="iso shift (ppm)\t Re signal (arb u)\t")

freq2,spec2_f,spec2 = get_spectrum("anisotropic/high-xNa/*/output.txt", sigma=10)
freq3,spec3_f,spec3 = get_spectrum("anisotropic/low-xNa/*/output.txt", sigma=10)
ax.plot(freq2, spec2_f, c='gold', label='aniso (rep256, CS+CSA+QC), $x_{Na} = 0.267$')
ax.plot(freq3, spec3_f, c='tab:blue', label='aniso (rep256, CS+CSA+QC), $x_{Na} = 0.004$')

#use this to save
'''
np.savetxt('summed_spectra/aniso_highNa_filter.dat',np.column_stack((freq2,spec2_f)),fmt="%.6f",header="iso shift (ppm)\t Re signal (arb u)")
np.savetxt('summed_spectra/aniso_lowNa_filter.dat',np.column_stack((freq3,spec3_f)),fmt="%.6f",header="iso shift (ppm)\t Re signal (arb u)")
np.savetxt('summed_spectra/aniso_highNa_raw.dat',np.column_stack((freq2,spec2)),fmt="%.6f",header="iso shift (ppm)\t Re signal (arb u)")
np.savetxt('summed_spectra/aniso_lowNa_raw.dat',np.column_stack((freq3,spec3)),fmt="%.6f",header="iso shift (ppm)\t Re signal (arb u)")
'''
#use this to plot exp spectra as well
exp_low = np.transpose(np.genfromtxt('../exp-spectra/23Na-Spec1-conc0.025.txt'))
exp_high = np.transpose(np.genfromtxt('../exp-spectra/23Na-Spec5-conc0.25.txt'))
#ax.plot(exp_low[0],exp_low[1]*0.018/np.max(exp_low[1]) + 0.0,c='tab:blue',linestyle='dashdot',label=r'exp, $x_\text{Na}$=0.025')
#ax.plot(exp_high[0],exp_high[1]*0.018/np.max(exp_high[1]) + (0.0008 - 0.00063), c='gold',linestyle='dashdot',label=r'exp, $x_\text{Na}$=0.25')


from mpl_toolkits.axes_grid1.inset_locator import inset_axes

ax_inset = inset_axes(
    ax,
    width="40%",      # width relative to parent
    height="40%",     # height relative to parent
    loc="upper left" # position
)

# Inset plot
ax_inset.plot(exp_low[0],exp_low[1],c='tab:blue',label=r'$x_\text{Na} = 0.025$')
ax_inset.plot(exp_high[0],exp_high[1],c='gold',label=r'$x_\text{Na}$ = 0.25')
ax_inset.set_title("Experiment", fontsize=10)
ax_inset.set_xlim(15,-10)
ax_inset.set_yticks([])
ax_inset.tick_params(labelsize=8)
ax_inset.legend()


lim=200
ax.set_xlabel("23Na $\delta$ [ppm]")
#plt.ylabel("intensity")
#plt.title(f"Summed NMR spectra")
ax.set_xlim(lim,-1*lim)
ax.legend()
plt.tight_layout()
plt.show()
