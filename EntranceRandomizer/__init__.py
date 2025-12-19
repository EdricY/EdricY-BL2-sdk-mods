import os
import json
import random
import unrealsdk
import unrealsdk.unreal as unreal
from unrealsdk.hooks import Block, prevent_hooking_direct_calls
from mods_base import build_mod, hook, ButtonOption, SliderOption
# from save_options.options import HiddenSaveOption
from mods_base.keybinds import keybind
from ui_utils import show_chat_message

orig_entrance_dict = {
    "GD_LevelTravelStations.StockadeToAridNexus": "GD_LevelTravelStations.AridNexusToStockade",
    "GD_LevelTravelStations.Interlude.InterludeToIce": "GD_LevelTravelStations.Zone1.IceToInterlude",
    "GD_LevelTravelStations.Interlude.LynchwoodToInterlude": "GD_LevelTravelStations.Interlude.InterludeToLynchwood",
    "GD_LevelTravelStations.OutwashToFridge": "GD_LevelTravelStations.Zone2.FridgeToGrass",
    "GD_LevelTravelStations.Zone1.SanctuaryToIce": "GD_LevelTravelStations.Zone1.IceToSanctuary",
    "GD_LevelTravelStations.WilhelmToTundraExpress": "GD_LevelTravelStations.TundraExpressToWilhelm",
    "GD_LevelTravelStations.Zone1.CavernsToSanctuaryHole": "GD_LevelTravelStations.Zone1.SanctuaryHoleToCaverns",
    "GD_LevelTravelStations.Zone1.DamTopToDam": "GD_LevelTravelStations.Zone1.DamToDamTop",
    "GD_LevelTravelStations.Zone1.DamToIce": "GD_LevelTravelStations.Zone1.IceToDam",
    "GD_LevelTravelStations.Zone1.IceCanyonToIce": "GD_LevelTravelStations.Zone1.IceToIceCanyon",
    "GD_LevelTravelStations.Zone1.IceToWaterfront": "GD_LevelTravelStations.Zone1.WaterfrontToIce",
    "GD_LevelTravelStations.FrostToIce": "GD_LevelTravelStations.IcetoFrost",
    "GD_LevelTravelStations.Zone1.WaterfrontToGlacial": "GD_LevelTravelStations.Zone1.GlacialToWaterfront",
    "GD_LevelTravelStations.Zone1.TundraExpressToIce": "GD_LevelTravelStations.Zone1.IceToTundraExpress",
    "GD_LevelTravelStations.Zone2.CliffsToGrass": "GD_LevelTravelStations.Zone2.GrassToCliffs",
    "GD_LevelTravelStations.Zone2.BossCliffsToCliffs": "GD_LevelTravelStations.Zone2.CliffsToBossCliffs",
    "GD_LevelTravelStations.Zone2.GrassToFridge": "GD_LevelTravelStations.Zone2.FridgeToGrass",
    "GD_LevelTravelStations.Zone2.HyperionCityToGrass": "GD_LevelTravelStations.Zone2.GrassToHyperionCity",
    "GD_LevelTravelStations.Zone2.PandoraParkToGrass": "GD_LevelTravelStations.Zone2.GrassToPandoraPark",
    "GD_LevelTravelStations.Zone2.FridgeToIce": "GD_LevelTravelStations.Zone1.IceToFridge",
    "GD_LevelTravelStations.Zone3.AshToInterlude": "GD_LevelTravelStations.Interlude.InterludeToAsh",
    "GD_LevelTravelStations.Interlude.InterludeToAsh": "GD_LevelTravelStations.Zone3.AshToInterlude",
    "GD_LevelTravelStations.Zone3.CraterLakeToAsh": "GD_LevelTravelStations.Zone3.AshToCraterLake",
    "GD_LevelTravelStations.Zone3.FinalBossAscentToAsh": "GD_LevelTravelStations.Zone3.AshToFinalBossAscent",
    "GD_LevelTravelStations.Zone3.FyrestoneToAsh": "GD_LevelTravelStations.Zone3.AshToFyrestone",
    "GD_LevelTravelStations.AridNexusToStockade": "GD_LevelTravelStations.StockadeToAridNexus",
    "GD_LevelTravelStations.IcetoFrost": "GD_LevelTravelStations.FrostToIce",
    "GD_LevelTravelStations.Interlude.HypInterToInterlude": "GD_LevelTravelStations.Interlude.InterludeToHypInter",
    "GD_LevelTravelStations.Interlude.InterludeToHypInter": "GD_LevelTravelStations.Interlude.HypInterToInterlude",
    "GD_LevelTravelStations.Interlude.InterludeToGrass": "GD_LevelTravelStations.Zone2.GrassToInterlude",
    "GD_LevelTravelStations.Zone2.GrassToInterlude": "GD_LevelTravelStations.Interlude.InterludeToGrass",
    "GD_LevelTravelStations.Zone1.IceToInterlude": "GD_LevelTravelStations.Interlude.InterludeToIce",
    "GD_LevelTravelStations.Interlude.InterludeToLynchwood": "GD_LevelTravelStations.Interlude.LynchwoodToInterlude",
    "GD_LevelTravelStations.Zone2.FridgeToGrass": "GD_LevelTravelStations.OutwashToFridge",
    "GD_LevelTravelStations.OutwashToGrass": "GD_LevelTravelStations.Zone2.GrassToFridge",
    "GD_LevelTravelStations.TundraExpressToWilhelm": "GD_LevelTravelStations.WilhelmToTundraExpress",
    "GD_LevelTravelStations.Zone1.SanctuaryHoleToCaverns": "GD_LevelTravelStations.Zone1.CavernsToSanctuaryHole",
    "GD_LevelTravelStations.Zone1.CoveToWaterfront": "GD_LevelTravelStations.Zone1.WaterfrontToCove",
    "GD_LevelTravelStations.Zone1.WaterfrontToCove": "GD_LevelTravelStations.Zone1.CoveToWaterfront",
    "GD_LevelTravelStations.Zone1.DamToDamTop": "GD_LevelTravelStations.Zone1.DamTopToDam",
    "GD_LevelTravelStations.Zone1.IceToDam": "GD_LevelTravelStations.Zone1.DamToIce",
    "GD_LevelTravelStations.Zone1.GlacialToWaterfront": "GD_LevelTravelStations.Zone1.WaterfrontToGlacial",
    "GD_LevelTravelStations.Zone1.IceToIceCanyon": "GD_LevelTravelStations.Zone1.IceCanyonToIce",
    "GD_LevelTravelStations.Zone1.IceToFridge": "GD_LevelTravelStations.Zone2.FridgeToIce",
    "GD_LevelTravelStations.Zone1.IceToSanctuary": "GD_LevelTravelStations.Zone1.SanctuaryToIce",
    "GD_LevelTravelStations.Zone1.IceToSanctuaryHole": "GD_LevelTravelStations.Zone1.SanctuaryHoleToIce",
    "GD_LevelTravelStations.Zone1.SanctuaryHoleToIce": "GD_LevelTravelStations.Zone1.IceToSanctuaryHole",
    "GD_LevelTravelStations.Zone1.IceToSouthpawFactory": "GD_LevelTravelStations.Zone1.SouthpawFactoryToIce",
    "GD_LevelTravelStations.Zone1.SouthpawFactoryToIce": "GD_LevelTravelStations.Zone1.IceToSouthpawFactory",
    "GD_LevelTravelStations.Zone1.IceToTundraExpress": "GD_LevelTravelStations.Zone1.TundraExpressToIce",
    "GD_LevelTravelStations.Zone1.WaterfrontToIce": "GD_LevelTravelStations.Zone1.IceToWaterfront",
    "GD_LevelTravelStations.Zone2.BanditSlaughterToFridge": "GD_LevelTravelStations.Zone2.FridgeToBanditSlaughter",
    "GD_LevelTravelStations.Zone2.FridgeToBanditSlaughter": "GD_LevelTravelStations.Zone2.BanditSlaughterToFridge",
    "GD_LevelTravelStations.Zone2.CliffsToBossCliffs": "GD_LevelTravelStations.Zone2.BossCliffsToCliffs",
    "GD_LevelTravelStations.Zone2.BossCliffsToVOGsChamber": "GD_LevelTravelStations.Zone2.VOGsChamberToBossCliffs",
    "GD_LevelTravelStations.Zone2.VOGsChamberToBossCliffs": "GD_LevelTravelStations.Zone2.BossCliffsToVOGsChamber",
    "GD_LevelTravelStations.Zone2.GrassToCliffs": "GD_LevelTravelStations.Zone2.CliffsToGrass",
    "GD_LevelTravelStations.Zone2.CliffsToThresherRaid": "GD_LevelTravelStations.Zone2.ThresherRaidToCliffs",
    "GD_LevelTravelStations.Zone2.ThresherRaidToCliffs": "GD_LevelTravelStations.Zone2.CliffsToThresherRaid",
    "GD_LevelTravelStations.Zone2.CreatureSlaughterToPandoraPark": "GD_LevelTravelStations.Zone2.PandoraParkToCreatureSlaughter",
    "GD_LevelTravelStations.Zone2.PandoraParkToCreatureSlaughter": "GD_LevelTravelStations.Zone2.CreatureSlaughterToPandoraPark",
    "GD_LevelTravelStations.Zone2.GrassToHyperionCity": "GD_LevelTravelStations.Zone2.HyperionCityToGrass",
    "GD_LevelTravelStations.Zone2.GrassToLuckys": "GD_LevelTravelStations.Zone2.GrassToLuckys",
    "GD_LevelTravelStations.Zone2.LuckysToGrass": "GD_LevelTravelStations.Zone2.LuckysToGrass",
    "GD_LevelTravelStations.Zone2.GrassToPandoraPark": "GD_LevelTravelStations.Zone2.PandoraParkToGrass",
    "GD_LevelTravelStations.Zone3.AshToCraterLake": "GD_LevelTravelStations.Zone3.CraterLakeToAsh",
    "GD_LevelTravelStations.Zone3.AshToFinalBossAscent": "GD_LevelTravelStations.Zone3.FinalBossAscentToAsh",
    "GD_LevelTravelStations.Zone3.AshToFyrestone": "GD_LevelTravelStations.Zone3.FyrestoneToAsh",
    "GD_LevelTravelStations.Zone3.AshToRobotSlaughter": "GD_LevelTravelStations.Zone3.RobotSlaughterToAsh",
    "GD_LevelTravelStations.Zone3.RobotSlaughterToAsh": "GD_LevelTravelStations.Zone3.AshToRobotSlaughter",
    "GD_LevelTravelStations.Zone3.FinalBossAscentToVolcano": "GD_LevelTravelStations.Zone3.VolcanoToFinalBossAscent",
    "GD_LevelTravelStations.Zone3.VolcanoToFinalBossAscent": "GD_LevelTravelStations.Zone3.FinalBossAscentToVolcano",
    "GD_LevelTravelStations.AshToVolcano": "GD_LevelTravelStations.VolcanoToAsh",
    "GD_LevelTravelStations.VolcanoToAsh": "GD_LevelTravelStations.AshToVolcano",
    "GD_LevelTravelStations.FrostToIce2": "GD_LevelTravelStations.IceToFrost2",
    "GD_LevelTravelStations.IceToFrost2": "GD_LevelTravelStations.FrostToIce2",
    "GD_LevelTravelStations.GrassRoadToOutwash": "GD_LevelTravelStations.OutwashToGrassRoad",
    "GD_LevelTravelStations.OutwashToGrassRoad": "GD_LevelTravelStations.GrassRoadToOutwash",
    # "GD_LevelTravelStations.Interlude.InterludeToDamTop": "GD_LevelTravelStations.Zone1.DamTopToInterlude",
    # "GD_LevelTravelStations.Interlude.InterludeToDLC": "",
    # "GD_LevelTravelStations.Zone1.DamTopToInterlude": "GD_LevelTravelStations.Interlude.InterludeToDamTop",
    "GD_LevelTravelStations.Zone1.SanctuaryToVOGsChamber": "GD_LevelTravelStations.Zone2.VOGsChamberToSanctuary",
    "GD_LevelTravelStations.Zone2.VOGsChamberToSanctuary": "GD_LevelTravelStations.Zone1.SanctuaryToVOGsChamber",
    # "GD_LevelTravelStations.Zone1.WaterfrontDocksToIce": "",
    # "GD_Anemone_LevelTravel.BackburnerToSanctIntro": "GD_Anemone_LevelTravel.SanctIntroToBackburner",
    "GD_Anemone_LevelTravel.HeliosToSandwormCavern": "GD_Anemone_LevelTravel.SandwormCavernToHelios",
    "GD_Anemone_LevelTravel.OldDustToBackburner": "GD_Anemone_LevelTravel.BackburnerToOldDust",
    "GD_Anemone_LevelTravel.ResearchCenterToOldDust": "GD_Anemone_LevelTravel.OldDustToResearchCenter",
    "GD_Anemone_LevelTravel.SandwormCavernToOldDust": "GD_Anemone_LevelTravel.OldDustToSandwormCavern",
    "GD_Anemone_LevelTravel.BackburnerToOldDust": "GD_Anemone_LevelTravel.OldDustToBackburner",
    # "GD_Anemone_LevelTravel.SanctIntroToBackburner": "GD_Anemone_LevelTravel.BackburnerToSanctIntro",
    "GD_Anemone_LevelTravel.SandwormCavernToHelios": "GD_Anemone_LevelTravel.HeliosToSandwormCavern",
    "GD_Anemone_LevelTravel.OldDustToResearchCenter": "GD_Anemone_LevelTravel.ResearchCenterToOldDust",
    "GD_Anemone_LevelTravel.OldDustToSandwormCavern": "GD_Anemone_LevelTravel.SandwormCavernToOldDust",
    "GD_Anemone_LevelTravel.RaidBossToSandwormCavern": "GD_Anemone_LevelTravel.SandwormCavernToRaidBoss",
    "GD_Anemone_LevelTravel.SandwormCavernToRaidBoss": "GD_Anemone_LevelTravel.RaidBossToSandwormCavern",
    "GD_Anemone_LevelTravel.ResearchCenterToSanctuary": "GD_Anemone_LevelTravel.SanctuaryToResearchCenter",
    "GD_Anemone_LevelTravel.SanctuaryToResearchCenter": "GD_Anemone_LevelTravel.ResearchCenterToSanctuary",
    "GD_Aster_LevelTravel.CastleExteriorToMines": "GD_Aster_LevelTravel.MinesToCastleExterior",
    "GD_Aster_LevelTravel.CastleKeepToDungeon": "GD_Aster_LevelTravel.DungeonToCastleKeep",
    "GD_Aster_LevelTravel.DarkForestToVillage": "GD_Aster_LevelTravel.VillageToDarkForest",
    "GD_Aster_LevelTravel.DeadForestToDarkForest": "GD_Aster_LevelTravel.DarkForestToDeadForest",
    "GD_Aster_LevelTravel.DungeonToCastleExterior": "GD_Aster_LevelTravel.CastleExteriorToDungeon",
    "GD_Aster_LevelTravel.MinesToDeadForest": "GD_Aster_LevelTravel.DeadForestToMines",
    "GD_Aster_LevelTravel.VillageToDocks": "GD_Aster_LevelTravel.DocksToVillage",
    # "GD_Aster_LevelTravel.CastleExteriorToCastleKeepFake": "",
    # "GD_Aster_LevelTravel.CastleKeepToCastleExteriorFake": "",
    "GD_Aster_LevelTravel.CastleExteriorToDungeon": "GD_Aster_LevelTravel.DungeonToCastleExterior",
    # "GD_Aster_LevelTravel.CastleExteriorToDungeons": "",
    # "GD_Aster_LevelTravel.DungeonsToCastleExterior": "",
    "GD_Aster_LevelTravel.MinesToCastleExterior": "GD_Aster_LevelTravel.CastleExteriorToMines",
    "GD_Aster_LevelTravel.DungeonToCastleKeep": "GD_Aster_LevelTravel.CastleKeepToDungeon",
    # "GD_Aster_LevelTravel.CastleKeepToDungeons": "",
    # "GD_Aster_LevelTravel.DungeonsToCastleKeep": "",
    "GD_Aster_LevelTravel.DarkForestToDeadForest": "GD_Aster_LevelTravel.DeadForestToDarkForest",
    # "GD_Aster_LevelTravel.DarkForestToMines": "",
    "GD_Aster_LevelTravel.VillageToDarkForest": "GD_Aster_LevelTravel.DarkForestToVillage",
    "GD_Aster_LevelTravel.DeadForestToMines": "GD_Aster_LevelTravel.MinesToDeadForest",
    "GD_Aster_LevelTravel.DocksToVillage": "GD_Aster_LevelTravel.VillageToDocks",
    "GD_Aster_LevelTravel.DungeonRaidToDungeon": "GD_Aster_LevelTravel.DungeonToDungeonRaid",
    "GD_Aster_LevelTravel.DungeonToDungeonRaid": "GD_Aster_LevelTravel.DungeonRaidToDungeon",
    # "GD_Aster_LevelTravel.DungeonRaidToDungeons": "",
    # "GD_Aster_LevelTravel.DungeonsToDungeonRaid": "",
    # "GD_Aster_LevelTravel.MinesToDarkForest": "",
    "GD_Aster_LevelTravel.TempleOfSlaughterToVillage": "GD_Aster_LevelTravel.VillageToTempleOfSlaughter",
    "GD_Aster_LevelTravel.VillageToTempleOfSlaughter": "GD_Aster_LevelTravel.TempleOfSlaughterToVillage",
    # "GD_Aster_LevelTravel.VillageToMines": "",
    "GD_Iris_LevelTravelStations.Hub.MoxxiToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToMoxxi",
    "GD_Iris_LevelTravelStations.Dogleg2.BeatdownToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToBeatdown",
    "GD_Iris_LevelTravelStations.Dogleg3.ForgeToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToForge",
    "GD_Iris_LevelTravelStations.Hub.MammaToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToMamma",
    "GD_Iris_LevelTravelStations.BeatdowntoPyroPeats": "GD_Iris_LevelTravelStations.PyroPetesToBeatdown",
    "GD_Iris_LevelTravelStations.PyroPetesToBeatdown": "GD_Iris_LevelTravelStations.BeatdowntoPyroPeats",
    # "GD_Iris_LevelTravelStations.BeatdowntoPyroPetes2": "",
    # "GD_Iris_LevelTravelStations.PyroPetesToBeatdown2": "",
    # "GD_Iris_LevelTravelStations.CraterToKickedOut": "GD_Iris_LevelTravelStations.KickedOutToCrater",
    # "GD_Iris_LevelTravelStations.KickedOutToCrater": "GD_Iris_LevelTravelStations.CraterToKickedOut",
    "GD_Iris_LevelTravelStations.Dogleg1.ArenaTASToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToArenaTAS",
    "GD_Iris_LevelTravelStations.Hub.CraterToArenaTAS": "GD_Iris_LevelTravelStations.Dogleg1.ArenaTASToCrater",
    "GD_Iris_LevelTravelStations.Dogleg1.ArenaToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToArena",
    "GD_Iris_LevelTravelStations.Hub.CraterToArena": "GD_Iris_LevelTravelStations.Dogleg1.ArenaToCrater",
    "GD_Iris_LevelTravelStations.Dogleg1.BackdoorToCrater": "GD_Iris_LevelTravelStations.Hub.CraterToBackdoor",
    "GD_Iris_LevelTravelStations.Hub.CraterToBackdoor": "GD_Iris_LevelTravelStations.Dogleg1.BackdoorToCrater",
    "GD_Iris_LevelTravelStations.Hub.CraterToBeatdown": "GD_Iris_LevelTravelStations.Dogleg2.BeatdownToCrater",
    "GD_Iris_LevelTravelStations.Hub.CraterToForge": "GD_Iris_LevelTravelStations.Dogleg3.ForgeToCrater",
    "GD_Iris_LevelTravelStations.Hub.CraterToMamma": "GD_Iris_LevelTravelStations.Hub.MammaToCrater",
    "GD_Iris_LevelTravelStations.Hub.CraterToMoxxi": "GD_Iris_LevelTravelStations.Hub.MoxxiToCrater",
    # "GD_Iris_LevelTravelStations.PyroPeteToBeatdown": "",
    # "GD_Iris_LevelTravelStations.PyroPetetoBeatdown2": "",
    "GD_Orchid_LevelTravel.Caves.CavesToOasisTown": "GD_Orchid_LevelTravel.OasisTown.OasisTownToCaves",
    "GD_Orchid_LevelTravel.Refinery.RefineryToSaltFlats": "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToRefinery",
    "GD_Orchid_LevelTravel.ShipGraveyard.ShipGraveyardToSaltFlats": "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToShipGraveyard",
    "GD_Orchid_LevelTravel.Spire.SpireToSaltFlats": "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToSpire",
    "GD_Orchid_LevelTravel.OasisTown.OasisTownToCaves": "GD_Orchid_LevelTravel.Caves.CavesToOasisTown",
    "GD_Orchid_LevelTravel.OasisTown.OasisTownToSaltFlats": "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToOasisTown",
    "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToOasisTown": "GD_Orchid_LevelTravel.OasisTown.OasisTownToSaltFlats",
    # "GD_Orchid_LevelTravel.OasisTown.OasisTownToSpire": "GD_Orchid_LevelTravel.Spire.SpireToOasisTown",
    "GD_Orchid_LevelTravel.OasisTown.OasisTownToWormBelly": "GD_Orchid_LevelTravel.WormBelly.WormBellyToOasisTown",
    "GD_Orchid_LevelTravel.WormBelly.WormBellyToOasisTown": "GD_Orchid_LevelTravel.OasisTown.OasisTownToWormBelly",
    "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToRefinery": "GD_Orchid_LevelTravel.Refinery.RefineryToSaltFlats",
    "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToShipGraveyard": "GD_Orchid_LevelTravel.ShipGraveyard.ShipGraveyardToSaltFlats",
    "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToSpire": "GD_Orchid_LevelTravel.Spire.SpireToSaltFlats",
    # "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToWormBelly": "GD_Orchid_LevelTravel.WormBelly.WormBellyToSaltFlats",
    # "GD_Orchid_LevelTravel.WormBelly.WormBellyToSaltFlats": "GD_Orchid_LevelTravel.SaltFlats.SaltFlatsToWormBelly",
    # "GD_Orchid_LevelTravel.Spire.SpireToOasisTown": "GD_Orchid_LevelTravel.OasisTown.OasisTownToSpire",
    "GD_Sage_LevelTravel.Sage_Travel_ShipToCliffs": "GD_Sage_LevelTravel.Sage_Travel_CliffsToShip",
    "GD_Sage_LevelTravel.Sage_Travel_PowerStationToRockForest": "GD_Sage_LevelTravel.Sage_Travel_RockForestToPowerStation",
    "GD_Sage_LevelTravel.Sage_Travel_RockForestToUnderground": "GD_Sage_LevelTravel.Sage_Travel_UndergroundToRockForest",
    "GD_Sage_LevelTravel.Sage_Travel_CliffsToUnderground": "GD_Sage_LevelTravel.Sage_Travel_UndergroundToCliffs",
    # "GD_Sage_LevelTravel.CliffsToUnderground": "",
    # "GD_Sage_LevelTravel.PowerStationToUnderground": "",
    "GD_Sage_LevelTravel.Sage_Travel_CliffsToShip": "GD_Sage_LevelTravel.Sage_Travel_ShipToCliffs",
    "GD_Sage_LevelTravel.Sage_Travel_UndergroundToCliffs": "GD_Sage_LevelTravel.Sage_Travel_CliffsToUnderground",
    "GD_Sage_LevelTravel.Sage_Travel_RockForestToPowerStation": "GD_Sage_LevelTravel.Sage_Travel_PowerStationToRockForest",
    "GD_Sage_LevelTravel.Sage_Travel_PowerStationToUnderground": "GD_Sage_LevelTravel.Sage_Travel_UndergroundToPowerStation",
    "GD_Sage_LevelTravel.Sage_Travel_UndergroundToPowerStation": "GD_Sage_LevelTravel.Sage_Travel_PowerStationToUnderground",
    "GD_Sage_LevelTravel.Sage_Travel_UndergroundToRockForest": "GD_Sage_LevelTravel.Sage_Travel_RockForestToUnderground",
    # "GD_Sage_LevelTravel.Sage_Travel_RockForestToVillage": "",
}

