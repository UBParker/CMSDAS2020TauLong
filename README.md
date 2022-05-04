
# This limit setting framework uses the data card creation workflow from CMSDAS2020TauLong


### How to set the limits for AN-20-098 ###
#########################################
``

### Creating the data cards

We use BDT distributions trained with either ST or TT signal MC for each year of data taking to create data cards using the following commands.

Below example creates all run 2 data cards for the LFV Vector U process.
This analysis will set limits on 20 such processes.

```
cd scripts

python construct_datacards_LFV_All_10bins.py --y 2016 --s LFVStVecU
python construct_datacards_LFV_All_10bins.py --y 2017 --s LFVStVecU
python construct_datacards_LFV_All_10bins.py --y 2018 --s LFVStVecU

python construct_datacards_LFV_All_10bins.py --y 2016 --s LFVTtVecU
python construct_datacards_LFV_All_10bins.py --y 2017 --s LFVTtVecU
python construct_datacards_LFV_All_10bins.py --y 2018 --s LFVTtVecU
```


### Combining the data cards

We combine the ST and TT data cards for each year and then we combine the years for a full run 2 data card.



```
cd lfv_analysis/

combineCards.py st2016=vecu_emul_emul_2016_2016_10bin_LFVStVecU.txt tt2016=vecu_emul_emul_2016_2016_10bin_LFVTtVecU.txt > vecu_emul_emul_2016_2016_10bin_TTandST.txt

combineCards.py st2017=vecu_emul_emul_2017_2017_10bin_LFVStVecU.txt tt2017=vecu_emul_emul_2017_2017_10bin_LFVTtVecU.txt > vecu_emul_emul_2017_2017_10bin_TTandST.txt

combineCards.py st2018=vecu_emul_emul_2018_2018_10bin_LFVStVecU.txt tt2018=vecu_emul_emul_2018_2018_10bin_LFVTtVecU.txt > vecu_emul_emul_2018_2018_10bin_TTandST.txt

combineCards.py b2016=vecu_emul_emul_2016_2016_10bin_TTandST.txt b2017=vecu_emul_emul_2017_2017_10bin_TTandST.txt b2018=vecu_emul_emul_2018_2018_10bin_TTandST.txt > vecu_emul_emul_run2_10bin_TTandST.txt

```

### Creating workspaces from the data cards

The impact plots require us to make the txt file data cards into ROOT workspaces so we do this and then use the workspaces to set limits and determine impacts of nuissance parameters.


```
combineTool.py -M T2W -i vecu_emul_emul_run2_10bin_TTandST.txt  -o ws_vecu_emul_emul_run2_10bin_TTandST.root  --parallel 4

combineTool.py -M T2W -i vecu_emul_emul_2016_2016_10bin_TTandST.txt  -o ws_vecu_emul_emul_2016_2016_10bin_TTandST.root  --parallel 4

combineTool.py -M T2W -i vecu_emul_emul_2017_2017_10bin_TTandST.txt  -o ws_vecu_emul_emul_2017_2017_10bin_TTandST.root  --parallel 4
combineTool.py -M T2W -i vecu_emul_emul_2018_2018_10bin_TTandST.txt  -o ws_vecu_emul_emul_2018_2018_10bin_TTandST.root  --parallel 4


```


### Set the Limit on signal strength of the combined process

Notice the first command determines the limit and the next gets the output from the first and puts it in a .json file for easy extraction.


```
 combine --run blind -M AsymptoticLimits -d  ws_vecu_emul_emul_2016_2016_10bin_TTandST.root  -n setrto1-16-May2-10bin --expectSignal 1

combineTool.py -M CollectLimits *setrto1-16-May2-10bin* --use-dirs -o setrto1-16limits_May2.json

 combine --run blind -M AsymptoticLimits -d  ws_vecu_emul_emul_2017_2017_10bin_TTandST.root  -n setrto1-17-May2-10bin --expectSignal 1

combineTool.py -M CollectLimits *setrto1-17-May2-10bin* --use-dirs -o setrto1-17limits_May2-10bin.json

 combine --run blind -M AsymptoticLimits -d  ws_vecu_emul_emul_2018_2018_10bin_TTandST.root  -n setrto1-18-May2-10bin --expectSignal 1

combineTool.py -M CollectLimits *setrto1-18-May2-10bin* --use-dirs -o setrto1-18limits_May2_10bin.json

combine --run blind -M AsymptoticLimits -d  ws_vecu_emul_emul_run2_10bin_TTandST.root  -n setrto1-run2 --expectSignal 1

combineTool.py -M CollectLimits *setrto1-run2* --use-dirs -o setrto1-run2limits.json

```

### Determine impacts of the nuissance parameters


These commands will give you the run 2 impacts.


```
combineTool.py -M Impacts -d ws_vecu_emul_emul_run2_10bin_TTandST.root -m 125  --rMin -5 --rMax 10 --robustFit 1 --doInitialFit  -t -1 --expectSignal 1 --cminDefaultMinimizerStrategy 0

combineTool.py -M Impacts -d ws_vecu_emul_emul_run2_10bin_TTandST.root  -m 125  --doFits  --rMin -5 --rMax 10 --robustFit 1  -t -1 --expectSignal 1 --cminDefaultMinimizerStrategy 0


combineTool.py -M Impacts -d ws_vecu_emul_emul_run2_10bin_TTandST.root  -m 125 -o All_expectSignal_May2_TTandST_impacts.json


plotImpacts.py -i All_expectSignal_May2_TTandST_impacts.json -o All_expectSignal_May2_TTandST_impacts
```


# Below are the original REAQDAME info from the cloned Repo

# CMSDAS2020TauLong



Analysis specific software for statistical inference to be used with CombinedLimit and CombineHarvester

Written in the context of the CMSvDAS2020 Tau Long Exercise:

CMSvDAS2020 indico agenda: https://indico.cern.ch/event/886923/

CMSvDAS2020 Long Exercises Twiki: https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookExercisesCMSDataAnalysisSchool#LongExercises2020CERN

For the details on the Tau Long Exercises, please have a look at:

https://github.com/ArturAkh/TauFW/blob/master/docs/CMSDAS2020/main.md

The software of this package is used in sections [8. Preparing for statistical inference](https://github.com/ArturAkh/TauFW/blob/master/docs/CMSDAS2020/prep_stat_inference.md) and
[9. Performing the measurement](https://github.com/ArturAkh/TauFW/blob/master/docs/CMSDAS2020/measurement.md).

The setup of this software is explained in [1. Setting up the analysis software](https://github.com/ArturAkh/TauFW/blob/master/docs/CMSDAS2020/sw_setup.md#checking-out-the-analysis-software)
