NegativeTime = -1
ConditionNotSatisfied = -2
NoWorkerExists = -3
WrongBuildingName = -4
WrongUpgradeName = -5
WrongUnitName = -6
UnknownError = -7
WrongFlag = -8
SupplyBlocked = -9
NoBarrackExists = -10
NoOneGathersGasOrMineral = -11
MineralFieldsAreFull = -12
NoOneGathersGas = -13
GasLayersAreFull = -14
NotEnoughWorkers = -15
NoRefineryExists = -16
ChronoCooldown = -17
ChronoNotAvailable = -18
AlreadyBoosted = -19 
UnboostableBuilding = -20
WrongIndex = -21
NoItemToDelete = -22
NoPathExists = -23
NotUnitType = -24
NotBuildingType = -25
UniqueOnly = -26
WrongRace = -27
WrongFileFormat = -28
IncompatibleVersion = -29

def ErrorMsg(e):
    if e == NegativeTime:
        return "Wrong time - negative number was inserted"
    elif e == ConditionNotSatisfied:
        return "Something is missing"
    elif e == NoWorkerExists:
        return "No worker exists"
    elif e == WrongBuildingName:
        return "Wrong building name"
    elif e == WrongUpgradeName:
        return "Wrong upgrade name"
    elif e == WrongUnitName:
        return "Wrong unit name"
    elif e == UnknownError:
        return "Unknown error"
    elif e == WrongFlag:
        return "wrong type - it must be 'unit', 'building' or 'upgrade'"
    elif e == SupplyBlocked:
        return "Supply blocked - you should construct pylon or etc"
    elif e == NoBarrackExists:
        return "No appropriate barrack exists"
    elif e == NoOneGathersGasOrMineral:
        return "No one gathers gas or mineral"
    elif e == MineralFieldsAreFull:
        return "Mineral fields are full"
    elif e == NoOneGathersGas:
        return "No one ghaters gas"
    elif e == GasLayersAreFull:
        return "Gas layers are full"
    elif e == NotEnoughWorkers:
        return "Not enough workers"
    elif e == NoRefineryExists:
        return "No refinery exists"
    elif e == ChronoCooldown:
        return "Chronoboost in cooldown"
    elif e == ChronoNotAvailable:
        return "Chronoboost is not available - you may not have a nexus"
    elif e == AlreadyBoosted:
        return "All buildings are already boosted"
    elif e == UnboostableBuilding:
        return "That building isn't able to be chronoboosted"
    elif e == WrongIndex:
        return "Wrong index"
    elif e== NoItemToDelete:
        return "No item to delete"
    elif e == NoPathExists:
        return "No Icon Exists"
    elif e == NotUnitType:
        return "not unit type"
    elif e == NotBuildingType:
        return "not building type"
    elif e == UniqueOnly:
        return "you can't do this more than once"
    elif e == WrongRace:
        return "wrong race name"
    elif e == WrongFileFormat:
        return "wrong file format or it's cracked"
    elif e == IncompatibleVersion:
        return "incompatible version file"
    else:
        return "Unknown error code"
