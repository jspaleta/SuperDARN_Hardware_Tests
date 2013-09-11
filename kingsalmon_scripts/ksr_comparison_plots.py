from csv_utils import *
import pylab as p
import sys

use_vvm=False

directory="/home/jspaleta/scratch/king_salmon_vnadata_sept_10_matrix_only"
plotdir="ksr_paired_recv_path_plots"
radar="KSR"

if use_vvm:
  from ksr_vvm_measurements import *
  ksr_vvm_12MHz=p.array(ksr_vvm_measurements)
#print "beam 1",ksr_vvm_12MHz[1]

plot_directory=os.path.join(directory,plotdir)
if not os.path.exists(plot_directory): os.mkdir(plot_directory)
colors={0:"red",1:"blue",2:"black",3:"green",4:"cyan",5:"yellow"}
for bmnum in range(16):
    p.figure(200+bmnum)
    p.clf()
    p.figure(300+bmnum)
    p.clf()
    p.figure(400+bmnum)
    p.clf()
    p.figure(500+bmnum)
    p.clf()
for bmnum in range(16):
  last_main=None
  last_interf=None
  p.figure(104)
  p.clf()
  for card in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:
    data_interf=None
    data_main=None
    if card in [7,8,9,10]:
      data_interf=csv_data()
      data_interf.card=card+10
      data_interf.beam=bmnum
      read_csv(directory,data_interf)
    else:
      data_interf=None

    data_main=csv_data()
    data_main.card=card
    data_main.beam=bmnum
    read_csv(directory,data_main)

    freqs=p.array(data_main.freqs)
    df=freqs[1]-freqs[0]
    f8_index=int((8E6-freqs[0])/df)+1
    f10_index=int((10E6-freqs[0])/df)+1
    f12_index=int((12E6-freqs[0])/df)+1
    f14_index=int((14E6-freqs[0])/df)+1
    f18_index=int((18E6-freqs[0])/df)+1
    main_tdelay=p.array(data_main.tdelay)
    main_ephase=p.array(data_main.ephase)
    main_ephase_slope=(main_ephase[700]-main_ephase[500])/(freqs[700]-freqs[500])
    main_ephase_offset=main_ephase[0]-main_ephase_slope*freqs[0]
    main_phase_from_tdelay=-main_tdelay*freqs*360.0
    main_ephase_diff=p.diff(data_main.ephase)
    freq_diff=p.diff(data_main.freqs)
    main_ephase_tdelay=-main_ephase_diff/360.0/freq_diff
    if last_main is not None:
      main_nearest_pair_phase_diff=p.array(data_main.ephase)-p.array(last_main.ephase)
      main_nearest_pair_phase_diff=main_nearest_pair_phase_diff % 360
      main_nearest_pair_phase_diff=p.array([(ph > 180) * -360 + ph for ph in main_nearest_pair_phase_diff])

    if card in [7,8,9,10]:
      interf_tdelay=p.array(data_interf.tdelay)
      diff_tdelay=interf_tdelay-main_tdelay
      phase_diff=p.array(data_interf.ephase)-p.array(data_main.ephase)
      phase_diff=(phase_diff % 360.0)
      phase_diff=p.array([(ph > 180) * -360 + ph for ph in phase_diff])
      phase_diff_diff=p.diff(phase_diff)
      phase_diff_tdelay=-(phase_diff_diff/360.0)/freq_diff
      interf_ephase_diff=p.diff(data_interf.ephase)
      interf_ephase_tdelay=-interf_ephase_diff/360.0/freq_diff
      diff_ephase_tdelay=interf_ephase_tdelay-main_ephase_tdelay
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
      if last_interf is not None:
        interf_nearest_pair_phase_diff=p.array(data_interf.ephase)-p.array(last_interf.ephase)
        interf_nearest_pair_phase_diff=interf_nearest_pair_phase_diff % 360
        interf_nearest_pair_phase_diff=p.array([(ph > 180) * -360 + ph for ph in interf_nearest_pair_phase_diff])

    p.figure(103)
    p.clf()
    p.grid(True)
    p.plot(freqs*1E-6,main_tdelay*1E9,color="red",label="Card %02d" % (card) )
    p.figtext(0.2,0.85, "Ave 10-18 MHz: %8.3f nsec" % (p.mean(main_tdelay[f10_index:f18_index]*1E9)),color="red") 
    p.figtext(0.2,0.80, "Std 10-18 MHz: %8.3f nsec" % (p.std(main_tdelay[f10_index:f18_index]*1E9)),color="red") 
    p.title("%s Recv Path Group Delay Comparison\n Card %02d Beam %d" % \
      (radar,data_main.card,data_main.beam))
    if card in [7,8,9,10]:
      p.plot(freqs*1E-6,interf_tdelay*1E9,color="blue",label="Card %02d" % (card+10) )
      p.figtext(0.5,0.75, "Ave 10-18 MHz: %8.3f nsec" % (p.mean(interf_tdelay[f10_index:f18_index]*1E9)),color="blue") 
      p.figtext(0.5,0.70, "Std 10-18 MHz: %8.3f nsec" % (p.std(interf_tdelay[f10_index:f18_index]*1E9)),color="blue") 
      p.title("%s Recv Path Group Delay Comparison\n Card %02d and Card %02d Beam %d" % \
        (radar,data_main.card,data_interf.card,data_main.beam))
    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((0,1000))
    p.xlabel("Freq [MHz]")
    p.ylabel("Group Delay [nsec]")
    figfile=os.path.join(plot_directory,"group_delay_c%02d_b%02d.png" % (card,bmnum))
    p.savefig(figfile)


    p.figure(200+bmnum)
    p.plot(freqs*1E-6,main_tdelay*1E9,color=colors[ card % 6 ],label="Card %02d" % (card) )
    if card in [7,8,9,10]:
      p.figure(300+bmnum)
      p.plot(freqs*1E-6,interf_tdelay*1E9,color=colors[card % 6 ],label="Card %02d" % (card+10) )

    if last_main is not None:
      p.figure(400+bmnum)
      p.plot(freqs*1E-6,main_nearest_pair_phase_diff,color=colors[ card % 6 ],label="Card %02d-%02d" % (card,card-1) )
    if last_interf is not None:
      if card in [7,8,9,10]:
        p.figure(500+bmnum)
        p.plot(freqs*1E-6,interf_nearest_pair_phase_diff,color=colors[ card % 6 ],label="Card %02d-%02d" % (card+10,card-1+10) )
    if card in [7,8,9,10]:
      p.figure(100)
      p.clf()
      p.grid(True)
