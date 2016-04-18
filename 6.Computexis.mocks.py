
# coding: utf-8

# In[1]:

execfile('/home/xiaodongli/software/pythonlib/Tpcftools.py')
execfile('/home/xiaodongli/software/pythonlib/bossdatamock.py')

datamockdir = datamockdir_cluster
smu_xis_covchisqdir = datamockdir + '/xis_covchisqs'
commands.getoutput('mkdir -p '+str(smu_xis_covchisqdir));


# In[6]:

### 1. List of omegam, w
#omwlist = Dense1subscan_omwlist

### 2. Basic name of outputfile
#baseoutputfile = 'Dense1subscan'

### 3. Range of imumin
imumins = range(20)+[30,40,50,60]

### 4. Maximal s
smax = 150 

### 5. Others
catnamelist = ['DR12v4-LOWZ', 'DR12v4-CMASS', 'DR12v4-LOWZ-N', 'DR12v4-CMASS-N','DR12v4-LOWZ-S', 'DR12v4-CMASS-S',]
totbin = 3
delta_time = 100


# In[7]:

### 6. Checking existence of files
if True:
        filelist = []
        for catname in catnamelist:
         for catname2 in catname2list:
            nummock = catinfo_nummock(catname, catname2)
            for RSDstr in ['noRSD', 'RSD']:
                for ibin in range(totbin):
                    for imock in range(nummock):
                        galfile = binsplittedfilename(mockfile(catname, catname2, imock, RSDstr), ibin+1, totbin)
                        rltfile = Tpcfrltfilename(galfile, smax, smax)
                        filelist.append(rltfile)
        isfiles(filelist)


# In[13]:

### 7. Compute    
if True:
    icompute = 0
    t0= time.clock(); t1=t0
    ncompute = len(filelist) * len(imumins)
    print '#######################'
    print ' Computing ', ncompute, 'files...'
    for imumin in imumins:
        outputfile =  smu_xis_covchisqdir+'/MockResult.imumin%03i'%imumin+'.xis'
        nowf = open(outputfile, 'w')
        nowf.write('# catname  catname2  RSDstr    imock    ibin    xi(s) at s<='+str(smax)+' \n')
        print ' Write to file:\n\t', outputfile
        for catname in catnamelist:
         for catname2 in catname2list:
            nummock = catinfo_nummock(catname, catname2)
            for RSDstr in ['noRSD', 'RSD']:
                for imock in range(nummock):
                    for ibin in range(totbin):
                        galfile = binsplittedfilename(mockfile(catname, catname2, imock, RSDstr), ibin+1, totbin)
                        rltfile = Tpcfrltfilename(galfile, smax, smax)
                        Y = smu_xis(rltfile, sfact=0, imumin=imumin, 
                            outputtofile=False,  smax=smax, nummubin=120, 
                            make_plot=False, savefig=False, figname=None)
                        nowf.write(array_to_str([catname,  catname2,  RSDstr,imock, ibin,])+'    '+array_to_str(Y)+'\n')
                        icompute+=1
                        t2 = time.clock()
                        if t2 - t1>delta_time:
                            print '  ', t2-t0, ' seconds:  ', icompute, '   of ',                                 ncompute, '  xi(s) done;      rat = %.4f'%(icompute/float(ncompute))
                            t1 = t2
        nowf.close()

    print 'Done. Time used = ', t2-t0

