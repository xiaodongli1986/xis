
# coding: utf-8

# In[10]:

execfile('/home/xiaodongli/software/pythonlib/Tpcftools.py')
execfile('/home/xiaodongli/software/pythonlib/bossdatamock.py')

datamockdir = datamockdir_cluster
smu_xis_covchisqdir = datamockdir + '/xis_covchisqs'
commands.getoutput('mkdir -p '+str(smu_xis_covchisqdir));


# In[6]:

### 1. List of omegam, w
omwlist = Dense1subscan_omwlist

### 2. Basic name of outputfile
baseoutputfile = 'Dense1subscan'

### 3. Range of imumin
imumins = range(20)+[30,40,50,60]

### 4. Maximal s
smax = 51 

### 5. Others
catnamelist = ['DR12v4-LOWZ', 'DR12v4-CMASS', ]
totbin = 3
delta_time = 100

icompute = 0
ncompute = len(imumins)*len(catnamelist)*totbin*len(omwlist)
print '###############################################'
print ' Computing ', ncompute, ' sets of xi(s)...'
t0 = time.clock(); t1 = t0


# In[8]:

### 6. Checking existence of files
if True:
        filelist = []
        for catname in catnamelist:
            for ibin in range(totbin):
                for omw in omwlist:
                    om, w = omw
                    galfile = binsplittedfilename(datafile(catname), ibin+1, totbin)
                    galfile = cosmoconvertedfilename(galfile, om, w)
                    rltfile = Tpcfrltfilename(galfile, smax, smax)
                    filelist.append(rltfile)
        isfiles(filelist)


# In[4]:

### 7. Compute    
if True:
    for imumin in imumins:
        outputfile =  smu_xis_covchisqdir+'/'+baseoutputfile+'.smax'+str(smax)+'.imumin%03i'%imumin+'.xis'
        nowf = open(outputfile, 'w')
        nowf.write('# Cataloguename   bin-number    om,w    xi(s) at s<='+str(smax)+' \n')
        print ' Write to file:\n\t', outputfile
        for catname in catnamelist:
            ### Filename
            for ibin in range(totbin):
                for omw in omwlist:
                    om, w = omw
                    galfile = binsplittedfilename(datafile(catname), ibin+1, totbin)
                    galfile = cosmoconvertedfilename(galfile, om, w)
                    rltfile = Tpcfrltfilename(galfile, smax, smax)
                    Y = smu_xis(rltfile, sfact=0, imumin=imumin, 
                            outputtofile=False,  smax=smax, nummubin=120, 
                            make_plot=False, savefig=False, figname=None)
                    nowf.write(catname+'   '+str(ibin+1)+'  '+omwstr(om, w)+'    '+array_to_str(Y)+'\n')
                    icompute+=1
                    t2 = time.clock()
                    if t2 - t1>delta_time:
                        print '  ', t2-t0, ' seconds:  ', icompute, '   of ',                             ncompute, '  xi(s) done;      rat = %.3f'%(icompute/float(ncompute))
                        t1 = t2
        nowf.close()

    print 'Done. Time used = ', t2-t0