#    p.plot(freqs[0:-1]*1E-6,diff_ephase_tdelay*1E9,color="black")
      p.plot(freqs*1E-6,diff_tdelay*1E9,color="black",label="Cards: %02d-%02d" % (card,card+10))
#    p.plot(freqs[0:-1]*1E-6,smooth_phase_diff_tdelay*1E9,color="black",label="Calculated from Diff of VNA Phase Measurement")
#    p.legend(loc=4)
      ax=p.gca()
      ax.set_xlim((8,20))
      ax.set_ylim((-60,60))
      p.xlabel("Freq [MHz]")
      p.ylabel("tdiff [nsec]")
      p.title("%s Recv Path Time Delay Difference\n Card %02d and Card %02d Beam %d" % \
        (radar,data_main.card,data_interf.card,data_main.beam))
      p.figtext(0.2,0.85, "Ave 10-18 MHz: %8.3f nsec" % (p.mean(diff_tdelay[f10_index:f18_index]*1E9))) 
      p.figtext(0.2,0.80, "Std 10-18 MHz: %8.3f nsec" % (p.std(diff_tdelay[f10_index:f18_index]*1E9))) 
      figfile=os.path.join(plot_directory,"tdiff_c%02d-c%02d_b%02d.png" % (card,card+10,bmnum))
      p.savefig(figfile)

      p.figure(102)
      p.clf()
      p.grid(True)
      p.plot(freqs*1E-6,phase_diff,color="black",label="Phase Diff")
      p.plot(freqs*1E-6,data_main.phase,color="red",label="Card %02d" % (card) )
      p.plot(freqs*1E-6,data_interf.phase,color="blue",label="Card %02d" % (card+10) )
      if use_vvm:
        pdiff=(ksr_vvm_12MHz[bmnum][card-1+10]-ksr_vvm_12MHz[bmnum][card-1]) % 360 
        pdiff=(pdiff > 180) * -360 + pdiff
        p.plot([12],[pdiff],"go",label="Diff of VVM")
        for i in xrange(9):
          if i==0: label="VVM Diff"
          else: label="_none_"
          p.plot([9+i],[ksr_vvm_pdiff[card][bmnum][i]],"co",label=label)
        
          if (i % 2) ==1:
            p.figtext(0.1*i+0.05,0.75,"%d MHz: %3.1f" % (i+9,ksr_vvm_pdiff[card][bmnum][i]),color="cyan",backgroundcolor="white")
        
      p.legend(loc=4)
      ax=p.gca()
      ax.set_xlim((8,20))
      ax.set_ylim((-300,300))
      p.figtext(0.15,0.85,"10 MHz: %3.1f" % (phase_diff[f10_index]),color="black",backgroundcolor="white")
      p.figtext(0.35,0.85,"12 MHz: %3.1f" % (phase_diff[f12_index]),color="black",backgroundcolor="white")
      p.figtext(0.55,0.85,"14 MHz: %3.1f" % (phase_diff[f14_index]),color="black",backgroundcolor="white")
      if use_vvm:
        p.figtext(0.35,0.80,"12 MHz: %3.1f" % (pdiff),color="green",backgroundcolor="white")
      p.xlabel("Freq [MHz]")
      p.ylabel("phase [deg]")
      p.title("%s Recv Path Phase Difference\n Card %02d and Card %02d Beam %d" % \
      (radar,data_main.card,data_interf.card,data_main.beam))
      figfile=os.path.join(plot_directory,"phase_diff_c%02d-c%02d_b%02d.png" % (card,card+10,bmnum))
      p.savefig(figfile)


      p.figure(104)
