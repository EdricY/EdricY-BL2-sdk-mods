import unrealsdk.unreal as unreal
from mods_base import build_mod, get_pc, hook, SpinnerOption
from unrealsdk.hooks import Block, prevent_hooking_direct_calls

@hook("WillowGame.WillowPawn:SetGameStage")
@hook("WillowGame.WillowInteractiveObject:SetGameStage")
@hook("WillowGame.WillowPawn:SetGameStageForSpawnedInventory")
@hook("WillowGame.WillowAIPawn:SetGameStageForSpawnedInventory")
def set_game_stage(obj: unreal.UObject, args: unreal.WrappedStruct, ret, func: unreal.BoundFunction):
  if obj.Class.Name == "WillowPlayerPawn":
    return None

  try:
    arg_level = args.NewGameStage
  except:
    arg_level = args.NewInventoryGameStage
  
  level = get_pc().PlayerReplicationInfo.ExpLevel

  with prevent_hooking_direct_calls():
    if oid_dir.value == "Both":
      func(level)
      return Block
    elif oid_dir.value == "Up" and arg_level < level:
      func(level)
      return Block
    elif oid_dir.value == "Down" and arg_level > level:
      func(level)
      return Block

# TODO: maybe look into these
# WillowGame.MissionDefinition:SetGameStage
# WillowGame.WillowPlayerController:SetGameStageForRegion
# WillowGame.WillowRegionDefinition:SetGameStageOverride

oid_dir = SpinnerOption(
    "Level Direction",
    "Both",
    ["Down", "Up", "Both"],
    True,
    description=("Should Enemies be leveled up only, down only, or both"
                "\nDown = Higher level enemies will be lowered to your level, lower level enemies will be untouched."
                "\nUp = Lower level enemies will be brought up to your level, higher level enemies will be untouched."
    ),
)

build_mod(
  hooks=[set_game_stage],
  options=[oid_dir]
)