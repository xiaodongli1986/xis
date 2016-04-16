
#py_Plot is the command to plot

execfile('/home/xiaodongli/software/pythonlib/Tpcftools.py')

is_sig_pi = False
make_plot = True

if True:
  smax = 51
  smusettings = {
            'smin':0.0, 'smax':smax, 'numsbin':smax,
#            'mumin':0.0, 'mumax':1.0, 'nummubin':50,
            'mumin':0.0, 'mumax':1.0, 'nummubin':120,
            'deltas':0, 'deltamu':0, 'slist':[], 'mulist':[]
               }
  smu__initsmusettings(smusettings)

imumin = 0; imumax = nummubin;
#for nowxtr in open('2pcffiles.txt','r').readlines():
#  filename = nowxtr; filename = filename[0:len(filename)-1]
for filename in getfilelist('../DR12v4-CMASS/xyzw.binsplitted/*.2pcf')+getfilelist('../DR12v4-LOWZ/xyzw.binsplitted/*.2pcf'):
  print filename
  outputfilename = filename+'.xi_s'
  if True:
		DDlist, DRlist, RRlist = Xsfrom2ddata(smu__loadin(filename, smusettings), [4,5,6])
		ismax = 50
		no_s_sq_in_y = False
		if make_plot: fig, ax1 = figax()

                ### packed count of xi as a function of s
                now_s = 0;
                sasx = []; packedxiasy = [];

                for now_s in range(ismax):
                    nowx=(slist[now_s]+slist[now_s+1])/2.0;   sasx.append(nowx)
                    if not no_s_sq_in_y:
			    if is_sig_pi:
			    	Y = []
			    	for nowxig in range(ismax-1):
				 nowpi = int(np.sqrt(nowx**2.0 - nowxig**2.0)) 
				 nowpi = max(nowpi,0)
				 Y.append(packedxi(DDlist,DRlist,RRlist,nowxig,nowxig+1,nowpi,nowpi+1))
			    	nowy = nowx*nowx*sum(Y) / (len(Y)+0.0)
				#nowy = np.log(np.abs(sum(Y)/len(Y)+0.0)) / np.log(10.0)
			    	packedxiasy.append(nowy)
			    else:
                                packedxiasy.append(nowx*nowx*packedxi(DDlist, DRlist, RRlist, now_s, now_s, imumin, imumax))
                    else:
                            packedxiasy.append(packedxi(DDlist, DRlist, RRlist, now_s, now_s, imumin, imumax))
                    now_s += 1;
                #print sasx
  	        #print packedxiasy
		np.savetxt(filename+'.xis', packedxiasy)
                if make_plot:
                        ax1.plot(sasx, packedxiasy, marker='o', markersize=1)
                        ax1.set_xlabel('$s\ [\\rm Mpc/h]$', fontsize=25)
                        if not no_s_sq_in_y:
                                ax1.set_ylabel('$s^2\\xi\ [\\rm Mpc/h]^2$', fontsize=25)
                        else:
                                ax1.set_ylabel('$\\xi\ [\\rm Mpc/h]^2$', fontsize=25)
                        ax1.set_xlim(0,ismax)
			ax1.set_title(filename)
		        fig.savefig(filename+'.png', format = 'png')
		        #plt.show()