#      p.plot(freqs[0:-1]*1E-6,diff_ephase_tdelay*1E9,color="black")
      p.plot(freqs*1E-6,diff_tdelay*1E9,color=colors[card % 6],label="Cards: %02d-%02d" % (card,card+10))
#      p.plot(freqs[0:-1]*1E-6,smooth_phase_diff_tdelay*1E9,color="black",label="Calculated from Diff of VNA Phase Measurement")

    p.figure(105)
    p.clf()
    p.grid(True)
    p.plot(freqs*1E-6,main_ephase-main_ephase_offset,color="red",label="Card %02d ephase" % (card) )
    p.plot(freqs*1E-6,main_ephase_slope*freqs,color="green",label="Card %02d ephase from slope" % (card) )
    p.plot(freqs*1E-6,main_phase_from_tdelay,color="blue",label="Card %02d ephase from tdelay" % (card) )
    p.legend(loc=4)
    ax=p.gca()
    ax.set_xlim((8,20))
    ax.set_ylim((-5000,0))
    p.xlabel("Freq [MHz]")
    p.ylabel("Phase [deg]")
    p.title("%s Recv Path Ephase Comparison\n Card %02d Beam %d" % \
      (radar,data_main.card,data_main.beam))
    figfile=os.path.join(plot_directory,"main_ephase_c%02d_b%02d.png" % (card,bmnum))
    p.savefig(figfile)


    last_main=data_main
    last_interf=data_interf


  p.figure(200+bmnum)
  p.grid(True)
  p.legend(loc=4)
  ax=p.gca()
  ax.set_xlim((8,20))
  ax.set_ylim((0,1000))
  p.xlabel("Freq [MHz]")
  p.ylabel("Group Delay [nsec]")
  p.title("%s Main Array Group Delay Comparison\n Beam %d" % \
      (radar,data_main.beam))
  figfile=os.path.join(plot_directory,"main_beam_group_delay_b%02d.png" % (bmnum))
  p.savefig(figfile)
  
  p.figure(300+bmnum)
  p.grid(True)
  p.legend(loc=4)
  ax=p.gca()
  ax.set_xlim((8,20))
  ax.set_ylim((0,1000))
  p.xlabel("Freq [MHz]")
  p.ylabel("Group Delay [nsec]")
  p.title("%s Interf Array Group Delay Comparison\n Beam %d" % \
      (radar,data_main.beam))
  figfile=os.path.join(plot_directory,"interf_beam_group_delay_b%02d.png" % (bmnum))
  p.savefig(figfile)

  p.figure(400+bmnum)
  p.grid(True)
  p.legend(loc=4)
  ax=p.gca()
  ax.set_xlim((8,20))
  ax.set_ylim((-360,360))
  p.xlabel("Freq [MHz]")
  p.ylabel("Phase difference [deg]")
  p.title("%s Main Array Nearest Neighbor Phase Diff Comparison\n Beam %d" % \
      (radar,data_main.beam))
  figfile=os.path.join(plot_directory,"main_beam_pair_phase_diff_b%02d.png" % (bmnum))
  p.savefig(figfile)

  p.figure(500+bmnum)
  p.grid(True)
  p.legend(loc=4)
  ax=p.gca()
  ax.set_xlim((8,20))
  ax.set_ylim(-360,360)
  p.xlabel("Freq [MHz]")
  p.ylabel("Phase difference [deg]")
  p.title("%s Interf Array Nearest Neighbor Phase Diff Comparison\n Beam %d" % \
      (radar,data_main.beam))
  figfile=os.path.join(plot_directory,"interf_beam_pair_phase_diff_b%02d.png" % (bmnum))
  p.savefig(figfile)

  p.figure(104)
  p.grid(True)
  p.legend(loc=4)
  ax=p.gca()
  ax.set_xlim((8,20))
  ax.set_ylim((-60,60))
  p.xlabel("Freq [MHz]")
  p.ylabel("tdiff [nsec]")
  p.title("%s Recv Path Time Delay Difference\nBeam %d" % \
      (radar,data_main.beam))
  figfile=os.path.join(plot_directory,"beam_tdiff_b%02d.png" % (bmnum))
  p.savefig(figfile)

#  p.show()
