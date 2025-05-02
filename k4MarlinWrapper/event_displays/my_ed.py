#!/usr/bin/env python3
#
# Copyright (c) 2019-2024 Key4hep-Project.
#
# This file is part of Key4hep.
# See https://key4hep.github.io/key4hep-doc/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from Configurables import EventDataSvc, GeoSvc, MarlinProcessorWrapper
from Gaudi.Configuration import INFO
from k4FWCore import ApplicationMgr, IOSvc
from k4FWCore.parseArgs import parser
from my_ced_viewer_config import config

from k4MarlinWrapper.io_helpers import IOHandlerHelper

parser.add_argument(
    "--inputFiles",
    action="extend",
    nargs="+",
    metavar=["file1", "file2"],
    help="One or multiple input files",
)

parser.add_argument(
    "--compactFile",
    help="Compact detector file to use",
    type=str,
    default="ILD/compact/ILD_sl5_v02/ILD_l5_o1_v02.xml",
)

reco_args = parser.parse_known_args()[0]

algList = []
svcList = [EventDataSvc("EventDataSvc")]

iosvc = IOSvc()

geoSvc = GeoSvc("GeoSvc")
geoSvc.detectors = [reco_args.compactFile]
geoSvc.OutputLevel = INFO
geoSvc.EnableGeant4Geo = False
svcList.append(geoSvc)

io_handler = IOHandlerHelper(algList, iosvc)
io_handler.add_reader(reco_args.inputFiles)

MyCEDViewer = MarlinProcessorWrapper("MyCEDViewer")
MyCEDViewer.OutputLevel = INFO
MyCEDViewer.ProcessorType = "DDCEDViewer"
MyCEDViewer.Parameters = config

algList.append(MyCEDViewer)

# We need to convert the inputs in case we have EDM4hep input
io_handler.finalize_converters()

ApplicationMgr(TopAlg=algList, EvtSel="NONE", EvtMax=10, ExtSvc=svcList, OutputLevel=INFO)
