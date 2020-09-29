#! /usr/bin/env python
import CombineHarvester.CombineTools.ch as ch
import os

cb = ch.CombineHarvester()
cb.SetFlag('workspaces-use-clone', True)

# Definition of process names to be used in the analysis
mc_backgrounds = ['TopT', 'TopJ', 'EWKT', 'EWKJ', 'ZL']
data_driven_backgrounds = ['QCD']
backgrounds = mc_backgrounds + data_driven_backgrounds

signals = ['ZTT']

mc = mc_backgrounds + signals

# Introduction of categories to be analysed
categories = {
    # this defines the CHANNEL name used in the context of CombineHarvester
    'mutau' : [( 1, 'signal_region' )], # way to assign a category, called BIN in CombineHarvester with a string name and a BIN index
    #TODO section 8: extend with emu channel here in the same manner
}

for channel in categories:
    cb.AddObservations(['*'], ['ztt'], ['2018'], [channel],              categories[channel]) # adding observed data
    cb.AddProcesses(   ['*'], ['ztt'], ['2018'], [channel], backgrounds, categories[channel], False) # adding backgrounds
    cb.AddProcesses(   ['*'], ['ztt'], ['2018'], [channel], signals,     categories[channel], True) # adding signals
    
cb.ForEachObs(lambda x : x.set_process('SingleMuon_Run2018')) # some hack to change the naming to the one in the input files; usual name: data_obs

# Adding systematic uncertainties

## Normalization uncertainties, modelled with nuisance parameters drawn from lnN distributions:

cb.cp().process(mc).AddSyst(cb,'lumi_2018', 'lnN', ch.SystMap()(1.025)) # 2.5 % uncertainty on luminosity for 2018 from the measurement
cb.cp().process(mc).AddSyst(cb,'muon_eff', 'lnN', ch.SystMap()(1.02)) # 2 % uncertainty on muon ID + Isolation efficiency

cb.cp().process(['TopT', 'TopJ']).AddSyst(cb, 'xsec_top', 'lnN', ch.SystMap()(1.06)) # conservative uncertainty estimate for ttbar (6%) single top (5%) cross-section
cb.cp().process(['EWKT', 'EWKJ']).AddSyst(cb, 'xsec_ewk', 'lnN', ch.SystMap()(1.05)) # conservative uncertainty estimate for w+jets (4%) and diboson (5%) cross-section
cb.cp().process(['ZL']).AddSyst(cb, 'xsec_zl', 'lnN', ch.SystMap()(1.04)) # uncertainty on DY production; note, that it is kept separated from signal here (for simplification)
cb.cp().process(['ZTT']).AddSyst(cb, 'xsec_ztt', 'lnN', ch.SystMap()(1.04)) # uncertainty on DY production; note, that it is kept separated from background here (for simplification)

cb.cp().process(['QCD']).AddSyst(cb, 'ss_to_os_extrap', 'lnN', ch.SystMap()(1.03)) # uncertainty on QCD extrapolation factor. # TODO section 8: update with the number measured by you


# Unconstrained rate parameter introduced for the tau ID efficiency, which usually is measured in the same region as the cross-section for Z->tautau.
#       This means, that these can not be disentangled in mutau final state alone. TODO section 8: consider, whether TopT and/or EWKT need to be considered
cb.cp().channel(['mutau']).process(['ZTT', 'TopT', 'EWKT']).AddSyst(cb, 'tauh_id', 'rateParam', ch.SystMap()(1.0))

# # TODO section 8: Introduce the tauh energy scale uncertainty. Consider, whether TopT and/or EWKT need to be considered
#cb.cp().channel(['mutau']).process(['ZTT', 'TopT', 'EWKT']).AddSyst(cb, 'tauh_es', 'shape', ch.SystMap()(1.0))

# Define access of the input histograms; please note how systematics shape variations should be stored:
#       $BIN/m_vis_$PROCESS_$SYSTEMATIC with $SYSTEMATIC containing the name like 'tau_es' and a postfix 'Up' or 'Down'
for channel in categories:
    filepath = os.path.join(os.environ['CMSSW_BASE'],'src/CombineHarvester/CMSDAS2020TauLong/shapes', channel+'.root')
    cb.cp().channel([channel]).backgrounds().ExtractShapes(filepath, '$BIN/m_vis_$PROCESS', '$BIN/m_vis_$PROCESS_$SYSTEMATIC')
    cb.cp().channel([channel]).signals().ExtractShapes(filepath, '$BIN/m_vis_$PROCESS', '$BIN/m_vis_$PROCESS_$SYSTEMATIC')

ch.SetStandardBinNames(cb, '$ANALYSIS_$CHANNEL_$BIN_$ERA') # Define the name of the category names
cb.SetAutoMCStats(cb, 0.0) # Introducing statistical uncertainties on the total background for each histogram bin (Barlow-Beeston lite approach)

writer = ch.CardWriter('ztt_analysis/2018/$CHANNEL/$BIN.txt','ztt_analysis/2018/$CHANNEL/common/$BIN.root') # define the paths for the .txt datacard and 
writer.SetWildcardMasses([])
writer.WriteCards('', cb)
