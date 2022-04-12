import ROOT
import os

# just MC for now
samples = [ 'LFVTtVecU', 'others' , 'TTbar', 'TX' , 'VV' , 'WZ', 'LFVStVecU', 'nonprompt' , 'data'  ] # 'data'

uncerts = [ 'jesAbsoluteMPFBias_', 'jesAbsoluteScale_', 'jesAbsoluteStat_','jesFlavorQCD_','jesFragmentation_','jesPileUpDataMC_','jesPileUpPtBB_','jesPileUpPtEC1_','jesPileUpPtEC2_' ,'jesPileUpPtHF_' ,'jesPileUpPtRef_','jesRelativeFSR_','jesRelativeJEREC1_','jesRelativeJEREC2_','jesRelativeJERHF_' ,'jesRelativePtBB_' ,'jesRelativePtEC1_','jesRelativePtEC2_','jesRelativePtHF_','jesRelativeBal_','jesRelativeSample_' ,'jesRelativeStatEC_' ,'jesRelativeStatFSR_','jesRelativeStatHF_','jesSinglePionECAL_','jesSinglePionHCAL_','jesTimePtEta_' , 'udsgTagSF_', 'pu_','prefiring_','eleR_','eleF_','muR_','muF_','jer_', 'bcTagSF_', 'eleRecoSf_' ,  'muIdSf_' , 'bcTagSF_'  ]

processes = ['ST' , 'TT'] 

for p in processes :

    years = ['2016','2017','2018']
    for y in years :
        string0 = 'rootcp ' + y + '_'
        for s in samples:
                string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_' + p + '  '
                string2 =  y+'_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p
                if s == 'nonprompt':
                    string1 = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT' + p + '  '
                    string2 =  y+'_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p
                if s == 'data':
                    string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_' + p + '  '
                    string2 =  y+'_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p
                if (s != 'data' and s != 'nonprompt' ) : 
                    string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_' + p + '  '
                    string2 =  y+'_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p 


                print string0 + string1+ string2
                os.system( string0 + string1+ string2  )        
                for u in uncerts :
                  u2= u
                  if 'jer' in u :
                      u2 = 'jer'+y+'_'
                  string1up = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Up '
                  string1down = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Down '

                  string2Up = y+'_HistsSplitMC.root:' + s+ '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Up '
                  string2Down = y+'_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Down '

                  if s == 'nonprompt':
                      string1up = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Up '
                      string1down = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Down '

                      string2Up = y+'_HistsSplitMC.root:' + s+ '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Up '
                      string2Down = y+'_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Down '
                  if s == 'data':
                      string1up = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Up '
                      string1down = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u + 'Down '

                      string2Up = y+'_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Up '
                      string2Down = y+'_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_'+p+'_'+ u2 + 'Down '



                  fstringUp = string0 + string1up +  string2Up 
                  fstringDown = string0 + string1down +  string2Down 
                  os.system( fstringUp )
                  print fstringUp

                  print fstringDown
                  os.system( fstringDown)
