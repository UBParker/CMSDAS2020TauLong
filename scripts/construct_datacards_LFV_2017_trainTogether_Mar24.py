#! /usr/bin/env python
import CombineHarvester.CombineTools.ch as ch
import os
import ROOT

cb = ch.CombineHarvester()
cb.SetFlag('workspaces-use-clone', True)

# Definition of process names to be used in the analysis
mc_backgrounds = [ 'VV', 'WZ', 'TX' ,'nonprompt' ]  # TODO : Add TX : '2017_TX'
data_driven_backgrounds = ['TTbar', 'others']
backgrounds = mc_backgrounds + data_driven_backgrounds

signals = ['LFVStVecU', 'LFVTtVecU' ]

mc = mc_backgrounds + signals

# Introduction of categories to be analysed
categories = {
    # this defines the CHANNEL name used in the context of CombineHarvester
    'emul' : [( 1, 'emul' )], # way to assign a category, c2017ed BIN in CombineHarvester with a string name and a BIN index
    #TODO section 8: extend with emu channel here in the same manner
}

for channel in categories:
    cb.AddObservations(['*'], ['vecu'], ['2017'], [channel],              categories[channel]) # adding observed data
    cb.AddProcesses(   ['*'], ['vecu'], ['2017'], [channel], backgrounds, categories[channel], False ) # adding backgrounds
    cb.AddProcesses(   ['*'], ['vecu'], ['2017'], [channel], signals,     categories[channel], True ) # adding signals
    
#cb.ForEachObs(lambda x : x.set_process('data_obs')) # some hack to changxe the naming to the one in the input files; usual name: data_obs
# Adding systematic uncertainties

## Normalization uncertainties, modelled with nuisance parameters drawn from lnN distributions:

cb.cp().process(mc).AddSyst(cb,'a2017lumi_', 'lnN', ch.SystMap()(1.02)) # 2.3 % uncertainty on luminosity for 2017 from the measurement

#cb.cp().process(mc).AddSyst(cb,'muon_eff', 'lnN', ch.SystMap()(1.02)) # 2 % uncertainty on muon ID + Isolation efficiency
# check if muon efficiency is dfferent than electron
# Below are taken into account using their _UP/DOWN variation
#b-tagging, trigger, JEC, PU, ECAL prefiring, L1 prefiring, 
# to be added later HEM

cb.cp().process(['nonprompt']).AddSyst(cb, 'unc_nonprompt', 'lnN', ch.SystMap()(1.1))
#cb.cp().process(['others']).AddSyst(cb, 'xsec_others', 'lnN', ch.SystMap()(1.2))
cb.cp().process(['VV']).AddSyst(cb, 'xsec_vv', 'lnN', ch.SystMap()(1.06)) 
cb.cp().process(['WZ']).AddSyst(cb, 'xsec_wz', 'lnN', ch.SystMap()(1.06)) 
cb.cp().process(['TX']).AddSyst(cb, 'xsec_tx', 'lnN', ch.SystMap()(1.12)) 

# Unconstrained rate parameter introduced for the tau ID efficiency, which usu2017y is measured in the same region as the cross-section for Z->tautau.
#       This means, that these can not be disentangled in mutau final state alone. TODO section 8: consider, whether TopT and/or EWKT need to be considered
#cb.cp().channel(['mutau']).process(['ZTT', 'TopT', 'EWKT']).AddSyst(cb, 'tauh_id', 'rateParam', ch.SystMap()(1.0))


#cb.cp().channel(['emul']).process(['VV', 'WZ']).AddSyst(cb, 'eleRecoSf_', 'shape', ch.SystMap()(1.0))
#cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU']).AddSyst(cb, 'jes_', 'shape', ch.SystMap()(1.0))                                  
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'jes_', 'shape', ch.SystMap()(1.0))                                   
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'a2017jer_', 'shape', ch.SystMap()(1.0))


cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'udsgTagSF_', 'shape', ch.SystMap()(1.0))     
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'pu_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'prefiring_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'eleR_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'eleF_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'muR_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['nonprompt']).AddSyst(cb, 'muF_', 'shape', ch.SystMap()(1.0))      
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'bcTagSF_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU']).AddSyst(cb, 'eleRecoSf_', 'shape', ch.SystMap()(1.0))
cb.cp().channel(['emul']).process(['VV', 'WZ','LFVStVecU','TX','LFVTtVecU' ]).AddSyst(cb, 'muIdSf_', 'shape', ch.SystMap()(1.0))

# Define access of the input histograms; please note how systematics shape variations should be stored:
#       $BIN/m_vis_$PROCESS_$SYSTEMATIC with $SYSTEMATIC containing the name like 'tau_es' and a postfix 'Up' or 'Down'
for channel in categories:

    filepath_mc = os.path.join(os.environ['CMSSW_BASE'],'src/CombineHarvester/CMSDAS2020TauLong/shapes/newMar24/2017/', '2017_HistsMC.root')

    cb.cp().channel([channel]).backgrounds().ExtractShapes(filepath_mc,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST_$SYSTEMATIC')

    #filepath_signal = os.path.join(os.environ['CMSSW_BASE'],'src/CombineHarvester/CMSDAS2020TauLong/shapes','2017_'+ signals[0]+'.root')

    cb.cp().channel([channel]).signals().ExtractShapes(filepath_mc, '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST'  ,  '$PROCESS_VR_$BIN_lllOffZMetg20Jetgeq1Bleq1_BDT_ST_$SYSTEMATIC')

ch.SetStandardBinNames(cb, '$ANALYSIS_$CHANNEL_$BIN_$ERA') # Define the name of the category names
cb.SetAutoMCStats(cb, 0.0) # Introducing statistical uncertainties on the total background for each histogram bin (Barlow-Beeston lite approach)

writer = ch.CardWriter('lfv_analysis/2017/$TAG/$BIN_2017_newMar24_together.txt','lfv_analysis/2017/$TAG/common/$BIN_2017_newMar24_together.root') # define the paths for the .txt datacard and the root inputs
writer.SetWildcardMasses([])

writer.WriteCards('cmb', cb) # writing 2017 datacards into one folder for combination

for channel in categories:
    writer.WriteCards(channel, cb.cp().channel([channel])) # writing datacards for each final state in a corresponding folder to be able to perform the measurement individu2017y in each final state