entrance_dict = {}

def create_entrance_dict(entrance_list):
    # tie every pair of entrances to each other
    d = {}
    for i in range(len(entrance_list)):
        if i % 2 == 0:
            side1 = entrance_list[i]
            side2 = entrance_list[i + 1]

            orig_dest1 = orig_entrance_dict[side1]
            orig_dest2 = orig_entrance_dict[side2]

            d[orig_dest1] = side2
            d[orig_dest2] = side1
    return d

def init_seeded_dict():
    local_random = random.Random(seed_option.value)
    local_list = list(orig_entrance_dict.keys()).copy()
    local_random.shuffle(local_list)

    global entrance_dict
    entrance_dict = create_entrance_dict(local_list)

def pathname(obj):
    if obj is None:
        return None
    return obj.PathName(obj)

@hook("WillowGame.WillowGameInfo:TravelToStation")
def travel_to_station(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    print(self)
    print(caller.DestTravelStation)
    pn = pathname(caller.DestTravelStation)
    rand_st_name = entrance_dict.get(pn)
    if rand_st_name is None:
        print("not randomized: " + pn)
        return
    print("orig dest: " + pn)
    st = unrealsdk.find_object("LevelTravelStationDefinition", rand_st_name)
    caller.DestTravelStation = st
    with prevent_hooking_direct_calls():
        self.TravelToStation(caller)
    return Block

def on_enable():
    print("enabled")
    init_seeded_dict()

@keybind("Emergency Teleport", "N", description="If you get stuck, emergency teleport back to Claptrap's Igloo")
def emergency_travel():
    gameinfo = unrealsdk.find_all("WillowCoopGameInfo")[-1]
    with prevent_hooking_direct_calls():
        gameinfo.TravelToStation(unrealsdk.find_object("FastTravelStationDefinition", "GD_FastTravelStations.Zone1.GlacialIgloo"))

@hook("WillowGame.WillowPlayerPawn:DoSprint")
def sprint_pressed(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    self.SprintingPct = sprint_option.value * .1

sprint_option = SliderOption(
    identifier="Sprint Speed",
    value=15,
    min_value=5,
    max_value=50,
    description=(
        "Sprint Speed"
    ),
)

def open_settings(ButtonInfo):
    os.startfile(os.path.dirname(mod_instance.settings_file))

oid_open_settings = ButtonOption(
    "Open Settings",
    on_press=open_settings,
    description="Open Settings Folder to View/Edit Seed and other settings",
)

def print_seed(ButtonInfo):
    show_chat_message("Seed: "+ str(seed_option.value))

oid_print_seed = ButtonOption(
    "Print Seed",
    on_press=print_seed,
    description="Show Seed",
)

def make_seed(ButtonInfo):
    seed = random.randint(1, 2147483647)
    seed_option.value = seed
    init_seeded_dict()
    show_chat_message("New Seed: "+ str(seed))

oid_make_seed = ButtonOption(
    "Randomize Seed",
    on_press=make_seed,
    description="Set seed to a random value",
)

seed_option = SliderOption(
    "Seed",
    value=1,
    min_value=1,
    max_value=2147483647,
    is_hidden=True,
)

mod_instance = build_mod(
    keybinds=[emergency_travel],
    options=[sprint_option, oid_open_settings, oid_print_seed, oid_make_seed, seed_option],
    on_enable=on_enable,
    hooks=[
        travel_to_station,
        sprint_pressed,
    ]
)

print(mod_instance.settings_file)
