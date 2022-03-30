import ROOT
import os

# just MC for now
samples = [ 'LFVTtVecU', 'others' , 'TTbar', 'TX' , 'VV' , 'WZ', 'LFVStVecU', 'nonprompt'  ] # 'data'

uncerts = [ 'jes_', 'udsgTagSF_', 'pu_','prefiring_','eleR_','eleF_','muR_','muF_','jer_', 'bcTagSF_', 'eleRecoSf_' ,  'muIdSf_' , 'bcTagSF_'  ]


string0 = 'rootcp 2017_'



for s in samples:
        string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT  '
        string2 =  '2017_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT'
        if s == 'nonprompt':
            string1 = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT   '
            string2 =  '2017_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT'
        if s == 'data':
            string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT   '
            string2 =  '2017_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT'
        if (s != 'data' and s != 'nonprompt' ) : 
            string1 = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT   '
            string2 =  '2017_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT' 


        print string0 + string1+ string2
        os.system( string0 + string1+ string2  )        
        for u in uncerts :
          u2= u
          if 'jer' in u :
              u2 = 'a2017jer_'
          string1up = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Up '
          string1down = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Down '

          string2Up = '2017_HistsSplitMC.root:' + s+ '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Up '
          string2Down = '2017_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Down '

          if s == 'nonprompt':
              string1up = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Up '
              string1down = 'data' + '.root:AR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Down '

              string2Up = '2017_HistsSplitMC.root:' + s+ '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Up '
              string2Down = '2017_HistsSplitMC.root:' + s + '_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Down '
          if s == 'data':
              string1up = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Up '
              string1down = s + '.root:VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u + 'Down '

              string2Up = '2017_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Up '
              string2Down = '2017_HistsSplitMC.root:data_obs_VR_emul_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_'+ u2 + 'Down '



          fstringUp = string0 + string1up +  string2Up 
          fstringDown = string0 + string1down +  string2Down 
          os.system( fstringUp )
          print fstringUp

          print fstringDown
          os.system( fstringDown)
