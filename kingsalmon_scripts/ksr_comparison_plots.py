from csv_utils import *
import pylab as p

directory="/home/jspaleta/scratch/kingsalmon_test/"
plotdir="ksr_paired_recv_path_plots"
radar="KSR"

plot_directory=os.path.join(directory,plotdir)
if not os.path.exists(plot_directory): os.mkdir(plot_directory)
colors={7:"red",8:"blue",9:"black",10:"green"}
for bmnum in range(16):
  p.figure(4)
  p.clf()
  for card in [7,8,9,10]:
    data_interf=csv_data()
    data_interf.card=card+10
    data_interf.beam=bmnum
    data_main=csv_data()
    data_main.card=card
    data_main.beam=bmnum
    read_csv(directory,data_interf)
    read_csv(directory,data_main)

    freqs=p.array(data_main.freqs)
    main_tdelay=p.array(data_main.tdelay)
    interf_tdelay=p.array(data_interf.tdelay)
    diff_tdelay=interf_tdelay-main_tdelay
    phase_diff=p.array(data_interf.ephase)-p.array(data_main.ephase)
    phase_diff=(phase_diff % 360.0)
    phase_diff=p.array([(ph > 180) * -360 + ph for ph in phase_diff])

    main_ephase_diff=p.diff(data_main.ephase)
    interf_ephase_diff=p.diff(data_interf.ephase)
    freq_diff=p.diff(data_main.freqs)
    main_ephase_tdelay=-main_ephase_diff/360.0/freq_diff
    interf_ephase_tdelay=-interf_ephase_diff/360.0/freq_diff
    diff_ephase_tdelay=interf_ephase_tdelay-main_ephase_tdelay

    phase_diff_diff=p.diff(phase_diff)
    phase_diff_tdelay=-(phase_diff_diff/360.0)/freq_diff

    smooth_phase_diff_tdelay=p.zeros_like(phase_diff_tdelay)
    sum_count=p.zeros_like(phase_diff_tdelay)
    for i in xrange(len(phase_diff_tdelay)):
      for j in xrange(40):
        if i+j < len(phase_diff_tdelay):
          smooth_phase_diff_tdelay[i]+=phase_diff_tdelay[i+j]
          sum_count[i]+=1
        if i-j >= 0:
          smooth_phase_diff_tdelay[i]+=phase_diff_tdelay[i-j]
          sum_count[i]+=1
    smooth_phase_diff_tdelay=smooth_phase_diff_tdelay/sum_count

    p.figure(1)
    p.clf()
    p.grid(True)
#    p.plot(freqs[0:-1]*1E-6,diff_ephase_tdelay*1E9,color="black")
    p.plot(freqs*1E-6,diff_tdelay*1E9,color="black",label="Cards: %02d-%02d" % (card,card+10))
#    p.plot(freqs[0:-1]*1E-6,smooth_phase_diff_tdelay*1E9,color="black",label="Calculated from Diff of VNA Phase Measurement")
#    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((-40,40))
    p.xlabel("Freq [MHz]")
    p.ylabel("tdiff [nsec]")
    p.title("%s Recv Path Time Delay Difference\n Card %02d and Card %02d Beam %d" % \
      (radar,data_main.card,data_interf.card,data_main.beam))
    figfile=os.path.join(plot_directory,"tdiff_c%02d-c%02d_b%02d.png" % (card,card+10,bmnum))
    p.savefig(figfile)

    p.figure(2)
    p.clf()
    p.grid(True)
    p.plot(freqs*1E-6,phase_diff,color="black",label="Phase Diff")
    p.plot(freqs*1E-6,data_main.phase,color="red",label="Card %02d" % (card) )
    p.plot(freqs*1E-6,data_interf.phase,color="blue",label="Card %02d" % (card+10) )
    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((-200,200))
    p.xlabel("Freq [MHz]")
    p.ylabel("phase [deg]")
    p.title("%s Recv Path Phase Difference\n Card %02d and Card %02d Beam %d" % \
      (radar,data_main.card,data_interf.card,data_main.beam))
    figfile=os.path.join(plot_directory,"phase_diff_c%02d-c%02d_b%02d.png" % (card,card+10,bmnum))
    p.savefig(figfile)

    p.figure(3)
    p.clf()
    p.grid(True)
    p.plot(freqs*1E-6,main_tdelay*1E9,color="red",label="Card %02d" % (card) )
    p.plot(freqs*1E-6,interf_tdelay*1E9,color="blue",label="Card %02d" % (card+10) )
    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((0,1000))
    p.xlabel("Freq [MHz]")
    p.ylabel("Group Delay [nsec]")
    p.title("%s Recv Path Group Delay Comparison\n Card %02d and Card %02d Beam %d" % \
      (radar,data_main.card,data_interf.card,data_main.beam))
    figfile=os.path.join(plot_directory,"group_delay_c%02d-c%02d_b%02d.png" % (card,card+10,bmnum))
    p.savefig(figfile)

    p.figure(4)
#    p.clf()
    p.grid(True)
#    p.plot(freqs[0:-1]*1E-6,diff_ephase_tdelay*1E9,color="black")
    p.plot(freqs*1E-6,diff_tdelay*1E9,color=colors[card],label="Cards: %02d-%02d" % (card,card+10))
#    p.plot(freqs[0:-1]*1E-6,smooth_phase_diff_tdelay*1E9,color="black",label="Calculated from Diff of VNA Phase Measurement")
    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((-40,40))
    p.xlabel("Freq [MHz]")
    p.ylabel("tdiff [nsec]")
    p.title("%s Recv Path Time Delay Difference\nBeam %d" % \
      (radar,data_main.beam))

  p.figure(4)
  figfile=os.path.join(plot_directory,"beam_tdiff_b%02d.png" % (bmnum))
  p.savefig(figfile)
#  p.show()
