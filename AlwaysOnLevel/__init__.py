import unrealsdk.unreal as unreal
from mods_base import build_mod, get_pc, hook, SpinnerOption
from unrealsdk.hooks import Block, prevent_hooking_direct_calls

@hook("WillowGame.WillowPawn:SetGameStage")
def set_game_stage(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
  if self.Class.Name == "WillowPlayerPawn":
    return None
  
  # print(f"set_game_stage {caller.NewGameStage}")
  level = get_pc().PlayerReplicationInfo.ExpLevel

  with prevent_hooking_direct_calls():
    if oid_dir.value == "Both":
      params(level)
      return Block
    elif oid_dir.value == "Up" and caller.NewGameStage < level:
      params(level)
      return Block
    elif oid_dir.value == "Down" and caller.NewGameStage > level:
      params(level)
      return Block

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

build_mod(hooks=[set_game_stage], options=[oid_dir])