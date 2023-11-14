from pathlib import Path

import numpy as np
from numpy.lib.arraysetops import isin

import ecgdigitize
import ecgdigitize.signal
import ecgdigitize.image
from ecgdigitize import common, visualization
from ecgdigitize.image import ColorImage, Rectangle

from model.InputParameters import InputParameters


def convertECGLeads(inputImage: ColorImage, parameters: InputParameters):
    # Apply rotation
    rotatedImage = ecgdigitize.image.rotated(inputImage, parameters.rotation)

    # Crop each lead
    leadImages = {
        leadId: ecgdigitize.image.cropped(rotatedImage, Rectangle(lead.x, lead.y, lead.width, lead.height))
        for leadId, lead in parameters.leads.items()
    }

    extractSignal = ecgdigitize.digitizeSignal
    extractGrid   = ecgdigitize.digitizeGrid

    # Map all lead images to signal data
    signals = {
        leadId: extractSignal(leadImage)
        for leadId, leadImage in leadImages.items()
    }

    # If all signals failed -> Failure
    if all([isinstance(signal, common.Failure) for _, signal in signals.items()]):
        return None, None
    for leadId, points in signals.items():
        signal,time = points
        print(leadId,signal,time)
    # bounds = {
    #     leadId: (max([])-min([]),max([])-min([]))
    #     for leadId, signal in signals
    # }

    previews = {
        leadId: visualization.overlaySignalOnImage(signal[0], image)
        for (leadId, image), (_, signal) in zip(leadImages.items(), signals.items())
    }

    # Map leads to grid size estimates
    # gridSpacings = {
    #     leadId: extractGrid(leadImage)
    #     for leadId, leadImage in leadImages.items()
    # }
    # Just got successful spacings
    spacings = [spacing for spacing in gridSpacings.values() if not isinstance(spacing, common.Failure)]

    if len(spacings) == 0:
        return None, None

    samplingPeriodInPixels = gridHeightInPixels = common.mean(spacings)

    # Scale signals
    # TODO: Scale According to px/mv/ms fiducials
    scaledSignals = {
        leadId: ecgdigitize.signal.verticallyScaleECGSignal(
            ecgdigitize.signal.zeroECGSignal(signal[0]),
            gridHeightInPixels,
            parameters.voltScale, gridSizeInMillimeters=1.0
        )
        for leadId, signal in signals.items()
    }

    # TODO: Pass in the grid size in mm
    samplingPeriod = ecgdigitize.signal.ecgSignalSamplingPeriod(samplingPeriodInPixels, parameters.timeScale, gridSizeInMillimeters=1.0)

    # 3. Zero pad all signals on the left based on their start times and the samplingPeriod
    # take the max([len(x) for x in signals]) and zero pad all signals on the right
    paddedSignals = {
        leadId: common.padLeft(signal, int(parameters.leads[leadId].startTime / samplingPeriod))
        for leadId, signal in scaledSignals.items()
    }

    # (should already be handled by (3)) Replace any None signals with all zeros
    maxLength = max([len(s) for _, s in paddedSignals.items()])
    fullSignals = {
        leadId: common.padRight(signal, maxLength - len(signal))
        for leadId, signal in paddedSignals.items()
    }
    fullSignals["samplingPeriod"]=samplingPeriod

    return fullSignals, previews


def exportSignals(leadSignals, filePath, separator='\t'):
    """Exports a dict of lead signals to file

    Args:
        leadSignals (Dict[str -> np.ndarray]): Dict mapping lead id's to np array of signal data (output from convertECGLeads)
    """

    samplingPeriod=leadSignals["samplingPeriod"]
    leads = common.zipDict(leadSignals)
    for lead,signal in leads:
        print(lead,type(signal))
    leads = common.filterList(leads,lambda pair:type(pair[1])==np.ndarray)
    leads.sort(key=lambda pair: pair[0].value)

    assert len(leads) >= 1
    lengthOfFirst = len(leads[0][1])

    assert all([len(signal) == lengthOfFirst for key, signal in leads])

    header = separator.join([str(leadId) for leadId,_ in leads])+"\n"
    collated = np.array([signal for _, signal in leads])
    output = np.swapaxes(collated, 0, 1)

    if not issubclass(type(filePath), Path):
        filePath = Path(filePath)

    if filePath.exists():
        print("Warning: Output file will be overwritten!")

    outputLines = [f"sample period {samplingPeriod}\n","\n"]
    outputLines += header
    outputLines += [
        separator.join(
            [str(val) for val in row]
        ) + "\n"
        for row in output
    ]

    with open(filePath, 'w') as outputFile:
        outputFile.writelines(outputLines)
