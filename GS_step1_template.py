#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

import sys
args = sys.argv

print '.............. enter GS_step1_template.py ............'

lhe = 'None'
nmax = 1
nskip = 0

if len(args)!=7:
    print 'Provide [sample][index][lhe file][nmax][nskip]', len(args)
    sys.exit(0)
else:
    sample = args[2]
    index = args[3]
    lhe = args[4]
    nmax = int(args[5])
    nskip = int(args[6])


print 'sample name = ', sample
print 'index = ', index
print 'LHE file = ', lhe
print 'nmax = ', nmax
print 'nskip = ', nskip


#########################

process = cms.Process("Gen")

process.source = cms.Source("LHESource",

fileNames = cms.untracked.vstring('file:' + lhe),

skipEvents = cms.untracked.uint32(nskip)
)

# YT
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(nmax))

# process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('alpha'),
	name = cms.untracked.string('LHEF input'),
	annotation = cms.untracked.string('ttbar')
)

process.load("Configuration.StandardSequences.Services_cff")

process.RandomNumberGeneratorService.generator = cms.PSet(
	initialSeed = cms.untracked.uint32(123456789),
	engineName = cms.untracked.string('HepJamesRandom')
)


from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'

#process.load("RecoJets.Configuration.RecoGenJets_cff")
#process.ak4PartonJets  =  process.ak4GenJets.clone()
#process.ak4PartonJets.src = cms.InputTag("genParticlesForPartonJets")

process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.ak5PartonJets  =  process.ak5GenJets.clone()
process.ak5PartonJets.src = cms.InputTag("genParticlesForPartonJets")

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.genParticlesForPartonJets = process.genParticlesForJets.clone()
#process.genParticlesForPartonJets.partonicFinalState = True
process.genParticlesForPartonJets.excludeFromResonancePids = cms.vuint32(11,12,13,14,15,16,7000001,7000021,6000007)
process.genParticlesForPartonJets.ignoreParticleIDs += cms.vuint32(11,12,13,14,15,16,7000001,7000021,6000007)

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
	eventsToPrint = cms.untracked.uint32(0),
        UseExternalGenerators = cms.untracked.bool(True),
	maxEventsToPrint = cms.untracked.int32(0),
    	pythiaPylistVerbosity = cms.untracked.int32(1),
    	filterEfficiency = cms.untracked.double(1.0),
    	pythiaHepMCVerbosity = cms.untracked.bool(False), 
        comEnergy = cms.double(13000.),
#        comEnergy = cms.double(8000.),
#	SLHAFileForPythia8 = cms.string('powheg-fh-output_tautau.slha'),
       	PythiaParameters = cms.PSet(
                processParameters = cms.vstring(
	        	'Main:timesAllowErrors = 10000',
        	        'ParticleDecays:limitTau0 = off',
			'ParticleDecays:tau0Max = 10',
        		'Tune:ee 3',
        		'Tune:pp 5',
			'SpaceShower:pTmaxMatch = 1',
			'SpaceShower:pTmaxFudge = 1',
			'SpaceShower:MEcorrections = off',
			'TimeShower:pTmaxMatch = 1',
			'TimeShower:pTmaxFudge = 1',
			'TimeShower:MEcorrections = off',
			'TimeShower:globalRecoil = on',
			'TimeShower:limitPTmaxGlobal = on',
			'TimeShower:nMaxGlobalRecoil = 1',
			'TimeShower:globalRecoilMode = 2',
			'TimeShower:nMaxGlobalBranch = 1',
			'Check:epTolErr = 0.01',
        		'SLHA:keepSM = on',
        		'SLHA:minMassSM = 10.',
#        		'25:onMode = off',
#			'25:onIfMatch = 15 -15',
#        		'36:onMode = off',
#      			'36:onIfMatch = 15 -15',
#                        '15:offIfAny = 11 13'
			),  
	       		parameterSets = cms.vstring('processParameters'))
)

#process.vlq_analysis = cms.EDAnalyzer("vlq",
#	    HistOutFile = cms.untracked.string('vn30GeV_R_V.root'),
#	    parton_jets = cms.InputTag("ak4PartonJets")#
#	    parton_or_gen_jets = cms.InputTag("ak5PartonJets")
#)

process.load("Configuration.StandardSequences.Generator_cff")

process.load("Configuration.StandardSequences.VtxSmearedNoSmear_cff")

process.genParticles.abortOnUnknownPDGCode = False

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.printList = cms.EDAnalyzer("ParticleListDrawer",
	src = cms.InputTag("genParticles"),
	maxEventsToPrint = cms.untracked.int32(0)
)

process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
	src = cms.InputTag("genParticles"),
	printP4 = cms.untracked.bool(False),
	printPtEtaPhi = cms.untracked.bool(False),
	printVertex = cms.untracked.bool(True),
	printStatus = cms.untracked.bool(False),
	printIndex = cms.untracked.bool(False),
	status = cms.untracked.vint32(1, 2, 3)
)

process.p = cms.Path(
#	process.printList *
	process.printTree
)

process.load("Configuration.EventContent.EventContent_cff")

process.GEN = cms.OutputModule("PoolOutputModule",
	process.FEVTSIMEventContent,
	dataset = cms.untracked.PSet(dataTier = cms.untracked.string('GEN')),
	SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p0')),
	fileName = cms.untracked.string('file:test.root')
)


process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
#    fileName = cms.untracked.string("root://eoscms//eos/cms/store/cmst3/user/ytakahas/LowMass/output.root"),
    fileName = cms.untracked.string("file:GS_" + sample + "_" + index + ".root"),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p0')
    )
)



process.p0 = cms.Path(
	process.generator *
	process.pgen
)

process.dump = cms.EDAnalyzer("EventContentAnalyzer")

process.dumpevent = cms.Path(process.dump)

#process.partonjets = cms.Path(process.genParticlesForPartonJets*process.ak5PartonJets)
#process.partonjets = cms.Path(process.genParticlesForPartonJets*process.ak4PartonJets)

#process.an = cms.Path(process.vlq_analysis)

#process.schedule = cms.Schedule(process.p0, process.partonjets, process.dumpevent, process.an)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

process.simulation_step = cms.Path(process.psim)


process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.p0, process.simulation_step, process.RAWSIMoutput_step)
