#! /usr/bin/env python
import CombineHarvester.CombineTools.ch as ch
import os
import ROOT

cb = ch.CombineHarvester()
cb.SetFlag('workspaces-use-clone', True)

# Definition of process names to be used in the analysis
mc_backgrounds = [ 'VV', 'WZ', 'TX' ,'nonprompt' ]  # TODO : Add TX : '2018_TX'
data_driven_backgrounds = ['TTbar', 'others']
backgrounds = mc_backgrounds #+ data_driven_backgrounds

years = ['2018']#['2017']#['2018'] # , 

signals = [ 'LFVTtVecU']# ,[ 'LFVStVecU' ] #  

for y in years :
    print y

    for s in signals :
        print s
        signals = [s]
        sig = [s]

        mc = mc_backgrounds + signals

        # Introduction of categories to be analysed
        categories = {
            # this defines the CHANNEL name used in the context of CombineHarvester
            'emul' : [( 1, 'emul' )], # way to assign a category, c2018ed BIN in CombineHarvester with a string name and a BIN index
            #TODO section 8: extend with emu channel here in the same manner
        }

        for channel in categories:
            cb.AddObservations(['*'], ['vecu'], [y], [channel],              categories[channel]) # adding observed data
            cb.AddProcesses(   ['*'], ['vecu'], [y], [channel], backgrounds, categories[channel], False ) # adding backgrounds
            cb.AddProcesses(   ['*'], ['vecu'], [y], [channel], signals ,          categories[channel], True ) # adding signals
            
        #cb.ForEachObs(lambda x : x.set_process('data_obs')) # some hack to changxe the naming to the one in the input files; usual name: data_obs
        # Adding systematic uncertainties

        ## Normalization uncertainties, modelled with nuisance parameters drawn from lnN distributions:
        if y == '2018':
            cb.cp().process(mc).AddSyst(cb,'lumi2018_', 'lnN', ch.SystMap()(1.025)) # 2.3 % uncertainty on luminosity for 2018 from the measurement
        elif y == '2017':
            cb.cp().process(mc).AddSyst(cb,'lumi2017_', 'lnN', ch.SystMap()(1.023)) # 2.3 % uncertainty on luminosity for 2018 from the measurement
        elif y == '2016':
            cb.cp().process(mc).AddSyst(cb,'lumi2016_', 'lnN', ch.SystMap()(1.012)) # 2.3 % uncertainty on luminosity for 2018 from the measurement

        ## FIX ME : these should be different per year and may need to be updated, these are 2018 numbers from Reza
        cb.cp().process(mc).AddSyst(cb,'lumiXY_', 'lnN', ch.SystMap()(1.02)) 
        cb.cp().process(mc).AddSyst(cb,'lumiLengthS_', 'lnN', ch.SystMap()(1.002)) 
        cb.cp().process(mc).AddSyst(cb,'lumiBeamCC_', 'lnN', ch.SystMap()(1.002)) 

        #cb.cp().process(mc).AddSyst(cb,'muon_eff', 'lnN', ch.SystMap()(1.02)) # 2 % uncertainty on muon ID + Isolation efficiency
        # check if muon efficiency is dfferent than electron
        # Below are taken into account using their _UP/DOWN variation
        #b-tagging, trigger, JEC, PU, ECAL prefiring, L1 prefiring, 
        # to be added later HEM

        cb.cp().process(['nonprompt']).AddSyst(cb, 'unc_nonprompt', 'lnN', ch.SystMap()(1.1))
        #cb.cp().process(['others']).AddSyst(cb, 'xsec_others', 'lnN', ch.SystMap()(1.2))
        cb.cp().process(['VV']).AddSyst(cb, 'xsec_vv', 'lnN', ch.SystMap()(1.06)) 
        cb.cp().process(['WZ']).AddSyst(cb, 'xsec_wz', 'lnN', ch.SystMap()(1.12)) 
        cb.cp().process(['TX']).AddSyst(cb, 'xsec_tx', 'lnN', ch.SystMap()(1.12)) 

        # Unconstrained rate parameter introduced for the tau ID efficiency, which usu2018y is measured in the same region as the cross-section for Z->tautau.
        #       This means, that these can not be disentangled in mutau final state alone. TODO section 8: consider, whether TopT and/or EWKT need to be considered
        #cb.cp().channel(['mutau']).process(['ZTT', 'TopT', 'EWKT']).AddSyst(cb, 'tauh_id', 'rateParam', ch.SystMap()(1.0))

        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'MET_', 'shape', ch.SystMap()(1.0))                                   


        #cb.cp().channel(['emul']).process(['VV', 'WZ']).AddSyst(cb, 'eleRecoSf_', 'shape', ch.SystMap()(1.0))
        #cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU']).AddSyst(cb, 'jes_', 'shape', ch.SystMap()(1.0))                                  
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesAbsoluteMPFBias_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesAbsoluteScale_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesFlavorQCD_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesFragmentation_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpDataMC_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpPtBB_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpPtEC1_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpPtEC2_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpPtHF_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesPileUpPtRef_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesRelativeFSR_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeJEREC1_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeJEREC2_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesRelativeJERHF_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesRelativePtBB_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativePtEC1_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativePtEC2_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesRelativePtHF_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesRelativeBal_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeSample_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeStatEC_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeStatFSR_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesRelativeStatHF_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesSinglePionECAL_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesSinglePionHCAL_', 'shape', ch.SystMap()(1.0))                                   
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y'+y+'jesTimePtEta_', 'shape', ch.SystMap()(1.0))                                   


        if y == '2018':
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jer2018_', 'shape', ch.SystMap()(1.0))
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y2018jesAbsoluteStat_', 'shape', ch.SystMap()(1.0))                                   

        elif y == '2017':
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jer2017_', 'shape', ch.SystMap()(1.0))
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y2017jesAbsoluteStat_', 'shape', ch.SystMap()(1.0))                                   

        elif y == '2016':
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jer2016_', 'shape', ch.SystMap()(1.0))
            cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'Y2016jesAbsoluteStat_', 'shape', ch.SystMap()(1.0))                                   



        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'jesHEMIssue_', 'shape', ch.SystMap()(1.0))


        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'udsgTagSF_', 'shape', ch.SystMap()(1.0))     
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'pu_', 'shape', ch.SystMap()(1.0))
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'prefiring_', 'shape', ch.SystMap()(1.0))
        #cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'eleR_', 'shape', ch.SystMap()(1.0))
        #cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'eleF_', 'shape', ch.SystMap()(1.0))
       # cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'muR_', 'shape', ch.SystMap()(1.0))
       # cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'muF_', 'shape', ch.SystMap()(1.0))      
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'bcTagSF_', 'shape', ch.SystMap()(1.0))
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0]]).AddSyst(cb, 'eleRecoSf_', 'shape', ch.SystMap()(1.0))
        cb.cp().channel(['emul']).process(['VV', 'WZ','TX',sig[0] ]).AddSyst(cb, 'muIdSf_', 'shape', ch.SystMap()(1.0))

        # Define access of the input histograms; please note how systematics shape variations should be stored:
        #       $BIN/m_vis_$PROCESS_$SYSTEMATIC with $SYSTEMATIC containing the name like 'tau_es' and a postfix 'Up' or 'Down'
        for channel in categories:

            filepath_mc = os.path.join(os.environ['CMSSW_BASE'],'src/CombineHarvester/CMSDAS2020TauLong/shapes/apr13/', y+'_correlationsHistsSplitMC.root')

            if s ==  'LFVTtVecU' :
                cb.cp().channel([channel]).backgrounds().ExtractShapes(filepath_mc,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_TT'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_$SYSTEMATIC')
            else :
                cb.cp().channel([channel]).backgrounds().ExtractShapes(filepath_mc,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST_$SYSTEMATIC')

            #filepath_signal = os.path.join(os.environ['CMSSW_BASE'],'src/CombineHarvester/CMSDAS2020TauLong/shapes','2018_'+ signals[0]+'.root')
            if s ==  'LFVTtVecU' :
                cb.cp().channel([channel]).signals().ExtractShapes(filepath_mc, '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_TT'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_TT_$SYSTEMATIC')
            else :
                cb.cp().channel([channel]).signals().ExtractShapes(filepath_mc, '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST_$SYSTEMATIC')

        ch.SetStandardBinNames(cb, '$ANALYSIS_$CHANNEL_$BIN_$ERA') # Define the name of the category names
        cb.SetAutoMCStats(cb, 0.0) # Introducing statistical uncertainties on the total background for each histogram bin (Barlow-Beeston lite approach)


        writer = ch.CardWriter('lfv_analysis/$BIN_'+y+'_Apr12_'+s+'_noRF.txt','lfv_analysis/$BIN_'+y+'_Apr12_'+s+'_noRF.root') 
        # define the paths for the .txt datacard and the root inputs


        writer.SetWildcardMasses([])

        writer.WriteCards('cmb', cb) # writing 2018 datacards into one folder for combination

        for channel in categories:
            writer.WriteCards(channel, cb.cp().channel([channel])) # writing datacards for each final state in a corresponding folder to be able to perform the measurement individu2018y in each final state




